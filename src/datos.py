import pandas as pd
import src.util as util


def leer_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    keep_cols = ['PCTE_ANIOS','PCTE_MESES','PCTE_DIAS','ATEMED_TIP_DIAG','ATEMED_CRON_DIAG','ATENCION_MES','ATENCION_AÑO']
    df_clean= df[df.columns.intersection(keep_cols)]
    df_clean = df_clean[(df_clean['ATEMED_TIP_DIAG'] == 'Prevención') & (df_clean['ATEMED_CRON_DIAG'] == 'Primera')]

    df_clean['RANGO'] = df_clean.apply(lambda x: util.rango_edad(x.PCTE_ANIOS, x.PCTE_MESES,x.PCTE_DIAS), axis=1)

    return df_clean