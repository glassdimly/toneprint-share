# toneprint-share

Read and edit **your own** TC Electronic TonePrint exports (`.tpr`), so you can set
parameters that TonePrint Editor greys out or limits, then import the result back into the editor.

## Requirements

- Python 3 (standard library only). It works anywhere Python runs; the editor itself can stay on Windows.
- TonePrint Editor 4.7 and the `.exe` you installed it from. The key is read from that file.
  This was tested with the 4.7.0.6 download, `TonePrint_64bit_4.7.0.6.exe`.
- At least one TonePrint you made yourself.

## Walkthrough: unlock a greyed-out setting

Example: in **Wham** mode, Brainwaves greys out **ToneBend Tone** (how far the MASH swoop
goes), so you can't make Voice 2 bend at all. Here's how to set it to a full octave anyway.

### 1. Export a TonePrint from the editor

In TonePrint Editor, go to **User TonePrints**, select yours, and use **export toneprint**.
Save it somewhere you can reach from a terminal, for example `~/toneprints/My Swoop.tpr`.

### 2. Find the key (once per editor version)

```sh
cd toneprint-share
export TPR_KEY_STRING="$(./tpr.py findkey \
    --exe ~/Downloads/TonePrint_64bit_4.7.0.6.exe \
    --sample ~/toneprints/'My Swoop.tpr')"
```

`findkey` tries the strings in the `.exe` until one decodes your export into valid TonePrint
JSON. It takes a few seconds and prints nothing else. Put the `export` line in your shell profile
if you don't want to run it again.

### 3. Look inside

```sh
./tpr.py decode ~/toneprints/'My Swoop.tpr' | head -c 300
```
```
{ "toneprintId" : "0123456789abcdef0123456789abcdef", "effectId" : "44428", "artistId" : "local",
  "midiId" : "52", "toneprintEffectTemplate" : "Othello Brainwaves Pitch Shifter",
  "toneprintName" : "My Swoop", "description" : "", "toneprintData" : "01050006..." }
```

The parameters live in `toneprintData`. `dump` lists them as numbered words:

```sh
./tpr.py dump ~/toneprints/'My Swoop.tpr'
```
```
header: 01050006 name: My Swoop
...
9 2          <- Subtype: 2 = Wham
10 -1000     <- Dry Level: -100.0 dB (units of 0.1 dB)
...
28 0         <- Voice 1 ToneBend Tone (cents)
29 0         <- Voice 1 ToneBend %
30 718       <- Voice 1 Bend time (ms)
...
39 300       <- Voice 2 ToneBend Tone (cents)
40 0         <- Voice 2 ToneBend %
41 718       <- Voice 2 Bend time (ms)
```

(The arrows are added here; the tool prints only the numbers.) [FORMAT.md](FORMAT.md) says which word
is which setting, and how sure each mapping is.

### 4. Change it and write a new file

`set` takes the source file, the output file, a new name (15 characters at most), and any number of
`WORD=VALUE` pairs:

```sh
./tpr.py set ~/toneprints/'My Swoop.tpr' ~/toneprints/'Swoop Octave.tpr' \
    "Swoop Octave" 28=1200 39=1200 30=200 41=200
```

This sets both voices to bend **+1200 cents (one octave)** and both bend times to **200 ms**.
`set` also gives the copy a fresh `toneprintId` and recomputes the file checksum.

Check the result:

```sh
./tpr.py dump ~/toneprints/'Swoop Octave.tpr' | grep -E '^(28|30|39|41) '
```
```
28 1200
30 200
39 1200
41 200
```

### 5. Import it

In TonePrint Editor, click **import toneprints** and pick `Swoop Octave.tpr`. It appears as a new
User TonePrint alongside the original. Open it to confirm the values, then send it to the pedal
as usual.

> Importing a file whose `toneprintId` already exists **replaces** that TonePrint. `set` always
> makes a new ID. If you hand-edit JSON with `decode`/`encode`, change the ID yourself.

## More examples

**Map MASH so a light press gives the full swoop.** MASH has 3 slots at words 138-158 (7 words each:
enabled, parameter index, then the value at 0/25/50/75/100 % pressure). Parameter index = word − 8,
so Voice 1 ToneBend % (word 29) is index 21:

```sh
./tpr.py set in.tpr out.tpr "Fast MASH" \
    138=1 139=21 140=0 141=100 142=100 143=100 144=100
```

**Make the MIX knob control swoop time** (knob slots start at word 54; Voice 1 Bend time is index 22):

```sh
./tpr.py set in.tpr out.tpr "Knob Speed" \
    54=1 55=22 56=10 57=50 58=150 59=400 60=1000
```

**Edit the raw JSON yourself:**

```sh
./tpr.py decode in.tpr > in.json
$EDITOR in.json                     # change values, the name, the toneprintId...
./tpr.py encode in.json > out.tpr   # the checksum is added for you
```

A complete preset is in [recipes/octave-swoop-v1v2.md](recipes/octave-swoop-v1v2.md).

## Using it with an AI assistant

This repo is set up so a coding assistant can design TonePrints with you. [AGENTS.md](AGENTS.md) holds
the workflow and the rules, and [docs/brainwaves-guide.md](docs/brainwaves-guide.md) explains what the
settings actually do.

1. Clone the repo and start your assistant **inside the folder**:
   ```sh
   git clone https://github.com/glassdimly/toneprint-share
   cd toneprint-share
   # then start your assistant here (Codex, opencode, Cursor, Claude Code, aider...)
   ```
   Many tools read `AGENTS.md` automatically. If yours doesn't, start with:
   *"Read AGENTS.md and follow it."*
2. Tell it where your files are, for example:
   > My TonePrint editor installer is at `~/Downloads/TonePrint_64bit_4.7.0.6.exe` and I exported
   > my TonePrint to `~/toneprints/My Swoop.tpr`. Make a version where holding MASH swoops the whole
   > note up an octave in about 200 ms, and put the swoop speed on the MIX knob.
3. It writes a new `.tpr` next to yours. Import it in TonePrint Editor, check the values it tells you to
   look at, play it, and tell it what you hear. Screenshots of the editor tabs help a lot.

The assistant runs `tpr.py` on your machine. The key stays in an environment variable and never goes
into files or chat.

## What this repo deliberately leaves out

- **No key material.** The tool finds the key in the copy of TonePrint Editor you have
  installed, and checks it against a file the editor exported for you.
- **No TC Electronic software, factory or artist TonePrints, or decrypted copies of them.**
- **No disassembly** or other code taken from the editor.

It exists so you can work on presets **you** made, with hardware you own, and get the
editor to accept them (interoperability). Please don't use it to extract or pass around other
people's TonePrints. To share a sound based on someone else's TonePrint, publish the settings
you changed (a recipe), not the file.

This is not legal advice. TonePrint, Plethora, Brainwaves and MASH are trademarks of
their owners. This project is not affiliated with or endorsed by TC Electronic or Music Tribe.

## Tested with

TonePrint Editor 4.7.0.6 (Windows), Plethora X5, Brainwaves Pitch Shifter TonePrints.
The editor checks the 2-byte file checksum on import. As of that version it does not check word 0
of `toneprintData`.
