# f0-converter

Converts Flipper Zero files into other formats:

- SubGhz files (`.sub`) into code files of [rf433](https://github.com/d03n3rfr1tz3/rf433), a 433 MHz
  OOK sender for the Raspberry Pi
- IR files (`.ir`) into LIRC remote files (`lircd.conf`)

Inputs and outputs are separate, so further formats and the way back to the Flipper Zero can be added.

> Work in progress: the project structure is in place, the functionality follows.

## Documentation

- [Inputs](docs/inputs.md)
- [Outputs](docs/outputs.md)
- [Extensions](docs/extensions.md)
- [Development](docs/development.md)

## License

MIT, see [LICENSE](LICENSE).
