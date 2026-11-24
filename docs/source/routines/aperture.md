# Aperture animation

**Address** `$4465-$44A0` &nbsp;·&nbsp; **Group** Records

<p class="lede">Dockable buildings only, and only while byte 3 bit 6 says the record is active. A missile lock (bit 4) or a hit (bit 5) shuts the iris two points a frame, except on type 27; otherwise it shuts while the scaled distance byte 13 is 2 or more, and opens two points a frame to <code class="addr">$48</code> while byte 13 is below 2. The door takes 36 frames to travel from shut to fully open.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">4465</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">4467</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4469</span>  <span class="rt-bytes">29 40   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">446B</span>  <span class="rt-bytes">F0 19   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4486</span>
<span class="rt-addr">446D</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">446F</span>  <span class="rt-bytes">29 30   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$30</span>
<span class="rt-addr">4471</span>  <span class="rt-bytes">F0 16   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4489</span>
<span class="rt-addr">4473</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4475</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4477</span>  <span class="rt-bytes">C9 1B   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$1B</span>
<span class="rt-addr">4479</span>  <span class="rt-bytes">F0 0E   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4489</span>
<span class="rt-addr">447B</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">447D</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">447F</span>  <span class="rt-bytes">F0 05   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4486</span>
<span class="rt-addr">4481</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4482</span>  <span class="rt-bytes">E9 02   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">4484</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4486</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4489</span>  <span class="rt-bytes">A0 0D   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0D</span>
<span class="rt-addr">448B</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">448D</span>  <span class="rt-bytes">C9 02   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">448F</span>  <span class="rt-bytes">B0 EA   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$447B</span>
<span class="rt-addr">4491</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4493</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4495</span>  <span class="rt-bytes">C9 48   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$48</span>
<span class="rt-addr">4497</span>  <span class="rt-bytes">B0 28   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$44C1</span>
<span class="rt-addr">4499</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">449A</span>  <span class="rt-bytes">69 02   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">449C</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">449E</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
</pre>

## Calls

*None recorded in this body.*

## Called by

*No call site found in the swept listings; this may be reached through a jump table or from undisassembled code.*

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
