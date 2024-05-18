import argparse

from reportlab.lib.units import mm
from reportlab_qrcode import QRCodeImage

from paperless_asn_qr_codes import avery_labels


def render(c, x, y):
    global startASN
    global digits
    barcode_value = f"ASN{startASN:0{digits}d}"
    startASN = startASN + 1

    qr = QRCodeImage(barcode_value, size=y * 0.9)
    qr.drawOn(c, 1 * mm, y * 0.05)
    c.setFont("Helvetica", 2 * mm)
    c.drawString(y, (y - 2 * mm) / 2, barcode_value)


def main():
    parser = argparse.ArgumentParser(
        prog="paperless-asn-qr-codes",
        description="CLI Tool for generating paperless ASN labels with QR codes",
    )
    parser.add_argument("start_asn", type=int, help="The value of the first ASN")
    parser.add_argument(
        "output_file",
        type=str,
        default="labels.pdf",
        help="The output file to write to (default: labels.pdf)",
    )
    parser.add_argument(
        "--format", "-f", choices=avery_labels.labelInfo.keys(), default="averyL4731"
    )
    parser.add_argument(
        "--digits",
        "-d",
        default=7,
        help="Number of digits in the ASN (default: 7, produces 'ASN0000001')",
        type=int,
    )
    parser.add_argument(
        "--border",
        "-b",
        action="store_true",
        help="Display borders around labels, useful for debugging the printer alignment",
    )
    args = parser.parse_args()
    global startASN
    global digits
    startASN = int(args.start_asn)
    digits = int(args.digits)
    label = avery_labels.AveryLabel(args.format, args.border)
    label.open(args.output_file)
    # by default, we render all labels possible on a single sheet
    count = (
        avery_labels.labelInfo[args.format].labels_horizontal
        * avery_labels.labelInfo[args.format].labels_vertical
    )
    label.render(render, count)
    label.close()
