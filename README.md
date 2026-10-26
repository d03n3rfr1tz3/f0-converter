# f0-converter

Converts Flipper Zero files into other formats:

- SubGhz files (`.sub`) into code files of [rf433](https://github.com/d03n3rfr1tz3/rf433), a 433 MHz
  OOK sender for the Raspberry Pi. Recordings (RAW) are cut down to the one frame that repeats most
  often; keys of static protocols (Princeton, Intertechno V3) are encoded.
- IR files (`.ir`) into LIRC remote files (`lircd.conf`): parsed signals become remotes with LIRC codes
  per protocol, raw signals become `raw_codes` per carrier.

Only the Python standard library is needed (Python 3.9 or newer); it runs on Windows, Linux and macOS.
Inputs and outputs are separate, so further formats and the way back to the Flipper Zero can be added
(see [docs/development.md](docs/development.md)).

## Installation

```
git clone https://github.com/d03n3rfr1tz3/f0-converter.git
```

Run it with `python f0-converter/bin/f0-converter …` or link `bin/f0-converter` into a folder of the
`PATH`, e.g. `sudo ln -s /opt/f0-converter/bin/f0-converter /usr/local/bin/f0-converter`.
`pip install .` installs the `f0-converter` command as well.

## Quick start

SubGhz recordings of one remote into a complete rf433 code file:

```
f0-converter rf433 "Garden/*.sub" --remote Garden --repeat 10 > garden.conf
```

Without `--remote` only the `name` blocks are printed, ready to be pasted into an existing code file:

```
f0-converter rf433 Garden/Light_On.sub --name Light_on
```

An IR file into a LIRC remote file:

```
f0-converter lirc "TV.ir" > tv.lircd.conf
f0-converter lirc "infrared/*.ir" --output lircd.conf.d
```

The converted text goes to stdout, everything else (what was found, warnings, errors) to stderr. The
exit code is 1 if a file or a signal could not be converted; the rest is converted anyway.

## Commands

| Command | Purpose |
|---|---|
| `rf433 FILES [--remote NAME [--repeat N]] [--name NAME] [--rename-suffix OLD=NEW]` | SubGhz files to rf433 codes |
| `lirc FILES [--remote NAME] [--output FOLDER]` | IR files to LIRC remote files |
| `formats` | list inputs, outputs, protocols and extensions |

Common options of `rf433` and `lirc`:

- `--from INPUT`: input format, if it is not recognized by the content (`flipper-subghz`, `flipper-ir`)
- `--extension NAME`: add comments for other tools, e.g. `webremote` for button colors and labels

`rf433` also takes `--min-gap US` and `--tolerance FACTOR` for difficult recordings. Patterns like
`*.sub` are expanded by f0-converter itself, so they work in the Windows shell as well.

## Documentation

- [Inputs](docs/inputs.md): Flipper Zero SubGhz and IR files, supported protocols
- [Outputs](docs/outputs.md): rf433 code files and LIRC remote files in detail
- [Extensions](docs/extensions.md): comments for other tools, e.g. a web remote
- [Development](docs/development.md): structure, tests, adding formats, the way back to the Flipper Zero

## License

MIT, see [LICENSE](LICENSE).
