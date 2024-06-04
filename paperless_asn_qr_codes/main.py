import argparse
import re

from reportlab.lib.units import mm
from reportlab_qrcode import QRCodeImage

from paperless_asn_qr_codes import avery_labels


def render(c, x, y):
    global startASN
    global digits
    global prefix
    global omit_prefix
    barcode_value = f"{startASN:0{digits}d}"
    startASN = startASN + 1
    splitting = split_at
    qr = QRCodeImage(f"{prefix}{barcode_value}", size=y *
                     qr_scale_factor, border=qr_border_size)
    qr.drawOn(c, 1 * mm, y * 0.05)
    if omit_prefix:
        c.setFont("Helvetica", 3.5 * mm)
        c.drawString(y, (y - 2 * mm) / 2,
                     format_number(barcode_value, splitting))
    else:
        c.setFont("Helvetica", 2 * mm)
        c.drawString(y, (y - 2 * mm) / 2,
                     f"{prefix}{format_number(barcode_value, splitting)}")


def format_number(s, positions):
    # Create a list to store the parts of the string
    parts = []
    start = 0

    # Loop through each position where you want to split the string
    for pos in positions:
        parts.append(s[start:pos])
        start = pos

    # Add the remaining part of the string after the last position
    parts.append(s[start:])

    # Join all parts together with a space in between each part
    return ' '.join(parts)


def main():
    # Match the starting position parameter. Allow x:y or n
    def _start_position(arg):
        if mat := re.match(r"^(\d{1,2}):(\d{1,2})$", arg):
            return (int(mat.group(1)), int(mat.group(2)))
        elif mat := re.match(r"^\d+$", arg):
            return int(arg)
        else:
            raise argparse.ArgumentTypeError("invalid value")

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
    parser.add_argument(
        "--row-wise",
        "-r",
        action="store_false",
        help="Increment the ASNs row-wise, go from left to right",
    )
    parser.add_argument(
        "--num-labels",
        "-n",
        type=int,
        help="Number of labels to be printed on the sheet",
    )
    parser.add_argument(
        "--pages",
        "-p",
        type=int,
        default=1,
        help="Number of pages to be printed, ignored if NUM_LABELS is set (default: 1)",
    )
    parser.add_argument(
        "--start-position",
        "-s",
        type=_start_position,
        help="Define the starting position on the sheet, eighter as ROW:COLUMN or COUNT, both starting from 1 (default: 1:1 or 1)",
    )
    parser.add_argument(
        "--prefix", "-P", default="ASN", help="Prefix in front of digits (default: ASN)", type=str
    )
    parser.add_argument(
        "--omit-prefix", action="store_true", help="Do not print prefix in front of digits"
    )
    parser.add_argument(
        "--x-offset", "-x", default=0, help="Horizontal (X) offset in mm (default: 0)", type=float
    )
    parser.add_argument(
        "--y-offset", "-y", default=0, help="Vertical (Y) offset in mm (default: 0)", type=float
    )
    parser.add_argument(
        "--qr-scale-factor", default=0.9, help="Scale Factor of QR code (default: 0.9)", type=float
    )
    parser.add_argument(
        "--qr-border-size", default=4, help="Size of white border around QR code (default: 4)", type=float
    )
    parser.add_argument(
        "--split-at", default=[], help="visually split number at digit. multiple allowed (default: mo splitting)", type=int, action='append'
    )

    args = parser.parse_args()
    global startASN
    global digits
    global prefix
    global omit_prefix
    global qr_scale_factor
    global qr_border_size
    global split_at
    startASN = int(args.start_asn)
    digits = int(args.digits)
    prefix = args.prefix
    omit_prefix = args.omit_prefix
    qr_scale_factor = args.qr_scale_factor
    qr_border_size = args.qr_border_size
    split_at = args.split_at
    print(split_at)

    label = avery_labels.AveryLabel(
        args.format, args.border, topDown=args.row_wise, start_pos=args.start_position
    )
    label.open(args.output_file)

    # If defined use parameter for number of labels
    if args.num_labels:
        count = args.num_labels
    else:
        # Otherwise number of pages*labels - offset
        count = args.pages * label.across * label.down - label.position
    label.margins = (label.margins[0] + args.x_offset *
                     mm, label.margins[1] + args.y_offset * mm)
    label.render(render, count)
    label.close()
