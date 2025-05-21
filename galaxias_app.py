import io

import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from fpdf import FPDF
from sklearn.linear_model import LinearRegression


def estadisticas_descriptivas(df):
    stats_dict = {}
    for col in df.columns:
        datos = df[col].dropna()
        moda = datos.mode()
        moda_val = moda.iloc[0] if not moda.empty else np.nan
        media = datos.mean()
        mediana = datos.median()
        varianza = datos.var()
        desv_std = datos.std()
        stats_dict[col] = {
            'moda': moda_val,
            'media': media,
            'mediana': mediana,
            'varianza': varianza,
            'desviacion_std': desv_std
        }
    covarianza = df.cov()
    return stats_dict, covarianza


def graficar(df_log, x_col, y_col, modelo):
    fig, ax = plt.subplots()
    sns.scatterplot(x=df_log[x_col], y=df_log[y_col], alpha=0.3, s=10, ax=ax)
    ax.set_xlabel(f'log10({x_col})')
    ax.set_ylabel(y_col)
    ax.set_title('Diagrama de dispersión con regresión lineal')

    x_vals = np.array(ax.get_xlim())
    y_vals = modelo.intercept_ + modelo.coef_[0] * x_vals
    ax.plot(x_vals, y_vals, color='red')
    return fig


def exportar_excel(df, stats_dict, cov_matrix, filename='resultados_galaxias.xlsx'):
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name='Datos')
        pd.DataFrame(stats_dict).to_excel(writer, sheet_name='Estadisticas')
        cov_matrix.to_excel(writer, sheet_name='Covarianza')


def exportar_pdf(fig, stats_dict, cov_matrix, filename='resultados_galaxias.pdf'):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resultados análisis galaxias", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    for col, stats_ in stats_dict.items():
        pdf.cell(0, 8, f"{col} - Media: {stats_['media']:.4f}, Desv. Std: {stats_['desviacion_std']:.4f}", ln=True)

    pdf.cell(0, 10, "Covarianza (muestra)", ln=True)
    cov_sample = cov_matrix.iloc[:5, :5].round(4)
    for i, row in cov_sample.iterrows():
        row_str = ', '.join([f"{v:.4f}" for v in row])
        pdf.cell(0, 6, f"{i}: {row_str}", ln=True)

    # Convertir figura matplotlib a PNG en buffer temporal para añadir imagen
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    pdf.image(buf, x=10, y=pdf.get_y()+5, w=180)

    pdf.output(filename)


def main():
    st.title("Análisis Estructural de Galaxias desde MySQL")

    st.sidebar.header("Conexión a la Base de Datos")
    host = st.sidebar.text_input("Host", value="70.35.199.139")
    port = st.sidebar.number_input("Puerto", value=5050)
    user = st.sidebar.text_input("Usuario", value="root")
    password = st.sidebar.text_input("Contraseña", type="password", value="Hola124")
    database = st.sidebar.text_input("Base de datos", value="galaxias1")
    tabla = st.sidebar.text_input("Tabla", value="data1")

    if st.sidebar.button("Conectar y cargar datos"):
        try:
            conexion = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                collation='utf8mb4_spanish_ci'
            )
            cursor = conexion.cursor()
            query = f"SELECT raefcorkpg, errreckg, muecorg, ermuecorg FROM {tabla}"
            cursor.execute(query)
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()
            conexion.close()

            df = pd.DataFrame(resultados, columns=columnas)

            st.success("Datos cargados exitosamente desde MySQL")
            st.dataframe(df.head())

            col_raefcorkpg = 'raefcorkpg'
            col_muecorg = 'muecorg'

            df_log = df.copy()
            df_log[col_raefcorkpg] = np.log10(df[col_raefcorkpg].replace(0, np.nan))

            # Paso 1: Reemplazar comas por puntos (si los hay)
            #df[col_raefcorkpg] = df[col_raefcorkpg].astype(str).str.replace(',', '.', regex=False)

            # Paso 2: Convertir a número
            #df[col_raefcorkpg] = pd.to_numeric(df[col_raefcorkpg], errors='coerce')

            # Paso 3: Reemplazar ceros por NaN
            #df[col_raefcorkpg] = df[col_raefcorkpg].replace(0, np.nan)

            # Paso 4: Aplicar log10 sin errores
            #df_log = df.copy()
            #df_log[col_raefcorkpg] = np.log10(df[col_raefcorkpg])


            stats_dict, cov_matrix = estadisticas_descriptivas(df_log[[col_raefcorkpg, col_muecorg]])

            st.subheader("Estadísticas descriptivas")
            for col, vals in stats_dict.items():
                st.write(f"**{col}**")
                st.write(vals)

            st.write("Covarianza:")
            st.dataframe(cov_matrix)

            X = df_log[[col_raefcorkpg]].dropna()
            y = df_log.loc[X.index, col_muecorg]
            modelo = LinearRegression().fit(X.values.reshape(-1, 1), y.values)

            st.subheader("Gráficas")
            fig_scatter = graficar(df_log, col_raefcorkpg, col_muecorg, modelo)
            st.pyplot(fig_scatter)

            #if st.button("Exportar resultados a Excel"):
            #    exportar_excel(df_log, stats_dict, cov_matrix)
            #    st.success("Archivo Excel generado: resultados_galaxias.xlsx")


            #if st.button("Exportar resultados a PDF"):
            #    exportar_pdf(fig_scatter, stats_dict, cov_matrix)
            #    st.success("Archivo PDF generado: resultados_galaxias.pdf")

        except Exception as e:
            st.error(f"Error al conectar o consultar MySQL: {e}")


if __name__ == '__main__':
    main()


#---Para ejecutarlo hay que poner en una terminal streamlit run galaxias_app.py
