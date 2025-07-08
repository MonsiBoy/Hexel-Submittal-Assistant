# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import messagebox


# Register Times New Roman fonts
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf'))
pdfmetrics.registerFont(TTFont("Century", "CENTURY.TTF"))  # regular
#pdfmetrics.registerFont(TTFont("Century-Bold", "CENSCBK-Bold.TTF"))  # bold



def generate_pdf(data, desktop_path):
    
    c = canvas.Canvas(desktop_path, pagesize=letter)
    width, height = letter
    top_margin = 35 * mm
    bot_margin = 30 * mm
    right_margin = 25.9 * mm
    left_margin = 30 * mm


    usable_width = width - (right_margin+left_margin)

    # Title
    c.setFont("Century", 14.04)
    c.setFillColor(colors.grey) 
    c.drawCentredString(width / 2, height - 50, data["title"])


    y_curr = height - (top_margin+5*mm)

    # Section
    c.setFont("Times-Bold", 14.04)
    c.setFillColor(colors.black) 
    c.drawString(left_margin,y_curr , f'SECTION {data["section_number"]}')
    y_curr -= 4.5*mm
    
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_curr, data["section_title"])
    y_curr -= 15.5*mm
    
    # SD Info
    c.setFont("Times-Bold", 14.04)
    c.drawString(left_margin, y_curr, f'{data["sd_type"]}')
    y_curr -= 4.5*mm

    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_curr, f'PARAGRAPH: {data["paragraph"]}')
    y_curr -= 4.5*mm

    for key, value in data['register item'].items():
        c.drawString(left_margin, y_curr, f'Item# {key} {value}')
        y_curr -= 4.5*mm
    y_curr -= 12.5*mm
   
    # Submittal Contents
    c.setFont("Times-Bold", 12)
    c.drawString(left_margin, y_curr, 'SUBMITTAL CONTENTS:')
    y_curr -= 4.5*mm

    longest_text = max([f'\u25CF  {key}' for key in data['item'].keys()], key=lambda s: pdfmetrics.stringWidth(s, 'Times-Bold', 12))
  
    # Measure its actual width
    est_width = pdfmetrics.stringWidth(longest_text, 'Times-Bold', 12)
    est_width2 = pdfmetrics.stringWidth('of 999 ', 'Times-Bold', 12)
    est_width3 = pdfmetrics.stringWidth('999 of 999 ', 'Times-Bold', 12)
    chosen_color = getattr(colors, data["color"].lower(), colors.black)
   

    #of 90  ~ {list(data['item'][item].items())[1][1]} of 90'
    for item, value in data['item'].items():
        c.drawString(left_margin, y_curr, f'\u25CF  {item}')
        c.setFillColor(chosen_color)
        c.drawString(left_margin+est_width+100, y_curr, f'{list(data['item'][item].items())[0][1]}')
        c.drawString((left_margin+est_width+100)+est_width2, y_curr, f'of {data['total pages']}')
        c.drawString((left_margin+est_width+100)+(est_width2)+(est_width3-20), y_curr, '~')
        c.drawString((left_margin+est_width+100)+(est_width2)+(est_width3-20)+14, y_curr, f'{list(data['item'][item].items())[1][1]}')
        c.drawString((left_margin+est_width+100)+(est_width2)+(est_width3-20)+14+(est_width2+7), y_curr, f'of {data['total pages']}')
        y_curr -= 4.5*mm
    y_curr -= 30.5*mm
    
     
    # Remarks
    c.setFont("Times-Bold", 14.04)
    c.setFillColor(colors.black)
    c.drawString(left_margin, y_curr, 'REMARKS:')
    y_curr -= 4.5*mm
    
  
    styles = getSampleStyleSheet()
    remark_style = styles["Normal"]
    remark_style.fontName = "Times-Bold"
    remark_style.fontSize = 12
    remark_style.leading = 14

    # Create paragraph object
    remarks_para = Paragraph(data["remarks"], remark_style)

    # Estimate frame height (remaining space on page)
    frame_height = y_curr - bot_margin

    # Create a Frame to restrict the drawing inside margins
    frame = Frame(left_margin-1.5*mm, bot_margin+5*mm, usable_width, frame_height, showBoundary=0)
  


    # Add the paragraph into the frame
    frame.addFromList([remarks_para], c)

    
    c.save()
    messagebox.showinfo("Sucess","PDF SAVED!")
 
   

