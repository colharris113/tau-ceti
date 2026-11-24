# New-game state reset

**Address** `$5766-$586B` &nbsp;·&nbsp; **Group** Flight

<p class="lede">Clears the counters, clock and target pointers, then lays out a fresh ship at <code class="addr">$57F0</code>: altitude 28, shield and fuel full (<code class="addr">$BF</code>), eight missiles, flares and AMMs, laser heat zero.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">5766</span>  <span class="rt-bytes">A9 80   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">5768</span>  <span class="rt-bytes">8D 35 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0335</span>
<span class="rt-addr">576B</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">576D</span>  <span class="rt-bytes">8D 36 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0336</span>
<span class="rt-addr">5770</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">5772</span>  <span class="rt-bytes">8D 38 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0338</span>   <span class="rt-cmt">; Launch heading (low)</span>
<span class="rt-addr">5775</span>  <span class="rt-bytes">A9 01   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">5777</span>  <span class="rt-bytes">8D 39 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0339</span>   <span class="rt-cmt">; Launch heading (high)</span>
<span class="rt-addr">577A</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">577C</span>  <span class="rt-bytes">8D AF 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03AF</span>
<span class="rt-addr">577F</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">5781</span>  <span class="rt-bytes">8D 40 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0340</span>   <span class="rt-cmt">; Frame counter</span>
<span class="rt-addr">5784</span>  <span class="rt-bytes">8D 41 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0341</span>   <span class="rt-cmt">; Seconds</span>
<span class="rt-addr">5787</span>  <span class="rt-bytes">8D 42 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0342</span>   <span class="rt-cmt">; Minutes</span>
<span class="rt-addr">578A</span>  <span class="rt-bytes">8D 43 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0343</span>   <span class="rt-cmt">; Hours</span>
<span class="rt-addr">578D</span>  <span class="rt-bytes">8D 53 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0353</span>   <span class="rt-cmt">; Speed</span>
<span class="rt-addr">5790</span>  <span class="rt-bytes">8D 8E 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$038E</span>
<span class="rt-addr">5793</span>  <span class="rt-bytes">8D 6F 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$036F</span>
<span class="rt-addr">5796</span>  <span class="rt-bytes">8D 70 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0370</span>   <span class="rt-cmt">; Laser lockout</span>
<span class="rt-addr">5799</span>  <span class="rt-bytes">8D 71 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0371</span>
<span class="rt-addr">579C</span>  <span class="rt-bytes">8D 72 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0372</span>
<span class="rt-addr">579F</span>  <span class="rt-bytes">8D 9E 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$039E</span>   <span class="rt-cmt">; Tank ruptured</span>
<span class="rt-addr">57A2</span>  <span class="rt-bytes">8D 34 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0334</span>
<span class="rt-addr">57A5</span>  <span class="rt-bytes">8D A3 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A3</span>   <span class="rt-cmt">; NO FUEL flag</span>
<span class="rt-addr">57A8</span>  <span class="rt-bytes">8D A2 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A2</span>   <span class="rt-cmt">; LOW FUEL flag</span>
<span class="rt-addr">57AB</span>  <span class="rt-bytes">8D A5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A5</span>   <span class="rt-cmt">; Kill count (low)</span>
<span class="rt-addr">57AE</span>  <span class="rt-bytes">8D A6 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A6</span>   <span class="rt-cmt">; Kill count (high)</span>
<span class="rt-addr">57B1</span>  <span class="rt-bytes">8D A7 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A7</span>
<span class="rt-addr">57B4</span>  <span class="rt-bytes">8D A8 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A8</span>
<span class="rt-addr">57B7</span>  <span class="rt-bytes">8D A9 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A9</span>
<span class="rt-addr">57BA</span>  <span class="rt-bytes">8D BE 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03BE</span>
<span class="rt-addr">57BD</span>  <span class="rt-bytes">8D 95 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0395</span>
<span class="rt-addr">57C0</span>  <span class="rt-bytes">8D 75 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0375</span>
<span class="rt-addr">57C3</span>  <span class="rt-bytes">A9 01   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">57C5</span>  <span class="rt-bytes">8D 54 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0354</span>
<span class="rt-addr">57C8</span>  <span class="rt-bytes">A9 88   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$88</span>
<span class="rt-addr">57CA</span>  <span class="rt-bytes">8D 3C 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033C</span>
<span class="rt-addr">57CD</span>  <span class="rt-bytes">8D 98 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0398</span>   <span class="rt-cmt">; Docked cell (low)</span>
<span class="rt-addr">57D0</span>  <span class="rt-bytes">A9 6C   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$6C</span>
<span class="rt-addr">57D2</span>  <span class="rt-bytes">8D 3F 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033F</span>
<span class="rt-addr">57D5</span>  <span class="rt-bytes">8D 99 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0399</span>   <span class="rt-cmt">; Docked cell (high)</span>
<span class="rt-addr">57D8</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">57DA</span>  <span class="rt-bytes">8D 3B 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033B</span>
<span class="rt-addr">57DD</span>  <span class="rt-bytes">8D 3A 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033A</span>
<span class="rt-addr">57E0</span>  <span class="rt-bytes">8D 3E 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033E</span>
<span class="rt-addr">57E3</span>  <span class="rt-bytes">8D 3D 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$033D</span>
<span class="rt-addr">57E6</span>  <span class="rt-bytes">A9 80   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">57E8</span>  <span class="rt-bytes">8D 96 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0396</span>   <span class="rt-cmt">; Dock state</span>
<span class="rt-addr">57EB</span>  <span class="rt-bytes">A9 1B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$1B</span>
<span class="rt-addr">57ED</span>  <span class="rt-bytes">8D A4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A4</span>   <span class="rt-cmt">; Docked type</span>
<span class="rt-addr">57F0</span>  <span class="rt-bytes">A9 1C   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$1C</span>
<span class="rt-addr">57F2</span>  <span class="rt-bytes">8D 44 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">57F5</span>  <span class="rt-bytes">A9 BF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$BF</span>
<span class="rt-addr">57F7</span>  <span class="rt-bytes">8D 77 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0377</span>   <span class="rt-cmt">; Shield</span>
<span class="rt-addr">57FA</span>  <span class="rt-bytes">8D 46 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0346</span>   <span class="rt-cmt">; Fuel (whole units)</span>
<span class="rt-addr">57FD</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">57FF</span>  <span class="rt-bytes">8D 45 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0345</span>   <span class="rt-cmt">; Fuel (low byte)</span>
<span class="rt-addr">5802</span>  <span class="rt-bytes">A9 08   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">5804</span>  <span class="rt-bytes">8D 58 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0358</span>   <span class="rt-cmt">; Missiles</span>
<span class="rt-addr">5807</span>  <span class="rt-bytes">8D 57 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0357</span>
<span class="rt-addr">580A</span>  <span class="rt-bytes">8D 55 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0355</span>
<span class="rt-addr">580D</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">580F</span>  <span class="rt-bytes">8D 47 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0347</span>   <span class="rt-cmt">; Laser heat</span>
<span class="rt-addr">5812</span>  <span class="rt-bytes">8D 80 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0380</span>
<span class="rt-addr">5815</span>  <span class="rt-bytes">8D 8E 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$038E</span>
<span class="rt-addr">5818</span>  <span class="rt-bytes">8D 81 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0381</span>   <span class="rt-cmt">; Dock refused</span>
<span class="rt-addr">581B</span>  <span class="rt-bytes">8D 89 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0389</span>
<span class="rt-addr">581E</span>  <span class="rt-bytes">8D 74 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0374</span>
<span class="rt-addr">5821</span>  <span class="rt-bytes">8D 8D 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$038D</span>
<span class="rt-addr">5824</span>  <span class="rt-bytes">A2 01   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">5826</span>  <span class="rt-bytes">20 22 84</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$8422</span>
<span class="rt-addr">5829</span>  <span class="rt-bytes">A9 07   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">582B</span>  <span class="rt-bytes">8D C2 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C2</span>
<span class="rt-addr">582E</span>  <span class="rt-bytes">20 DB 86</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$86DB</span>
<span class="rt-addr">5831</span>  <span class="rt-bytes">A9 80   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">5833</span>  <span class="rt-bytes">8D 76 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0376</span>
<span class="rt-addr">5836</span>  <span class="rt-bytes">20 1E 35</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$351E</span>
<span class="rt-addr">5839</span>  <span class="rt-bytes">20 B6 34</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$34B6</span>
<span class="rt-addr">583C</span>  <span class="rt-bytes">20 C8 34</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$34C8</span>
<span class="rt-addr">583F</span>  <span class="rt-bytes">20 DA 34</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$34DA</span>
<span class="rt-addr">5842</span>  <span class="rt-bytes">20 00 35</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3500</span>
<span class="rt-addr">5845</span>  <span class="rt-bytes">20 0A 35</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$350A</span>
<span class="rt-addr">5848</span>  <span class="rt-bytes">20 14 35</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3514</span>
<span class="rt-addr">584B</span>  <span class="rt-bytes">20 A8 37</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$37A8</span>
<span class="rt-addr">584E</span>  <span class="rt-bytes">20 8C 29</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$298C</span>
<span class="rt-addr">5851</span>  <span class="rt-bytes">20 06 49</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4906</span>
<span class="rt-addr">5854</span>  <span class="rt-bytes">20 23 37</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3723</span>
<span class="rt-addr">5857</span>  <span class="rt-bytes">20 36 34</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3436</span>
<span class="rt-addr">585A</span>  <span class="rt-bytes">20 AC 40</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$40AC</span>
<span class="rt-addr">585D</span>  <span class="rt-bytes">20 BF 3F</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3FBF</span>
<span class="rt-addr">5860</span>  <span class="rt-bytes">20 19 73</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$7319</span>
<span class="rt-addr">5863</span>  <span class="rt-bytes">20 21 29</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$2921</span>   <span class="rt-cmt">; City restore: stripping the state bits</span>
<span class="rt-addr">5866</span>  <span class="rt-bytes">A9 08   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">5868</span>  <span class="rt-bytes">8D 9D 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$039D</span>
<span class="rt-addr">586B</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`City restore: stripping the state bits`](city-restore.md) from `$5863`

## Called by

- `JSR` at `$2009`
- `JSR` at `$64F0`
- `JSR` at `$654D`
- `JSR` at `$83A6`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
