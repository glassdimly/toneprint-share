# TonePrint Editor: general notes

Behaviour that applies to every effect, seen with TonePrint Editor 4.7.0.6 and a Plethora X5.

- **Live editing is not guaranteed.** Changes were often heard immediately while the pedal was
  connected, but in some sessions the pedal kept playing the previously saved version until the
  TonePrint was saved to it. If a change seems to do nothing, save it to the pedal and test again.
- **Knobs, expression pedal and MASH each have 3 mapping slots.** Each slot drives one parameter
  along a 5-point curve (at 0, 25, 50, 75 and 100 % of the knob, pedal or pressure). A curve can
  run backwards or be flat.
- **A mapped knob wins.** If a parameter is mapped to a physical knob, the knob's position
  overrides the value set on screen. If a value "won't stick", check the MAPPING tab.
- **MASH** is the pressure-sensitive footswitch. A click turns the effect on or off, and pressure
  after that drives the mapped parameters. A curve that rises late (for example 0, 0, 30, 62, 100) needs a
  hard press; 0, 100, 100, 100, 100 reaches full value with a light press.
- **The Plethora X5 runs 5 slots in a chain.** Sound from another active slot can be mistaken for
  the slot being edited.
- **To test without your foot,** set the MASH slot to "No selection" and drag the parameter on screen.
  Put the mapping back before saving.
- **User TonePrints stay on the computer that made them.** The editor has no sharing; `.tpr`
  export and import is the only way to move them.
- **Importing replaces by ID.** A `.tpr` whose `toneprintId` matches an existing TonePrint
  overwrites it, even if the name differs.
- **Greyed-out does not mean unused.** The editor greys some parameters out depending on the mode, but
  the pedal can still use the stored value (see Wham in the [Brainwaves guide](brainwaves-guide.md)). Editing the file is the only way to
  change them.
- A **PRODUCT SETTINGS** tab (shown only for some products) holds things like turning MASH on or off and
  calibrating an expression pedal. Not tested here.
