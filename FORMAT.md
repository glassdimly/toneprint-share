# The .tpr format (TonePrint Editor 4.7.0.6, Brainwaves Pitch Shifter)

These notes come from studying TonePrints that I made and exported myself, plus the editor's
behaviour on import. Each entry says how sure it is:
**confirmed** means a value was changed and the editor showed the expected result;
**inferred** means it follows from the order or the ranges and has not been tested one at a time.

## File layout

| Bytes | Content |
| --- | --- |
| 0-1 | CRC-16/MODBUS of bytes 2..end, big-endian (reflected poly 0xA001, init 0xFFFF, no final xor). **Confirmed**: the editor rejects a file whose checksum does not match. |
| 2..end | JSON text, XORed with a repeating keystream |

The keystream is built from a string stored in the editor: `ks[j] = S[j] XOR S[len-1-j]`, and
byte `i` of the body is XORed with `ks[i mod len]`. This repo does not include `S`.
`tpr.py findkey` finds it in your installed editor and checks it against a `.tpr` you
exported yourself.

The decrypted JSON contains `toneprintId`, `effectId`, `artistId`, `midiId`, `toneprintEffectTemplate`,
`toneprintName`, `description` and `toneprintData`. Exports are deterministic: exporting the
same TonePrint twice gives identical files. Importing a file with an existing
`toneprintId` replaces that TonePrint in the editor, so give every edited file a new ID
(`tpr.py set` does this).

## toneprintData

A hex string. Bytes 0-3 are `01 05 00 06`. Bytes 4-19 are the name, NUL-terminated (15 characters
at most). From byte 20 onwards come big-endian signed 32-bit words, numbered from 0.

Mapping slots refer to parameters by **index**, where **word = index + 8**.

| Word | Index | Parameter | Units / values | Status |
| --- | --- | --- | --- | --- |
| 0 | | changes whenever the content changes, so possibly a checksum | the editor does not check it on import | confirmed not checked |
| 1-8 | | unknown | | |
| 9 | 1 | Subtype | 0 Pitch, 1 V1V2, 2 Wham (3 Detune, inferred) | confirmed |
| 10 | 2 | Dry Level | 0.1 dB (-1000 = -100.0 dB) | confirmed |
| 11 | 3 | In Level | 0.1 dB | inferred |
| 13 | 5 | Link Delay | 0/1 | inferred |
| 14 | 6 | Common Delay | ms | inferred |
| 15 | 7 | Link Delay Feedback | 0/1 | inferred |
| 16 | 8 | Common Delay Feedback | % | inferred (a factory TonePrint maps MASH to it, 0-100) |
| 17 | 9 | Link Wet Feedback | 0/1 | inferred |
| 18 | 10 | Common Wet Feedback | % | inferred |
| 19 | 11 | Link Mix | 0/1 | inferred |
| 20 | 12 | Common Mix | 0.1 % (1000 = 100 %) | confirmed in use (the MIX knob mapping) |
| 21-31 | 13-23 | Voice 1 block | see below | |
| 32-42 | 24-34 | Voice 2 block | see below | |
| 47-53 | | SoftClipper: LoCut freq (raw), LoCut Q x100, HiCut distance (raw), HiCut Q x100, Clip Type, Drive dB, Symmetry | Clip Type 0 = None, 10 = Dirty Square Root | Q, type and drive confirmed |
| 54-74 | | MIX knob mapping, 3 slots | | confirmed |
| 75-95 | | VOICE 1 knob mapping, 3 slots | | confirmed |
| 96-116 | | VOICE 2 knob mapping, 3 slots | | confirmed |
| 117-137 | | Expression pedal mapping, 3 slots | | inferred |
| 138-158 | | MASH mapping, 3 slots | | confirmed |

### Voice block (11 words; Voice 1 starts at word 21, Voice 2 at word 32)

| Offset | Parameter | Units | Status |
| --- | --- | --- | --- |
| +0 | Harmony (interval; the VOICE knobs map to it with values 0-51) | 25 = knob centre | confirmed changes the interval |
| +1 | Custom Voice | 0-2400 | confirmed position; unused in Wham |
| +2 | Wet Level | 0.1 dB | confirmed (-1000 = -100.0 dB) |
| +3 | Delay | ms (0-260) | confirmed via a factory TonePrint's MASH mapping |
| +4 | Dry Feedback | % | inferred |
| +5 | DryIn FB Mix | % | inferred |
| +6 | Wet Feedback | % | inferred |
| +7 | ToneBend Tone | cents (1200 = one octave) | confirmed |
| +8 | ToneBend % | % | confirmed |
| +9 | Bend time | ms | confirmed |
| +10 | Fit to nearest semitone | 0/1 | inferred |

### Mapping slot (7 words)

`[enabled, parameter index, y at 0 %, 25 %, 50 %, 75 %, 100 %]`, where the y values are in the
parameter's own units. An empty slot is `-1, -1` followed by five filler words (seen as `0` or `-1`).
For MASH, x is footswitch pressure. For knobs, x is knob position, and the physical knob's
position overrides the stored parameter value.

### Behaviour notes

- **Pitch**: the voices sit at fixed intervals (a harmonizer). The ToneBend settings do not move the pitch.
- **Wham**: MASH drives ToneBend % toward ToneBend Tone. The editor greys ToneBend Tone out but
  still uses it, so the only way to change it is by editing the file.
- **V1V2**: ToneBend morphs from Voice 1's interval to Voice 2's. Common Mix below 100 % leaves
  part of the signal unshifted.
