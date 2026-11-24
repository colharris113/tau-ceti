# Frame tick: clock, shield and fuel

**Address** `$25D3-$26CB` &nbsp;·&nbsp; **Group** Flight

<p class="lede">Runs once a frame. A BCD counter at <code class="addr">$0340</code> counts 50 frames to a second, then the BCD clock at <code class="addr">$0341</code>-<code class="addr">$0343</code> advances. While not docked the shield creeps back one point a second and fuel is burned: (speed &gt;&gt; 3) + 16 while airborne, zero at altitude zero, plus 96 when the tank is ruptured. The burn is subtracted from the 16-bit value at <code class="addr">$0345</code>/<code class="addr">$0346</code>; a high byte of <code class="addr">$20</code> raises the LOW FUEL flag, and an underflow clamps at zero and sets <code class="addr">$03A3</code>. Docking or grounding skips both the burn and the shield regeneration.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">25D3</span>  <span class="rt-bytes">E6 11   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$11</span>
<span class="rt-addr">25D5</span>  <span class="rt-bytes">AD AF 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03AF</span>
<span class="rt-addr">25D8</span>  <span class="rt-bytes">F0 01   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$25DB</span>
<span class="rt-addr">25DA</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">25DB</span>  <span class="rt-bytes">F8      </span>  <span class="rt-op">SED</span>  <span class="rt-arg"></span>
<span class="rt-addr">25DC</span>  <span class="rt-bytes">AD 40 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0340</span>   <span class="rt-cmt">; Frame counter</span>
<span class="rt-addr">25DF</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">25E0</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">25E2</span>  <span class="rt-bytes">8D 40 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0340</span>   <span class="rt-cmt">; Frame counter</span>
<span class="rt-addr">25E5</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">25E6</span>  <span class="rt-bytes">29 0F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">25E8</span>  <span class="rt-bytes">D0 08   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$25F2</span>
<span class="rt-addr">25EA</span>  <span class="rt-bytes">AD 56 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0356</span>
<span class="rt-addr">25ED</span>  <span class="rt-bytes">F0 03   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$25F2</span>
<span class="rt-addr">25EF</span>  <span class="rt-bytes">CE 56 03</span>  <span class="rt-op">DEC</span>  <span class="rt-arg">$0356</span>
<span class="rt-addr">25F2</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">25F3</span>  <span class="rt-bytes">C9 50   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$50</span>
<span class="rt-addr">25F5</span>  <span class="rt-bytes">B0 03   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$25FA</span>
<span class="rt-addr">25F7</span>  <span class="rt-bytes">4C A0 26</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$26A0</span>
<span class="rt-addr">25FA</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">25FC</span>  <span class="rt-bytes">8D 40 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0340</span>   <span class="rt-cmt">; Frame counter</span>
<span class="rt-addr">25FF</span>  <span class="rt-bytes">6D 41 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0341</span>   <span class="rt-cmt">; Seconds</span>
<span class="rt-addr">2602</span>  <span class="rt-bytes">8D 41 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0341</span>   <span class="rt-cmt">; Seconds</span>
<span class="rt-addr">2605</span>  <span class="rt-bytes">EE 76 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$0376</span>
<span class="rt-addr">2608</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2609</span>  <span class="rt-bytes">29 01   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">260B</span>  <span class="rt-bytes">D0 1A   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2627</span>
<span class="rt-addr">260D</span>  <span class="rt-bytes">EE 35 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$0335</span>
<span class="rt-addr">2610</span>  <span class="rt-bytes">D0 0B   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$261D</span>
<span class="rt-addr">2612</span>  <span class="rt-bytes">AD 36 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0336</span>
<span class="rt-addr">2615</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2616</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2618</span>  <span class="rt-bytes">29 01   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">261A</span>  <span class="rt-bytes">8D 36 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0336</span>
<span class="rt-addr">261D</span>  <span class="rt-bytes">AD 35 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0335</span>
<span class="rt-addr">2620</span>  <span class="rt-bytes">29 1F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$1F</span>
<span class="rt-addr">2622</span>  <span class="rt-bytes">D0 03   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2627</span>
<span class="rt-addr">2624</span>  <span class="rt-bytes">EE 9C 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$039C</span>
<span class="rt-addr">2627</span>  <span class="rt-bytes">AD 96 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0396</span>   <span class="rt-cmt">; Dock state</span>
<span class="rt-addr">262A</span>  <span class="rt-bytes">D0 4C   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2678</span>
<span class="rt-addr">262C</span>  <span class="rt-bytes">AD 77 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0377</span>   <span class="rt-cmt">; Shield</span>
<span class="rt-addr">262F</span>  <span class="rt-bytes">C9 BF   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$BF</span>
<span class="rt-addr">2631</span>  <span class="rt-bytes">B0 03   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2636</span>
<span class="rt-addr">2633</span>  <span class="rt-bytes">EE 77 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$0377</span>   <span class="rt-cmt">; Shield</span>
<span class="rt-addr">2636</span>  <span class="rt-bytes">D8      </span>  <span class="rt-op">CLD</span>  <span class="rt-arg"></span>
<span class="rt-addr">2637</span>  <span class="rt-bytes">AD 44 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">263A</span>  <span class="rt-bytes">F0 09   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$2645</span>
<span class="rt-addr">263C</span>  <span class="rt-bytes">AD 53 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0353</span>   <span class="rt-cmt">; Speed</span>
<span class="rt-addr">263F</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2640</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2641</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2642</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2643</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2645</span>  <span class="rt-bytes">AE 9E 03</span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$039E</span>   <span class="rt-cmt">; Tank ruptured</span>
<span class="rt-addr">2648</span>  <span class="rt-bytes">F0 03   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$264D</span>
<span class="rt-addr">264A</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">264B</span>  <span class="rt-bytes">69 60   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$60</span>
<span class="rt-addr">264D</span>  <span class="rt-bytes">49 FF   </span>  <span class="rt-op">EOR</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">264F</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2650</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2652</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2653</span>  <span class="rt-bytes">6D 45 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0345</span>   <span class="rt-cmt">; Fuel (low byte)</span>
<span class="rt-addr">2656</span>  <span class="rt-bytes">8D 45 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0345</span>   <span class="rt-cmt">; Fuel (low byte)</span>
<span class="rt-addr">2659</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">265B</span>  <span class="rt-bytes">6D 46 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0346</span>   <span class="rt-cmt">; Fuel (whole units)</span>
<span class="rt-addr">265E</span>  <span class="rt-bytes">8D 46 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0346</span>   <span class="rt-cmt">; Fuel (whole units)</span>
<span class="rt-addr">2661</span>  <span class="rt-bytes">B0 08   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$266B</span>
<span class="rt-addr">2663</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2665</span>  <span class="rt-bytes">8D 46 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0346</span>   <span class="rt-cmt">; Fuel (whole units)</span>
<span class="rt-addr">2668</span>  <span class="rt-bytes">EE A3 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$03A3</span>   <span class="rt-cmt">; NO FUEL flag</span>
<span class="rt-addr">266B</span>  <span class="rt-bytes">C9 20   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">266D</span>  <span class="rt-bytes">D0 08   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2677</span>
<span class="rt-addr">266F</span>  <span class="rt-bytes">AD A2 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03A2</span>   <span class="rt-cmt">; LOW FUEL flag</span>
<span class="rt-addr">2672</span>  <span class="rt-bytes">D0 03   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2677</span>
<span class="rt-addr">2674</span>  <span class="rt-bytes">EE A2 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$03A2</span>   <span class="rt-cmt">; LOW FUEL flag</span>
<span class="rt-addr">2677</span>  <span class="rt-bytes">F8      </span>  <span class="rt-op">SED</span>  <span class="rt-arg"></span>
<span class="rt-addr">2678</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2679</span>  <span class="rt-bytes">C9 60   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$60</span>
<span class="rt-addr">267B</span>  <span class="rt-bytes">90 23   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$26A0</span>
<span class="rt-addr">267D</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">267F</span>  <span class="rt-bytes">8D 41 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0341</span>   <span class="rt-cmt">; Seconds</span>
<span class="rt-addr">2682</span>  <span class="rt-bytes">6D 42 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0342</span>   <span class="rt-cmt">; Minutes</span>
<span class="rt-addr">2685</span>  <span class="rt-bytes">8D 42 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0342</span>   <span class="rt-cmt">; Minutes</span>
<span class="rt-addr">2688</span>  <span class="rt-bytes">C9 60   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$60</span>
<span class="rt-addr">268A</span>  <span class="rt-bytes">90 14   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$26A0</span>
<span class="rt-addr">268C</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">268E</span>  <span class="rt-bytes">8D 42 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0342</span>   <span class="rt-cmt">; Minutes</span>
<span class="rt-addr">2691</span>  <span class="rt-bytes">6D 43 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0343</span>   <span class="rt-cmt">; Hours</span>
<span class="rt-addr">2694</span>  <span class="rt-bytes">8D 43 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0343</span>   <span class="rt-cmt">; Hours</span>
<span class="rt-addr">2697</span>  <span class="rt-bytes">C9 24   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$24</span>
<span class="rt-addr">2699</span>  <span class="rt-bytes">90 05   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$26A0</span>
<span class="rt-addr">269B</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">269D</span>  <span class="rt-bytes">8D 43 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0343</span>   <span class="rt-cmt">; Hours</span>
<span class="rt-addr">26A0</span>  <span class="rt-bytes">D8      </span>  <span class="rt-op">CLD</span>  <span class="rt-arg"></span>
<span class="rt-addr">26A1</span>  <span class="rt-bytes">A5 11   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$11</span>
<span class="rt-addr">26A3</span>  <span class="rt-bytes">AE 74 03</span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$0374</span>
<span class="rt-addr">26A6</span>  <span class="rt-bytes">D0 01   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$26A9</span>
<span class="rt-addr">26A8</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">26A9</span>  <span class="rt-bytes">29 04   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">26AB</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">26AC</span>  <span class="rt-bytes">AD 75 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0375</span>
<span class="rt-addr">26AF</span>  <span class="rt-bytes">29 70   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$70</span>
<span class="rt-addr">26B1</span>  <span class="rt-bytes">F0 07   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$26BA</span>
<span class="rt-addr">26B3</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">26B4</span>  <span class="rt-bytes">09 02   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">26B6</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">26B7</span>  <span class="rt-bytes">4C C5 26</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$26C5</span>
<span class="rt-addr">26BA</span>  <span class="rt-bytes">AD 75 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0375</span>
<span class="rt-addr">26BD</span>  <span class="rt-bytes">29 08   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">26BF</span>  <span class="rt-bytes">F0 04   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$26C5</span>
<span class="rt-addr">26C1</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">26C2</span>  <span class="rt-bytes">09 01   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">26C4</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">26C5</span>  <span class="rt-bytes">BD 52 64</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$6452,X</span>
<span class="rt-addr">26C8</span>  <span class="rt-bytes">8D A6 DA</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$DAA6</span>
<span class="rt-addr">26CB</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JSR` at `$4A08`
- `JSR` at `$4A44`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
