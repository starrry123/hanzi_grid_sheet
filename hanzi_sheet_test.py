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
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


def hanzi_stroke_list(hanzi):
    hanzi_json=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bishun_data',hanzi+'.json')
    if os.path.isfile(hanzi_json):
        hanzi_strokes=json.load(open(hanzi_json,'r'))['strokes']
        return hanzi_strokes
        


def grid_lines(string):
    string_len=len(string)
    packet = io.BytesIO()
    c = canvas.Canvas(packet,pagesize=A4)#, pagesize=landscape(A3))
    string_list=list(string)
    margin=30
    grid_size=40
    page_total=len(string_list)//20+1
    print (page_total)
    w,h=(A4[0]-margin,A4[1]-margin)
    for _ in range(page_total):
        for i in range(20):
            if string_list:
                hanzi=string_list.pop(0)
                hanzi_strokes=hanzi_stroke_list(hanzi)
                hanzi_strokes_len=len(hanzi_strokes)
            else:
                hanzi=''
            svg_head='''<svg width="40px" height="40px"><path d="M0 20 L40 20" stroke-dasharray="4,4" stroke-width="1" stroke="#666" fill-opacity="0"/>
    <path d="M20 0 L20 40" stroke-dasharray="4,4" stroke-width="0.7" stroke="#666" fill-opacity="0"/><path d="M0 0 l40 0 l0 40 l-40 0 z" stroke-width="1" stroke="#111" fill-opacity="0"/><g transform="scale(0.038, -0.038) translate(0, -900) ">'''
            svg_stroke_path_head='''<path stroke-dasharray="4,4" stroke="red" fill='grey' fill-opacity="0.5" d="'''
            svg_stroke_path_end='''"/>'''
            svg_tail='''</g></svg>'''
            svg_gridbox=''.join((svg_head,svg_tail))
            for j in range(13):
                if j==0:
                    stroke=svg_stroke_path_head+hanzi_strokes[j]+svg_stroke_path_end
                elif j<hanzi_strokes_len:
                    stroke+=svg_stroke_path_head+hanzi_strokes[j]+svg_stroke_path_end
                full_stroke=''.join((svg_head,stroke,svg_tail))
                if j<hanzi_strokes_len and hanzi:
                    f_svg=io.StringIO(full_stroke)
                else:
                    f_svg=io.StringIO(svg_gridbox)
                drawing=svg2rlg(f_svg)
                f_svg.close()
                renderPDF.draw(drawing,c,margin+j*(grid_size+1),h-margin-i*(grid_size+0))
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

grid_lines('一丁七万丈三上下不与丐丑专且世一丁七万丈三上下不与丐丑专且世一丁七万丈三上下不与丐丑专一丁七万丈三上下不与世')
