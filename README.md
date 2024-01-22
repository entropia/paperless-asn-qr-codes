# paperless-asn-qr-codes

`paperless-asn-qr-codes` is a command line utility for generating ASN labels
for paperless with both a human-readable representation, as well as a QR code
for machine consumption. The labels are Avery 4731 labels.

## Installation

```console
pip install paperless-asn-qr-codes
```

## Usage

```
usage: paperless-asn-qr-codes [-h] [--format {averyL4731,avery5160,avery5161,avery5163,avery5167,avery5371}] [--border] start_asn output_file

CLI Tool for generating paperless ASN labels with QR codes

positional arguments:
  start_asn             The value of the first ASN
  output_file           The output file to write to (default: labels.pdf)

options:
  -h, --help            show this help message and exit
  --format {averyL4731,avery5160,avery5161,avery5163,avery5167,avery5371}, -f {averyL4731,avery5160,avery5161,avery5163,avery5167,avery5371}
  --border, -b          Display borders around labels, useful for debugging the printer alignment
```

### Mandatory arguments

- `<start_asn>`: The value of the first ASN to generate

### Optional arguments

- `<output_file>`: The name of the output file to write to (default: labels.pdf)

---

- `-h`, `--help`: Shows the help message
- `-f`, `--format`: Selects the format of the output sheet (see [Supported Sheets](#supported-sheets))
- `-b`, `--border`: Generates the borders around the labels to help debug alignment issues (see [Tips & Tricks](#tips--tricks))

## Supported Sheets
Some different sheet types are supported with the `-f`/`--format` argument, however, not all are tested.

The default is Avery L4731.

Currently tested and known working are:
- Avery L4731 (DIN A4 Labels)

## Tips & Tricks

In case your printer has alignment issues, you can generate a PDF with borders around the labels by using the
`-b`/`--border` option.

## License

`paperless-asn-qr-codes` is distributed under the terms of the
[GPL-3.0](https://spdx.org/licenses/GPL-3.0.html) license.
