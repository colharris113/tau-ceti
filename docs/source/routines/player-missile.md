# Player missile launch

**Address** `$4878-$4905` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Refuses to fire at <code class="addr">$0389</code> = 0 (no target). Otherwise finds a free record, makes it type 10, copies the ship's cell and sub-cell, sets byte 6 to altitude + <code class="addr">$40</code>, points bytes 14/15 at the target, sets the target's lock bit (byte 3 bit 4) and decrements the missile count at <code class="addr">$0358</code>.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">4878</span>  <span class="rt-bytes">AD 89 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0389</span>
<span class="rt-addr">487B</span>  <span class="rt-bytes">D0 08   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4885</span>
<span class="rt-addr">487D</span>  <span class="rt-bytes">A9 70   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$70</span>
<span class="rt-addr">487F</span>  <span class="rt-bytes">A2 3C   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$3C</span>
<span class="rt-addr">4881</span>  <span class="rt-bytes">20 27 41</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4127</span>   <span class="rt-cmt">; Message queue</span>
<span class="rt-addr">4884</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">4885</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4887</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">4889</span>  <span class="rt-bytes">A9 0E   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">488B</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">488C</span>  <span class="rt-bytes">69 02   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">488E</span>  <span class="rt-bytes">85 62   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">4890</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4892</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4894</span>  <span class="rt-bytes">30 08   </span>  <span class="rt-op">BMI</span>  <span class="rt-arg">$489E</span>
<span class="rt-addr">4896</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4897</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4898</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">489A</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">489B</span>  <span class="rt-bytes">D0 F5   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4892</span>
<span class="rt-addr">489D</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">489E</span>  <span class="rt-bytes">CE 58 03</span>  <span class="rt-op">DEC</span>  <span class="rt-arg">$0358</span>   <span class="rt-cmt">; Missiles</span>
<span class="rt-addr">48A1</span>  <span class="rt-bytes">A9 05   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$05</span>
<span class="rt-addr">48A3</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">48A6</span>  <span class="rt-bytes">A9 0A   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0A</span>
<span class="rt-addr">48A8</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48AA</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48AB</span>  <span class="rt-bytes">AD 3C 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033C</span>
<span class="rt-addr">48AE</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48B0</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48B1</span>  <span class="rt-bytes">AD 3F 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033F</span>
<span class="rt-addr">48B4</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48B6</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48B7</span>  <span class="rt-bytes">A9 40   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">48B9</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48BB</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48BC</span>  <span class="rt-bytes">AD 3B 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033B</span>
<span class="rt-addr">48BF</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48C1</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48C2</span>  <span class="rt-bytes">AD 3E 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033E</span>
<span class="rt-addr">48C5</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48C7</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48C8</span>  <span class="rt-bytes">AD 44 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">48CB</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">48CC</span>  <span class="rt-bytes">69 40   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">48CE</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48D0</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48D1</span>  <span class="rt-bytes">A9 01   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">48D3</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48D5</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48D6</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">48D8</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48DA</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">48DB</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">48DC</span>  <span class="rt-bytes">69 06   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">48DE</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48DF</span>  <span class="rt-bytes">AD 88 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0388</span>   <span class="rt-cmt">; Missile target</span>
<span class="rt-addr">48E2</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48E4</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">48E6</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">48E7</span>  <span class="rt-bytes">AD 89 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0389</span>
<span class="rt-addr">48EA</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">48EC</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">48EE</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">48F0</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">48F2</span>  <span class="rt-bytes">09 10   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">48F4</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">48F6</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">48F8</span>  <span class="rt-bytes">8D BF 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03BF</span>   <span class="rt-cmt">; Provocation latch</span>
<span class="rt-addr">48FB</span>  <span class="rt-bytes">A9 83   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$83</span>
<span class="rt-addr">48FD</span>  <span class="rt-bytes">A2 3C   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$3C</span>
<span class="rt-addr">48FF</span>  <span class="rt-bytes">20 27 41</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4127</span>   <span class="rt-cmt">; Message queue</span>
<span class="rt-addr">4902</span>  <span class="rt-bytes">20 0A 35</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$350A</span>
<span class="rt-addr">4905</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`Message queue`](message-queue.md) from `$4881`

## Called by

- `JSR` at `$3BB9`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
