from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget

BAR_WIDTH = 1.5
BAR_HEIGHT = 45.0
TEXT_Y = -50
BARCODE_Y = -100

LABEL_WIDTH = 150
LABEL_HEIGHT = 70

def label(ean13: str, description: str) -> Drawing:
    """
    Generate a drawing with EAN-13 barcode and descriptive text.
    :param ean13: The EAN-13 Code.
    :type ean13: str
    :param description: Short product description.
    :type description: str
    :return: Drawing with barcode and description
    :rtype: Drawing
    """
    text = String(0, TEXT_Y, description, fontName="Helvetica",
                  fontSize=10, textAnchor="middle")
    text.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)

    barcode = Ean13BarcodeWidget(ean13)
    barcode.barWidth = BAR_WIDTH
    barcode.barHeight = BAR_HEIGHT
    x0, y0, bw, bh = barcode.getBounds()
    barcode.x = (LABEL_WIDTH - bw) / 2  # center barcode
    barcode.y = BARCODE_Y  # spacing from label bottom (pt)

    label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
    label_drawing.add(text)
    label_drawing.add(barcode)
    return label_drawing