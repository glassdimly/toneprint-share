# Octave swoop (Brainwaves, V1V2 mode)

Hold MASH to swoop the whole note up an octave; release it to swoop back down. MIX sets the swoop time.
Start from any Brainwaves TonePrint of your own, export it, then apply:

```sh
./tpr.py set mine.tpr swoop.tpr "Octave Swoop" \
  9=1 10=-1000 19=1 20=1000 \
  21=25 32=37 \
  54=1 55=22 56=10 57=50 58=150 59=400 60=1000 \
  61=1 62=33 63=10 64=50 65=150 66=400 67=1000 \
  138=1 139=21 140=0 141=100 142=100 143=100 144=100 \
  145=1 146=32 147=0 148=100 149=100 150=100 151=100
```

| Words | Setting |
| --- | --- |
| 9=1 | Subtype V1V2 |
| 10=-1000 | Dry Level -100 dB |
| 19=1, 20=1000 | Link Mix on, Common Mix 100 %, so nothing is left unshifted |
| 21=25 | Voice 1 Harmony at the knob centre (the resting pitch) |
| 32=37 | Voice 2 Harmony, a starting point; tune it to the octave by ear with the VOICE 2 knob |
| 54-67 | MIX knob -> Bend time for both voices, 10 / 50 / 150 / 400 / 1000 ms |
| 138-151 | MASH -> ToneBend % for both voices; full swoop from a light press |

Remove any existing mapping on the VOICE 2 knob only if you want the interval fixed.

**Shimmer on top:** put MASH slot 3 (words 152-158) on Common Delay Feedback
(`152=1 153=8 154=0 155=60 156=60 157=60 158=60`), with Link Delay on and a Common Delay
of about 180 ms (`13=1 14=180`).
