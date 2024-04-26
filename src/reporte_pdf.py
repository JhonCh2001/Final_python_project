from fpdf import FPDF
import base64
import src.util as util

class PDFWithBackground(FPDF):
    def __init__(self):
        super().__init__()
        self.background = None
 
    def set_background(self, image_path):
        self.background = image_path
 
    def add_page(self, orientation=''):
        super().add_page(orientation)
        if self.background:
            self.image(self.background, 0, 0, self.w, self.h)
 
    def footer(self):
        # Posición a 1.5 cm desde el fondo
        self.set_y(-15)
        # Configurar la fuente para el pie de página
        self.set_font('Arial', 'I', 8)
        # Número de página
        self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')

def crear_reporte(df_clean, mes):
    pdf = PDFWithBackground()
    pdf.set_background('Background/background.png')
    pdf.add_page()

    year = df_clean['ATENCION_AÑO'].iloc[0]

    pdf.set_y(100)
    pdf.set_font('Courier', style = 'B', size = 45)
    pdf.multi_cell(190,15,'Coberturas de atención de las unidades operativas de primer nivel de la dirección distrital 04D02 Montufar Bolivar Salud',0,1,'L')

    if mes == 0:
        # Primera página del informe

        pdf.add_page()

        meses = df_clean['ATENCION_MES'].unique()

        pdf.set_y(15)
        pdf.set_font('Courier',style = 'B', size = 27) # Vienen por defecto, Arial, Times, Courier
        pdf.multi_cell(170,10,f'Consultas de prevención en primer nivel de atención D04D02 Montúfar Bolívar Salud {util.mes_num(meses[0])}-{util.mes_num(meses[-1])} {year}',0,1,'R')

        pdf.set_y(62)
        pdf.set_font('Courier', size = 15) # Vienen por defecto, Arial, Times, Courier
        pdf.multi_cell(180,6,f'El número de consultas en el periodo {util.mes_num(meses[0])}-{util.mes_num(meses[-1])} por rango de edades es:',0,1,'L')

        etiquetas = ['Menores a 1 año','De 1 a 4 años','De 5 a 9 años','De 10 a 14 años','De 15 a 19 años','De 20 a 64 años','Mayores a 65 años']
        llaves = ['Menor_1','1_a_4','5_a_9','10_a_14','15_a_19','20_a_64','Mayor_65']

        lista = list(zip(etiquetas,llaves))

        aux = 0

        for etiqueta,llave in lista:
            pdf.set_y(80+aux)
            pdf.set_font('Courier', size = 15)
            pdf.multi_cell(180,6,f'{chr(149)} {etiqueta}: {util.edad_por_rango(0,llave,df_clean)}',0,1,'L')
            aux += 6

        pdf.image('hist.png',x=43,y=130,w=145)

        for mes_it in meses:

            pdf.add_page()

            pdf.set_y(15)
            pdf.set_font('Courier',style = 'B', size = 27) # Vienen por defecto, Arial, Times, Courier
            pdf.multi_cell(170,10,f'Consultas de prevención en primer nivel de atención D04D02 Montúfar Bolívar Salud {util.mes_num(mes_it)} {year}',0,1,'R')

            pdf.set_y(62)
            pdf.set_font('Courier', size = 15) # Vienen por defecto, Arial, Times, Courier
            pdf.multi_cell(180,6,f'El número de consultas en {util.mes_num(mes_it)} por rango de edades es:',0,1,'L')

            aux = 0

            for etiqueta,llave in lista:
                pdf.set_y(80+aux)
                pdf.set_font('Courier', size = 15)
                pdf.multi_cell(180,6,f'{chr(149)} {etiqueta}: {util.edad_por_rango(mes_it,llave,df_clean)}',0,1,'L')
                aux += 6

            pdf.image(f'hist_{mes_it}.png',x=43,y=130,w=145)

        return pdf
    
    pdf.add_page()

    pdf.set_y(15)
    pdf.set_font('Courier',style = 'B', size = 27) # Vienen por defecto, Arial, Times, Courier
    pdf.multi_cell(170,10,f'Consultas de prevención en primer nivel de atención D04D02 Montúfar Bolívar Salud {util.mes_num(mes)} {year}',0,1,'R')

    pdf.set_y(62)
    pdf.set_font('Courier', size = 15) # Vienen por defecto, Arial, Times, Courier
    pdf.multi_cell(180,6,f'El número de consultas en {util.mes_num(mes)} por rango de edades es:',0,1,'L')

    etiquetas = ['Menores a 1 año','De 1 a 4 años','De 5 a 9 años','De 10 a 14 años','De 15 a 19 años','De 20 a 64 años','Mayores a 65 años']
    llaves = ['Menor_1','1_a_4','5_a_9','10_a_14','15_a_19','20_a_64','Mayor_65']

    lista = list(zip(etiquetas,llaves))

    aux = 0

    for etiqueta,llave in lista:
        pdf.set_y(80+aux)
        pdf.set_font('Courier', size = 15)
        pdf.multi_cell(180,6,f'{chr(149)} {etiqueta}: {util.edad_por_rango(mes,llave,df_clean)}',0,1,'L')
        aux += 6

    pdf.image(f'hist_{mes}.png',x=43,y=130,w=145)

    return pdf

def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Descargar reporte en PDF</a>'