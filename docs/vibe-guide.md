# Viscous Vibe in the TonePrint Editor

What the editor shows for a Viscous Vibe TonePrint ("cali vibes moment") on a Plethora X5, TonePrint
Editor 4.7.0.6. The file layout of this effect has not been decoded yet.

## Tabs

| Tab | Controls shown |
| --- | --- |
| **ROUTER** | Input Level, FX Level (dB). There is no Kill Dry control |
| **VIBE** | Attack (s), Release (s), Drive (dB), Highcut Freq, Highcut Damp (dB), Mix (%), Boost (dB), Out Level (dB), Feedback (%); further down, Subtype and Depth (%) |
| **MODULATION** | Speed (Hz), Depth 1-3 (%), Mod HiCut, Mod Mix (%), Output Level (dB), Delay Time 1-3 (ms), Mod Feedback, Mod Feedback HiCut. Mod Type, Mod Active, Tape Flanger and LFO Type are also in the parameter list |
| **MAPPING / EXPRESSION PEDAL / MASH** | 3 slots each |
| **PRODUCT SETTINGS** | Not examined |

## Parameters available to MASH, knobs and expression pedal

In menu order:

- Router: Input Level, FX Level
- Vibe: Attack, Release, Drive, Highcut Freq, Highcut Damp, Mix, Boost, Out Level, Feedback,
  PhaRevLeft, PhaRevRight, Subtype, Default Speed, High Speed, Depth
- Modulation: Mod Type, Mod Active, Tape Flanger, 1. LFO Type, Speed, Depth 1, Depth 2, Depth 3, …
  (the list continues past the visible part)

**Vibe Subtype** options: Modern, Vintage, Vintage2, Simple.

Per the editor manual: Default Speed is the normal speed and High Speed the speed in Ramp mode;
Attack is the time to change speed in Ramp mode and Release the time to return (0.05-5 s each).
Ranges: Drive and Boost 0-12 dB, Mix and Depth 0-100 %, Out Level -100-0 dB, Feedback -100-100 %,
Default Speed and High Speed 0.2-20 Hz. Ramp mode was not tested.

Default Speed, High Speed, PhaRevLeft and PhaRevRight appear in the mapping list but were not in the
screenshots of the VIBE tab.

## Values in the TonePrint examined

| Setting | Value |
| --- | --- |
| Vibe Attack, Release | 4.170 s each, mapped (link icon) |
| Vibe Drive | 12 dB |
| Vibe Mix | 50 % |
| Vibe Subtype | Vintage |
| Vibe Depth | about 83 %, mapped (link icon) |
| Mod Mix | 0 %, mapped (link icon) |
| Mod Speed | 1.80 Hz |
| Mod Depth 1/2/3 | 1.1 / 2.2 / 1.3 % |
| Mod Delay Time 1/2/3 | 4.9 / 14.1 / 22.1 ms |
