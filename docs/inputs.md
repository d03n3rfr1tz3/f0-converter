# Inputs

An input reads one kind of file into signals of the model (`f0converter/model`). The kind is
recognized by the content (`Filetype:` line); `--from` chooses it when that fails.
`f0-converter formats` lists all inputs and their protocols.

## flipper-subghz: Flipper Zero SubGhz files (`.sub`)

Every file holds one signal. Its name is the file name without `.sub` (a trailing `.bak` is dropped
as well).

### RAW recordings

`RAW_Data` lines hold pulses (positive) and pauses (negative) in µs, as the Flipper Zero recorded
them while the button was held down. f0-converter:

1. joins all `RAW_Data` lines, drops zero values and leading pauses and merges neighbours with the
   same sign,
2. splits the recording into frames at every pause of at least `--min-gap` µs (default 5000),
3. drops the last frame (usually cut off) and frames with fewer than 16 values (noise),
4. groups frames of the same length whose values differ by at most `--tolerance` (default 25 %, at
   least 120 µs); the pause at the end is not compared,
5. takes the median of every value over the biggest group, which needs at least two frames,
6. cleans the frame: values within the tolerance get the most frequent value of their group, pulses
   and pauses separately.

A recording with only one frame that ends with a long pause is taken as it is. Errors:

- `no frame with at least 16 values and a pause of 5000 us found (noise only?)`: record again, closer
  to the remote, or try a smaller `--min-gap`.
- `no frame repeats in N frames`: hold the button longer, or the pause between the frames is shorter
  than `--min-gap`.

The output `rf433` cleans all recordings of one call together once more, so codes of one remote end
up with the same values.

### Keys of static protocols

| Protocol | Encoding |
|---|---|
| `Princeton` | bit 1 = 3 TE pulse + 1 TE pause, bit 0 the other way round, then 1 TE pulse and `Guard_time` TE pause; TE from `TE` (default 390 µs), `Guard_time` default 30 |
| `Intertechno_V3` | 32 bit only (KlikAanKlikUit, Nexa): sync 270/2700 µs, every bit as two pulses of 270 µs with 270/1300 µs pauses, 10400 µs pause at the end |

Rolling code protocols (KeeLoq, Security+, Somfy, Nice FloR-S …) are refused: their recording
contains a counter, so sending it again does not work or even desynchronizes the remote. Other
protocols are refused with the hint to record the button as RAW.

`Frequency` and `Preset` are kept; the `rf433` output warns if they are not 433.92 MHz and OOK.

## flipper-ir: Flipper Zero IR files (`.ir`)

One file holds many signals, each starting with `name`.

- `type: parsed`: `protocol`, `address` and `command`; the numbers are written as four bytes, lowest
  first (`07 00 00 00`). The protocol is checked by the output, which knows what it can write.
- `type: raw`: `frequency` in Hz, `duty_cycle` (0.33 = 33 %) and `data` in µs, pulse first.

A broken signal is reported with its name and skipped; the others are converted. Lines starting with
`#` separate the signals, other lines without a colon are ignored, a UTF-8 BOM is allowed.
