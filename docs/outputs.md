# Outputs

An output takes signals of the model and writes them in one format. Signals it cannot take (e.g. IR
signals for `rf433`) are reported as errors: `Power: not supported by the rf433 output, try another
command`.

## rf433: code files of rf433 (command `rf433`)

Takes SubGhz signals. The format of the code files is described in the
[rf433 documentation](https://github.com/d03n3rfr1tz3/rf433/blob/main/docs/code-files.md): one frame
per code, values in µs, pulse first, ending with the pause after the frame.

Without `--remote` only the `name` blocks are printed, indented to be pasted into the `raw_codes` of an
existing code file:

```
    # Light_On.sub, Princeton 24 bit, TE 350
    name Light_On
      350 1050 1050 350 350 1050 ...
      350 10500
```

With `--remote NAME` a complete code file follows, with `repeat` if `--repeat` is given:

```
f0-converter rf433 "Garden/*.sub" --remote Garden --repeat 10 > /etc/rf433/rf433.conf.d/Garden.conf
rf433 check
```

Code names:

- The code name is the file name, made plain: letters, digits, `_` and `-` (`Küche Licht` becomes
  `Kueche_Licht`).
- `--name NAME` sets it for a single file.
- `--rename-suffix OLD=NEW` changes the end of names, e.g. `--rename-suffix On=an --rename-suffix
  Off=aus` turns `Light_On` into `Light_an` (case-insensitive). It may be given several times.
- Two files with the same code name are an error; convert one of them alone with `--name`.

Checks: a code must end with a pause, contain no zero values, have at most 1025 values and be at most
500 ms long, because rf433 sends a frame in one write of `gpio-ir-tx`. Signals that are not on
433.92 MHz or not OOK get a warning, since the usual transmitter modules cannot send them.

## lirc: LIRC remote files (command `lirc`)

Takes IR signals. Every input file becomes one `lircd.conf` text with several remotes:

- one remote per parsed protocol; the protocol with the most signals gets the name of the remote,
  the others a suffix (`TV`, `TV_Samsung32`),
- one `RAW_CODES` remote per carrier frequency and duty cycle (`TV_raw`, or `TV_raw_38000` …
  when there are several).

The remote name is the file name without a leading number (`05. HDMI-Switcher.ir` becomes
`HDMI-Switcher`), or `--remote NAME` for a single file. Several files need `--output FOLDER`; each is
written to `<file name>.lircd.conf` there, existing files are not overwritten.

### Parsed signals

| Flipper protocol | LIRC |
|---|---|
| `NEC`, `NECext`, `NEC42`, `NEC42ext`, `Pioneer` | `SPACE_ENC`, 32 or 42 bit |
| `Samsung32` | `SPACE_ENC`, 32 bit |
| `RCA` | `SPACE_ENC`, 24 bit |
| `SIRC`, `SIRC15`, `SIRC20` | `SPACE_ENC`, 12, 15 or 20 bit |
| `Kaseikyo` | `SPACE_ENC`, 48 bit |
| `RC5`, `RC5X` | `RC5`, 13 bit |
| `RC6` | `RC6`, 21 bit |

Address and command become the LIRC code in the bit order LIRC sends them. If all codes of a remote
share their address part, it becomes `pre_data` (e.g. NEC: 16 bit `pre_data`, 16 bit codes).
Key names are made from the signal names: `Vol+` becomes `KEY_VOL`, names that start with `KEY_` or
`BTN_` are kept, the same name twice becomes `KEY_X` and `KEY_X_2`.

### Raw signals

The values are written as they are. A raw signal that ends with a pause has it removed; the longest of
these pauses becomes the `gap` of the remote (with a warning), otherwise the gap is 100 ms. lircd sends
at most 255 values per signal; longer signals are reported as errors.
