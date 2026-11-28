# The .tpr format (TonePrint Editor 4.7.0.6)

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
| 47-53 | | SoftClipper: LoCut freq (raw), LoCut Q x100, HiCut distance (raw), HiCut Q x100, Clip Type, Drive dB, Symmetry | frequencies use the filter scale below; Clip Type 0 = None, 10 = Dirty Square Root | Q, type and drive confirmed; frequency scale confirmed against screenshots |
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
| +2 | Wet Level | 0.1 dB, maximum 0 dB (higher values, even from a knob mapping, are capped) | confirmed (-1000 = -100.0 dB) |
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

## Filter frequency scale (all effects seen so far)

Filter frequencies are stored as a raw step from 0 to 60, on a log scale from 20 Hz to 20 kHz:

    Hz = 20 × 1000^(raw / 60)        raw = 60 × log10(Hz / 20) / 3

| Raw | Hz | Raw | Hz |
| --- | --- | --- | --- |
| 0 | 20 | 40 | 2000 |
| 11 | 71 | 51 | 7100 |
| 15 | 112 | 55 | 11 200 |
| 20 | 200 | 56 | 12 600 |
| 30 | 630 | 60 | 20 000 |

**Confirmed**: these values match the editor's display on the Brainwaves SoftClipper tab and on the
Flashback 2 Delay, Modulation and Octaver tabs.

## Flashback 2 Delay

`toneprintEffectTemplate` is `"Othello Flashback 2 Delay"` and `effectId` is `41402`. It uses the same
header and name layout as Brainwaves, and the same word numbering from byte 20.

The positions below were found by matching values shown in the editor against one export. Values that
are not unique (0, 100) are marked **inferred** where several words could match.

| Word | Parameter | Units | Status |
| --- | --- | --- | --- |
| 13, 14 | Router: Input Level, FX Level | dB | inferred (both 0 in the export) |
| 17 | Delay 1 | ms | confirmed |
| 18 | Delay 2 | ms | confirmed |
| 19 | Feedback | % | confirmed position |
| 20 | Feedback 2 | % | inferred |
| 21 | Saturation | dB | inferred |
| 22 | Feedback HiCut | filter scale | confirmed (40 = 2.00 kHz) |
| 23 | Feedback LoCut | filter scale | confirmed (15 = 112 Hz) |
| 24 | Feedback EQ Type | 0 = Bypass | inferred |
| 25 | Feedback EQ Freq | filter scale | inferred |
| 26 | Feedback EQ Gain | dB | inferred |
| 27 | Feedback EQ BW | ×100 | confirmed (536 = 5.36) |
| 28 | Feedback EQ Slope | list, 0 = 3 dB/oct | inferred |
| 29 | Feedback EQ Cut Order | | inferred |
| 30, 31 | Pan 1, Pan 2 | | inferred |
| 32 | Output Level | dB | inferred |
| 33 | Width | % | inferred |
| 34, 35 | Dynamic Delay Sens, Dynamic Damping | dB | inferred |
| 37 | Dynamic Release | ms | confirmed (1000) |
| 38 | Reverse Delay | ms | confirmed (800) |
| 62-65 | Modulation: Mod Type, Mod Active, Tape Flanger, LFO Type | | Tape Flanger (64 = 40) confirmed; the others inferred |
| 66 | Mod Speed | raw, scale unknown | inferred (192 shown as 7.10 Hz, but the knob is mapped) |
| 67 | Mod Depth 1 | % ×100 | confirmed (4510 = 45.1 %) |
| 68, 69 | Mod Depth 2, Depth 3 | % ×100 | inferred |
| 70 | Mod HiCut | filter scale | confirmed (60 = 20 kHz) |
| 71 | Mod Mix | % | inferred |
| 72 | Mod Output Level | dB | inferred |
| 73-75 | Mod Delay Time 1-3 | µs | confirmed (100 = 0.1 ms, 3911 = 3.9 ms) |
| 78 | Mod Feedback | % ×100 | confirmed (2549 = 25.5 %) |
| 79 | Mod Feedback HiCut | filter scale | confirmed (60 = 20 kHz) |
| 83 | Octaver Input Filter Count | | confirmed (80) |
| 84 | Octaver Input Filter Q | ×10 | confirmed (200 = 20.0) |
| 86 | Octaver Q Output Rel Up | ×100 | confirmed (1 = 0.01) |
| 87 | Octaver FX Level Up | dB | confirmed (-100) |
| 89 | Octaver Output HiCut Freq | filter scale | confirmed (51 = 7.10 kHz) |
| 92-196 | knob, expression and MASH mappings | 7-word slots | **not decoded yet** |

The mapping slots do not follow the Brainwaves `[enabled, index, ...]` pattern: the first two
words take values such as `0 6`, `1 4` and `3 4`. Decoding them needs the two-exports method
(change one mapping in the editor, export again, diff).
