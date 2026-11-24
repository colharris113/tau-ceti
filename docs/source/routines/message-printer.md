# Message text renderer

**Address** `$41F7-$424B` &nbsp;·&nbsp; **Group** Messages

<p class="lede">Reads one character code at a time from the pointer in <code class="addr">$1C</code>/<code class="addr">$1D</code>. Codes under <code class="addr">$80</code> select an 8-byte glyph from the game's own font at <code class="addr">$9000</code>-<code class="addr">$92FF</code> (32 glyphs a page); <code class="addr">$80</code> is a control code, and <code class="addr">$FF</code> ends the string. The glyph is copied into the character/sprite buffer at <code class="addr">$FCC8</code>.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">41F7</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">41F9</span>  <span class="rt-bytes">B1 1C   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($1C),Y</span>
<span class="rt-addr">41FB</span>  <span class="rt-bytes">E6 1C   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$1C</span>
<span class="rt-addr">41FD</span>  <span class="rt-bytes">D0 02   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4201</span>
<span class="rt-addr">41FF</span>  <span class="rt-bytes">E6 1D   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$1D</span>
<span class="rt-addr">4201</span>  <span class="rt-bytes">C9 80   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">4203</span>  <span class="rt-bytes">90 0B   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$4210</span>
<span class="rt-addr">4205</span>  <span class="rt-bytes">F0 06   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$420D</span>
<span class="rt-addr">4207</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4209</span>  <span class="rt-bytes">8D A1 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A1</span>
<span class="rt-addr">420C</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">420D</span>  <span class="rt-bytes">4C E4 40</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$40E4</span>
<span class="rt-addr">4210</span>  <span class="rt-bytes">AC 85 03</span>  <span class="rt-op">LDY</span>  <span class="rt-arg">$0385</span>
<span class="rt-addr">4213</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">4214</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">4215</span>  <span class="rt-bytes">B0 22   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$4239</span>
<span class="rt-addr">4217</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">4218</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4219</span>  <span class="rt-bytes">B0 0F   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$422A</span>
<span class="rt-addr">421B</span>  <span class="rt-bytes">BD 00 90</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$9000,X</span>
<span class="rt-addr">421E</span>  <span class="rt-bytes">99 C8 FC</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FCC8,Y</span>
<span class="rt-addr">4221</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4222</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4223</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4224</span>  <span class="rt-bytes">29 07   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">4226</span>  <span class="rt-bytes">D0 F3   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$421B</span>
<span class="rt-addr">4228</span>  <span class="rt-bytes">F0 1E   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4248</span>
<span class="rt-addr">422A</span>  <span class="rt-bytes">BD 00 91</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$9100,X</span>
<span class="rt-addr">422D</span>  <span class="rt-bytes">99 C8 FC</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FCC8,Y</span>
<span class="rt-addr">4230</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4231</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4232</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4233</span>  <span class="rt-bytes">29 07   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">4235</span>  <span class="rt-bytes">D0 F3   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$422A</span>
<span class="rt-addr">4237</span>  <span class="rt-bytes">F0 0F   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$4248</span>
<span class="rt-addr">4239</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">423A</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">423B</span>  <span class="rt-bytes">BD 00 92</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$9200,X</span>
<span class="rt-addr">423E</span>  <span class="rt-bytes">99 C8 FC</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FCC8,Y</span>
<span class="rt-addr">4241</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4242</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4243</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4244</span>  <span class="rt-bytes">29 07   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">4246</span>  <span class="rt-bytes">D0 F3   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$423B</span>
<span class="rt-addr">4248</span>  <span class="rt-bytes">8C 85 03</span>  <span class="rt-op">STY</span>  <span class="rt-arg">$0385</span>
<span class="rt-addr">424B</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JMP` at `$3CB2`
- `JSR` at `$4180`
- `JSR` at `$41D0`
- `JSR` at `$534A`
- `JMP` at `$5F4F`
- `JMP` at `$6009`
- `JMP` at `$79E3`
- `JSR` at `$BED9`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
