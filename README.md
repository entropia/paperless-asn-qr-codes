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
usage: paperless-asn-qr-codes [-h] [--format {averyL4731,avery5160,avery5161,avery5163,avery5167,avery5371}] [--digits DIGITS] [--border] [--row-wise] [--num-labels NUM_LABELS] [--pages PAGES]
                              [--start-position START_POSITION]
                              start_asn output_file

CLI Tool for generating paperless ASN labels with QR codes

positional arguments:
  start_asn             The value of the first ASN
  output_file           The output file to write to (default: labels.pdf)

options:
  -h, --help            show this help message and exit
  --format {averyL4731, averyL6026, avery5160,avery5161,avery5163,avery5167,avery5371}, -f {averyL4731,avery5160,avery5161,avery5163,avery5167,avery5371}
  --digits DIGITS, -d DIGITS
                        Number of digits in the ASN (default: 7, produces 'ASN0000001')
  --border, -b          Display borders around labels, useful for debugging the printer alignment
  --row-wise, -r        Increment the ASNs row-wise, go from left to right
  --num-labels NUM_LABELS, -n NUM_LABELS
                        Number of labels to be printed on the sheet
  --pages PAGES, -p PAGES
                        Number of pages to be printed, ignored if NUM_LABELS is set (default: 1)
  --start-position START_POSITION, -s START_POSITION
                        Define the starting position on the sheet, eighter as ROW:COLUMN or COUNT, both starting from 1 (default: 1:1 or 1)
```

### Mandatory arguments

- `<start_asn>`: The value of the first ASN to generate

### Optional arguments

- `<output_file>`: The name of the output file to write to (default: labels.pdf)

---

- `-h`, `--help`: Shows the help message
- `-f`, `--format`: Selects the format of the output sheet (see [Supported Sheets](#supported-sheets))
- `-d`, `--digits`: Specifies the number of digits in the ASN (e.g. for the default number 7, the ASN will look like 'ASN0000001')
- `-b`, `--border`: Generates the borders around the labels to help debug alignment issues (see [Tips & Tricks](#tips--tricks))
- `-r`, `--row-wise`: Increments the labels from left to right instead of top to bottom
- `-n`, `--num-labels`: Number of lables to be printed on the sheet
- `-p`, `--pages`: Number of pages to be generated, ignored if -n is present.
- `-s`, `--start-position`: Positon of first label to be printed, eighter defined as ROW:COLUMN or NUMBER. Starting from 1 eg. to use the whole sheet it would be 1:1 or 1. Useful if you have a partly used sheet from using `-n`.
- `-l`, `--line-break`: Break line after ASN and display number in new line (default `false`)
- `-z`, `--size`: Font size for the printed number (default 2 mm)

## Supported Sheets
Some different sheet types are supported with the `-f`/`--format` argument, however, not all are tested.

The default is Avery L4731.

Currently tested and known working are:
- Avery L4731 (DIN A4 Labels)
- Avery L6026 (DIN A4 Labels)

## Tips & Tricks

In case your printer has alignment issues, you can generate a PDF with borders around the labels by using the
`-b`/`--border` option.

## License

`paperless-asn-qr-codes` is distributed under the terms of the
[GPL-3.0](https://spdx.org/licenses/GPL-3.0.html) license.
