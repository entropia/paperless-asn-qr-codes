# paperless-asn-qr-codes

`paperless-asn-qr-codes` is a command line utility for generating ASN labels
for paperless with both a human readable representation, as well as a QR code
for machine consumption. The labels are Avery 4731 labels.

## Installation

```console
pip install paperless-asn-qr-codes
```

## Supported Sheets
Some different sheet types are supported with the `--format` argument, however, not all are tested.

Default is Avery L4731.

Currently tested and known working are:
- Avery L4731 (DIN A4 Labels)

## Tips & Tricks

In case your printer has alignment issues, you can generate a PDF with borders around the labels by using the
`--border` option.

## License

`paperless-asn-qr-codes` is distributed under the terms of the
[GPL-3.0](https://spdx.org/licenses/GPL-3.0.html) license.
