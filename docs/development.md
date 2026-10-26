# Development

## Running from the repository

```
python bin/f0-converter rf433 "tests/fixtures/*.sub" --remote Garden
python -m f0converter lirc "tests/fixtures/01. Example TV.ir" --extension webremote
```

## Tests

```
python -m unittest discover -s tests
```

The tests only use the standard library and made-up files: `tests/support.py` builds the Flipper Zero
files in `tests/fixtures` from code (`python tests/support.py` writes them anew). Please keep
recordings of real remotes out of the tests.

`tests/test_goldens.py` converts the fixtures and compares the result with `tests/goldens`. After an
intended change of the output, write the goldens anew and check the difference before committing:

```
UPDATE_GOLDENS=1 python -m unittest discover -s tests
git diff tests/goldens
```

## Structure

```
f0converter/
  cli.py                parser built from the command list, errors -> exit code
  messages.py           info, warnings and errors to stderr
  names.py              file, code, key and remote names
  model/                format-neutral signals: SubGhzSignal (with PulseCode), IrParsedSignal, IrRawSignal,
                        InputResult (signals, warnings and errors of one file)
  formats/              reading and writing of file formats, without conversion logic
    flipper/            FlipperFile: read() and write()
    lirc/               writer.py, protocols/ (Flipper address and command -> LIRC code and timing)
    rf433/              writer.py
  signal/               cluster.py (clean), frames.py (frame extraction)
  inputs/               one folder per input, INPUTS in registry.py
    flipper_subghz/     raw.py, protocols/ (one file per static protocol, rolling codes)
    flipper_ir/         parsed.py, raw.py
  outputs/              one folder per output, OUTPUTS in registry.py
    rf433/              Rf433Output, checks.py
    lirc/               LircOutput, keys.py
  extensions/           Extension, EXTENSIONS in registry.py, webremote.py
  commands/             convert/ (one file per output, common flow in base.py), info/formats.py
```

The flow of a conversion (`commands/convert/base.py`): expand the patterns, read every file with
the input that recognizes it, hand all `InputResult`s to the output, print or write its documents.

The architecture is symmetric: inputs only produce signals of the model and outputs only take them,
so any input can be combined with any output that accepts its signals. Knowledge of a file format
lives in `formats/` and is shared by its input and its output.

## Adding a format

**A new output** (e.g. ESPHome, Pronto, Broadlink):

1. `outputs/<name>/__init__.py` with a class derived from `outputs.base.Output`: `name`,
   `description`, `accepts(signal)` and `convert(results, options, messages)` returning `Document`s.
   Use `self.accepted(result, messages)` to get the signals and report the others.
2. Add it to `OUTPUTS` in `outputs/registry.py`.
3. A command in `commands/convert/<name>.py` derived from `ConvertCommand` with `output_class`, and
   its options; add it to `COMMANDS` in `commands/__init__.py`.
4. Golden tests in `tests/test_goldens.py`.

Outputs that need IR pulses instead of LIRC codes need a format-neutral IR pulse encoder first, e.g.
`f0converter/protocols/infrared/`; the timings in `formats/lirc/protocols` are a good template.

**A new SubGhz protocol**: a file in `inputs/flipper_subghz/protocols/` with an `encode(block)`
returning the values and a description, added to `PROTOCOLS` there, and a test with a made-up key.

**A new IR protocol for LIRC**: an `IrProtocol` in the fitting file of `formats/lirc/protocols/`
(bits, `pre_data` bits, timing, encoder) and a test against a publicly known code.

**A new input**: `inputs/<name>/` with a class derived from `inputs.base.Input`: `detect(text)`,
`read(path, text, settings)` and `protocols()`; add it to `INPUTS` in `inputs/registry.py`. The order
matters for the detection.

## The way back to the Flipper Zero (planned)

LIRC has old but very large databases of remotes; converting them to the Flipper Zero is the next
step. The structure is prepared for it:

1. **LIRC → Flipper IR** (`f0-converter flipper remote.lircd.conf`)
   - `formats/lirc/parser.py` reads lircd.conf: several remotes, `flags`, `header`/`one`/`zero`,
     `plead`/`ptrail`, `pre_data`/`post_data`, `repeat`, `gap`, `toggle_bit_mask`, `codes` and
     `raw_codes`.
   - `inputs/lirc/` turns it into signals of the model. If bits and timing fit a Flipper protocol
     family, the inverse of its encoder in `formats/lirc/protocols/` gives an `IrParsedSignal` with
     address and command. Otherwise a LIRC pulse encoder (SPACE_ENC, RC5/RC6 bi-phase, CONST_LENGTH
     for the gap) gives an `IrRawSignal`.
   - `outputs/flipper_ir/` writes the `.ir` file with `formats/flipper/fileformat.py`, which can
     already write (with a roundtrip test).
   - Tests: Flipper → LIRC → Flipper roundtrip with the public codes of `tests/test_ir.py`; made-up
     LIRC files with unusual timing become raw.
2. **rf433 → Flipper SubGhz RAW**: `.sub` with frequency 433920000 and an OOK preset, the frame
   times the repeat as `RAW_Data`. This needs `formats/rf433/parser.py` and `inputs/rf433/`; the
   parser is a copy of the one in the rf433 repository, since both repositories stay independent.
3. `commands/convert/flipper.py` recognizes the input by its content: `Filetype:` for Flipper,
   `begin remote` with `flags` for LIRC, `begin remote` without `flags` but with `raw_codes` for
   rf433; `--from` stays the way out.

Further candidates: outputs for ESPHome, Pronto Hex, Broadlink Base64 (Home Assistant
`remote.send_command`) and Tasmota; inputs for more static SubGhz protocols (CAME, Nice FLO,
Holtek, Linear …), SubGhz BinRAW and IR universal libraries.
