# Dying animation

**Address** `$441E-$445C` &nbsp;·&nbsp; **Group** Records

<p class="lede">Byte 6 falls by 8 a frame; when it reaches zero, byte 8 climbs by 8 a frame. At <code class="addr">$F8</code> the record is freed. Types carrying bit 0 of <code class="addr">$C39A</code> (including both missile types) are freed at <code class="addr">$78</code> instead, after 15 frames rather than 31.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">441E</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">4420</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4422</span>  <span class="rt-bytes">F0 0C   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4430</span>
<span class="rt-addr">4424</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4425</span>  <span class="rt-bytes">E9 08   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4427</span>  <span class="rt-bytes">B0 02   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$442B</span>
<span class="rt-addr">4429</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">442B</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">442D</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4430</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4432</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4434</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4435</span>  <span class="rt-bytes">69 08   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4437</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4439</span>  <span class="rt-bytes">C9 F8   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$F8</span>
<span class="rt-addr">443B</span>  <span class="rt-bytes">B0 13   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$4450</span>
<span class="rt-addr">443D</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">443E</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4440</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4442</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">4444</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4445</span>  <span class="rt-bytes">B9 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,Y</span>
<span class="rt-addr">4448</span>  <span class="rt-bytes">29 01   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">444A</span>  <span class="rt-bytes">F0 9F   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">444C</span>  <span class="rt-bytes">E0 78   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$78</span>
<span class="rt-addr">444E</span>  <span class="rt-bytes">90 9B   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4450</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4452</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4454</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">4456</span>  <span class="rt-bytes">09 80   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">4458</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">445A</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JMP` at `$5B6F`
- `JMP` at `$5EF6`
- `JMP` at `$6979`
- `JMP` at `$7B8C`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
