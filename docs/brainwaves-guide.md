# Brainwaves and the TonePrint Editor: how the settings behave

Observations from building TonePrints on a Plethora X5 with TonePrint Editor 4.7.0.6: what we changed,
and what we heard or saw. Word numbers refer to [FORMAT.md](../FORMAT.md).

General editor behaviour is in [editor-notes.md](editor-notes.md).

## Brainwaves modes (COMMON > Subtype, word 9)

| Subtype | What we observed |
| --- | --- |
| **Pitch** (0) | Each voice sat at its interval. ToneBend % on MASH did not move the pitch. |
| **V1V2** (1) | ToneBend % on MASH moved the pitch from Voice 1's interval to Voice 2's. With Common Mix at 100 % the whole note moved; below 100 % part of the signal stayed at the original pitch. |
| **Wham** (2) | ToneBend % on MASH bent the pitch toward ToneBend Tone, which the editor greys out. Custom Voice made no audible difference. It sounded thin to us. |
| **Detune** | Not tested. |

## Parameters

**Levels and mix**
- **Dry Level** (word 10, 0.1 dB): at -100 dB only the voices were heard.
- **Common Mix** (word 20, 0.1 %): below 100 %, part of the note stayed unshifted.
- **Wet Level** (per voice, 0.1 dB): a knob mapping with values above 0 dB still showed 0 dB in the
  editor. With one voice muted in Wham mode, the effect was noticeably quieter.
- With Common Mix at 100 % and a voice at unison, a distorted guitar sounded quieter, duller and
  garbled compared with bypass. Putting the distortion after the Plethora reduced this.

**Per voice (Voice 1 at words 21-31, Voice 2 at words 32-42)**
- **Harmony** (+0): the voice's interval. The VOICE knob mappings use values 0-51, and 25 (the knob
  centre) sounded like unison. Other values were not measured.
- **Custom Voice** (+1): no audible effect in Wham mode.
- **ToneBend Tone** (+7, cents): the bend target.
- **ToneBend %** (+8): how far along the bend. MASH mapped to it moved the pitch.
- **Bend time** (+9, ms): how long the bend takes.
- **Wet Feedback**: no audible effect while the voice's Delay was 0.

**SoftClipper (words 47-52)**
- The SoftClipper tab shows LoCut Freq and Q, HiCut Freq Distance and Q, SoftClip Type, Drive and Symmetry.

## Recipe

- **Octave swoop:** see [recipes/octave-swoop-v1v2.md](../recipes/octave-swoop-v1v2.md).
