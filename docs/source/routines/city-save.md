# City save: writing damage back to the sheet

**Address** `$28E6-$2920` &nbsp;·&nbsp; **Group** Records

<p class="lede">Called before a jump (<code class="addr">$51C5</code>) and from <code class="addr">$6A77</code>. Walks the city sheet at <code class="addr">$9400</code> and the loaded record table at <code class="addr">$0E00</code> in step, copying one byte per record — byte 0 — from the record back into the sheet. Types whose flags at <code class="addr">$C39A</code> hold both the mobile and armed bits (<code class="addr">$60</code>: types 3, 6, 9, 20 and 21) are skipped, so the armed mobile units always return. A destroyed building has already been marked type | <code class="addr">$80</code> by the dying animation, so it is written back as free and stays destroyed on the next visit.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">28E6</span>  <span class="rt-bytes">20 EC 27</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$27EC</span>   <span class="rt-cmt">; City loader: the sheet at $9400 into the record table</span>
<span class="rt-addr">28E9</span>  <span class="rt-bytes">A2 20   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">28EB</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">28ED</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">28EF</span>  <span class="rt-bytes">C9 C0   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">28F1</span>  <span class="rt-bytes">F0 2D   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$2920</span>
<span class="rt-addr">28F3</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28F5</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">28F7</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">28F8</span>  <span class="rt-bytes">B9 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,Y</span>
<span class="rt-addr">28FB</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">28FD</span>  <span class="rt-bytes">29 60   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$60</span>
<span class="rt-addr">28FF</span>  <span class="rt-bytes">C9 60   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$60</span>
<span class="rt-addr">2901</span>  <span class="rt-bytes">F0 04   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$2907</span>
<span class="rt-addr">2903</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2905</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2907</span>  <span class="rt-bytes">A5 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">2909</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">290A</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">290C</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">290E</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2912</span>
<span class="rt-addr">2910</span>  <span class="rt-bytes">E6 64   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">2912</span>  <span class="rt-bytes">A5 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">2914</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2915</span>  <span class="rt-bytes">69 03   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">2917</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">2919</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$291D</span>
<span class="rt-addr">291B</span>  <span class="rt-bytes">E6 62   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">291D</span>  <span class="rt-bytes">CA      </span>  <span class="rt-op">DEX</span>  <span class="rt-arg"></span>
<span class="rt-addr">291E</span>  <span class="rt-bytes">D0 CD   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$28ED</span>
<span class="rt-addr">2920</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`City loader: the sheet at $9400 into the record table`](city-loader.md) from `$28E6`

## Called by

- `JSR` at `$51C5`
- `JSR` at `$6A77`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
