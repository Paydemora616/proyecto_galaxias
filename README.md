# 📊 Analizador de Parámetros de Galaxias

Esta aplicación en Python permite analizar un archivo Excel con más de 240,000 registros sobre parámetros estructurales de galaxias. Se diseñó con una interfaz visual usando `Tkinter` para facilitar su uso.

---

## 📁 Datos Esperados

El archivo Excel debe tener el siguiente formato:

| A (raefcorkpg) | B (error) | C (muecorg) | D (error) |
|----------------|------------|--------------|------------|
| Radio efectivo | Error      | Brillo medio | Error      |

---

## ✅ Funcionalidades

- 📈 **Cálculo de estadísticas**: moda, media, mediana, varianza, desviación estándar, covarianza.
- 🔢 **Transformación logarítmica**: se aplica logaritmo base 10 a `raefcorkpg`.
- 🟦 **Gráficas**: diagrama de dispersión y regresión lineal.
- 📤 **Exportación de resultados**:
  - `resultados_analisis.xlsx` → Estadísticas y regresión en hojas separadas.
  - `resultados_analisis.pdf` → Reporte legible y listo para entregar.
  - `resultados_analisis.json` → Resultados en formato estructurado.

---

## ▶️ Cómo ejecutar

1. Asegúrate de tener Python 3.10+ instalado.
2. Instala las dependencias necesarias:

```bash
pip install pandas numpy matplotlib scipy fpdf xlsxwriter
