"""This module provides classes for building a single paperless ASN label with a given layout."""
from dataclasses import dataclass, KW_ONLY
from reportlab.lib.units import mm
from reportlab_qrcode import QRCodeImage

@dataclass
class LabelInfo:
    """Class for modeling label sheet info"""

    _: KW_ONLY
    digits: int

class Label:
    """Class for building the label"""

    def __init__(self, start_asn):
        self.current = start_asn

    def render(self, canvas, x_size, y_size):
        barcode_value = f"ASN{self.current:0{7}d}"

        qr = QRCodeImage(barcode_value, size=y_size * 0.9)
        qr.drawOn(canvas, 1 * mm, y_size* 0.05)
        canvas.setFont("Helvetica", 2 * mm)
        canvas.drawString(y_size, (y_size - 2 * mm) / 2, barcode_value)
        self.current += 1
