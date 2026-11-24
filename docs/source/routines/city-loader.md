# City loader: the sheet at $9400 into the record table

**Address** `$27EC-$28E5` &nbsp;·&nbsp; **Group** Records

<p class="lede">Rebuilds the 48-record table at <code class="addr">$0E00</code> for the city index in <code class="addr">$0354</code>. The pointer builder at <code class="addr">$27EC</code> multiplies the index by three and then shifts right three times, which is exactly a stride of 96 bytes: <code class="addr">$9400</code> + city × <code class="addr">$60</code>. The loop copies up to 32 three-byte records (type, x, y) from that sheet, stopping at a type byte of <code class="addr">$C0</code>, zeroes bytes 3-15 of each record, and copies hit points from <code class="addr">$C3BF</code>[type &amp; <code class="addr">$3F</code>] into byte 7. It then scans the city's four bytes at <code class="addr">$8900</code>, which hold jump destinations (a byte of <code class="addr">$80</code> or more is empty), and appends a pair of pad records for each one from the four shared templates at <code class="addr">$C4BE</code> + n × 8. Whatever space is left in the table is filled with type <code class="addr">$C0</code>, and the provocation latch at <code class="addr">$03BF</code> is cleared.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">27EC</span>  <span class="rt-bytes">AD 54 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0354</span>
<span class="rt-addr">27EF</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">27F0</span>  <span class="rt-bytes">6D 54 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$0354</span>
<span class="rt-addr">27F3</span>  <span class="rt-bytes">A2 00   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">27F5</span>  <span class="rt-bytes">86 61   </span>  <span class="rt-op">STX</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">27F7</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">27F8</span>  <span class="rt-bytes">66 61   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">27FA</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">27FB</span>  <span class="rt-bytes">66 61   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">27FD</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">27FE</span>  <span class="rt-bytes">66 61   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">2800</span>  <span class="rt-bytes">69 94   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$94</span>
<span class="rt-addr">2802</span>  <span class="rt-bytes">85 62   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">2804</span>  <span class="rt-bytes">86 63   </span>  <span class="rt-op">STX</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">2806</span>  <span class="rt-bytes">A9 0E   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">2808</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">280A</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">280B</span>  <span class="rt-bytes">20 EC 27</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$27EC</span>   <span class="rt-cmt">; City loader: the sheet at $9400 into the record table</span>
<span class="rt-addr">280E</span>  <span class="rt-bytes">A2 20   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">2810</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2812</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2814</span>  <span class="rt-bytes">C9 C0   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">2816</span>  <span class="rt-bytes">F0 39   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$2851</span>
<span class="rt-addr">2818</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">281A</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">281C</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">281D</span>  <span class="rt-bytes">C0 03   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">281F</span>  <span class="rt-bytes">90 F7   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2818</span>
<span class="rt-addr">2821</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2823</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2825</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2826</span>  <span class="rt-bytes">C0 10   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2828</span>  <span class="rt-bytes">D0 F9   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2823</span>
<span class="rt-addr">282A</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">282C</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">282E</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">2830</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2831</span>  <span class="rt-bytes">B9 BF C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C3BF,Y</span>
<span class="rt-addr">2834</span>  <span class="rt-bytes">A0 07   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">2836</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2838</span>  <span class="rt-bytes">A5 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">283A</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">283B</span>  <span class="rt-bytes">69 03   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">283D</span>  <span class="rt-bytes">85 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$61</span>
<span class="rt-addr">283F</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2843</span>
<span class="rt-addr">2841</span>  <span class="rt-bytes">E6 62   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$62</span>
<span class="rt-addr">2843</span>  <span class="rt-bytes">A5 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">2845</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2846</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2848</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">284A</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$284E</span>
<span class="rt-addr">284C</span>  <span class="rt-bytes">E6 64   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">284E</span>  <span class="rt-bytes">CA      </span>  <span class="rt-op">DEX</span>  <span class="rt-arg"></span>
<span class="rt-addr">284F</span>  <span class="rt-bytes">D0 BF   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2810</span>
<span class="rt-addr">2851</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2852</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2853</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2855</span>  <span class="rt-bytes">85 67   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">2857</span>  <span class="rt-bytes">AD 54 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0354</span>
<span class="rt-addr">285A</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">285B</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">285C</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">285D</span>  <span class="rt-bytes">BD 00 89</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$8900,X</span>
<span class="rt-addr">2860</span>  <span class="rt-bytes">10 09   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$286B</span>
<span class="rt-addr">2862</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">2863</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2864</span>  <span class="rt-bytes">29 03   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">2866</span>  <span class="rt-bytes">D0 F5   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$285D</span>
<span class="rt-addr">2868</span>  <span class="rt-bytes">4C C4 28</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$28C4</span>
<span class="rt-addr">286B</span>  <span class="rt-bytes">A0 1F   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$1F</span>
<span class="rt-addr">286D</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">286F</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2871</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2872</span>  <span class="rt-bytes">10 FB   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$286F</span>
<span class="rt-addr">2874</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2875</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2876</span>  <span class="rt-bytes">29 03   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">2878</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2879</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">287A</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">287B</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">287C</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">287E</span>  <span class="rt-bytes">BD BE C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4BE,X</span>
<span class="rt-addr">2881</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2883</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2884</span>  <span class="rt-bytes">BD BF C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4BF,X</span>
<span class="rt-addr">2887</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2889</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">288A</span>  <span class="rt-bytes">BD C0 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C0,X</span>
<span class="rt-addr">288D</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">288F</span>  <span class="rt-bytes">A0 07   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">2891</span>  <span class="rt-bytes">BD C1 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C1,X</span>
<span class="rt-addr">2894</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">2896</span>  <span class="rt-bytes">A0 10   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2898</span>  <span class="rt-bytes">BD C2 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C2,X</span>
<span class="rt-addr">289B</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">289D</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">289E</span>  <span class="rt-bytes">BD C3 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C3,X</span>
<span class="rt-addr">28A1</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28A3</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">28A4</span>  <span class="rt-bytes">BD C4 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C4,X</span>
<span class="rt-addr">28A7</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28A9</span>  <span class="rt-bytes">A0 17   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$17</span>
<span class="rt-addr">28AB</span>  <span class="rt-bytes">BD C5 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C4C5,X</span>
<span class="rt-addr">28AE</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28B0</span>  <span class="rt-bytes">A5 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">28B2</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">28B3</span>  <span class="rt-bytes">69 20   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">28B5</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">28B7</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$28BB</span>
<span class="rt-addr">28B9</span>  <span class="rt-bytes">E6 64   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">28BB</span>  <span class="rt-bytes">C6 67   </span>  <span class="rt-op">DEC</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">28BD</span>  <span class="rt-bytes">C6 67   </span>  <span class="rt-op">DEC</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">28BF</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">28C0</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">28C1</span>  <span class="rt-bytes">4C 62 28</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2862</span>
<span class="rt-addr">28C4</span>  <span class="rt-bytes">A0 0F   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">28C6</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">28C8</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28CA</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">28CB</span>  <span class="rt-bytes">D0 FB   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$28C8</span>
<span class="rt-addr">28CD</span>  <span class="rt-bytes">A9 C0   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">28CF</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">28D1</span>  <span class="rt-bytes">A5 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">28D3</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">28D4</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">28D6</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">28D8</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$28DC</span>
<span class="rt-addr">28DA</span>  <span class="rt-bytes">E6 64   </span>  <span class="rt-op">INC</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">28DC</span>  <span class="rt-bytes">C6 67   </span>  <span class="rt-op">DEC</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">28DE</span>  <span class="rt-bytes">D0 E4   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$28C4</span>
<span class="rt-addr">28E0</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">28E2</span>  <span class="rt-bytes">8D BF 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03BF</span>   <span class="rt-cmt">; Provocation latch</span>
<span class="rt-addr">28E5</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JSR` at `$28E6` in [`City save: writing damage back to the sheet`](city-save.md)
- `JSR` at `$51DB`
- `JSR` at `$64F3`
- `JSR` at `$6B72`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
