# Flashback 2 Delay in the TonePrint Editor

What the editor shows for Flashback 2 Delay on a Plethora X5, TonePrint Editor 4.7.0.6. Word numbers are in
[FORMAT.md](../FORMAT.md#flashback-2-delay).

## Tabs

| Tab | What's on it |
| --- | --- |
| **ROUTER** | Input Level, FX Level (the delay's volume), Octaver to FX (feeds the octaver into the delay), Kill Dry (removes the unprocessed guitar) |
| **DELAY** | Delay 1 / Delay 2 times, Feedback / Feedback 2, Saturation, a high cut and low cut on the repeats, an optional Feedback EQ (type, freq, gain, bandwidth, slope, cut order), Pan 1/2, Output Level, Width, the Dynamic settings (Sens, Damping, Release: ducking the repeats while you play) and Reverse Delay |
| **MODULATION** | Mod Type (e.g. Vib.Ramp), Mod Active, Tape Flanger, LFO Type (e.g. Triangle), Speed, Depth 1-3, Mod HiCut, Mod Mix, Output Level, Delay Time 1-3, Mod Feedback and its HiCut |
| **OCTAVER** | An octave-up generator (filter bank, Q, output high cut, drive). Silent unless Router > Octaver to FX is turned up |
| **MAPPING / EXPRESSION PEDAL / MASH** | What the knobs, an expression pedal and MASH pressure control (3 slots each) |
| **PRODUCT SETTINGS** | Pedal-level options (not tested) |

Greyed-out controls belong to modes or settings that are switched off (e.g. Delay 2 when only one tap
is in use). A **link icon** above a value means a knob, the pedal or MASH is mapped to it. The value
shown is then the live one, not the stored one.

## Observed behaviour

- With MASH slot 1 set to Router - FX Level and MASH not pressed, the ROUTER tab showed FX Level as
  -4.0 dB with a link icon. The export showed a knob also mapped to FX Level (-79 to 0 dB); the
  knob's value applied.
