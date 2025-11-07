REPORT_PROMPT = """
Genera un informe analítico con base en la siguiente consulta realizada por el usuario:

Consulta: "{query}"

El informe debe tener una extensión aproximada de dos páginas y debe estar redactado en un lenguaje claro,
técnico-moderado, preciso y orientado a la interpretación económica fundamentado en los datos. Evita lenguaje genérico o superficial.

---
### 1. Identificación del Contexto
Antes de redactar el informe, identifica claramente:
- El Presidente que corresponde al período mencionado o inferido.
- El período de gobierno (años exactos).


Presidente: [Nombre]
Periodo de Gobierno: [Año inicio - Año fin]

---
### 2. Estructura del Informe

**Introducción**
Contextualiza el entorno político-económico del país durante el período, mencionando la situación macroeconómica
relevante y la importancia de evaluar la producción y demanda agregada. (Usa los datos para sustentar tus afirmaciones )

**Análisis Sectorial**
Analiza los sectores económicos utilizando las variables relevantes del dataset. No es necesario incluir todos los
sectores, solo aquellos que presenten variaciones significativas o que sean destacados en el período analizado.

Variables principales disponibles para análisis (usar solo si aportan valor):
- PIB_TC (PIB total a precios constantes)
- PIB_Valor_Agregado_TC
- PIB_Agricultura_Silvicultura_Pesca_TC
- PIB_Minas_Canteras_TC
- PIB_Manufactura_TC
- PIB_Electricidad_Agua_Saneamiento_TC
- PIB_Construccion_TC
- PIB_Comercio_TC
- PIB_Transporte_Almacenamiento_TC
- PIB_Informacion_Comunicaciones_TC
- PIB_Intermediacion_Financiera_Seguros_TC
- PIB_Servicios_Inmobiliarios_TC
- PIB_Servicios_Empresariales_TC
- PIB_Administracion_Publica_TC
- PIB_Educacion_TC
- PIB_Salud_TC
- PIB_Otros_Servicios_TC
- PIB_Demanda_Interna_TC
- PIB_Consumo_Final_TC
- PIB_Formacion_Bruta_Capital_TC
- PIB_Exportaciones_TC
- PIB_Importaciones_TC
- PIB_RegDef_TC
- PIB_RegEsp_TC
- PIB_Terminos_Intercambio
- PIB_USD

Para cada sector relevante:
- Describe su tendencia (crecimiento, desaceleración o caída usando datos de refencia).
- Explica sus posibles causas (política fiscal, entorno internacional, inversión, consumo, etc. usando datos de referencia).
- Señala el impacto macroeconómico general y sectorial usando datos de referencia.

**Conclusiones**
Resume los principales cambios observados, identificando la dirección general del desempeño económico del gobierno.

**Recomendaciones**
Incluye sugerencias estratégicas realistas, basadas en la evidencia observada. Pueden ser de política pública o
estrategias productivas sectoriales.

---
### 3. Estilo
- No inventes datos ni cifras exactas: describe tendencias.
- Usa lenguaje formal y claro.
- Evita frases genéricas como “hubo crecimiento por factores económicos”.
- Explica *cómo* y *por qué*, no solo *qué* ocurrió.

"""