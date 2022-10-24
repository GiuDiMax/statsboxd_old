from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.image('sfondo.jpg', x = 0, y = 0, w = 0, h = 0, type = '', link = '')
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 13.0)
pdf.cell(ln=0, h=5.0, align='L', w=0, txt="Hello", border=0)
pdf.output('b.pdf', 'F')