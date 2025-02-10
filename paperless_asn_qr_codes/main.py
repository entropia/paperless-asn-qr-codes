""" Main module for the paperless ASN QR code generator, fills the labels with content """
import argparse
import re

from paperless_asn_qr_codes import label_sheet, label

def main():
    """ Main function for the paperless ASN QR code generator """
    # Match the starting position parameter. Allow x:y or n
    def _start_position(arg):
        if mat := re.match(r"^(\d{1,2}):(\d{1,2})$", arg):
            return (int(mat.group(1)), int(mat.group(2)))
        if mat := re.match(r"^\d+$", arg):
            return int(arg)
        raise argparse.ArgumentTypeError("invalid value")

    # prepare a sorted list of all formats
    available_formats = list(label_sheet.labelSheetInfo.keys())
    available_formats.sort()

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
        "--format", "-f", choices=available_formats, default="averyL4731"
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
        help="""Define the starting position on the sheet,
                eighter as ROW:COLUMN or COUNT, both starting from 1 (default: 1:1 or 1)""",
    )

    args = parser.parse_args()
    start_asn = int(args.start_asn)
    digits = int(args.digits)
    # TODO: set digits to LabelInfo

    # setup LabelSheet
    sheet = label_sheet.LabelSheet(
        args.format, args.border, topDown=args.row_wise, start_pos=args.start_position
    )
    sheet.open(args.output_file)

    # setup LabelRenderer with Label
    l = label.Label(start_asn)

    # If defined use parameter for number of labels
    if args.num_labels:
        count = args.num_labels
    else:
        # Otherwise number of pages*labels - offset
        count = args.pages * sheet.across * sheet.down - sheet.position
    sheet.render(l.render, count)
    sheet.close()
