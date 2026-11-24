# Mobile unit AI

**Address** `$80C3-$81F2` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Dispatched from <code class="addr">$4620</code> for records whose type flags carry bit 5. Types 36 and 21 bob between two altitudes first, flipping byte 3 bit 0; every mobile then runs the class-range test, closes on the ship and fires. Out of range it clears byte 8 and returns.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">80C3</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">80C5</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80C7</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">80C8</span>  <span class="rt-bytes">E0 24   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$24</span>
<span class="rt-addr">80CA</span>  <span class="rt-bytes">F0 04   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$80D0</span>
<span class="rt-addr">80CC</span>  <span class="rt-bytes">C9 15   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$15</span>
<span class="rt-addr">80CE</span>  <span class="rt-bytes">D0 34   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$8104</span>
<span class="rt-addr">80D0</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">80D2</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80D4</span>  <span class="rt-bytes">29 01   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">80D6</span>  <span class="rt-bytes">49 01   </span>  <span class="rt-op">EOR</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">80D8</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">80D9</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">80DA</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">80DB</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">80DC</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">80DD</span>  <span class="rt-bytes">E9 08   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">80DF</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">80E1</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">80E2</span>  <span class="rt-bytes">71 61   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80E4</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80E6</span>  <span class="rt-bytes">F0 0F   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$80F7</span>
<span class="rt-addr">80E8</span>  <span class="rt-bytes">B0 15   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$80FF</span>
<span class="rt-addr">80EA</span>  <span class="rt-bytes">10 13   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$80FF</span>
<span class="rt-addr">80EC</span>  <span class="rt-bytes">C9 F8   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$F8</span>
<span class="rt-addr">80EE</span>  <span class="rt-bytes">B0 07   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$80F7</span>
<span class="rt-addr">80F0</span>  <span class="rt-bytes">20 0E 33</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$330E</span>
<span class="rt-addr">80F3</span>  <span class="rt-bytes">C9 10   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">80F5</span>  <span class="rt-bytes">B0 08   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$80FF</span>
<span class="rt-addr">80F7</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">80F9</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80FB</span>  <span class="rt-bytes">49 01   </span>  <span class="rt-op">EOR</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">80FD</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">80FF</span>  <span class="rt-bytes">E0 15   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$15</span>
<span class="rt-addr">8101</span>  <span class="rt-bytes">F0 01   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$8104</span>
<span class="rt-addr">8103</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">8104</span>  <span class="rt-bytes">BD 09 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C409,X</span>
<span class="rt-addr">8107</span>  <span class="rt-bytes">29 0F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">8109</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">810A</span>  <span class="rt-bytes">A0 0D   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0D</span>
<span class="rt-addr">810C</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">810E</span>  <span class="rt-bytes">DD 2E C4</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$C42E,X</span>
<span class="rt-addr">8111</span>  <span class="rt-bytes">90 07   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$811A</span>
<span class="rt-addr">8113</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">8115</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8117</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8119</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">811A</span>  <span class="rt-bytes">AD B0 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">811D</span>  <span class="rt-bytes">09 20   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">811F</span>  <span class="rt-bytes">8D B0 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">8122</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">8124</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8126</span>  <span class="rt-bytes">C9 40   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">8128</span>  <span class="rt-bytes">F0 0A   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$8134</span>
<span class="rt-addr">812A</span>  <span class="rt-bytes">E0 00   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">812C</span>  <span class="rt-bytes">F0 06   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$8134</span>
<span class="rt-addr">812E</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">812F</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">8131</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8133</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">8134</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">8136</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8138</span>  <span class="rt-bytes">30 32   </span>  <span class="rt-op">BMI</span>  <span class="rt-arg">$816C</span>
<span class="rt-addr">813A</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">813B</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">813D</span>  <span class="rt-bytes">C9 10   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">813F</span>  <span class="rt-bytes">B0 03   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$8144</span>
<span class="rt-addr">8141</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8143</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">8144</span>  <span class="rt-bytes">20 0E 33</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$330E</span>
<span class="rt-addr">8147</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">8148</span>  <span class="rt-bytes">29 0F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">814A</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">814B</span>  <span class="rt-bytes">E9 08   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">814D</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">814E</span>  <span class="rt-bytes">6D 3C 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$033C</span>
<span class="rt-addr">8151</span>  <span class="rt-bytes">A0 0E   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">8153</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8155</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">8156</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">8157</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">8158</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">8159</span>  <span class="rt-bytes">4A      </span>  <span class="rt-op">LSR</span>  <span class="rt-arg">A</span>
<span class="rt-addr">815A</span>  <span class="rt-bytes">29 0F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">815C</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">815D</span>  <span class="rt-bytes">E9 08   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">815F</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">8160</span>  <span class="rt-bytes">6D 3F 03</span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$033F</span>
<span class="rt-addr">8163</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8164</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8166</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">8168</span>  <span class="rt-bytes">A9 80   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">816A</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">816C</span>  <span class="rt-bytes">BD 3E C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C43E,X</span>
<span class="rt-addr">816F</span>  <span class="rt-bytes">85 68   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">8171</span>  <span class="rt-bytes">E0 00   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8173</span>  <span class="rt-bytes">D0 0D   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$8182</span>
<span class="rt-addr">8175</span>  <span class="rt-bytes">A0 0E   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">8177</span>  <span class="rt-bytes">AD 3C 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033C</span>
<span class="rt-addr">817A</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">817C</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">817D</span>  <span class="rt-bytes">AD 3F 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$033F</span>
<span class="rt-addr">8180</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8182</span>  <span class="rt-bytes">A2 00   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8184</span>  <span class="rt-bytes">A0 0E   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0E</span>
<span class="rt-addr">8186</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8188</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">818A</span>  <span class="rt-bytes">D1 61   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">818C</span>  <span class="rt-bytes">F0 28   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$81B6</span>
<span class="rt-addr">818E</span>  <span class="rt-bytes">90 14   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$81A4</span>
<span class="rt-addr">8190</span>  <span class="rt-bytes">A0 04   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">8192</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8194</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">8195</span>  <span class="rt-bytes">65 68   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">8197</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8199</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">819B</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">819D</span>  <span class="rt-bytes">69 00   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">819F</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81A1</span>  <span class="rt-bytes">4C B5 81</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$81B5</span>
<span class="rt-addr">81A4</span>  <span class="rt-bytes">A0 04   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">81A6</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81A8</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">81A9</span>  <span class="rt-bytes">E5 68   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">81AB</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81AD</span>  <span class="rt-bytes">A0 01   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">81AF</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81B1</span>  <span class="rt-bytes">E9 00   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81B3</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81B5</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">81B6</span>  <span class="rt-bytes">A0 0F   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">81B8</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81BA</span>  <span class="rt-bytes">A0 02   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">81BC</span>  <span class="rt-bytes">D1 61   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81BE</span>  <span class="rt-bytes">F0 28   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$81E8</span>
<span class="rt-addr">81C0</span>  <span class="rt-bytes">90 14   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$81D6</span>
<span class="rt-addr">81C2</span>  <span class="rt-bytes">A0 05   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$05</span>
<span class="rt-addr">81C4</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81C6</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">81C7</span>  <span class="rt-bytes">65 68   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">81C9</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81CB</span>  <span class="rt-bytes">A0 02   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">81CD</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81CF</span>  <span class="rt-bytes">69 00   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81D1</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81D3</span>  <span class="rt-bytes">4C E7 81</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$81E7</span>
<span class="rt-addr">81D6</span>  <span class="rt-bytes">A0 05   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$05</span>
<span class="rt-addr">81D8</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81DA</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">81DB</span>  <span class="rt-bytes">E5 68   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">81DD</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81DF</span>  <span class="rt-bytes">A0 02   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$02</span>
<span class="rt-addr">81E1</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81E3</span>  <span class="rt-bytes">E9 00   </span>  <span class="rt-op">SBC</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81E5</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81E7</span>  <span class="rt-bytes">E8      </span>  <span class="rt-op">INX</span>  <span class="rt-arg"></span>
<span class="rt-addr">81E8</span>  <span class="rt-bytes">E0 00   </span>  <span class="rt-op">CPX</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81EA</span>  <span class="rt-bytes">D0 06   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$81F2</span>
<span class="rt-addr">81EC</span>  <span class="rt-bytes">A0 08   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">81EE</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81F0</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81F2</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

*None recorded in this body.*

## Called by

- `JSR` at `$4648` in [`Robot dispatch`](ai-dispatch.md)
- `JSR` at `$8377`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
