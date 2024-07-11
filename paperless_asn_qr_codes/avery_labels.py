from dataclasses import dataclass, KW_ONLY
from collections.abc import Iterator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.lib.units import mm, inch


# Usage:
#   label = AveryLabels.AveryLabel(5160)
#   label.open( "labels5160.pdf" )
#   label.render( RenderAddress, 30 )
#   label.close()
#
# 'render' can either pass a callable, which receives the canvas object
# (with X,Y=0,0 at the lower right) or a string "form" name of a form
# previously created with canv.beginForm().


@dataclass
class LabelInfo:
    """Class for modeling label info"""

    _: KW_ONLY
    labels_horizontal: int
    labels_vertical: int
    label_size: tuple[float, float]
    gutter_size: tuple[float, float]
    margin: tuple[float, float]
    pagesize: tuple[float, float]
    textsize: float


labelInfo: dict[str, LabelInfo] = {
    "averyL4731": LabelInfo(
        labels_horizontal=7,
        labels_vertical=27,
        label_size=(25.4 * mm, 10 * mm),
        gutter_size=(2.5 * mm, 0),
        margin=(9 * mm, 13.5 * mm),
        pagesize=A4,
        textsize=2 * mm,
    ),
    # 2.6 x 1 address labels
    "avery5160": LabelInfo(
        labels_horizontal=3,
        labels_vertical=10,
        label_size=(187, 72),
        gutter_size=(11, 0),
        margin=(14, 36),
        pagesize=LETTER,
        textsize=2 * mm,
    ),
    "avery5161": LabelInfo(
        labels_horizontal=2,
        labels_vertical=10,
        label_size=(288, 72),
        gutter_size=(0, 0),
        margin=(18, 36),
        pagesize=LETTER,
        textsize=2 * mm,
    ),
    # 4 x 2 address labels
    "avery5163": LabelInfo(
        labels_horizontal=2,
        labels_vertical=5,
        label_size=(288, 144),
        gutter_size=(0, 0),
        margin=(18, 36),
        pagesize=LETTER,
        textsize=2 * mm,
    ),
    # 1.75 x 0.5 return address labels
    "avery5167": LabelInfo(
        labels_horizontal=4,
        labels_vertical=20,
        label_size=(1.75 * inch, 0.5 * inch),
        gutter_size=(0.3 * inch, 0),
        margin=(0.3 * inch, 0.5 * inch),
        pagesize=LETTER,
        textsize=2 * mm,
    ),
    # 3.5 x 2 business cards
    "avery5371": LabelInfo(
        labels_horizontal=2,
        labels_vertical=5,
        label_size=(252, 144),
        gutter_size=(0, 0),
        margin=(54, 36),
        pagesize=LETTER,
        textsize=2 * mm,
    ),
    # generic uncut A4 label paper
    # (slightly larger for bad scanners & printers)
    "genericA4large": LabelInfo(
        labels_horizontal=5,
        labels_vertical=14,
        label_size=(40 * mm, 20 * mm),
        gutter_size=(0 * mm, 0),
        margin=(5 * mm, 4 * mm),
        pagesize=A4,
        textsize=3 * mm,
    )
}

RETURN_ADDRESS = 5167
BUSINESS_CARDS = 5371


class AveryLabel:
    def __init__(self, label, debug,
                 topDown=True, start_pos=None,
                 **kwargs):
        data = labelInfo[label]
        self.across = data.labels_horizontal
        self.down = data.labels_vertical
        self.size = data.label_size
        self.textsize = data.textsize
        self.labelsep = (
            self.size[0] + data.gutter_size[0],
            self.size[1] + data.gutter_size[1],
        )
        self.margins = data.margin
        self.topDown = topDown
        self.debug = debug
        self.pagesize = data.pagesize

        #Calculate start offset
        if isinstance(start_pos, tuple):
            rows, columns = start_pos
            # Minimum Value 1 for row/column
            rows = max(rows, 1)
            columns = max(columns, 1)
            if self.topDown:
                offset = (columns - 1) * self.down + rows - 1
            else:
                offset = (rows - 1) * self.across + columns - 1
        elif start_pos:
            offset = start_pos - 1
        else:
            offset = 0
        # Limit start position to number of labels - 1
        self.position = min(offset,  self.across * self.down - 1)

        self.__dict__.update(kwargs)

    def open(self, filename):
        self.canvas = canvas.Canvas(filename, pagesize=self.pagesize)
        if self.debug:
            self.canvas.setPageCompression(0)
        self.canvas.setLineJoin(1)
        self.canvas.setLineCap(1)

    def topLeft(self, x=None, y=None):
        if x is None:
            x = self.position
        if y is None:
            if self.topDown:
                x, y = divmod(x, self.down)
            else:
                y, x = divmod(x, self.across)

        return (
            self.margins[0] + x * self.labelsep[0],
            self.pagesize[1] - self.margins[1] - (y + 1) * self.labelsep[1],
        )

    def advance(self):
        self.position += 1
        if self.position == self.across * self.down:
            self.canvas.showPage()
            self.position = 0

    def close(self):
        if self.position:
            self.canvas.showPage()
        self.canvas.save()
        self.canvas = None

    # To render, you can either create a template and tell me
    # "go draw N of these templates" or provide a callback.
    # Callback receives canvas, width, height.
    #
    # Or, pass a callable and an iterator.  We'll do one label
    # per iteration of the iterator.

    def render(self, thing, count, *args):
        assert callable(thing) or isinstance(thing, str)
        if isinstance(count, Iterator):
            return self.render_iterator(thing, count)

        canv = self.canvas
        for i in range(count):
            canv.saveState()
            canv.translate(*self.topLeft())
            if self.debug:
                canv.setLineWidth(0.25)
                canv.rect(0, 0, self.size[0], self.size[1])
            if callable(thing):
                thing(canv, self.size[0], self.size[1], self.textsize, *args)
            elif isinstance(thing, str):
                canv.doForm(thing)
            canv.restoreState()
            self.advance()

    def render_iterator(self, func, iterator):
        canv = self.canvas
        for chunk in iterator:
            canv.saveState()
            canv.translate(*self.topLeft())
            if self.debug:
                canv.setLineWidth(0.25)
                canv.rect(0, 0, self.size[0], self.size[1])
            func(canv, self.size[0], self.size[1], self.textsize, chunk)
            canv.restoreState()
            self.advance()
