import io,os, re, json
from functools import reduce
from pypinyin import pinyin
from tkinter import *
from tkinter import ttk
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import messagebox #for messagebox.
from reportlab.pdfgen import canvas
#from reportlab.lib.units import mm
from reportlab.lib.colors import Color,black,blue,red,white, green
from reportlab.lib.pagesizes import A4
from datetime import date, time, datetime,timedelta
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import reportlab.pdfbase.ttfonts
hei=reportlab.pdfbase.ttfonts.TTFont('hei','simhei.ttf') #Import font
kai=reportlab.pdfbase.ttfonts.TTFont('kai','simkai.ttf') #Import font
reportlab.pdfbase.pdfmetrics.registerFont(kai) #Register the font in the current directory
reportlab.pdfbase.pdfmetrics.registerFont(hei) #Register the font in the current directory

IMG_DATA = b'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'

def hanzi_stroke_list(hanzi):
    hanzi_json=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bishun_data',hanzi+'.json')
    if os.path.isfile(hanzi_json):
        hanzi_strokes=json.load(open(hanzi_json,'r'))['strokes']
        return hanzi_strokes
        
def hanzi_full_stroke_svg(hanzi_strokes):
    svg_stroke_path_head='''<path stroke-dasharray="50,30" stroke="black" fill='black' fill-opacity="0.9" d="'''
    svg_stroke_path_end='''"/>'''
    stroke=''
    for i_stroke in hanzi_strokes:
        stroke+=svg_stroke_path_head+ i_stroke +svg_stroke_path_end
    return stroke    


def grid_lines(string):
    string_len=len(string)
    packet = io.BytesIO()
    c = canvas.Canvas(packet,pagesize=A4)#, pagesize=landscape(A3))
    hanzi_list=list(string)
    margin=30
    grid_size=40
    page_total=len(hanzi_list)//20+1
    print (page_total)
    w,h=(A4[0]-margin,A4[1]-margin)
    for _ in range(page_total):
        for i in range(20):
            if hanzi_list and hanzi_stroke_list(hanzi_list[0]):
                hanzi=hanzi_list.pop(0)
                hanzi_py=re.sub(r"\[\[\'(.+)\'\]\]", r'\1',str(pinyin(hanzi)))
                hanzi_strokes=hanzi_stroke_list(hanzi)
                hanzi_strokes_len=len(hanzi_strokes)
            else:
                hanzi=''
            svg_head='''<svg width="40px" height="40px"><path d="M0 20 L40 20" stroke-dasharray="4,4" stroke-width="1" stroke="#666" fill-opacity="0"/>
        <path d="M20 0 L20 40" stroke-dasharray="4,4" stroke-width="0.7" stroke="#666" fill-opacity="0"/><path d="M0 0 l40 0 l0 40 l-40 0 z" stroke-width="1" stroke="red" fill-opacity="0"/><g transform="scale(0.038, -0.038) translate(50, -900) ">'''
            svg_stroke_path_head='''<path stroke-dasharray="50,30" stroke="black" fill='red' fill-opacity="0.2" d="'''
            svg_stroke_path_end='''"/>'''
            svg_tail='''</g></svg>'''
            svg_gridbox=''.join((svg_head,svg_tail))
            for j in range(13):
                if j==0:
                    stroke=hanzi_full_stroke_svg(hanzi_strokes)
                elif j==1:    
                    stroke=svg_stroke_path_head+hanzi_strokes[j-1]+svg_stroke_path_end
                elif j<hanzi_strokes_len:
                    stroke+=svg_stroke_path_head+hanzi_strokes[j-1]+svg_stroke_path_end
                full_SVG_stroke=''.join((svg_head,stroke,svg_tail))
                if j==0:
                    full_SVG_stroke=full_SVG_stroke.replace('scale(0.038, -0.038) translate(50, -900)','scale(0.028, -0.028) translate(200, -1200)')

                if j<hanzi_strokes_len and hanzi:
                    f_svg=io.StringIO(full_SVG_stroke)
                else:
                    f_svg=io.StringIO(svg_gridbox)
                drawing=svg2rlg(f_svg)
                f_svg.close()
                renderPDF.draw(drawing,c,margin+j*(grid_size+1),h-margin-i*(grid_size+0))
            c.setFont('hei',7)
            c.setFillColor(blue)             
            c.drawString(margin+1, h-margin-i*grid_size+0.85*grid_size,hanzi_py)
            hanzi_py=''

        c.showPage()

    c.save()

    packet.seek(0)#buffer start from 0
    new_pdf = PdfFileReader(packet)
    output = PdfFileWriter()
    page=None
    new_pdf_file_name=None

    new_pdf_file_name=os.path.join(os.path.dirname(__file__), 'Hanzi.'+str(datetime.timestamp(datetime.now()))+'.pdf')
    pdf=open(new_pdf_file_name,'wb')
    pdf.write(packet.getvalue())     # Finally output new pdf


    os.startfile(new_pdf_file_name,'open')




def chinese_grid_lines():
    default_hanzi='天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰馀成岁律吕调阳云腾致雨露结为霜金生丽水玉出昆冈剑号巨阙珠称夜光果珍李柰菜重芥姜海咸河淡鳞潜羽翔龙师火帝鸟官人皇始制文字'
    t_box_text=t_box.get('1.0','end-1c')
    if len(t_box_text)>0:
        string=t_box_text
        string=string.replace('\n','')
        grid_lines(string.strip())
    else:
        messagebox.showinfo("Notification", 'Please enter Hanzi... default PDF file saved!')
        grid_lines(default_hanzi)


app=Tk()
app.title("Python汉字田字格生成器")
img=PhotoImage(data=IMG_DATA)
app.tk.call('wm', 'iconphoto', app._w, img)
app.resizable(False, False)

app.geometry("+600+400")
frame0= LabelFrame(app,font=('SimSun',14,'bold'),text='壹贰叁肆伍陆柒捌玖拾一二三四五六七八九')
frame0.grid(row=0,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=N+S+W)

frame1=LabelFrame(frame0)
frame1.grid(row=0,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=E+N+S+W)
t_box=Text(frame1,font=('SimSun',14,'bold'),width=35,height=5)
t_box.grid(row=0,column=0)

frame2= LabelFrame(frame0)
frame2.grid(row=1,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=E+N+S+W)

l_color=Label(frame2,text='Color:')
l_color.grid(row=0,column=0,sticky=E+W+N+S)
color_list=StringVar(value='black')
combo_color = ttk.Combobox(frame2,textvariable=color_list, value=['black','red','green'])
combo_color.grid(row=0,column=1,sticky=E+W+N+S)
l_spin=Label(frame2,text='Columns:')
l_spin.grid(row=0,column=2,sticky=E+W+N+S)
col_spin=Spinbox(frame2, width=25, from_=4, to=11)
col_spin.grid(row=0, column=3,sticky=E+N+S+W)

frame3= LabelFrame(frame0)
frame3.grid(row=3,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=E+N+S+W)
l_icon=Label(frame3,image=img)
l_icon.grid(row=0,column=0,sticky=E+W+N+S)

b_ok=Button(frame3,command=chinese_grid_lines,text='OK',width=15,fg='green', font='Tahoma 10 bold')
b_ok.grid(row=0,column=1,sticky=E)
b_clear=Button(frame3,command=lambda: t_box.delete('1.0','end-1c'), text='Clear',width=15,font='Tahoma 10 bold')
b_clear.grid(row=0,column=2, sticky=E)
mainloop()


