from django.http import FileResponse
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import Image, Spacer
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from datetime import date
import os
from io import StringIO


class PrintStudentDetails:

    @staticmethod
    def printMainClassStudentDetails(students):
        file_name = 'Lista e detyrimit.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4, title='Lista e detyrimit klasa kujdestari')

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=13,
            parent=styles['BodyText'],
            alignment=1,
        )

        footer_title = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=2,
        )

        left_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=11,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), .25, colors.gray),
            ('FONT', (0, 0), (-1, -1), 'Times-Roman', 12,),
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
            canvas.setFont('Times-Roman', 9)
            text_serial = "Lista e detyrimit " + str(datetime.now().year)
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, 'Shkolla 9-vjeçare "Azem Hajdari"')

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Times-Roman', 9)
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

        student_data = [
            [
                Paragraph(str("<b>Nr.</b>"), table_head),
                Paragraph(str("<b>Emri</b>"), table_head),
                Paragraph(str("<b>Mbiemri</b>"), table_head),
                Paragraph(str("<b>Atësia</b>"), table_head),
                Paragraph(str("<b>NID</b>"), table_head),
                Paragraph(str("<b>Datëlindja</b>"), table_head),
                Paragraph(str("<b>Vendlindja</b>"), table_head),
                Paragraph(str("<b>Nr. i amzës</b>"), table_head)
            ]
        ]

        listNumber = 0

        for student in students:
            listNumber += 1
            student_data.append(
                [
                    Paragraph(str(listNumber), left_light),
                    Paragraph(str(student.name), left_light),
                    Paragraph(str(student.surname), left_light),
                    Paragraph(str(student.father_name), left_light),
                    Paragraph(str(student.nid), left_light),
                    Paragraph(str(student.birth_date), left_light),
                    Paragraph(str(student.birth_place), left_light),
                    Paragraph(str(student.amze_number), left_light)
                ]
            )

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Paragraph("<b>LISTA E DETYRIMIT KLASA VIII-D</b>", title_style))
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                student_data,
                style=order_details_table_style,
                colWidths=[0.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch]
            )
        )
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(Paragraph("Mësuesja kujdestare: Drita Kurti", footer_title))
        doc.addPageTemplates([
            PageTemplate(id='StudentDetails', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response
