# Shaker Vibrato in the TonePrint Editor

What the editor shows for a Shaker Vibrato TonePrint ("Shaker Default Momentary") on a Plethora X5,
TonePrint Editor 4.7.0.6. The file layout of this effect has not been decoded yet.

## Tabs

| Tab | Controls |
| --- | --- |
| **ROUTER** | Kill Dry (on/off), FX Level (-100-0 dB) |
| **MODULATION** | Mod Type, Mod Active, Tape Flanger, 1. LFO Type, Speed, Depth 1-3, Mod HiCut, Mod Mix, Output Level, Delay Time 1-3, Mod Feedback, Mod Feedback HiCut, **Ramp Time** |
| **MAPPING / EXPRESSION PEDAL / MASH** | 3 slots each |
| **PRODUCT SETTINGS** | Pedal-level options (not examined) |

The MODULATION tab is the same block used by other effects (Flashback 2 and Viscous Vibe have it too),
plus **Ramp Time** (0-5000 ms), which only Shaker Vibrato has.

## Mod Type

Options: Classic Cho, Adv.Cho, Classic Fla, Adv.Flanger, Vibrato, Vib.Ramp, TriChorus, TriChoAltn,
TZFlanger (the list may continue).

- **Vibrato:** the vibrato runs whenever the effect is on.
- **Vib.Ramp:** the 2012 editor manual describes it as vibrato that is applied only while the
  footswitch of a Shaker Vibrato pedal is held, with Ramp Time as the build-up time. Its behaviour on the
  Plethora X5 has not been tested yet.

## Observed behaviour

- MASH slot 1 on **Modulation - Speed**, starting at the minimum speed with no pressure
  and rising with pressure, gave no audible vibrato at rest and vibrato while MASH was pressed.

## Values in the TonePrint examined

| Setting | Value |
| --- | --- |
| Mod Type | Vibrato |
| Mod Active | on |
| Tape Flanger | 0 (greyed out) |
| 1. LFO Type | Sine of Cosine |
| Speed | 8.00 Hz, mapped (link icon) |
| Depth 1 | 14.3 %, mapped (link icon) |
| Depth 2, Depth 3 | 0.1 % (greyed out) |
| Mod HiCut | 5.00 kHz |
| Mod Mix | 100 % |
| Output Level | 0 dB |
| Delay Time 1 | 0.1 ms |
| Delay Time 2, 3 | 0.1 ms (greyed out) |
| Mod Feedback | -35.5 % |
| Mod Feedback HiCut | 20.0 kHz |
| Ramp Time | 3330 ms, mapped (link icon) |

