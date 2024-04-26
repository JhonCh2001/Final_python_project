import streamlit as st

import src.datos as datos
import src.graficos as graficos
import src.util as util
import src.reporte_pdf as reporte_pdf
import src.reporte_excel as reporte_excel

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

                placeholder = st.empty()
                placeholder.text("Generando reporte en PDF")
                pdf = reporte_pdf.crear_reporte(st.session_state.df,mes)
                placeholder.empty()

                html = reporte_pdf.create_download_link(pdf.output(dest="S").encode("latin-1"), f"Reporte_{option_mes}")
                st.markdown(html, unsafe_allow_html=True)

                placeholder = st.empty()
                placeholder.text("Generando reporte en excel.")
                pdf = reporte_pdf.crear_reporte(st.session_state.df,mes)
                placeholder.empty()

                wb = reporte_excel.crear_reporte_excel(st.session_state.df)
                excel_file = reporte_excel.descargar_excel(wb)
                st.download_button(
                    label="Descargar Reporte en Excel",
                    data=excel_file,
                    file_name=f"Reporte_total.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except:
        st.warning('Revise la estructura del archivo.', icon = '⭕')