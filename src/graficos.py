import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import src.util as util

def graf_hist(mes,df_clean,file_name):
    if mes == 0:

        df_mes = df_clean.groupby(by = 'RANGO').count()[['PCTE_ANIOS']].reset_index()
        sort_rango = {'Menor_1':0, '1_a_4':1, '5_a_9':2, '10_a_14':3, '15_a_19':4, '20_a_64':5, 'Mayor_65':6}

        df_aux = df_mes.copy()

        for rango in list(sort_rango.keys()):
            if rango in list(df_mes['RANGO']):
                continue
            else:
                df_aux.loc[len(df_aux)] = {'RANGO':rango, 'PCTE_ANIOS':0}

        df_mes = df_aux.sort_values(by='RANGO', key=lambda x: x.map(sort_rango)).reset_index().drop('index',axis = 1)
        # Crear el gráfico de barras usando Matplotlib
        fig, ax = plt.subplots()
        label_edad = ['< 1', '1 - 4', '5 - 9', '10 - 14', '15 - 19', '20 - 64', '> 65']
        grafico = ax.bar(label_edad, df_mes['PCTE_ANIOS'],color='blue')  # Crea barras
        ax.set_xlabel('Edades (Años)')
        ax.set_ylabel('Número de personas')

        ax.bar_label(grafico)

        fig.savefig(f'{file_name}.png')
        plt.close(fig)
        return

    df_mes = df_clean[df_clean['ATENCION_MES'] == mes].groupby(by = 'RANGO').count()[['PCTE_ANIOS']].reset_index()
    
    sort_rango = {'Menor_1':0, '1_a_4':1, '5_a_9':2, '10_a_14':3, '15_a_19':4, '20_a_64':5, 'Mayor_65':6}
    
    df_aux = df_mes.copy()

    for rango in list(sort_rango.keys()):
        if rango in list(df_mes['RANGO']):
            continue
        else:
            df_aux.loc[len(df_aux)] = {'RANGO':rango, 'PCTE_ANIOS':0}

    df_mes = df_aux.sort_values(by='RANGO', key=lambda x: x.map(sort_rango)).reset_index().drop('index',axis = 1)

    # Crear el gráfico de barras usando Matplotlib
    fig, ax = plt.subplots()
    label_edad = ['< 1', '1 - 4', '5 - 9', '10 - 14', '15 - 19', '20 - 64', '> 65']

    grafico = ax.bar(label_edad, df_mes['PCTE_ANIOS'],color='blue')  # Crea barras
    
    ax.set_xlabel('Edades (Años)')
    ax.set_ylabel('Número de personas')
    
    ax.bar_label(grafico)

    fig.savefig(f'{file_name}.png')
    plt.close(fig)
    return

def generar_graficos(df_clean):
    meses = df_clean['ATENCION_MES'].unique()
    graf_hist(0,df_clean,'hist') #Gráfico de todos los meses disponibles
    for mes in meses:
        graf_hist(mes,df_clean,f'hist_{mes}')
    return


def mostrar_grafico(mes,ultimo_mes):
    if mes == 0:
        st.image('hist.png',caption = f'Consultas de prevención en primer nivel de atención D04D02 Montúfar Bolívar Salud periodo enero - {util.mes_num(ultimo_mes)}.')
        return
    st.image(f'hist_{mes}.png',caption = f'Consultas de prevención en primer nivel de atención D04D02 Montúfar Bolívar Salud mes {util.mes_num(mes)}.')