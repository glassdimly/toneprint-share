# AGENTS.md: instructions for AI assistants

You are helping someone design or edit TC Electronic TonePrints (currently Brainwaves Pitch
Shifter on a Plethora X5) by editing `.tpr` export files with `tpr.py`. Read these first:

1. **This file**: the workflow and the rules.
2. **[FORMAT.md](FORMAT.md)**: the file layout and the word map (which number is which setting, and how sure each is).
3. **[docs/brainwaves-guide.md](docs/brainwaves-guide.md)**: how the modes and settings actually behave,
   including the common traps.
4. **[recipes/](recipes/)**: presets known to work.

## Rules

- **Never write the key string anywhere:** not in files, commits, issues, logs or chat output.
  It goes only in the `TPR_KEY_STRING` environment variable, from `tpr.py findkey`. Never commit
  `.exe`, `.tpr` or decoded `.json` files (`.gitignore` already blocks them).
- **Never overwrite the user's exports.** Write edited files to a new path with a new name. `tpr.py set`
  also gives each file a new `toneprintId`. Importing a file whose ID already exists **replaces** that
  TonePrint in the editor.
- **Don't claim a setting works until the user has confirmed it in the editor or on the pedal.** Many
  word positions are marked *inferred* in FORMAT.md. After making a file, tell the user what to look at
  (which tab, which value), and ask for a screenshot if you're unsure.

## Workflow

```sh
# once per session (or per editor version)
export TPR_KEY_STRING="$(./tpr.py findkey --exe <TonePrint .exe> --sample <user's own .tpr>)"

./tpr.py dump  <file.tpr>                      # read the current values
./tpr.py set   <in.tpr> <out.tpr> "<Name>" W=V ...   # write a new file (new ID, checksum fixed)
./tpr.py dump  <out.tpr> | grep -E '^(W1|W2) '      # verify what you wrote
```

Then the user imports `<out.tpr>` with **import toneprints** in the editor, checks the values, and plays.

**When you need to learn where a setting lives:** ask the user to export the same TonePrint twice,
changing exactly one setting in the editor in between. Then diff the two `dump` outputs. This is how
every **confirmed** entry in FORMAT.md was found. Update FORMAT.md when you confirm something new.

## Tips for talking to the user

- Describe settings by their **editor labels** ("VOICE 1 → 1. ToneBend Tone"), not only by word numbers.
- The user hears the pedal and you don't. Turn their descriptions into checks: "only a harmony moves" means
  Common Mix is below 100 % or a voice isn't bending; "it does nothing" means wrong subtype, a mapped
  knob overriding the value, or a delay time of 0.
- Remember the units: levels are in 0.1 dB, mix in 0.1 %, bends in cents (1200 = an octave), times in ms.

## Repo hygiene

- Keep docs in our own words, based on our own testing. Don't paste text from TC manuals.
- Before committing, check that no key material, `.tpr`, `.exe` or decoded JSON is staged.
