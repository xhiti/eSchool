from django.http import FileResponse
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import Image, Spacer
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from datetime import date
import os
from io import StringIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial Narrow', 'arialn.ttf'))
pdfmetrics.registerFont(TTFont('Arial Narrow-Bold', 'arialnb.ttf'))



class PrintStatistics8E:

    @staticmethod
    def print8EStatisticFullYear(grades):
        file_name = 'Statistika Vjetore Klasa VIII-E.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4, title='Statistika Vjetore Klasa VIII-E ' + str(datetime.now().year))

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=13,
            parent=styles['BodyText'],
            alignment=1,
        )

        title_style_2 = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=1,
        )

        footer_title = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=2,
        )

        left_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        table_head_2 = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), .25, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Arial Narrow', 11),
            ('TOPPADDING', (0, 0), (-1, -1), 4.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'VCENTER')
        ])

        # ============================= #
        #          CONSTANTS            #
        # ============================= #
        # Spaces
        DEAFULT_SPACE_WIDTH = 0.1 * inch
        DEAFULT_SPACE_HEIGHT = 0.1 * inch
        SPACE_WIDTH_FOOTER = 0.4 * inch
        SPACE_HEIGHT_FOOTER = 0.4 * inch

        # ELEMENTS POSITIONS
        # Frame position
        FRAME_X = doc.leftMargin / 2
        FRAME_Y = doc.bottomMargin / 2
        FRAME_WIDTH = doc.width + doc.leftMargin
        FRAME_HEIGHT = doc.height + doc.bottomMargin - 20

        # Header line position
        HEADER_LINE_X1 = doc.leftMargin / 2
        HEADER_LINE_Y1 = doc.height + doc.topMargin + 25
        HEADER_LINE_X2 = doc.width + 1.5 * doc.leftMargin
        HEADER_LINE_Y2 = HEADER_LINE_Y1

        # Footer line position
        FOOTER_LINE_X1 = HEADER_LINE_X1
        FOOTER_LINE_Y1 = doc.bottomMargin / 2 + 5
        FOOTER_LINE_X2 = HEADER_LINE_X2
        FOOTER_LINE_Y2 = FOOTER_LINE_Y1

        # Serial Number position
        SERIAL_NUMBER_X = HEADER_LINE_X1 + doc.width + doc.rightMargin
        SERIAL_NUMBER_Y = HEADER_LINE_Y1 + 5

        # Institution position
        INSTITUTION_X = HEADER_LINE_X1
        INSTITUTION_Y = HEADER_LINE_Y1 + 5

        # Page Number position
        PAGE_NUMBER_X = FOOTER_LINE_X1 + doc.width + doc.rightMargin
        PAGE_NUMBER_Y = FOOTER_LINE_Y1 - 10

        # Printed Date position
        PRINTED_DATE_X = FOOTER_LINE_X1
        PRINTED_DATE_Y = FOOTER_LINE_Y1 - 10

        # PDF Header (same for all pages)
        def header(canvas, doc):
            canvas.line(HEADER_LINE_X1, HEADER_LINE_Y1, HEADER_LINE_X2, HEADER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            text_serial = "Vlerësimi i nxënësve VIII-E " + str(datetime.now().year)
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, 'Shkolla 9-vjeçare "Azem Hajdari"')

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            current_date = datetime.now()
            day = str(current_date.day)
            month = str(current_date.month)
            year = str(current_date.year)
            text_printed_date = "Lënda: Gjuhë Shqipe"
            canvas.drawString(PRINTED_DATE_X, PRINTED_DATE_Y, text_printed_date)
            text_page_number = "Drita Kurti"
            canvas.drawRightString(PAGE_NUMBER_X, PAGE_NUMBER_Y, text_page_number)

        # FRAME
        full_page_frame = Frame(
            FRAME_X,
            FRAME_Y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            id='normal',
            showBoundary=0
        )

        # TABLE DATAS

        header_data = [
            [
                Paragraph(str("<b>Nr.</b>"), table_head),
                Paragraph(str("<b>Emri</b>"), table_head),
                Paragraph(str("<b>Mbiemri</b>"), table_head),
                Paragraph(str("<b>Periudha 1</b>"), table_head),
                Paragraph(str("<b>Periudha 2</b>"), table_head),
                Paragraph(str("<b>Periudha 3</b>"), table_head),
                Paragraph(str("<b>Mes</b>"), table_head),
                Paragraph(str("<b>Nota</b>"), table_head)
            ]
        ]

        extended_header_data = [
            [
                Paragraph(str(""), table_head),
                Paragraph(str(""), table_head),
                Paragraph(str(""), table_head),
                Paragraph(str("<b>VLV</b>"), table_head_2),
                Paragraph(str("<b>VLP</b>"), table_head_2),
                Paragraph(str("<b>VLT</b>"), table_head_2),
                Paragraph(str("<b>VLV</b>"), table_head_2),
                Paragraph(str("<b>VLP</b>"), table_head_2),
                Paragraph(str("<b>VLT</b>"), table_head_2),
                Paragraph(str("<b>VLV</b>"), table_head_2),
                Paragraph(str("<b>VLP</b>"), table_head_2),
                Paragraph(str("<b>VLT</b>"), table_head_2),
                Paragraph(str(""), table_head),
                Paragraph(str(""), table_head)
            ]
        ]

        albanian_language_data = []
        listNumber = 0

        for grade in grades:
            if grade.continuous_grade_p1 == 0:
                grade.continuous_grade_p1 = ""
            if grade.continuous_grade_p2 == 0:
                grade.continuous_grade_p2 = ""
            if grade.continuous_grade_p3 == 0:
                grade.continuous_grade_p3 = ""
            if grade.project_grade_p1 == 0:
                grade.project_grade_p1 = ""
            if grade.project_grade_p2 == 0:
                grade.project_grade_p2 = ""
            if grade.project_grade_p3 == 0:
                grade.project_grade_p3 = ""
            if grade.test_grade_p1 == 0:
                grade.test_grade_p1 = ""
            if grade.test_grade_p2 == 0:
                grade.test_grade_p2 = ""
            if grade.test_grade_p3 == 0:
                grade.test_grade_p3 = ""

            listNumber += 1

            albanian_language_data.append(
                [
                    Paragraph(str(listNumber), left_light),
                    Paragraph(str(grade.student.name), left_light),
                    Paragraph(str(grade.student.surname), left_light),
                    Paragraph(str(grade.continuous_grade_p1), center_light),
                    Paragraph(str(grade.project_grade_p1), center_light),
                    Paragraph(str(grade.test_grade_p1), center_light),
                    Paragraph(str(grade.continuous_grade_p2), center_light),
                    Paragraph(str(grade.project_grade_p2), center_light),
                    Paragraph(str(grade.test_grade_p2), center_light),
                    Paragraph(str(grade.continuous_grade_p3), center_light),
                    Paragraph(str(grade.project_grade_p3), center_light),
                    Paragraph(str(grade.test_grade_p3), center_light),
                    Paragraph(str(""), center_light),
                    Paragraph(str(""), center_light)
            ])

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("<b>STATISTIKË VJETORE</b>", title_style))
        elements.append(Paragraph("<b> KLASA VIII-E</b>", title_style_2))
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                header_data,
                style=order_details_table_style,
                colWidths=[0.4 * inch, 1 * inch, 1 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 0.7 * inch, 0.7 * inch]
            )
        )
        elements.append(
            Table(
                extended_header_data,
                style=order_details_table_style,
                colWidths=[0.4 * inch, 1 * inch, 1 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch,
                           0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.7 * inch, 0.7 * inch]
            )
        )
        elements.append(
            Table(
                albanian_language_data,
                style=order_details_table_style,
                colWidths=[0.4 * inch, 1 * inch, 1 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch,
                           0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch, 0.7 * inch, 0.7 * inch]
            )
        )
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("Mësuesja: Drita Kurti", footer_title))

        doc.addPageTemplates([
            PageTemplate(id='StatisticDetailsFullYear', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response


    @staticmethod
    def print8EStatisticFirstPeriod():
        file_name = 'Statistika Periudha 1 Klasa VIII-E.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4,
                              title='Statistika Periudha 1 Klasa VIII-E ' + str(datetime.now().year))

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=13,
            parent=styles['BodyText'],
            alignment=1,
        )

        footer_title = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=2,
        )

        left_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), .25, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Arial Narrow', 12,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        # ============================= #
        #          CONSTANTS            #
        # ============================= #
        # Spaces
        DEAFULT_SPACE_WIDTH = 0.1 * inch
        DEAFULT_SPACE_HEIGHT = 0.1 * inch
        SPACE_WIDTH_FOOTER = 0.4 * inch
        SPACE_HEIGHT_FOOTER = 0.4 * inch

        # ELEMENTS POSITIONS
        # Frame position
        FRAME_X = doc.leftMargin / 2
        FRAME_Y = doc.bottomMargin / 2
        FRAME_WIDTH = doc.width + doc.leftMargin
        FRAME_HEIGHT = doc.height + doc.bottomMargin - 20

        # Header line position
        HEADER_LINE_X1 = doc.leftMargin / 2
        HEADER_LINE_Y1 = doc.height + doc.topMargin + 25
        HEADER_LINE_X2 = doc.width + 1.5 * doc.leftMargin
        HEADER_LINE_Y2 = HEADER_LINE_Y1

        # Footer line position
        FOOTER_LINE_X1 = HEADER_LINE_X1
        FOOTER_LINE_Y1 = doc.bottomMargin / 2 + 5
        FOOTER_LINE_X2 = HEADER_LINE_X2
        FOOTER_LINE_Y2 = FOOTER_LINE_Y1

        # Serial Number position
        SERIAL_NUMBER_X = HEADER_LINE_X1 + doc.width + doc.rightMargin
        SERIAL_NUMBER_Y = HEADER_LINE_Y1 + 5

        # Institution position
        INSTITUTION_X = HEADER_LINE_X1
        INSTITUTION_Y = HEADER_LINE_Y1 + 5

        # Page Number position
        PAGE_NUMBER_X = FOOTER_LINE_X1 + doc.width + doc.rightMargin
        PAGE_NUMBER_Y = FOOTER_LINE_Y1 - 10

        # Printed Date position
        PRINTED_DATE_X = FOOTER_LINE_X1
        PRINTED_DATE_Y = FOOTER_LINE_Y1 - 10

        # PDF Header (same for all pages)
        def header(canvas, doc):
            canvas.line(HEADER_LINE_X1, HEADER_LINE_Y1, HEADER_LINE_X2, HEADER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            text_serial = "Statistika Klasa VIII-E " + str(datetime.now().year)
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, 'Shkolla 9-vjeçare "Azem Hajdari"')

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            current_date = datetime.now()
            day = str(current_date.day)
            month = str(current_date.month)
            year = str(current_date.year)
            text_printed_date = "Krijuar më datë: " + str(day + "/" + month + "/" + year)
            canvas.drawString(PRINTED_DATE_X, PRINTED_DATE_Y, text_printed_date)
            text_page_number = "Fq. " + str(doc.page)
            canvas.drawRightString(PAGE_NUMBER_X, PAGE_NUMBER_Y, text_page_number)

        # FRAME
        full_page_frame = Frame(
            FRAME_X,
            FRAME_Y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            id='normal',
            showBoundary=0
        )

        # TABLE DATAS

        header_data = [
            [
                Paragraph(str("<b>Nr.</b>"), table_head),
                Paragraph(str("<b>Emri</b>"), table_head),
                Paragraph(str("<b>Mbiemri</b>"), table_head),
                Paragraph(str("<b>VLV</b>"), table_head),
                Paragraph(str("<b>VLP</b>"), table_head),
                Paragraph(str("<b>VLT</b>"), table_head),
                Paragraph(str("<b>Shënime</b>"), table_head)
            ]
        ]

        albanian_language_data = []

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("<b>STATISTIKË PERIUDHA 1 KLASA VIII-E</b>", title_style))


        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                header_data,
                style=order_details_table_style,
                colWidths=[0.5 * inch, 1.5 * inch, 1.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 1 * inch]
            )
        )
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(Paragraph("Lënda: Gjuhë Shqipe", footer_title))
        elements.append(Paragraph("Mësuesja: Drita Kurti", footer_title))

        doc.addPageTemplates([
            PageTemplate(id='StatisticDetailsFirstPeriod', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response


    @staticmethod
    def print8EStatisticSecondPeriod():
        file_name = 'Statistika Periudha 2 Klasa VIII-E.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4,
                              title='Statistika Periudha 2 Klasa VIII-E ' + str(datetime.now().year))

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=13,
            parent=styles['BodyText'],
            alignment=1,
        )

        footer_title = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=2,
        )

        left_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), .25, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Arial Narrow', 12,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        # ============================= #
        #          CONSTANTS            #
        # ============================= #
        # Spaces
        DEAFULT_SPACE_WIDTH = 0.1 * inch
        DEAFULT_SPACE_HEIGHT = 0.1 * inch
        SPACE_WIDTH_FOOTER = 0.4 * inch
        SPACE_HEIGHT_FOOTER = 0.4 * inch

        # ELEMENTS POSITIONS
        # Frame position
        FRAME_X = doc.leftMargin / 2
        FRAME_Y = doc.bottomMargin / 2
        FRAME_WIDTH = doc.width + doc.leftMargin
        FRAME_HEIGHT = doc.height + doc.bottomMargin - 20

        # Header line position
        HEADER_LINE_X1 = doc.leftMargin / 2
        HEADER_LINE_Y1 = doc.height + doc.topMargin + 25
        HEADER_LINE_X2 = doc.width + 1.5 * doc.leftMargin
        HEADER_LINE_Y2 = HEADER_LINE_Y1

        # Footer line position
        FOOTER_LINE_X1 = HEADER_LINE_X1
        FOOTER_LINE_Y1 = doc.bottomMargin / 2 + 5
        FOOTER_LINE_X2 = HEADER_LINE_X2
        FOOTER_LINE_Y2 = FOOTER_LINE_Y1

        # Serial Number position
        SERIAL_NUMBER_X = HEADER_LINE_X1 + doc.width + doc.rightMargin
        SERIAL_NUMBER_Y = HEADER_LINE_Y1 + 5

        # Institution position
        INSTITUTION_X = HEADER_LINE_X1
        INSTITUTION_Y = HEADER_LINE_Y1 + 5

        # Page Number position
        PAGE_NUMBER_X = FOOTER_LINE_X1 + doc.width + doc.rightMargin
        PAGE_NUMBER_Y = FOOTER_LINE_Y1 - 10

        # Printed Date position
        PRINTED_DATE_X = FOOTER_LINE_X1
        PRINTED_DATE_Y = FOOTER_LINE_Y1 - 10

        # PDF Header (same for all pages)
        def header(canvas, doc):
            canvas.line(HEADER_LINE_X1, HEADER_LINE_Y1, HEADER_LINE_X2, HEADER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            text_serial = "Statistika Klasa VIII-E " + str(datetime.now().year)
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, 'Shkolla 9-vjeçare "Azem Hajdari"')

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            current_date = datetime.now()
            day = str(current_date.day)
            month = str(current_date.month)
            year = str(current_date.year)
            text_printed_date = "Krijuar më datë: " + str(day + "/" + month + "/" + year)
            canvas.drawString(PRINTED_DATE_X, PRINTED_DATE_Y, text_printed_date)
            text_page_number = "Fq. " + str(doc.page)
            canvas.drawRightString(PAGE_NUMBER_X, PAGE_NUMBER_Y, text_page_number)

        # FRAME
        full_page_frame = Frame(
            FRAME_X,
            FRAME_Y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            id='normal',
            showBoundary=0
        )

        # TABLE DATAS

        header_data = [
            [
                Paragraph(str("<b>Nr.</b>"), table_head),
                Paragraph(str("<b>Emri</b>"), table_head),
                Paragraph(str("<b>Mbiemri</b>"), table_head),
                Paragraph(str("<b>VLV</b>"), table_head),
                Paragraph(str("<b>VLP</b>"), table_head),
                Paragraph(str("<b>VLT</b>"), table_head),
                Paragraph(str("<b>Shënime</b>"), table_head)
            ]
        ]

        albanian_language_data = []

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("<b>STATISTIKË PERIUDHA 2 KLASA VIII-E</b>", title_style))

        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                header_data,
                style=order_details_table_style,
                colWidths=[0.5 * inch, 1.5 * inch, 1.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 1 * inch]
            )
        )
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(Paragraph("Lënda: Gjuhë Shqipe", footer_title))
        elements.append(Paragraph("Mësuesja: Drita Kurti", footer_title))

        doc.addPageTemplates([
            PageTemplate(id='StatisticDetailsSecondPeriod', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response


    @staticmethod
    def print8EStatisticThirdPeriod():
        file_name = 'Statistika Periudha 3 Klasa VIII-E.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4,
                              title='Statistika Periudha 3 Klasa VIII-E ' + str(datetime.now().year))

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=13,
            parent=styles['BodyText'],
            alignment=1,
        )

        footer_title = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=2,
        )

        left_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Arial Narrow-Bold',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), .25, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Arial Narrow', 12,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        # ============================= #
        #          CONSTANTS            #
        # ============================= #
        # Spaces
        DEAFULT_SPACE_WIDTH = 0.1 * inch
        DEAFULT_SPACE_HEIGHT = 0.1 * inch
        SPACE_WIDTH_FOOTER = 0.4 * inch
        SPACE_HEIGHT_FOOTER = 0.4 * inch

        # ELEMENTS POSITIONS
        # Frame position
        FRAME_X = doc.leftMargin / 2
        FRAME_Y = doc.bottomMargin / 2
        FRAME_WIDTH = doc.width + doc.leftMargin
        FRAME_HEIGHT = doc.height + doc.bottomMargin - 20

        # Header line position
        HEADER_LINE_X1 = doc.leftMargin / 2
        HEADER_LINE_Y1 = doc.height + doc.topMargin + 25
        HEADER_LINE_X2 = doc.width + 1.5 * doc.leftMargin
        HEADER_LINE_Y2 = HEADER_LINE_Y1

        # Footer line position
        FOOTER_LINE_X1 = HEADER_LINE_X1
        FOOTER_LINE_Y1 = doc.bottomMargin / 2 + 5
        FOOTER_LINE_X2 = HEADER_LINE_X2
        FOOTER_LINE_Y2 = FOOTER_LINE_Y1

        # Serial Number position
        SERIAL_NUMBER_X = HEADER_LINE_X1 + doc.width + doc.rightMargin
        SERIAL_NUMBER_Y = HEADER_LINE_Y1 + 5

        # Institution position
        INSTITUTION_X = HEADER_LINE_X1
        INSTITUTION_Y = HEADER_LINE_Y1 + 5

        # Page Number position
        PAGE_NUMBER_X = FOOTER_LINE_X1 + doc.width + doc.rightMargin
        PAGE_NUMBER_Y = FOOTER_LINE_Y1 - 10

        # Printed Date position
        PRINTED_DATE_X = FOOTER_LINE_X1
        PRINTED_DATE_Y = FOOTER_LINE_Y1 - 10

        # PDF Header (same for all pages)
        def header(canvas, doc):
            canvas.line(HEADER_LINE_X1, HEADER_LINE_Y1, HEADER_LINE_X2, HEADER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            text_serial = "Statistika Klasa VIII-E " + str(datetime.now().year)
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, 'Shkolla 9-vjeçare "Azem Hajdari"')

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Arial Narrow', 9)
            current_date = datetime.now()
            day = str(current_date.day)
            month = str(current_date.month)
            year = str(current_date.year)
            text_printed_date = "Krijuar më datë: " + str(day + "/" + month + "/" + year)
            canvas.drawString(PRINTED_DATE_X, PRINTED_DATE_Y, text_printed_date)
            text_page_number = "Fq. " + str(doc.page)
            canvas.drawRightString(PAGE_NUMBER_X, PAGE_NUMBER_Y, text_page_number)

        # FRAME
        full_page_frame = Frame(
            FRAME_X,
            FRAME_Y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            id='normal',
            showBoundary=0
        )

        # TABLE DATAS

        header_data = [
            [
                Paragraph(str("<b>Nr.</b>"), table_head),
                Paragraph(str("<b>Emri</b>"), table_head),
                Paragraph(str("<b>Mbiemri</b>"), table_head),
                Paragraph(str("<b>VLV</b>"), table_head),
                Paragraph(str("<b>VLP</b>"), table_head),
                Paragraph(str("<b>VLT</b>"), table_head),
                Paragraph(str("<b>Shënime</b>"), table_head)
            ]
        ]

        albanian_language_data = []

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("<b>STATISTIKË PERIUDHA 3 KLASA VIII-E</b>", title_style))

        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                header_data,
                style=order_details_table_style,
                colWidths=[0.5 * inch, 1.5 * inch, 1.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 1 * inch]
            )
        )
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(Paragraph("Lënda: Gjuhë Shqipe", footer_title))
        elements.append(Paragraph("Mësuesja: Drita Kurti", footer_title))

        doc.addPageTemplates([
            PageTemplate(id='StatisticDetailsThirdPeriod', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response
