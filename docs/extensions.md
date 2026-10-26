# Extensions

Without extensions the output contains only what its format needs, plus a comment where each code
comes from. An extension adds comments that other tools read; to rf433 and lircd they are ordinary
comments. Extensions are switched on with `--extension NAME`, several times if needed.

An extension returns one annotation per code (a comment starting with `#`) and a few header lines
that explain it. The output decides where the annotation goes:

| Output | Place of the annotation |
|---|---|
| `lirc`, parsed codes | behind the code on the same line |
| `lirc`, raw codes | a line of its own above `name` |
| `rf433` | a line of its own above `name` |

## webremote

Button color and label for a web remote, as `#RGB Label`. Converted codes get a white button (`#FFF`)
labelled with the code name, underscores replaced by spaces:

```
      begin codes
          KEY_POWER                0x10EF       #FFF Power
          KEY_VOL_UP               0x40BF       #FFF Vol up
      end codes
```

```
  begin raw_codes
    #FFF Light an
    name Light_an
      350 1050 1050 350 ...
```

The convention it follows:

- In `codes`, a line with a code, a color and a label is a button.
- In `raw_codes` and rf433 code files, the last `#RGB Label` line above `name` belongs to that code;
  a code without one is shown as a white button with its name.
- Empty lines between codes are spacers. That is why the converter writes no empty lines between
  codes: edit colors, labels and spacers by hand afterwards.

## Writing an extension

Derive from `f0converter.extensions.base.Extension`, set `name` and `description`, implement
`annotate(signal, label)` and `header_lines()`, and add the class to `EXTENSIONS` in
`f0converter/extensions/registry.py`. `signal` is a signal of the model (`SubGhzSignal`,
`IrParsedSignal`, `IrRawSignal`), so an extension can annotate depending on protocol or frequency.
Return `None` for codes that need no annotation.
