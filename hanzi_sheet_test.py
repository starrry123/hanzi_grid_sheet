import io,os, re,json
#from pypinyin import pinyin
from tkinter import *
from tkinter import ttk
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import messagebox #for messagebox.
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color,black,blue,red,white, green
from reportlab.lib.pagesizes import A4
from datetime import date, time, datetime,timedelta
import reportlab.pdfbase.ttfonts #Import the registered font module of reportlab
hei=reportlab.pdfbase.ttfonts.TTFont('hei','simhei.ttf') #Import font
kai=reportlab.pdfbase.ttfonts.TTFont('kai','simkai.ttf') #Import font
song=reportlab.pdfbase.ttfonts.TTFont('song','simsun.ttc') #Import font
reportlab.pdfbase.pdfmetrics.registerFont(kai) #Register the font in the current directory
reportlab.pdfbase.pdfmetrics.registerFont(song) #Register the font in the current directory
reportlab.pdfbase.pdfmetrics.registerFont(hei) #Register the font in the current directory
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

IMG_DATA = b'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'

def hanzi_stroke_list(hanzi):
    hanzi_json=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bishun_data',hanzi+'.json')
    if os.path.isfile(hanzi_json):
        hanzi_strokes=json.load(open(hanzi_json,'r'))['strokes']
        return hanzi_strokes
        


def grid_lines(string):
    packet = io.BytesIO()
    c = canvas.Canvas(packet,pagesize=A4)#, pagesize=landscape(A3))
    string_list=list(string)
    margin=40
    grid_size=20
    w,h=A4
    w,h=w-margin,h-margin
    w1,h1=w//grid_size,h//grid_size
    page_total=len(string_list)//20+1
    print (page_total)
    for page_i in range(page_total):
        x,y = margin,margin
        i=0
        while x < w+grid_size :
            if i % 2 ==0 :
                c.setLineWidth(0.8)
                #c.setStrokeColor(color_list.get())
                c.setDash(1,0)
            else:
                c.setLineWidth(0.2)
                c.setStrokeColor('#C0C0C0')
                c.setDash(6,3)             
            c.line(x, margin, x, h)
            x += grid_size
            i+=1
        # draw horizontal lines
        i=0
        while y < h :
            if i % 2 ==0 :
                c.setLineWidth(0.8)
                #c.setStrokeColor(color_list.get())
                c.setDash(1,0)
            else:
                c.setLineWidth(0.2)
                c.setStrokeColor('#C0C0C0')
                c.setDash(6,3)
            c.line(margin, y, w, y)
            y += grid_size
            i+=1

        x,y = margin+grid_size,h-1.7*grid_size
        #hanzi_strokes=''

        while y>margin and len(string_list)>0:
            hanzi=string_list.pop(0)
            hanzi_strokes=hanzi_stroke_list(hanzi)
            svg_head='''<svg width="40px" height="40px" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M0 20 L40 20" stroke-dasharray="4,4" stroke-width="1" stroke="#666" fill-opacity="0"/>
<path d="M20 0 L20 40" stroke-dasharray="4,4" stroke-width="1" stroke="#666" fill-opacity="0"/><path d="M1 1 l58 0 l0 58 l-58 0 Z" stroke-width="2" stroke="#111" fill-opacity="0"/>
<g transform="translate(-2,50) scale(0.058, -0.0572)">'''
            svg_stroke_path_head='''<path d="'''
            svg_stroke_path_end='''"/>'''
            svg_tail='''</g></svg>'''
            c.setFont('kai',32)
            c.setFillColor(black)           
            #c.drawCentredString(x, y,hanzi) #regular hanzi
            c.setFont('kai',32)
            c.setFillColor('#DCDCDC')
            c.setFont('hei',7)
            c.setFillColor(blue)
            y -= 2*grid_size    
        c.setFont('Helvetica',8)
        #c.drawCentredString(w/2,margin/2,'Page '+str(page_i+1))
        #c.drawRightString(w,margin/2,str(datetime.now().date()))
        c.setFont('hei',8)
        #c.drawRightString(w,h+grid_size,'Python Hanzi Sheet Generator 汉字田字格生成器')
        stroke=''
        for i in range(len(hanzi_strokes)):
            if i==0:
                stroke=svg_stroke_path_head+hanzi_strokes[i]+svg_stroke_path_end
            else:
                stroke+=svg_stroke_path_head+hanzi_strokes[i]+svg_stroke_path_end
            full_stroke=''.join((svg_head,svg_stroke_path_head,svg_stroke_path_end,stroke,svg_tail))
            print (full_stroke)
            f=io.StringIO(full_stroke)
            drawing=svg2rlg(f)
            f.close()
            c.setFillColor('#DCDCDC')
            c.setStrokeColor('#DCDCDC')            
            renderPDF.draw(drawing,c,margin+60*i,h-margin)
        c.showPage()

    c.save()

    #buffer start from 0
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    output = PdfFileWriter()
    page=None
    new_pdf_file_name=None

    new_pdf_file_name=os.path.join(os.path.dirname(__file__), 'Hanzi.'+str(datetime.timestamp(datetime.now()))+'.pdf')
    pdf=open(new_pdf_file_name,'wb')
    pdf.write(packet.getvalue())
    # Finally output new pdf


    os.startfile(new_pdf_file_name,'open')

grid_lines('万')
#grid_lines('一丁七万丈三上下不与丐丑专且世')
