import pandas as pd

def edad_en_dias(anios,meses,dias):
    dias1 = dias
    if dias == -1:
        dias1 = 29
    return dias1+30*meses+12*30*anios

def rango_edad(anios,meses,dias):

    edad = edad_en_dias(anios,meses,dias)

    if edad < edad_en_dias(1,0,0):
        return 'Menor_1'
    if edad < edad_en_dias(5,0,0):
        return '1_a_4'
    if edad < edad_en_dias(10,0,0):
        return '5_a_9'
    if edad < edad_en_dias(15,0,0):
        return '10_a_14'
    if edad < edad_en_dias(20,0,0):
        return '15_a_19'
    if edad < edad_en_dias(65,0,0):
        return '20_a_64'
    if edad >= edad_en_dias(65,0,0):
        return 'Mayor_65'

def mes_num(num):
    if num == 0:
        return 'todos'
    if num == 1:
        return 'enero'
    if num == 2:
        return 'febrero'
    if num == 3:
        return 'marzo'
    if num == 4:
        return 'abril'
    if num == 5:
        return 'mayo'
    if num == 6:
        return 'junio'
    if num == 7:
        return 'julio'
    if num == 8:
        return 'agosto'
    if num == 9:
        return 'septiembre'
    if num == 10:
        return 'octubre'
    if num == 11:
        return 'noviembre'
    if num == 12:
        return 'diciembre'

def num_mes(mes):
    if mes == 'todos':
        return 0
    if mes == 'enero':
        return 1
    if mes == 'febrero':
        return 2
    if mes == 'marzo':
        return 3
    if mes == 'abril':
        return 4
    if mes == 'mayo':
        return 5
    if mes == 'junio':
        return 6
    if mes == 'julio':
        return 7
    if mes == 'agosto':
        return 8
    if mes == 'septiembre':
        return 9
    if mes == 'octubre':
        return 10
    if mes == 'noviembre':
        return 11
    if mes == 'diciembre':
        return 12
    
def edad_por_rango(mes,rango,df_clean):

    if mes == 0:
        df_mes = df_clean.groupby(by = 'RANGO').count()[['PCTE_ANIOS']].reset_index()

        return df_mes[df_mes['RANGO'] == rango]['PCTE_ANIOS'].iloc[0]

    df_mes = df_clean[df_clean['ATENCION_MES'] == mes].groupby(by = 'RANGO').count()[['PCTE_ANIOS']].reset_index()
    
    return df_mes[df_mes['RANGO'] == rango]['PCTE_ANIOS'].iloc[0]