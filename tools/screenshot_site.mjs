// Screenshot the built site: each page top, plus every <figure>, in both
// light and dark palettes.  Uses a private headless Chrome and talks CDP
// directly, so there are no npm dependencies.
//
//   node tools/screenshot_site.mjs work/shots
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const SITE = path.join(ROOT, 'site');
const OUT = path.resolve(process.argv[2] || path.join(ROOT, 'work', 'shots'));
const PORT = 9224;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const PAGES = [
  ['index', 'index.html'],
  ['record-table', 'deep-dives/the-record-table/index.html'],
  ['docking', 'deep-dives/docking-and-the-aperture/index.html'],
  ['fuel', 'deep-dives/fuel-and-jumping/index.html'],
  ['method', 'about/method/index.html'],
  ['type-tables', 'reference/type-tables/index.html'],
  ['source-index', 'source/index.html'],
  ['frame-tick', 'source/routines/frame-tick/index.html'],
];

function findChrome() {
  const cands = [
    process.env.CHROME_BIN,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'),
  ];
  return cands.find((p) => p && fs.existsSync(p));
}

async function pageTarget() {
  try {
    const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
    return list.find((p) => p.type === 'page') || null;
  } catch {
    return null;
  }
}

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Map();
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      } else if (msg.method && this.listeners.has(msg.method)) {
        for (const fn of this.listeners.get(msg.method)) fn(msg.params);
        this.listeners.delete(msg.method);
      }
    };
  }
  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
  once(method) {
    return new Promise((resolve) => {
      const fn = (params) => resolve(params);
      this.listeners.set(method, [...(this.listeners.get(method) || []), fn]);
    });
  }
}

// Material stores the palette it resolved on first load in localStorage and
// honours that over the media query afterwards, so each scheme needs its own
// fresh profile.
async function launch(chrome, scheme) {
  const profile = path.join(ROOT, 'work', `chrome-shot-${scheme}`);
  fs.rmSync(profile, { recursive: true, force: true });
  fs.mkdirSync(profile, { recursive: true });
  const proc = spawn(chrome, [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${profile}`,
    '--allow-file-access-from-files',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-gpu',
    'about:blank',
  ], { stdio: 'ignore', windowsHide: true });
  let target = null;
  for (let i = 0; i < 100 && !target; i++) {
    await sleep(150);
    target = await pageTarget();
  }
  if (!target) {
    proc.kill();
    throw new Error(`Chrome did not open CDP port ${PORT}`);
  }
  return { proc, target };
}

async function main() {
  const chrome = findChrome();
  if (!chrome) throw new Error('Chrome not found; set CHROME_BIN');

  fs.mkdirSync(OUT, { recursive: true });

  for (const scheme of ['light', 'dark']) {
    const { proc, target } = await launch(chrome, scheme);
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    const cdp = new CDP(ws);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1200, height: 900, deviceScaleFactor: 1, mobile: false,
    });
    await cdp.send('Emulation.setEmulatedMedia', {
      features: [{ name: 'prefers-color-scheme', value: scheme }],
    });
    for (const [name, rel] of PAGES) {
      const url = 'file:///' + path.join(SITE, rel).replace(/\\/g, '/');
      const loaded = cdp.once('Page.loadEventFired');
      await cdp.send('Page.navigate', { url });
      await loaded;
      await sleep(1200);
      const probe = await cdp.send('Runtime.evaluate', {
        expression: `JSON.stringify({dark:matchMedia('(prefers-color-scheme: dark)').matches,
          bg:getComputedStyle(document.body).backgroundColor})`,
        returnByValue: true,
      });
      console.log(scheme, name, probe.result.value);
      await cdp.send('Runtime.evaluate', { expression: 'window.scrollTo(0,0)' });

      const top = await cdp.send('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(OUT, `${scheme}-${name}-top.png`),
        Buffer.from(top.data, 'base64'));

      const { result } = await cdp.send('Runtime.evaluate', {
        expression: `JSON.stringify([...document.querySelectorAll('figure')].map((f, i) => {
          const r = f.getBoundingClientRect();
          return { i, x: r.x + window.scrollX, y: r.y + window.scrollY,
                   w: Math.ceil(r.width), h: Math.ceil(r.height) };
        }))`,
        returnByValue: true,
      });
      for (const f of JSON.parse(result.value)) {
        const shot = await cdp.send('Page.captureScreenshot', {
          format: 'png',
          captureBeyondViewport: true,
          clip: { x: f.x, y: f.y, width: f.w, height: f.h, scale: 1 },
        });
        fs.writeFileSync(path.join(OUT, `${scheme}-${name}-fig${f.i}.png`),
          Buffer.from(shot.data, 'base64'));
        console.log('wrote', `${scheme}-${name}-fig${f.i}.png`, `${f.w}x${f.h}`);
      }
      console.log('wrote', `${scheme}-${name}-top.png`);
    }
    ws.close();
    proc.kill();
    await sleep(600);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
