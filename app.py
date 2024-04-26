import streamlit as st

import src.datos as datos
import src.graficos as graficos
import src.util as util

st.title('Análisis consultas pacientes')

st.write('Si quiere cargar otro archivo por favor refresque la página.')

st.divider()

archivo_base = st.file_uploader('Subir base de datos: ',type={'csv'},accept_multiple_files=False)

if archivo_base:
    try:
        if 'df' not in st.session_state:
            st.session_state.df = datos.leer_datos(archivo_base)
        
        st.success('Datos cargados correctamente.', icon = '✅')
        graficos.generar_graficos(st.session_state.df)
        
        option_list = [util.mes_num(i) for i in st.session_state.df['ATENCION_MES'].unique()]
        option_list.append('todos')

        if not st.session_state.df.empty:
            option_mes = st.selectbox(
            "Seleccione el mes o 'todos' para tener un análisis de todos los meses:",
            option_list,
            index=None,
            placeholder="Seleccione el mes.",
            )

            if option_mes:
                mes = util.num_mes(option_mes)
                ultimo_mes = util.num_mes(option_list[-2])
                graficos.mostrar_grafico(mes,ultimo_mes)
    except:
        st.warning('Revise la estructura del archivo.', icon = '⭕')