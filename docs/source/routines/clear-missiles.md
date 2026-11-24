# Clear all missiles (AMM)

**Address** `$4838-$4877` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Walks the record table and marks every missile record dying - the player's type 10 and the robots' type 11 alike. Nothing else is touched: the selected target in <code class="addr">$0388</code>/<code class="addr">$0389</code> survives, as does the target's lock bit. Both missile types are freed after 15 frames.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">4838</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">483A</span>  <span class="rt-bytes">8D 59 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0359</span>
<span class="rt-addr">483D</span>  <span class="rt-bytes">A9 02   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">483F</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">4842</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4844</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">4846</span>  <span class="rt-bytes">A9 10   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">4848</span>  <span class="rt-bytes">85 62   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">484A</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">484C</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">484E</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">484F</span>  <span class="rt-bytes">29 C0   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">4851</span>  <span class="rt-bytes">D0 1B   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$486E</span>
<span class="rt-addr">4853</span>  <span class="rt-bytes">BD 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,X</span>
<span class="rt-addr">4856</span>  <span class="rt-bytes">29 0C   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0C</span>
<span class="rt-addr">4858</span>  <span class="rt-bytes">F0 14   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$486E</span>
<span class="rt-addr">485A</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">485C</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">485E</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4860</span>  <span class="rt-bytes">A9 0B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0B</span>
<span class="rt-addr">4862</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">4865</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4866</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4867</span>  <span class="rt-bytes">69 08   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">4869</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">486A</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">486C</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">486E</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">486F</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4870</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">4872</span>  <span class="rt-bytes">29 F0   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$F0</span>
<span class="rt-addr">4874</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4875</span>  <span class="rt-bytes">D0 D5   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$484C</span>
<span class="rt-addr">4877</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JSR` at `$3BDA`
- `JSR` at `$527B`
- `JSR` at `$829A` in [`Static defence AI`](static-defence-ai.md)
- `JSR` at `$C1F2`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
