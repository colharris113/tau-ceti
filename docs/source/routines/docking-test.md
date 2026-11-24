# Object distance and the docking test

**Address** `$2B60-$2CBF` &nbsp;·&nbsp; **Group** Docking

<p class="lede">Works out the distance to the record in <code class="addr">$61</code>/<code class="addr">$62</code>, scales it through the tables at <code class="addr">$C800</code>/<code class="addr">$C900</code> and stores the product in bytes 12/13. Only a product under 128 is close enough to dock; anything up to 4,095 is added to the target list, and anything larger is dropped. For a close record, type 16 docks as a jump pad before anything else. A dockable building must pass |altitude - 28| + 55 &lt; aperture, then a bearing test that allows a window of |bearing offset| + 56 against the same aperture. Passing both sets <code class="addr">$0396</code> = <code class="addr">$80</code> and copies the building's type and cell to <code class="addr">$03A4</code>/<code class="addr">$0398</code>/<code class="addr">$0399</code>.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">2B60</span>  <span class="rt-bytes">A6 5A   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2B62</span>  <span class="rt-bytes">A5 5B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$5B</span>
<span class="rt-addr">2B64</span>  <span class="rt-bytes">C9 01   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2B66</span>  <span class="rt-bytes">F0 1A   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$2B82</span>
<span class="rt-addr">2B68</span>  <span class="rt-bytes">C9 0A   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$0A</span>
<span class="rt-addr">2B6A</span>  <span class="rt-bytes">B0 1C   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2B88</span>
<span class="rt-addr">2B6C</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2B6D</span>  <span class="rt-bytes">E9 02   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">2B6F</span>  <span class="rt-bytes">86 55   </span>  <span class="rt-op">STX</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B71</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2B72</span>  <span class="rt-bytes">66 55   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B74</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2B75</span>  <span class="rt-bytes">66 55   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B77</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2B78</span>  <span class="rt-bytes">66 55   </span>  <span class="rt-op">ROR</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B7A</span>  <span class="rt-bytes">A6 55   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B7C</span>  <span class="rt-bytes">BD 00 C9</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C900,X</span>
<span class="rt-addr">2B7F</span>  <span class="rt-bytes">4C 8A 2B</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2B8A</span>
<span class="rt-addr">2B82</span>  <span class="rt-bytes">BD 00 C8</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C800,X</span>
<span class="rt-addr">2B85</span>  <span class="rt-bytes">4C 8A 2B</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2B8A</span>
<span class="rt-addr">2B88</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2B8A</span>  <span class="rt-bytes">85 26   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2B8C</span>  <span class="rt-bytes">A6 58   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$58</span>
<span class="rt-addr">2B8E</span>  <span class="rt-bytes">A4 59   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">$59</span>
<span class="rt-addr">2B90</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2B92</span>  <span class="rt-bytes">85 57   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$57</span>
<span class="rt-addr">2B94</span>  <span class="rt-bytes">85 55   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2B96</span>  <span class="rt-bytes">46 26   </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2B98</span>  <span class="rt-bytes">90 0F   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2BA9</span>
<span class="rt-addr">2B9A</span>  <span class="rt-bytes">A5 57   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$57</span>
<span class="rt-addr">2B9C</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2B9D</span>  <span class="rt-bytes">65 58   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$58</span>
<span class="rt-addr">2B9F</span>  <span class="rt-bytes">85 57   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$57</span>
<span class="rt-addr">2BA1</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BA2</span>  <span class="rt-bytes">65 59   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$59</span>
<span class="rt-addr">2BA4</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BA5</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BA6</span>  <span class="rt-bytes">65 55   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2BA8</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BA9</span>  <span class="rt-bytes">06 58   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$58</span>
<span class="rt-addr">2BAB</span>  <span class="rt-bytes">26 59   </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">$59</span>
<span class="rt-addr">2BAD</span>  <span class="rt-bytes">26 55   </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">$55</span>
<span class="rt-addr">2BAF</span>  <span class="rt-bytes">A5 26   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2BB1</span>  <span class="rt-bytes">D0 E3   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2B96</span>
<span class="rt-addr">2BB3</span>  <span class="rt-bytes">C0 10   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2BB5</span>  <span class="rt-bytes">90 03   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2BBA</span>
<span class="rt-addr">2BB7</span>  <span class="rt-bytes">4C 5B 2A</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2A5B</span>
<span class="rt-addr">2BBA</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BBB</span>  <span class="rt-bytes">08      </span>  <span class="rt-op">PHP</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BBC</span>  <span class="rt-bytes">A0 0D   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0D</span>
<span class="rt-addr">2BBE</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BC0</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BC1</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BC2</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BC4</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">2BC6</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BC8</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">2BCA</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BCC</span>  <span class="rt-bytes">28      </span>  <span class="rt-op">PLP</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BCD</span>  <span class="rt-bytes">D0 04   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2BD3</span>
<span class="rt-addr">2BCF</span>  <span class="rt-bytes">E0 80   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">2BD1</span>  <span class="rt-bytes">90 03   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2BD6</span>
<span class="rt-addr">2BD3</span>  <span class="rt-bytes">4C C0 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CC0</span>
<span class="rt-addr">2BD6</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2BD8</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BDA</span>  <span class="rt-bytes">29 C0   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">2BDC</span>  <span class="rt-bytes">D0 3B   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2C19</span>
<span class="rt-addr">2BDE</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2BE0</span>  <span class="rt-bytes">C9 10   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2BE2</span>  <span class="rt-bytes">D0 15   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2BF9</span>
<span class="rt-addr">2BE4</span>  <span class="rt-bytes">AD 6C 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$036C</span>
<span class="rt-addr">2BE7</span>  <span class="rt-bytes">D0 08   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2BF1</span>
<span class="rt-addr">2BE9</span>  <span class="rt-bytes">AE 0F 01</span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$010F</span>
<span class="rt-addr">2BEC</span>  <span class="rt-bytes">20 18 3D</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3D18</span>   <span class="rt-cmt">; Flag-bit test</span>
<span class="rt-addr">2BEF</span>  <span class="rt-bytes">D0 28   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2C19</span>
<span class="rt-addr">2BF1</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2BF3</span>  <span class="rt-bytes">8D 9B 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$039B</span>   <span class="rt-cmt">; Jump pad docked</span>
<span class="rt-addr">2BF6</span>  <span class="rt-bytes">4C BD 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2BF9</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2BFA</span>  <span class="rt-bytes">B9 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,Y</span>
<span class="rt-addr">2BFD</span>  <span class="rt-bytes">10 61   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$2C60</span>
<span class="rt-addr">2BFF</span>  <span class="rt-bytes">AD 44 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">2C02</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C03</span>  <span class="rt-bytes">E9 1C   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$1C</span>
<span class="rt-addr">2C05</span>  <span class="rt-bytes">B0 04   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C0B</span>
<span class="rt-addr">2C07</span>  <span class="rt-bytes">49 FF   </span>  <span class="rt-op">EOR</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2C09</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2C0B</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C0C</span>  <span class="rt-bytes">69 37   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$37</span>
<span class="rt-addr">2C0E</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">2C10</span>  <span class="rt-bytes">D1 61   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C12</span>  <span class="rt-bytes">90 08   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2C1C</span>
<span class="rt-addr">2C14</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2C16</span>  <span class="rt-bytes">8D 81 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0381</span>   <span class="rt-cmt">; Dock refused</span>
<span class="rt-addr">2C19</span>  <span class="rt-bytes">4C BD 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2C1C</span>  <span class="rt-bytes">20 C6 2C</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$2CC6</span>
<span class="rt-addr">2C1F</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C20</span>  <span class="rt-bytes">ED 38 03</span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$0338</span>   <span class="rt-cmt">; Launch heading (low)</span>
<span class="rt-addr">2C23</span>  <span class="rt-bytes">08      </span>  <span class="rt-op">PHP</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C24</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C25</span>  <span class="rt-bytes">E9 20   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">2C27</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C28</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C29</span>  <span class="rt-bytes">E9 00   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2C2B</span>  <span class="rt-bytes">28      </span>  <span class="rt-op">PLP</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C2C</span>  <span class="rt-bytes">ED 39 03</span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$0339</span>   <span class="rt-cmt">; Launch heading (high)</span>
<span class="rt-addr">2C2F</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2C30</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C31</span>  <span class="rt-bytes">90 04   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2C37</span>
<span class="rt-addr">2C33</span>  <span class="rt-bytes">49 FF   </span>  <span class="rt-op">EOR</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2C35</span>  <span class="rt-bytes">69 00   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2C37</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C38</span>  <span class="rt-bytes">69 1C   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$1C</span>
<span class="rt-addr">2C3A</span>  <span class="rt-bytes">B0 D8   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C14</span>
<span class="rt-addr">2C3C</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2C3D</span>  <span class="rt-bytes">B0 D5   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C14</span>
<span class="rt-addr">2C3F</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">2C41</span>  <span class="rt-bytes">D1 61   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C43</span>  <span class="rt-bytes">B0 CF   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C14</span>
<span class="rt-addr">2C45</span>  <span class="rt-bytes">A9 80   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">2C47</span>  <span class="rt-bytes">8D 96 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0396</span>   <span class="rt-cmt">; Dock state</span>
<span class="rt-addr">2C4A</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2C4C</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C4E</span>  <span class="rt-bytes">8D A4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03A4</span>   <span class="rt-cmt">; Docked type</span>
<span class="rt-addr">2C51</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C52</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C54</span>  <span class="rt-bytes">8D 98 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0398</span>   <span class="rt-cmt">; Docked cell (low)</span>
<span class="rt-addr">2C57</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C58</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C5A</span>  <span class="rt-bytes">8D 99 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0399</span>   <span class="rt-cmt">; Docked cell (high)</span>
<span class="rt-addr">2C5D</span>  <span class="rt-bytes">4C BD 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2C60</span>  <span class="rt-bytes">29 0C   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0C</span>
<span class="rt-addr">2C62</span>  <span class="rt-bytes">D0 59   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2C64</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">2C66</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C68</span>  <span class="rt-bytes">CD 44 03</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">2C6B</span>  <span class="rt-bytes">90 3C   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2CA9</span>
<span class="rt-addr">2C6D</span>  <span class="rt-bytes">E9 80   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">2C6F</span>  <span class="rt-bytes">90 05   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2C76</span>
<span class="rt-addr">2C71</span>  <span class="rt-bytes">CD 44 03</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">2C74</span>  <span class="rt-bytes">B0 47   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2C76</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2C78</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C7A</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">2C7C</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C7E</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">2C80</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2C82</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C84</span>  <span class="rt-bytes">A0 07   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$07</span>
<span class="rt-addr">2C86</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2C88</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2C89</span>  <span class="rt-bytes">69 40   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">2C8B</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2C8F</span>
<span class="rt-addr">2C8D</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2C8F</span>  <span class="rt-bytes">20 65 3E</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3E65</span>
<span class="rt-addr">2C92</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2C94</span>  <span class="rt-bytes">8D 92 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0392</span>
<span class="rt-addr">2C97</span>  <span class="rt-bytes">A9 01   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2C99</span>  <span class="rt-bytes">8D 93 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0393</span>
<span class="rt-addr">2C9C</span>  <span class="rt-bytes">A9 04   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">2C9E</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">2CA1</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2CA3</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">2CA6</span>  <span class="rt-bytes">4C BD 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CBD</span>
<span class="rt-addr">2CA9</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CAA</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2CAC</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">2CAE</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">2CB0</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CB1</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CB2</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CB3</span>  <span class="rt-bytes">79 E4 C3</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$C3E4,Y</span>
<span class="rt-addr">2CB6</span>  <span class="rt-bytes">B0 BE   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C76</span>
<span class="rt-addr">2CB8</span>  <span class="rt-bytes">CD 44 03</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">2CBB</span>  <span class="rt-bytes">B0 B9   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2C76</span>
<span class="rt-addr">2CBD</span>  <span class="rt-bytes">4C 5B 2A</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2A5B</span>
</pre>

### Additional code at `$2CC0`

<pre class="rt-listing">
<span class="rt-addr">2CC0</span>  <span class="rt-bytes">20 C6 2C</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$2CC6</span>
<span class="rt-addr">2CC3</span>  <span class="rt-bytes">4C 5F 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D5F</span>
</pre>

### Additional code at `$2CC6`

<pre class="rt-listing">
<span class="rt-addr">2CC6</span>  <span class="rt-bytes">A5 5B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$5B</span>
<span class="rt-addr">2CC8</span>  <span class="rt-bytes">C9 40   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">2CCA</span>  <span class="rt-bytes">90 04   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$2CD0</span>
<span class="rt-addr">2CCC</span>  <span class="rt-bytes">A9 7F   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$7F</span>
<span class="rt-addr">2CCE</span>  <span class="rt-bytes">D0 21   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2CF1</span>
<span class="rt-addr">2CD0</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CD2</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CD3</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CD5</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CD6</span>  <span class="rt-bytes">C9 10   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">2CD8</span>  <span class="rt-bytes">B0 13   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$2CED</span>
<span class="rt-addr">2CDA</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CDC</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CDD</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CDF</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CE0</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CE2</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CE3</span>  <span class="rt-bytes">06 5A   </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">$5A</span>
<span class="rt-addr">2CE5</span>  <span class="rt-bytes">2A      </span>  <span class="rt-op">ROL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">2CE6</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CE7</span>  <span class="rt-bytes">B9 00 8B</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$8B00,Y</span>
<span class="rt-addr">2CEA</span>  <span class="rt-bytes">4C F1 2C</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2CF1</span>
<span class="rt-addr">2CED</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">2CEE</span>  <span class="rt-bytes">B9 00 8A</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$8A00,Y</span>
<span class="rt-addr">2CF1</span>  <span class="rt-bytes">85 26   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2CF3</span>  <span class="rt-bytes">A5 E7   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E7</span>
<span class="rt-addr">2CF5</span>  <span class="rt-bytes">D0 28   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D1F</span>
<span class="rt-addr">2CF7</span>  <span class="rt-bytes">A5 E8   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E8</span>
<span class="rt-addr">2CF9</span>  <span class="rt-bytes">D0 12   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D0D</span>
<span class="rt-addr">2CFB</span>  <span class="rt-bytes">A5 E9   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E9</span>
<span class="rt-addr">2CFD</span>  <span class="rt-bytes">D0 07   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D06</span>
<span class="rt-addr">2CFF</span>  <span class="rt-bytes">A2 00   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D01</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D03</span>  <span class="rt-bytes">4C 47 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D47</span>
<span class="rt-addr">2D06</span>  <span class="rt-bytes">A2 7F   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$7F</span>
<span class="rt-addr">2D08</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D0A</span>  <span class="rt-bytes">4C 52 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D52</span>
<span class="rt-addr">2D0D</span>  <span class="rt-bytes">A5 E9   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E9</span>
<span class="rt-addr">2D0F</span>  <span class="rt-bytes">D0 07   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D18</span>
<span class="rt-addr">2D11</span>  <span class="rt-bytes">A2 FF   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2D13</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D15</span>  <span class="rt-bytes">4C 52 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D52</span>
<span class="rt-addr">2D18</span>  <span class="rt-bytes">A2 80   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">2D1A</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D1C</span>  <span class="rt-bytes">4C 47 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D47</span>
<span class="rt-addr">2D1F</span>  <span class="rt-bytes">A5 E8   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E8</span>
<span class="rt-addr">2D21</span>  <span class="rt-bytes">D0 12   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D35</span>
<span class="rt-addr">2D23</span>  <span class="rt-bytes">A5 E9   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E9</span>
<span class="rt-addr">2D25</span>  <span class="rt-bytes">D0 07   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D2E</span>
<span class="rt-addr">2D27</span>  <span class="rt-bytes">A2 FF   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">2D29</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2D2B</span>  <span class="rt-bytes">4C 52 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D52</span>
<span class="rt-addr">2D2E</span>  <span class="rt-bytes">A2 80   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">2D30</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2D32</span>  <span class="rt-bytes">4C 47 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D47</span>
<span class="rt-addr">2D35</span>  <span class="rt-bytes">A5 E9   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$E9</span>
<span class="rt-addr">2D37</span>  <span class="rt-bytes">D0 07   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$2D40</span>
<span class="rt-addr">2D39</span>  <span class="rt-bytes">A2 00   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D3B</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2D3D</span>  <span class="rt-bytes">4C 47 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D47</span>
<span class="rt-addr">2D40</span>  <span class="rt-bytes">A2 7F   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$7F</span>
<span class="rt-addr">2D42</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2D44</span>  <span class="rt-bytes">4C 52 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D52</span>
<span class="rt-addr">2D47</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D48</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D49</span>  <span class="rt-bytes">65 26   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2D4B</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D4C</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D4D</span>  <span class="rt-bytes">69 00   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D4F</span>  <span class="rt-bytes">4C 5A 2D</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$2D5A</span>
<span class="rt-addr">2D52</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D53</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D54</span>  <span class="rt-bytes">E5 26   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$26</span>
<span class="rt-addr">2D56</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D57</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D58</span>  <span class="rt-bytes">E9 00   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">2D5A</span>  <span class="rt-bytes">29 01   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">2D5C</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D5D</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">2D5E</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`Flag-bit test`](bit-test.md) from `$2BEC`

## Called by

- `JMP` at `$2ADB`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
