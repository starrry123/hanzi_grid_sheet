#This version use data file hanzi_strokes.json
#The json file was generated from *graphics.txt* from https://github.com/skishore/makemeahanzi
#To run this script, please place a copy of hanzi_strokes.json under the same folder
import io,os, re, json
from pypinyin import pinyin
from tkinter import *
from tkinter import ttk
from tkinter import messagebox #for messagebox.
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color,black,blue,red,white, green
from reportlab.lib.pagesizes import A4
from datetime import date, time, datetime,timedelta
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import reportlab.pdfbase.ttfonts
hei=reportlab.pdfbase.ttfonts.TTFont('hei','simhei.ttf') #Import font
kai=reportlab.pdfbase.ttfonts.TTFont('kai','simkai.ttf') #Import font
reportlab.pdfbase.pdfmetrics.registerFont(kai) #Register the font in the current directory
reportlab.pdfbase.pdfmetrics.registerFont(hei) #Register the font in the current directory

IMG_DATA = b'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'
GRID_ROW_NUM, GRID_COLUMN_NUM = 20,13
SVG_HEAD='''<svg width="40px" height="40px">
<path d="M0 20 L40 20 M20 0 L20 40" stroke-dasharray="6,3" stroke-width="0.4" stroke="grey" fill-opacity="0"/>
<path d="M0 0 l40 0 l0 40 l-40 0 z" stroke-width="1" stroke="red" fill-opacity="0"/>
<g transform="scale(0.038, -0.038) translate(50, -900) ">'''
PATH_HEAD='''<path stroke-dasharray="1,0" stroke="black" fill='black' fill-opacity="0.2" d="'''
PATH_TAIL='''"/>'''
SVG_TAIL='''</g></svg>'''
GRIDBOX_SVG=SVG_HEAD+SVG_TAIL

graphics_data = {} #define a hanzi strokes dictionary
json_data=os.path.join(os.path.dirname(__file__), 'hanzi_strokes.json')
with open(json_data,'r',encoding='utf8') as f:
    graphics_data=json.load(f)

def hanzi_svg(hanzi_strokes):
    stroke=''.join(map(lambda x: PATH_HEAD+x+PATH_TAIL,hanzi_strokes))
    hanzi_SVG=''.join((SVG_HEAD,stroke,SVG_TAIL))
    hanzi_SVG=hanzi_SVG.replace('scale(0.038, -0.038) translate(50, -900)','scale(0.028, -0.028) translate(200, -1100)')
    hanzi_SVG=hanzi_SVG.replace('fill-opacity="0.2"','fill-opacity="1"')
    yield hanzi_SVG # 1st yield as full hanzi strokes
    stroke=''
    for i in hanzi_strokes:
        stroke+=PATH_HEAD+i+PATH_TAIL
        yield ''.join((SVG_HEAD,stroke,SVG_TAIL)) #yield hanzi strokes in sequence

def pdf_gen(string):
    packet = io.BytesIO()
    c = canvas.Canvas(packet,pagesize=A4)
    filter_non_hanzi=re.compile(u'[^\u4E00-\u9FA5]')
    hanzis=filter_non_hanzi.sub(r'',string) # filter out non-Chinese characters
    margin, grid_size=30,40 #define page margin
    page_height=A4[1]-margin
    page_total=len(hanzis)//(GRID_ROW_NUM+1)+1
    print ('Total Page: ', page_total)
    row_i=0
    for k,hanzi in enumerate(hanzis):
        pb.start() #progress bar tracker
        pb['value']=(k+1)/len(hanzis)
        pb.update()
        hanzi_pinyin=re.sub(r"\[\[\'(.+)\'\]\]", r'\1',str(pinyin(hanzi)))
        hanzi_strokes=graphics_data[hanzi] if hanzi in graphics_data.keys() else '' #get stroks from dictionary
        hanzi_strokes_len=len(hanzi_strokes)
        hanzi_svgs=hanzi_svg(hanzi_strokes) #define a hanzi SVG generator
        hz_row=hanzi_strokes_len//GRID_COLUMN_NUM
        if (row_i+hz_row+1)>GRID_ROW_NUM:
            row_i=0
            c.showPage()
        
        if not hanzi_strokes: # drawString method if stroke data not available
            c.setFont('kai',30)
            c.setFillColor('red')
            c.setStrokeColor('blue')
            x=margin+0.5*grid_size
            y=page_height-0.7*margin-row_i*(grid_size)            
            c.drawCentredString(x,y,hanzi) #regular hanzi
            for i in range(1,GRID_COLUMN_NUM): #draw shaded hanzi if stroke data not available
                c.setFillColor('grey')
                c.setFont('kai',32)
                x=margin+0.5*grid_size+i*(grid_size+1)
                y=page_height-0.7*margin-row_i*(grid_size) #y0-(row_i+i//13)*(grid_size+0)            
                c.drawCentredString(x,y,hanzi) #regular hanzi

        for i in range((hz_row+1)*GRID_COLUMN_NUM):
            if i>hanzi_strokes_len:
                f_svg=io.StringIO(GRIDBOX_SVG)
            else:
                hanzi_text=next(hanzi_svgs)
                f_svg=io.StringIO(hanzi_text)
            drawing=svg2rlg(f_svg)
            x=margin+(i%13)*(grid_size+1)
            y=page_height-margin-(row_i+i//13)*(grid_size+0)
            renderPDF.draw(drawing,c,x,y)
        
        if hanzi:
            c.setFont('hei',7)
            c.setFillColor(blue)
            c.drawString(margin+1, page_height-margin-row_i*grid_size+0.85*grid_size,hanzi_pinyin)
    
        row_i+=hz_row+1
        #print(hanzi,hanzi_strokes_len,hz_row,row_i)
    c.save()
    new_pdf_file_name=os.path.join(os.path.dirname(__file__), 'Hanzi.'+str(datetime.timestamp(datetime.now()))+'.pdf')
    pdf=open(new_pdf_file_name,'wb')
    pdf.write(packet.getvalue())     # Finally output new pdf

    os.startfile(new_pdf_file_name,'open')

#pdf_gen('藏龘靐齉齾龗龖鱻麤爩籲灪灩鱺鸝鸞麣驫饢籱癵爨厵鸜麷驪鬱韊靏钃讟纞虋齽齼鼺嘢嬈雌御噠蕴颱藏嘢嬈雌御噠蕴颱')   

def chinese_grid_lines():
    default_hanzi='藏龘靐齉齾龗龖鱻天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰馀成岁律吕调阳云腾致雨露结为霜金生丽水玉出昆冈剑号巨阙珠称夜光果珍李柰菜重芥姜海咸河淡鳞潜羽翔龙师火帝鸟官人皇始制文字'
    t_box_text=t_box.get('1.0','end-1c')
    if len(t_box_text)>0:
        pdf_gen(t_box_text.strip())
    else:
        t_box.insert(END,default_hanzi)
        messagebox.showinfo("Notification", 'Please enter Hanzi... default PDF file saved!')
        pdf_gen(default_hanzi)

app=Tk()
app.title("Hanzi Writing Sheet Generator")
img=PhotoImage(data=IMG_DATA)
app.tk.call('wm', 'iconphoto', app._w, img)
app.resizable(False, False)

app.geometry("+600+400")
frame0= LabelFrame(app,font='Tahoma 10 bold',text='Please enter Hanzi below')
frame0.grid(row=0,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=N+S+W)

frame1=LabelFrame(frame0)
frame1.grid(row=0,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=E+N+S+W)
t_box=Text(frame1,font=('SimSun',14,'bold'),width=35,height=5)
t_box.grid(row=0,column=0)

frame3= LabelFrame(frame0)
frame3.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky=E+N+S+W)
l_icon=Label(frame3,image=img)
l_icon.grid(row=0,column=0,sticky=E+W+N+S)

b_ok=Button(frame3,command=chinese_grid_lines,text='OK',width=15,fg='green', font='Tahoma 10 bold')
b_ok.grid(row=0,column=1,sticky=E)
b_clear=Button(frame3,command=lambda: t_box.delete('1.0','end-1c'), text='Clear',width=15,font='Tahoma 10 bold')
b_clear.grid(row=0,column=2, sticky=E)

pb=ttk.Progressbar(frame0, mode = 'determinate')
pb.grid(row=3,column=0,sticky=N+S+E+W)
pb['maximum'] = 1
mainloop()
