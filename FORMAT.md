# The .tpr format (TonePrint Editor 4.7.0.6)

These notes come from studying TonePrints that I made and exported myself, plus the editor's
behaviour on import. Each entry says how sure it is:
**confirmed** means a value was changed and the editor showed the expected result;
**matched** means the value in an export equals the value the editor displayed, and that value
appears only once in the export. Settings whose position is not known are left out.

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
| 0 | | changes whenever the content changes; meaning unknown | the editor does not check it on import | confirmed not checked |
| 9 | 1 | Subtype | 0 Pitch, 1 V1V2, 2 Wham | confirmed |
| 10 | 2 | Dry Level | 0.1 dB (-1000 = -100.0 dB) | confirmed |
| 20 | 12 | Common Mix | 0.1 % (1000 = 100 %) | confirmed |
| 21-31 | 13-23 | Voice 1 block | see below | |
| 32-42 | 24-34 | Voice 2 block | see below | |
| 47-52 | | SoftClipper: LoCut Freq, LoCut Q ×100, HiCut Freq Distance, HiCut Q ×100, Clip Type, Drive (dB) | frequencies use the filter scale below; Clip Type 0 = None, 10 = Dirty SQ Root | matched against the editor |
| 54-74 | | MIX knob mapping, 3 slots | | confirmed |
| 75-95 | | VOICE 1 knob mapping, 3 slots | | confirmed |
| 96-116 | | VOICE 2 knob mapping, 3 slots | | confirmed |
| 117-137 | | Expression pedal mapping, 3 slots | | by elimination; not tested |
| 138-158 | | MASH mapping, 3 slots | | confirmed |

### Voice block (11 words; Voice 1 starts at word 21, Voice 2 at word 32)

| Offset | Parameter | Units | Status |
| --- | --- | --- | --- |
| +0 | Harmony (interval; the VOICE knobs map to it with values 0-51) | 25 = knob centre | confirmed changes the interval |
| +1 | Custom Voice | | confirmed position |
| +2 | Wet Level | 0.1 dB; the editor showed 0 dB for mapped values above 0 | confirmed (-1000 = -100.0 dB) |
| +3 | Delay | ms | matched (a MASH curve on it showed 0-260 ms) |
| +7 | ToneBend Tone | cents (1200 = one octave) | confirmed |
| +8 | ToneBend % | % | confirmed |
| +9 | Bend time | ms | confirmed |

Offsets +4 to +6 and +10 are not identified.

### Mapping slot (7 words)

`[enabled, parameter index, y at 0 %, 25 %, 50 %, 75 %, 100 %]`, where the y values are in the
parameter's own units. An empty slot is `-1, -1` followed by five filler words (seen as `0` or `-1`).
For MASH, x is footswitch pressure. For knobs, x is knob position, and the physical knob's
position overrides the stored parameter value.

### Behaviour notes

- **Pitch**: the voices sat at fixed intervals. ToneBend % on MASH did not move the pitch.
- **Wham**: ToneBend % on MASH bent the pitch, and changing ToneBend Tone in the file changed the
  bend, although the editor greys ToneBend Tone out.
- **V1V2**: ToneBend % on MASH moved the pitch from Voice 1's interval to Voice 2's. With Common Mix
  below 100 %, part of the signal stayed unshifted.

## Filter frequency scale (Brainwaves SoftClipper, Flashback 2)

Filter frequencies are stored as a raw step from 0 to 60, on a log scale from 20 Hz to 20 kHz:

    Hz = 20 × 1000^(raw / 60)        raw = 60 × log10(Hz / 20) / 3

Raw values seen next to the editor's display:

| Raw | Editor showed |
| --- | --- |
| 11 | 71.0 Hz |
| 15 | 112 Hz |
| 40 | 2.00 kHz |
| 51 | 7.10 kHz |
| 56 | 12.5 kHz |

## Flashback 2 Delay

`toneprintEffectTemplate` is `"Othello Flashback 2 Delay"` and `effectId` is `41402`. It uses the same
header and name layout as Brainwaves, and the same word numbering from byte 20.

The positions below come from one export and screenshots of the same TonePrint. Only values that
appear once in the export are listed.

| Word | Parameter | Units | Status |
| --- | --- | --- | --- |
| 18 | Delay 2 | ms | matched (654) |
| 22 | Feedback HiCut | filter scale | matched (40 = 2.00 kHz) |
| 23 | Feedback LoCut | filter scale | matched (15 = 112 Hz) |
| 27 | Feedback EQ BW | ×100 | matched (536 = 5.36) |
| 37 | Dynamic Release | ms | matched (1000) |
| 38 | Reverse Delay | ms | matched (800) |
| 64 | Tape Flanger | | matched (40) |
| 67 | Mod Depth 1 | % ×100 | matched (4510 = 45.1 %) |
| 75 | Mod Delay Time 3 | µs | matched (3911 = 3.9 ms) |
| 78 | Mod Feedback | % ×100 | matched (2549 = 25.5 %) |
| 83 | Octaver Input Filter Count | | matched (80) |
| 84 | Octaver Input Filter Q | ×10 | matched (200 = 20.0) |
| 89 | Octaver Output HiCut Freq | filter scale | matched (51 = 7.10 kHz) |
| 92-196 | knob, expression and MASH mappings | 7-word slots | not decoded |

In this export the first two words of the used mapping slots were `1 2`, `1 4`, `3 4` and `0 6`,
not the Brainwaves `1, index` pattern.
