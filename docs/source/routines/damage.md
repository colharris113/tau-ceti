# Damage

**Address** `$4951-$4989` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Shared by lasers and everything else. Subtracts the damage in A from byte 7. On underflow it clears byte 8, sets the death sound counter, marks byte 0 dying, and for armed types adds one to the 16-bit kill count at <code class="addr">$03A5</code>/<code class="addr">$03A6</code>. Finally it sets <code class="addr">$0359</code> = <code class="addr">$FF</code> for the screen flash. A record whose byte 7 is already negative is immune.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">4951</span>  <span class="rt-bytes">85 68   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">4953</span>  <span class="rt-bytes">A0 07   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">4955</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4957</span>  <span class="rt-bytes">30 30   </span>  <span class="rt-op">BMI</span>  <span class="rt-arg">$4989</span>
<span class="rt-addr">4959</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">495A</span>  <span class="rt-bytes">E5 68   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">495C</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">495E</span>  <span class="rt-bytes">B0 29   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$4989</span>
<span class="rt-addr">4960</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4962</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4963</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4965</span>  <span class="rt-bytes">A9 04   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">4967</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">496A</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">496C</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">496E</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">4970</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4972</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">4974</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4975</span>  <span class="rt-bytes">BD 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,X</span>
<span class="rt-addr">4978</span>  <span class="rt-bytes">29 40   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">497A</span>  <span class="rt-bytes">F0 08   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4984</span>
<span class="rt-addr">497C</span>  <span class="rt-bytes">EE A5 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$03A5</span>   <span class="rt-cmt">; Kill count (low)</span>
<span class="rt-addr">497F</span>  <span class="rt-bytes">D0 03   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4984</span>
<span class="rt-addr">4981</span>  <span class="rt-bytes">EE A6 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$03A6</span>   <span class="rt-cmt">; Kill count (high)</span>
<span class="rt-addr">4984</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">4986</span>  <span class="rt-bytes">8D 59 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0359</span>
<span class="rt-addr">4989</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JSR` at `$3D89` in [`Laser bolt: timer and hit`](laser-bolt.md)
- `JSR` at `$4615` in [`Guided-object handling`](guided-objects.md)
- `JSR` at `$52A8`
- `JSR` at `$61E3`
- `JSR` at `$7D3D`
- `JSR` at `$C0F9`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
