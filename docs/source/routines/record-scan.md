# Record scan

**Address** `$43CF-$441D` &nbsp;·&nbsp; **Group** Records

<p class="lede">Walks the 48 sixteen-byte records at <code class="addr">$0E00</code>-<code class="addr">$10FF</code>. Byte 0 sorts them: <code class="addr">$80</code> is free and skipped, <code class="addr">$40</code> is dying and goes to the death animation, anything else is live and goes to the dispatcher at <code class="addr">$445D</code>. At the end of the sweep the game rotates the 6-bit round-robin index at <code class="addr">$038F</code> and advances its frame counters.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">43CF</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">43D1</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">43D3</span>  <span class="rt-bytes">A9 0E   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">43D5</span>  <span class="rt-bytes">85 62   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">43D7</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">43D9</span>  <span class="rt-bytes">8D 73 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0373</span>
<span class="rt-addr">43DC</span>  <span class="rt-bytes">8D B0 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">43DF</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">43E1</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">43E3</span>  <span class="rt-bytes">29 C0   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">43E5</span>  <span class="rt-bytes">C9 40   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">43E7</span>  <span class="rt-bytes">90 74   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$445D</span>   <span class="rt-cmt">; Live-record dispatch</span>
<span class="rt-addr">43E9</span>  <span class="rt-bytes">F0 33   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$441E</span>   <span class="rt-cmt">; Dying animation</span>
<span class="rt-addr">43EB</span>  <span class="rt-bytes">A5 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">43ED</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">43EE</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">43F0</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">43F2</span>  <span class="rt-bytes">90 EB   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$43DF</span>
<span class="rt-addr">43F4</span>  <span class="rt-bytes">E6 62   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">43F6</span>  <span class="rt-bytes">A5 62   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">43F8</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">43F9</span>  <span class="rt-bytes">E9 0E   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">43FB</span>  <span class="rt-bytes">C9 03   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">43FD</span>  <span class="rt-bytes">90 E0   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$43DF</span>
<span class="rt-addr">43FF</span>  <span class="rt-bytes">AD 8F 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$038F</span>
<span class="rt-addr">4402</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4403</span>  <span class="rt-bytes">69 08   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4405</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">4407</span>  <span class="rt-bytes">8D 8F 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$038F</span>
<span class="rt-addr">440A</span>  <span class="rt-bytes">AD 73 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0373</span>
<span class="rt-addr">440D</span>  <span class="rt-bytes">8D 74 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0374</span>
<span class="rt-addr">4410</span>  <span class="rt-bytes">AD B0 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">4413</span>  <span class="rt-bytes">8D 75 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0375</span>
<span class="rt-addr">4416</span>  <span class="rt-bytes">A5 EA   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$EA</span>
<span class="rt-addr">4418</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4419</span>  <span class="rt-bytes">69 4D   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$4D</span>
<span class="rt-addr">441B</span>  <span class="rt-bytes">85 EA   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$EA</span>
<span class="rt-addr">441D</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`Live-record dispatch`](live-dispatch.md) from `$43E7`
- [`Dying animation`](dying.md) from `$43E9`

## Called by

- `JSR` at `$2057`
- `JMP` at `$442D` in [`Dying animation`](dying.md)
- `JMP` at `$445A` in [`Dying animation`](dying.md)
- `JMP` at `$4486` in [`Aperture animation`](aperture.md)
- `JMP` at `$449E` in [`Aperture animation`](aperture.md)
- `JMP` at `$44C1` in [`Sensor records`](sensors.md)
- `JMP` at `$452D` in [`Guided-object handling`](guided-objects.md)
- `JMP` at `$4542` in [`Guided-object handling`](guided-objects.md)
- `JMP` at `$45E6` in [`Guided-object handling`](guided-objects.md)
- `JMP` at `$4612` in [`Guided-object handling`](guided-objects.md)
- `JMP` at `$461D` in [`Guided-object handling`](guided-objects.md)
- `JMP` at `$4637` in [`Robot dispatch`](ai-dispatch.md)
- `JMP` at `$464B` in [`Robot dispatch`](ai-dispatch.md)
- `JSR` at `$7ADB`
- `JSR` at `$C13F`
- `JSR` at `$C1D9`
- `JSR` at `$C1F8`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
