# Brainwaves and the TonePrint Editor: how the settings behave

Practical notes gathered while building an octave-swoop TonePrint on a Plethora X5 with
TonePrint Editor 4.7.0.6. They are written from our own testing: what we changed, and what we heard or
saw. Where a note is a guess rather than a test, it says so. Word numbers refer to [FORMAT.md](../FORMAT.md).

General editor behaviour is in [editor-notes.md](editor-notes.md).

## Brainwaves modes (COMMON > Subtype, word 9)

| Subtype | What it does | Notes from testing |
| --- | --- | --- |
| **Pitch** (0) | Fixed-interval harmonizer | Each voice sits at its interval. ToneBend did not move the pitch, so MASH appeared to do nothing. |
| **V1V2** (1) | ToneBend morphs from Voice 1's interval to Voice 2's | With Voice 1 at unison and Voice 2 at another interval, MASH sweeps the pitch between them. Common Mix 100 % shifts the whole note; lower values keep part of the dry signal. |
| **Wham** (2) | Whammy-style bend driven by ToneBend % toward ToneBend Tone | ToneBend Tone is greyed out but is used. Custom Voice has no effect. Sounded thin or soft at the top for us. |
| **Detune** (3) | Detuning | Not tested. |

## Parameters

**Levels and mix**
- **Dry Level** (word 10, 0.1 dB): the unprocessed signal. Set -100 dB to hear only the voices.
- **Common Mix** (word 20, 0.1 %) together with **Link Mix** (word 19): when linked, Common Mix sets the voices' share.
  **Below 100 % some of the note stays unshifted.** That is the usual cause of "the root doesn't move".
- **Wet Level** (per voice, 0.1 dB): the voice's volume. **It can't go above 0 dB**: a knob mapped to
  +12 dB stops at 0. Muting one voice of two drops the level a lot.
  If one voice is muted and the other moves, the result is quieter.
- **The shifter changes the tone even at unison.** With Common Mix at 100 % and the voice at unison,
  a distorted guitar came out quieter, duller and garbled compared with bypass. Putting the
  distortion after the Plethora reduced this.
- **Volume drop or clipping when engaged:** shifted voices can come out quieter or hotter than
  dry. SoftClipper **Drive** adds level (a factory TonePrint used about 17 dB with a gritty type);
  for headroom, lower each Wet Level by about 3 dB. Lowering Common Mix brings the unshifted root back,
  so don't use it as a volume control.

**Per voice (Voice 1 at words 21-31, Voice 2 at words 32-42)**
- **Harmony** (+0): the voice's interval. The VOICE knobs map it as 0-51, and the knob centre
  (25) sounded like unison. Treat other values as approximate and tune by ear.
- **Custom Voice** (+1, 0-2400): a custom pitch amount. It had no effect in Wham mode in our tests.
- **ToneBend Tone** (+7, cents, ±4800, audible up to about 2 octaves): how far a bend goes. **+1200 = one octave
  up; negative values bend down.** A factory "whammy" TonePrint bent downward for this reason.
- **ToneBend %** (+8): how far along the bend you are. This is what to put on MASH.
- **Bend time** (+9, ms, 0-10000): how long the bend takes to travel. It is the "swoop speed";
  20 ms is a snap and 200-300 ms is a clear glide. Mapping it to a knob is very handy.
- **Delay** (+3, ms, 0-260), **Dry / Wet Feedback**: per-voice delay. **Wet Feedback does nothing while
  Delay is 0.** Wet feedback sends the echoes back through the pitch shifter, so the repeats climb.

**Common delay (words 13-18; positions inferred)**
- Link Delay / Common Delay, Link Delay Feedback / Common Delay Feedback, Link Wet Feedback /
  Common Wet Feedback. When a Link setting is on, the Common value replaces the per-voice ones.

**SoftClipper (words 47-53)**
- A low cut and a high cut on the effect signal, a clip type (0 = None), Drive (dB) and Symmetry.

## Recipes that worked

- **Octave swoop:** V1V2 mode, Dry -100 dB, Common Mix 100 %, Voice 1 at unison, Voice 2 at +1 octave;
  MASH drives both voices' ToneBend % with a curve of 0, 100, 100, 100, 100; the MIX knob drives Bend time for both voices.
  See [recipes/octave-swoop-v1v2.md](../recipes/octave-swoop-v1v2.md).
- **Shimmer and warble on press** (as in a factory TonePrint): MASH sweeps **voice Delay times**
  (0 to 260 ms and 0 to 130 ms) and raises **Common Delay Feedback** from 0 to 100 %. A delay
  time that moves bends the pitch of the echoes, so the shimmer is strongest when you release.
- **Echo that climbs:** Link Delay on, Common Delay about 180 ms, MASH slot 3 raising Common Delay Feedback to
  about 60 %.
