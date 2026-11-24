# Guided-object handling

**Address** `$44C4-$461F` &nbsp;·&nbsp; **Group** Records

<p class="lede">Reached from the dispatcher when a live record is neither dockable nor a sensor. Missiles and other guided objects take their target from bytes 14/15, publish their state to the eight-byte block at <code class="addr">$FFC0</code>, and run the homing and detonation logic that follows.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">44C4</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">44C5</span>  <span class="rt-bytes">29 0C   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0C</span>
<span class="rt-addr">44C7</span>  <span class="rt-bytes">D0 03   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$44CC</span>
<span class="rt-addr">44C9</span>  <span class="rt-bytes">4C 20 46</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$4620</span>   <span class="rt-cmt">; Robot dispatch</span>
<span class="rt-addr">44CC</span>  <span class="rt-bytes">29 08   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">44CE</span>  <span class="rt-bytes">85 67   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">44D0</span>  <span class="rt-bytes">F0 0E   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$44E0</span>
<span class="rt-addr">44D2</span>  <span class="rt-bytes">A0 0E   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">44D4</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">44D6</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">44D8</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">44D9</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">44DB</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">44DD</span>  <span class="rt-bytes">4C 1F 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$451F</span>
<span class="rt-addr">44E0</span>  <span class="rt-bytes">AD B0 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">44E3</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">44E5</span>  <span class="rt-bytes">8D B0 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">44E8</span>  <span class="rt-bytes">A9 C0   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">44EA</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">44EC</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">44EE</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">44F0</span>  <span class="rt-bytes">A9 0A   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0A</span>
<span class="rt-addr">44F2</span>  <span class="rt-bytes">8D C0 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC0</span>
<span class="rt-addr">44F5</span>  <span class="rt-bytes">AD 3C 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033C</span>
<span class="rt-addr">44F8</span>  <span class="rt-bytes">8D C1 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC1</span>
<span class="rt-addr">44FB</span>  <span class="rt-bytes">AD 3F 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033F</span>
<span class="rt-addr">44FE</span>  <span class="rt-bytes">8D C2 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC2</span>
<span class="rt-addr">4501</span>  <span class="rt-bytes">A9 40   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">4503</span>  <span class="rt-bytes">8D C3 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC3</span>
<span class="rt-addr">4506</span>  <span class="rt-bytes">AD 3B 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033B</span>
<span class="rt-addr">4509</span>  <span class="rt-bytes">8D C4 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC4</span>
<span class="rt-addr">450C</span>  <span class="rt-bytes">AD 3E 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033E</span>
<span class="rt-addr">450F</span>  <span class="rt-bytes">8D C5 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC5</span>
<span class="rt-addr">4512</span>  <span class="rt-bytes">AD 44 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0344</span>   <span class="rt-cmt">; Altitude</span>
<span class="rt-addr">4515</span>  <span class="rt-bytes">8D C6 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC6</span>
<span class="rt-addr">4518</span>  <span class="rt-bytes">AD 77 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0377</span>   <span class="rt-cmt">; Shield</span>
<span class="rt-addr">451B</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">451C</span>  <span class="rt-bytes">8D C7 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FFC7</span>
<span class="rt-addr">451F</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">4521</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4523</span>  <span class="rt-bytes">29 40   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">4525</span>  <span class="rt-bytes">D0 09   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4530</span>
<span class="rt-addr">4527</span>  <span class="rt-bytes">A9 C0   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">4529</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">452B</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">452D</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4530</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4532</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4534</span>  <span class="rt-bytes">10 0F   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$4545</span>
<span class="rt-addr">4536</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4538</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">453A</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">453C</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">453E</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4540</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4542</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4545</span>  <span class="rt-bytes">A0 04   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">4547</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4549</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">454A</span>  <span class="rt-bytes">F1 61   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">454C</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">454D</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">454E</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">454F</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4550</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4552</span>  <span class="rt-bytes">F1 61   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4554</span>  <span class="rt-bytes">90 1F   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$4575</span>
<span class="rt-addr">4556</span>  <span class="rt-bytes">D0 04   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$455C</span>
<span class="rt-addr">4558</span>  <span class="rt-bytes">E0 40   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">455A</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$455E</span>
<span class="rt-addr">455C</span>  <span class="rt-bytes">A2 40   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">455E</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">4560</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4561</span>  <span class="rt-bytes">8A      </span>  <span class="rt-op">TXA</span>  <span class="rt-arg"></span>
<span class="rt-addr">4562</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4563</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4564</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4565</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">4566</span>  <span class="rt-bytes">71 61   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4568</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">456A</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">456B</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">456C</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">456D</span>  <span class="rt-bytes">88      </span>  <span class="rt-op">DEY</span>  <span class="rt-arg"></span>
<span class="rt-addr">456E</span>  <span class="rt-bytes">71 61   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4570</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">4572</span>  <span class="rt-bytes">4C 84 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$4584</span>
<span class="rt-addr">4575</span>  <span class="rt-bytes">C9 FF   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">4577</span>  <span class="rt-bytes">D0 04   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$457D</span>
<span class="rt-addr">4579</span>  <span class="rt-bytes">E0 BF   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$BF</span>
<span class="rt-addr">457B</span>  <span class="rt-bytes">B0 02   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$457F</span>
<span class="rt-addr">457D</span>  <span class="rt-bytes">A2 BF   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$BF</span>
<span class="rt-addr">457F</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">4581</span>  <span class="rt-bytes">4C 60 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$4560</span>
<span class="rt-addr">4584</span>  <span class="rt-bytes">C0 01   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">4586</span>  <span class="rt-bytes">D0 05   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$458D</span>
<span class="rt-addr">4588</span>  <span class="rt-bytes">A0 05   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$05</span>
<span class="rt-addr">458A</span>  <span class="rt-bytes">4C 47 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$4547</span>
<span class="rt-addr">458D</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">458F</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">4591</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">4592</span>  <span class="rt-bytes">BD E4 C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C3E4,X</span>
<span class="rt-addr">4595</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">4596</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">4597</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">4599</span>  <span class="rt-bytes">71 63   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">459B</span>  <span class="rt-bytes">90 09   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$45A6</span>
<span class="rt-addr">459D</span>  <span class="rt-bytes">E9 24   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$24</span>
<span class="rt-addr">459F</span>  <span class="rt-bytes">90 0C   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$45AD</span>
<span class="rt-addr">45A1</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">45A3</span>  <span class="rt-bytes">4C AD 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$45AD</span>
<span class="rt-addr">45A6</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">45A7</span>  <span class="rt-bytes">E9 24   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$24</span>
<span class="rt-addr">45A9</span>  <span class="rt-bytes">B0 02   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$45AD</span>
<span class="rt-addr">45AB</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">45AD</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">45AE</span>  <span class="rt-bytes">F1 61   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45B0</span>  <span class="rt-bytes">F0 16   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$45C8</span>
<span class="rt-addr">45B2</span>  <span class="rt-bytes">90 09   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$45BD</span>
<span class="rt-addr">45B4</span>  <span class="rt-bytes">C9 04   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">45B6</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$45BA</span>
<span class="rt-addr">45B8</span>  <span class="rt-bytes">A9 04   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">45BA</span>  <span class="rt-bytes">4C C3 45</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$45C3</span>
<span class="rt-addr">45BD</span>  <span class="rt-bytes">C9 FC   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$FC</span>
<span class="rt-addr">45BF</span>  <span class="rt-bytes">B0 02   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$45C3</span>
<span class="rt-addr">45C1</span>  <span class="rt-bytes">A9 FC   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FC</span>
<span class="rt-addr">45C3</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">45C4</span>  <span class="rt-bytes">71 61   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45C6</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45C8</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">45CA</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45CC</span>  <span class="rt-bytes">D1 63   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">45CE</span>  <span class="rt-bytes">D0 16   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$45E6</span>
<span class="rt-addr">45D0</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">45D1</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45D3</span>  <span class="rt-bytes">D1 63   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">45D5</span>  <span class="rt-bytes">D0 0F   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$45E6</span>
<span class="rt-addr">45D7</span>  <span class="rt-bytes">A0 04   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">45D9</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45DB</span>  <span class="rt-bytes">D1 63   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">45DD</span>  <span class="rt-bytes">D0 07   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$45E6</span>
<span class="rt-addr">45DF</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">45E0</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45E2</span>  <span class="rt-bytes">D1 63   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">45E4</span>  <span class="rt-bytes">F0 03   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$45E9</span>
<span class="rt-addr">45E6</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">45E9</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">45EB</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">45ED</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45EF</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">45F1</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45F3</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">45F5</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">45F7</span>  <span class="rt-bytes">A9 30   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$30</span>
<span class="rt-addr">45F9</span>  <span class="rt-bytes">A6 67   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">45FB</span>  <span class="rt-bytes">D0 18   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$4615</span>
<span class="rt-addr">45FD</span>  <span class="rt-bytes">20 65 3E</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3E65</span>
<span class="rt-addr">4600</span>  <span class="rt-bytes">A9 28   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$28</span>
<span class="rt-addr">4602</span>  <span class="rt-bytes">8D 79 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0379</span>
<span class="rt-addr">4605</span>  <span class="rt-bytes">8D 92 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0392</span>
<span class="rt-addr">4608</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">460A</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">460D</span>  <span class="rt-bytes">A9 0B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0B</span>
<span class="rt-addr">460F</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">4612</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
<span class="rt-addr">4615</span>  <span class="rt-bytes">20 51 49</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4951</span>   <span class="rt-cmt">; Damage</span>
<span class="rt-addr">4618</span>  <span class="rt-bytes">A9 0B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0B</span>
<span class="rt-addr">461A</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">461D</span>  <span class="rt-bytes">4C EB 43</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$43EB</span>
</pre>

## Calls

- [`Damage`](damage.md) from `$4615`

**Tail jumps**

- [`Robot dispatch`](ai-dispatch.md) at `$44C9`

## Called by

- `JSR` at `$3C58`
- `JSR` at `$3C6A`
- `JSR` at `$529B`
- `JMP` at `$5B97`
- `JSR` at `$5E72`
- `JSR` at `$5EB6`
- `JSR` at `$60EB`
- `JSR` at `$6109`
- `JSR` at `$6202`
- `JSR` at `$62BA`
- `JSR` at `$6308`
- `JMP` at `$6ED5`
- `JMP` at `$6EEB`
- `JMP` at `$6EFA`
- `JSR` at `$79F7`
- `JSR` at `$7B24`
- `JSR` at `$7D1D`
- `JSR` at `$C0A2`
- `JSR` at `$C0C6`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
