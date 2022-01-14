import datetime
from reportlab.lib import utils
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, TableStyle, Paragraph, Image, Spacer, Frame, Paragraph
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from barcode import label

pdfmetrics.registerFont(TTFont('jf', "./data/fonts/jf-openhuninn.ttf"))

def getwebdetail(webtitle):
    if webtitle == "夢玩家包車旅遊":
        url = "https://www.taiwantourcar.com/"
        detail = "寶島之旅，最佳夥伴。"
        logo = "./data/logo/01.png"
        color = "#ffb606"
    elif webtitle == "九賓商務租車":
        url = "https://www.jobincar.com/"
        detail = "商務包車 | 各式接送 | 包車旅遊"
        logo = "./data/logo/02.png"
        color = "#db9423"
    elif webtitle == "天地玩家包車旅遊":
        url = "https://skytour.tw/"
        detail = "包車旅遊、機場接送、包車自由行"
        logo = "./data/logo/03.jpg"
        color = "#e7483c"
    elif webtitle == "海山林玩家包車旅遊":
        url = "https://www.ctplayer.com/"
        detail = "想要來東部旅行？請交給在地的 海山林玩家包車旅遊！"
        logo = "./data/logo/04.png"
        color = "#0079a3"
    elif webtitle == "天地遊覽車":
        url = "https://skybus.tw/"
        detail = "完整透明的評價、最合理的遊覽車價格！"
        logo = "./data/logo/05.png"
        color = "#d4af37"
    return url, detail, logo, color

def get_image(path, width=200):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def html2pdf(row, varstr):
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    width, height = A4
    elements = []

    im = get_image(getwebdetail(varstr)[2], width=150)
    im.hAlign = 'LEFT'

    titlestyle = ParagraphStyle(
        name='titlestyle',
        fontName='jf',
        alignment=TA_CENTER,
        fontSize=16
    )
    insidestyle = ParagraphStyle(
        name='insidestyle',
        fontName='jf',
        fontSize=10
    )
    doctorstyle = ParagraphStyle(
        name='MyDoctorHeader',
        fontName='jf',
        fontSize=13,
        leading=10
    )
    normalstyle = ParagraphStyle(
        name='nomalstyle',
        fontName='jf'
    )
    declare = Paragraph(f"{varstr}預訂用車確認書", style=titlestyle)
    elements.append(declare)
    elements.append(Spacer(1, 40))
    line1 = ("貴賓", "", "")
    line2 = ("", row[4], row[5])
    data = [line1, line2]

    title = [[Paragraph(getwebdetail(varstr)[0], style=normalstyle)], [Paragraph(getwebdetail(varstr)[1], style=doctorstyle)]]
    patientdetailstable = Table(title)

    col1 = Table([[im]])
    col2 = Table(data, repeatRows=1)
    col2.setStyle(
        TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'jf')
        ]))

    tblrow1 = Table([[col1, f"[ {row[0]} ]\n"], [patientdetailstable, col2]], colWidths=None)
    tblrow1.setStyle(
        TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
    elements.append(tblrow1)


    elements.append(Spacer(1, 20))
    # We use paragraph style because we need to wrap text. We cant directly wrap cells otherwise
    line1 = ["#", "行程內容", "上車位置", "下車位置", "車款", "出發日期"]
    line2 = ["1", Paragraph(row[11], style=insidestyle), Paragraph(row[9], style=insidestyle), Paragraph(row[10], style=insidestyle), Paragraph(row[8], style=insidestyle), row[2]]
    line3 = ["2", "", "", "", "", ""]
    data = [line1, line2, line3]
    for i in range(3, 5):
        temp = [str(i), "", "", "", "", ""]
        data.append(temp)

    medstable = Table(data, repeatRows=1, colWidths=[0.3*inch, 5.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
    medstable.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), getwebdetail(varstr)[3]),
        ('GRID', (0, 1), (-1, -1), 0.5, '#cccccc'),
        ('FONTNAME', (0, 0), (-1, -1), 'jf')
    ]))
    elements.append(medstable)
    elements.append(Spacer(1, 20))

    line3 = ("", "總金額:", row[12])
    line4 = ("", "訂金:", row[13])
    data = [line3, line4]
    col4 = Table(data, repeatRows=1, hAlign='RIGHT')
    col4.setStyle(
        TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'jf'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
    elements.append(col4)
    printtimenow = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' ' + row[1]

    sticker = label(row[0], printtimenow)
    elements.append(sticker)


    doc = SimpleDocTemplate(f'./output/{row[0]}.pdf', pagesize=landscape(A4), rightMargin=30, leftMargin=30, \
                            topMargin=40, bottomMargin=20, allowSplitting=0, \
                            title="", author="九賓旅遊資訊社")

    doc.build(elements)