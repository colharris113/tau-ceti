# Static defence AI

**Address** `$81F3-$8359` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Static defence AI. Type flags bit 5 (mobile units) always run; everyone else runs only while the provocation latch <code class="addr">$03BF</code> is set. Out of class range it does nothing. In range it sets byte 3 bit 3, answers a player lock with an AMM after 24 frames (clearing its own lock first), and otherwise counts byte 9 against the fire interval at <code class="addr">$C45E</code>. A random roll masked by <code class="addr">$C44E</code> reloads the counter; behaviour bit 7 units also roll against <code class="addr">$C46E</code> and, on success, take a free record from <code class="addr">$1000</code> and spawn a missile into it. Type 26 has an early path of its own at <code class="addr">$8202</code>. Movement ends at <code class="addr">$8347</code>.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">81F3</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">81F5</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">81F7</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">81F9</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">81FA</span>  <span class="rt-bytes">B9 09 C4</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C409,Y</span>
<span class="rt-addr">81FD</span>  <span class="rt-bytes">85 67   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">81FF</span>  <span class="rt-bytes">29 0F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$0F</span>
<span class="rt-addr">8201</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">8202</span>  <span class="rt-bytes">C0 1A   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$1A</span>
<span class="rt-addr">8204</span>  <span class="rt-bytes">D0 39   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$823F</span>
<span class="rt-addr">8206</span>  <span class="rt-bytes">A0 0D   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0D</span>
<span class="rt-addr">8208</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">820A</span>  <span class="rt-bytes">C9 06   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">820C</span>  <span class="rt-bytes">B0 0C   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$821A</span>
<span class="rt-addr">820E</span>  <span class="rt-bytes">C9 04   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">8210</span>  <span class="rt-bytes">90 09   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$821B</span>
<span class="rt-addr">8212</span>  <span class="rt-bytes">AD B0 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">8215</span>  <span class="rt-bytes">09 10   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">8217</span>  <span class="rt-bytes">8D B0 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">821A</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">821B</span>  <span class="rt-bytes">A9 E8   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$E8</span>
<span class="rt-addr">821D</span>  <span class="rt-bytes">A2 65   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$65</span>
<span class="rt-addr">821F</span>  <span class="rt-bytes">20 27 41</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4127</span>   <span class="rt-cmt">; Message queue</span>
<span class="rt-addr">8222</span>  <span class="rt-bytes">A9 32   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$32</span>
<span class="rt-addr">8224</span>  <span class="rt-bytes">8D 79 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$0379</span>
<span class="rt-addr">8227</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8229</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">822B</span>  <span class="rt-bytes">09 40   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">822D</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">822F</span>  <span class="rt-bytes">A9 30   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$30</span>
<span class="rt-addr">8231</span>  <span class="rt-bytes">20 65 3E</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3E65</span>
<span class="rt-addr">8234</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8236</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">8239</span>  <span class="rt-bytes">A9 04   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">823B</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">823E</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">823F</span>  <span class="rt-bytes">B9 9A C3</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$C39A,Y</span>
<span class="rt-addr">8242</span>  <span class="rt-bytes">29 20   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">8244</span>  <span class="rt-bytes">0D BF 03</span>  <span class="rt-op">ORA</span>  <span class="rt-arg">$03BF</span>   <span class="rt-cmt">; Provocation latch</span>
<span class="rt-addr">8247</span>  <span class="rt-bytes">D0 01   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$824A</span>
<span class="rt-addr">8249</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">824A</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">824C</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">824E</span>  <span class="rt-bytes">29 F3   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$F3</span>
<span class="rt-addr">8250</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8252</span>  <span class="rt-bytes">A0 0D   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$0D</span>
<span class="rt-addr">8254</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8256</span>  <span class="rt-bytes">DD 2E C4</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$C42E,X</span>
<span class="rt-addr">8259</span>  <span class="rt-bytes">90 01   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$825C</span>
<span class="rt-addr">825B</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">825C</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">825E</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8260</span>  <span class="rt-bytes">09 08   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">8262</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8264</span>  <span class="rt-bytes">AD B0 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">8267</span>  <span class="rt-bytes">09 08   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$08</span>
<span class="rt-addr">8269</span>  <span class="rt-bytes">8D B0 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03B0</span>
<span class="rt-addr">826C</span>  <span class="rt-bytes">A5 67   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">826E</span>  <span class="rt-bytes">29 40   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">8270</span>  <span class="rt-bytes">F0 2C   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$829E</span>
<span class="rt-addr">8272</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">8274</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8276</span>  <span class="rt-bytes">29 10   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">8278</span>  <span class="rt-bytes">F0 24   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$829E</span>
<span class="rt-addr">827A</span>  <span class="rt-bytes">A0 09   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$09</span>
<span class="rt-addr">827C</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">827E</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">827F</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">8281</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8283</span>  <span class="rt-bytes">C9 18   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$18</span>
<span class="rt-addr">8285</span>  <span class="rt-bytes">90 16   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$829D</span>
<span class="rt-addr">8287</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8289</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">828B</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">828D</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">828F</span>  <span class="rt-bytes">29 EF   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$EF</span>
<span class="rt-addr">8291</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8293</span>  <span class="rt-bytes">A9 D3   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$D3</span>
<span class="rt-addr">8295</span>  <span class="rt-bytes">A2 65   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$65</span>
<span class="rt-addr">8297</span>  <span class="rt-bytes">20 27 41</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4127</span>   <span class="rt-cmt">; Message queue</span>
<span class="rt-addr">829A</span>  <span class="rt-bytes">20 38 48</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4838</span>   <span class="rt-cmt">; Clear all missiles (AMM)</span>
<span class="rt-addr">829D</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">829E</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">82A0</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82A2</span>  <span class="rt-bytes">C9 15   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$15</span>
<span class="rt-addr">82A4</span>  <span class="rt-bytes">F0 0B   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$82B1</span>
<span class="rt-addr">82A6</span>  <span class="rt-bytes">A0 06   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">82A8</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82AA</span>  <span class="rt-bytes">F0 05   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$82B1</span>
<span class="rt-addr">82AC</span>  <span class="rt-bytes">C9 40   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$40</span>
<span class="rt-addr">82AE</span>  <span class="rt-bytes">F0 01   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$82B1</span>
<span class="rt-addr">82B0</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">82B1</span>  <span class="rt-bytes">A5 67   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">82B3</span>  <span class="rt-bytes">29 20   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">82B5</span>  <span class="rt-bytes">F0 09   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$82C0</span>
<span class="rt-addr">82B7</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">82B9</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82BB</span>  <span class="rt-bytes">29 30   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$30</span>
<span class="rt-addr">82BD</span>  <span class="rt-bytes">D0 01   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$82C0</span>
<span class="rt-addr">82BF</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">82C0</span>  <span class="rt-bytes">A0 09   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$09</span>
<span class="rt-addr">82C2</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82C4</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">82C5</span>  <span class="rt-bytes">69 01   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">82C7</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82C9</span>  <span class="rt-bytes">29 3F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$3F</span>
<span class="rt-addr">82CB</span>  <span class="rt-bytes">AC 74 03</span>  <span class="rt-op">LDY</span>  <span class="rt-arg">$0374</span>
<span class="rt-addr">82CE</span>  <span class="rt-bytes">F0 01   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$82D1</span>
<span class="rt-addr">82D0</span>  <span class="rt-bytes">0A      </span>  <span class="rt-op">ASL</span>  <span class="rt-arg">A</span>
<span class="rt-addr">82D1</span>  <span class="rt-bytes">DD 5E C4</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$C45E,X</span>
<span class="rt-addr">82D4</span>  <span class="rt-bytes">B0 01   </span>  <span class="rt-op">BCS</span>  <span class="rt-arg">$82D7</span>
<span class="rt-addr">82D6</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">82D7</span>  <span class="rt-bytes">20 0E 33</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$330E</span>
<span class="rt-addr">82DA</span>  <span class="rt-bytes">A0 09   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$09</span>
<span class="rt-addr">82DC</span>  <span class="rt-bytes">3D 4E C4</span>  <span class="rt-op">AND</span>  <span class="rt-arg">$C44E,X</span>
<span class="rt-addr">82DF</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">82E1</span>  <span class="rt-bytes">A5 67   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$67</span>
<span class="rt-addr">82E3</span>  <span class="rt-bytes">10 62   </span>  <span class="rt-op">BPL</span>  <span class="rt-arg">$8347</span>
<span class="rt-addr">82E5</span>  <span class="rt-bytes">20 0E 33</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$330E</span>
<span class="rt-addr">82E8</span>  <span class="rt-bytes">DD 6E C4</span>  <span class="rt-op">CMP</span>  <span class="rt-arg">$C46E,X</span>
<span class="rt-addr">82EB</span>  <span class="rt-bytes">90 5A   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$8347</span>
<span class="rt-addr">82ED</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">82EF</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">82F1</span>  <span class="rt-bytes">A9 10   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">82F3</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">82F5</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">82F7</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">82F9</span>  <span class="rt-bytes">30 0A   </span>  <span class="rt-op">BMI</span>  <span class="rt-arg">$8305</span>
<span class="rt-addr">82FB</span>  <span class="rt-bytes">98      </span>  <span class="rt-op">TYA</span>  <span class="rt-arg"></span>
<span class="rt-addr">82FC</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">82FD</span>  <span class="rt-bytes">69 10   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">82FF</span>  <span class="rt-bytes">A8      </span>  <span class="rt-op">TAY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8300</span>  <span class="rt-bytes">D0 F5   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$82F7</span>
<span class="rt-addr">8302</span>  <span class="rt-bytes">4C 47 83</span>  <span class="rt-op">JMP</span>  <span class="rt-arg">$8347</span>
<span class="rt-addr">8305</span>  <span class="rt-bytes">84 63   </span>  <span class="rt-op">STY</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">8307</span>  <span class="rt-bytes">A9 BE   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$BE</span>
<span class="rt-addr">8309</span>  <span class="rt-bytes">A2 65   </span>  <span class="rt-op">LDX</span>  <span class="rt-arg">#$65</span>
<span class="rt-addr">830B</span>  <span class="rt-bytes">20 27 41</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4127</span>   <span class="rt-cmt">; Message queue</span>
<span class="rt-addr">830E</span>  <span class="rt-bytes">A9 06   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$06</span>
<span class="rt-addr">8310</span>  <span class="rt-bytes">8D C5 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C5</span>
<span class="rt-addr">8313</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8315</span>  <span class="rt-bytes">A9 0B   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$0B</span>
<span class="rt-addr">8317</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">8319</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">831A</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">831C</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">831E</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">831F</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8321</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">8323</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8324</span>  <span class="rt-bytes">A9 48   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$48</span>
<span class="rt-addr">8326</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">8328</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8329</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">832B</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">832D</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">832E</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">8330</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8331</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8333</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">8334</span>  <span class="rt-bytes">69 80   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$80</span>
<span class="rt-addr">8336</span>  <span class="rt-bytes">90 02   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$833A</span>
<span class="rt-addr">8338</span>  <span class="rt-bytes">A9 FF   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$FF</span>
<span class="rt-addr">833A</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">833C</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">833D</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">833F</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">8341</span>  <span class="rt-bytes">C8      </span>  <span class="rt-op">INY</span>  <span class="rt-arg"></span>
<span class="rt-addr">8342</span>  <span class="rt-bytes">C0 10   </span>  <span class="rt-op">CPY</span>  <span class="rt-arg">#$10</span>
<span class="rt-addr">8344</span>  <span class="rt-bytes">D0 F4   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$833A</span>
<span class="rt-addr">8346</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">8347</span>  <span class="rt-bytes">A9 03   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">8349</span>  <span class="rt-bytes">20 65 3E</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$3E65</span>
<span class="rt-addr">834C</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">834E</span>  <span class="rt-bytes">B1 61   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8350</span>  <span class="rt-bytes">09 04   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">8352</span>  <span class="rt-bytes">91 61   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($61),Y</span>
<span class="rt-addr">8354</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">8356</span>  <span class="rt-bytes">8D C4 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$03C4</span>
<span class="rt-addr">8359</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`Message queue`](message-queue.md) from `$821F`
- [`Clear all missiles (AMM)`](clear-missiles.md) from `$829A`

## Called by

- `JSR` at `$4640` in [`Robot dispatch`](ai-dispatch.md)

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
