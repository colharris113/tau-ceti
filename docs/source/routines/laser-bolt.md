# Laser bolt: timer and hit

**Address** `$3D41-$3DD4` &nbsp;·&nbsp; **Group** Combat

<p class="lede">Counts the bolt's flight in the low seven bits of <code class="addr">$036E</code>. At 22 frames it clears the bolt colour, resets <code class="addr">$036E</code> and resolves the shot against <code class="addr">$038C</code>/<code class="addr">$038D</code>: exactly one target, only if still alive, takes 4 points through the damage routine at <code class="addr">$4951</code> and gets byte 3 bit 5 set.</p>

## Listing

*Re-disassembled from the byte map: every instruction shown is one the game really executes from this entry, and gaps are branch targets that follow an early return.*

<pre class="rt-listing">
<span class="rt-addr">3D41</span>  <span class="rt-bytes">AD 6E 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$036E</span>   <span class="rt-cmt">; Bolt timer</span>
<span class="rt-addr">3D44</span>  <span class="rt-bytes">D0 01   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$3D47</span>
<span class="rt-addr">3D46</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D47</span>  <span class="rt-bytes">EE 6E 03</span>  <span class="rt-op">INC</span>  <span class="rt-arg">$036E</span>   <span class="rt-cmt">; Bolt timer</span>
<span class="rt-addr">3D4A</span>  <span class="rt-bytes">29 7F   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$7F</span>
<span class="rt-addr">3D4C</span>  <span class="rt-bytes">C9 16   </span>  <span class="rt-op">CMP</span>  <span class="rt-arg">#$16</span>
<span class="rt-addr">3D4E</span>  <span class="rt-bytes">90 46   </span>  <span class="rt-op">BCC</span>  <span class="rt-arg">$3D96</span>
<span class="rt-addr">3D50</span>  <span class="rt-bytes">AD 51 FF</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$FF51</span>
<span class="rt-addr">3D53</span>  <span class="rt-bytes">29 FC   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$FC</span>
<span class="rt-addr">3D55</span>  <span class="rt-bytes">8D 51 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF51</span>
<span class="rt-addr">3D58</span>  <span class="rt-bytes">A9 00   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">3D5A</span>  <span class="rt-bytes">8D 6E 03</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$036E</span>   <span class="rt-cmt">; Bolt timer</span>
<span class="rt-addr">3D5D</span>  <span class="rt-bytes">AD 80 03</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$0380</span>
<span class="rt-addr">3D60</span>  <span class="rt-bytes">D0 33   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$3D95</span>
<span class="rt-addr">3D62</span>  <span class="rt-bytes">AE 8C 03</span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$038C</span>   <span class="rt-cmt">; Laser target</span>
<span class="rt-addr">3D65</span>  <span class="rt-bytes">AC 8D 03</span>  <span class="rt-op">LDY</span>  <span class="rt-arg">$038D</span>
<span class="rt-addr">3D68</span>  <span class="rt-bytes">F0 2B   </span>  <span class="rt-op">BEQ</span>  <span class="rt-arg">$3D95</span>
<span class="rt-addr">3D6A</span>  <span class="rt-bytes">A5 68   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">3D6C</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D6D</span>  <span class="rt-bytes">A5 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">3D6F</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D70</span>  <span class="rt-bytes">A5 64   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">3D72</span>  <span class="rt-bytes">48      </span>  <span class="rt-op">PHA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D73</span>  <span class="rt-bytes">86 63   </span>  <span class="rt-op">STX</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">3D75</span>  <span class="rt-bytes">84 64   </span>  <span class="rt-op">STY</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">3D77</span>  <span class="rt-bytes">A0 00   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$00</span>
<span class="rt-addr">3D79</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">3D7B</span>  <span class="rt-bytes">29 C0   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$C0</span>
<span class="rt-addr">3D7D</span>  <span class="rt-bytes">D0 0D   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$3D8C</span>
<span class="rt-addr">3D7F</span>  <span class="rt-bytes">A0 03   </span>  <span class="rt-op">LDY</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">3D81</span>  <span class="rt-bytes">B1 63   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">3D83</span>  <span class="rt-bytes">09 20   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$20</span>
<span class="rt-addr">3D85</span>  <span class="rt-bytes">91 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">($63),Y</span>
<span class="rt-addr">3D87</span>  <span class="rt-bytes">A9 04   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$04</span>
<span class="rt-addr">3D89</span>  <span class="rt-bytes">20 51 49</span>  <span class="rt-op">JSR</span>  <span class="rt-arg">$4951</span>   <span class="rt-cmt">; Damage</span>
<span class="rt-addr">3D8C</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D8D</span>  <span class="rt-bytes">85 64   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$64</span>
<span class="rt-addr">3D8F</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D90</span>  <span class="rt-bytes">85 63   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$63</span>
<span class="rt-addr">3D92</span>  <span class="rt-bytes">68      </span>  <span class="rt-op">PLA</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D93</span>  <span class="rt-bytes">85 68   </span>  <span class="rt-op">STA</span>  <span class="rt-arg">$68</span>
<span class="rt-addr">3D95</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D96</span>  <span class="rt-bytes">AA      </span>  <span class="rt-op">TAX</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D97</span>  <span class="rt-bytes">BD D5 3D</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$3DD5,X</span>
<span class="rt-addr">3D9A</span>  <span class="rt-bytes">18      </span>  <span class="rt-op">CLC</span>  <span class="rt-arg"></span>
<span class="rt-addr">3D9B</span>  <span class="rt-bytes">69 3E   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$3E</span>
<span class="rt-addr">3D9D</span>  <span class="rt-bytes">8D 5E FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF5E</span>
<span class="rt-addr">3DA0</span>  <span class="rt-bytes">69 09   </span>  <span class="rt-op">ADC</span>  <span class="rt-arg">#$09</span>
<span class="rt-addr">3DA2</span>  <span class="rt-bytes">8D 5F FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF5F</span>
<span class="rt-addr">3DA5</span>  <span class="rt-bytes">BD 01 3E</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$3E01,X</span>
<span class="rt-addr">3DA8</span>  <span class="rt-bytes">8D 41 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF41</span>
<span class="rt-addr">3DAB</span>  <span class="rt-bytes">8D 43 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF43</span>
<span class="rt-addr">3DAE</span>  <span class="rt-bytes">BD EB 3D</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$3DEB,X</span>
<span class="rt-addr">3DB1</span>  <span class="rt-bytes">8D 40 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF40</span>
<span class="rt-addr">3DB4</span>  <span class="rt-bytes">A9 A8   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$A8</span>
<span class="rt-addr">3DB6</span>  <span class="rt-bytes">38      </span>  <span class="rt-op">SEC</span>  <span class="rt-arg"></span>
<span class="rt-addr">3DB7</span>  <span class="rt-bytes">FD EB 3D</span>  <span class="rt-op">SBC</span>  <span class="rt-arg">$3DEB,X</span>
<span class="rt-addr">3DBA</span>  <span class="rt-bytes">8D 42 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF42</span>
<span class="rt-addr">3DBD</span>  <span class="rt-bytes">A9 01   </span>  <span class="rt-op">LDA</span>  <span class="rt-arg">#$01</span>
<span class="rt-addr">3DBF</span>  <span class="rt-bytes">8D 56 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF56</span>
<span class="rt-addr">3DC2</span>  <span class="rt-bytes">8D 57 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF57</span>
<span class="rt-addr">3DC5</span>  <span class="rt-bytes">AD 51 FF</span>  <span class="rt-op">LDA</span>  <span class="rt-arg">$FF51</span>
<span class="rt-addr">3DC8</span>  <span class="rt-bytes">29 FC   </span>  <span class="rt-op">AND</span>  <span class="rt-arg">#$FC</span>
<span class="rt-addr">3DCA</span>  <span class="rt-bytes">AE 80 03</span>  <span class="rt-op">LDX</span>  <span class="rt-arg">$0380</span>
<span class="rt-addr">3DCD</span>  <span class="rt-bytes">D0 02   </span>  <span class="rt-op">BNE</span>  <span class="rt-arg">$3DD1</span>
<span class="rt-addr">3DCF</span>  <span class="rt-bytes">09 03   </span>  <span class="rt-op">ORA</span>  <span class="rt-arg">#$03</span>
<span class="rt-addr">3DD1</span>  <span class="rt-bytes">8D 51 FF</span>  <span class="rt-op">STA</span>  <span class="rt-arg">$FF51</span>
<span class="rt-addr">3DD4</span>  <span class="rt-bytes">60      </span>  <span class="rt-op">RTS</span>  <span class="rt-arg"></span>
</pre>

## Calls

- [`Damage`](damage.md) from `$3D89`

## Called by

- `JSR` at `$49F6`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
