# informed_economist

Proyecto en **Python** para analizar y comparar el crecimiento económico de Costa Rica a lo largo de diferentes gobiernos, con base en datos del **Banco Central de Costa Rica (BCCR)**.  

La primera fase se centra en el **PIB trimestral (tendencia-ciclo)** desde la perspectiva del gasto, de las actividades económicas y del régimen de producción. Posteriormente, el proyecto podrá extenderse a otras variables como empleo, precios, etc.  

Los resultados iniciales se entregarán en **gráficos HTML estáticos** y, en fases posteriores, se desarrollará un **dashboard interactivo tipo Sneat** con Dash.

---

## 🚀 Estructura del Proyecto

informed_economist/
├─ src/ # Código fuente
│ ├─ backend/ # Lógica de extracción, procesamiento, modelos
│ └─ frontend/ # Layouts y callbacks de Dash (futuro)
├─ data/ # Archivos de datos (crudos y procesados)
├─ machine_learning_and_ai_models/ # Modelos ML/IA entrenados
├─ tests/ # Pruebas unitarias
├─ notebooks/ # Exploración y análisis inicial
├─ venv/ # Entorno virtual (ignorado en Git)
├─ requirements.txt # Dependencias
└─ README.md # Este archivo


---

## ⚙️ Requisitos Previos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- (Opcional) [Jupyter Notebook](https://jupyter.org/) o [JupyterLab](https://jupyter.org/install)

---

## 📥 Instalación y Configuración

1. Clonar este repositorio:
```bash
   git clone https://github.com/adoljc87/informed_economist.git
   cd informed_economist
```

2. Crear y activar entorno virtual (Windows):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```


