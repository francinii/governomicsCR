REPORT_PROMPT = (
    "Basado en la siguiente consulta: '{query}', genera un informe detallado de aproximadamente dos páginas. "
    "El informe debe incluir un análisis exhaustivo de los crecimientos de los sectores económicos "
    "durante el período y gobierno especificados, siguiendo el siguiente formato:" +
    "\n\n" +
    "Presidente: [Nombre del Presidente, inferido de la consulta] \n" +
    "Periodo: [Período de gobierno, inferido de la consulta] \n" +
    "\n" +
    "Introducción: \n" +
    "[Texto introductorio que contextualiza el informe] \n" +
    "\n" +
    "Considera específicamente las siguientes variables económicas y sus descripciones en tu análisis:" +
    "\n\n" +
    "- **Fecha**: Fecha del trimestre correspondiente al dato del PIB." +
    "- **PIB_TC**: PIB total a precios constantes, indicador del valor total de los bienes y servicios producidos en la economía." +
    "- **PIB_Impuestos_TC**: Valor de los impuestos netos de subsidios sobre los productos, a precios constantes." +
    "- **PIB_Valor_Agregado_TC**: Valor agregado bruto total de la economía, a precios constantes." +
    "- **PIB_Agricultura_Silvicultura_Pesca_TC**: Producción económica del sector Agricultura, Silvicultura y Pesca ajustada por inflación." +
    "- **PIB_Minas_Canteras_TC**: Producción del sector de Minería y Canteras a precios constantes." +
    "- **PIB_Manufactura_TC**: Producción industrial manufacturera ajustada por inflación." +
    "- **PIB_Electricidad_Agua_Saneamiento_TC**: Valor agregado del sector de suministro de electricidad, agua y saneamiento." +
    "- **PIB_Construccion_TC**: Producción del sector de construcción a precios constantes." +
    "- **PIB_Comercio_TC**: Valor agregado del comercio al por mayor y al por menor a precios constantes." +
    "- **PIB_Transporte_Almacenamiento_TC**: Producción del sector transporte y almacenamiento, ajustado por inflación." +
    "- **PIB_Informacion_Comunicaciones_TC**: Actividad económica de información y comunicaciones a precios constantes." +
    "- **PIB_Intermediacion_Financiera_Seguros_TC**: Valor agregado de la intermediación financiera y seguros." +
    "- **PIB_Servicios_Inmobiliarios_TC**: Actividad del sector inmobiliario a precios constantes." +
    "- **PIB_Servicios_Empresariales_TC**: Servicios profesionales, científicos y de apoyo empresarial ajustados por inflación." +
    "- **PIB_Administracion_Publica_TC**: Gasto y producción del sector público en administración, defensa y servicios sociales." +
    "- **PIB_Educacion_TC**: Valor agregado de los servicios educativos, públicos y privados." +
    "- **PIB_Salud_TC**: Producción del sector de salud humana y asistencia social." +
    "- **PIB_Otros_Servicios_TC**: Otros servicios personales, culturales y de esparcimiento a precios constantes." +
    "- **PIB_Demanda_Interna_TC**: Demanda interna total, suma del consumo e inversión doméstica ajustada por inflación." +
    "- **PIB_Consumo_Final_TC**: Consumo final total, incluyendo hogares y gobierno, a precios constantes." +
    "- **PIB_Consumo_Hogares_TC**: Consumo final de los hogares a precios constantes." +
    "- **PIB_Consumo_Gobierno_TC**: Consumo final del gobierno general ajustado por inflación." +
    "- **PIB_Formacion_Brut-Capital_TC**: Formación bruta de capital, inversión total en activos fijos a precios constantes." +
    "- **PIB_Exportaciones_TC**: Exportaciones totales de bienes y servicios a precios constantes." +
    "- **PIB_Importaciones_TC**: Importaciones totales de bienes y servicios a precios constantes." +
    "- **PIB_Servicios_Alimentos_Alojamiento_TC**: Servicios de alojamiento y de comida a precios constantes." +
    "- **PIB_Actividades_Financieras_TC**: Actividades financieras y de seguros a precios constantes." +
    "- **PIB_Profesionales_Cientificas_TC**: Actividades profesionales, científicas y técnicas a precios constantes." +
    "- **PIB_Actividades_Inmobiliarias_TC**: Actividades inmobiliarias a precios constantes." +
    "- **PIB_Informacion_Comunicaciones_TC**: Información y comunicaciones a precios constantes." +
    "- **PIB_Actividades_Servicios_Adm_TC**: Actividades de servicios administrativos y de apoyo a precios constantes." +
    "- **PIB_Defens-Adm_Pub_TC**: Administración pública y defensa a precios constantes." +
    "- **PIB_Educacion_TC**: Educación a precios constantes." +
    "- **PIB_Salud_Asistencia_TC**: Actividades de atención de la salud humana y de asistencia social a precios constantes." +
    "- **PIB_Actividades_Artisticas_TC**: Actividades artísticas, de entretenimiento y recreativas a precios constantes." +
    "- **PIB_Hogares_Privados_TC**: Actividades de los hogares como empleadores; actividades no diferenciadas de los hogares productores de bienes y servicios para uso propio a precios constantes." +
    "- **PIB_Organizaciones_Extraterritoriales_TC**: Actividades de organizaciones y organismos extraterritoriales a precios constantes." +
    "- **PIB_Exportaciones_Bienes_TC**: Exportaciones de bienes a precios constantes." +
    "- **PIB_Exportaciones_Servicios_TC**: Exportaciones de servicios a precios constantes." +
    "- **PIB_Importaciones_Bienes_TC**: Importaciones de bienes a precios constantes." +
    "- **PIB_Importaciones_Servicios_TC**: Importaciones de servicios a precios constantes." +
    "- **PIB_Exportacion_Bienes_RegDef_TC**: Exportaciones de bienes del régimen definitivo a precios constantes." +
    "- **PIB_Exportacion_Bienes_RegEsp_TC**: Exportaciones de bienes del régimen especial a precios constantes." +
    "- **PIB_Importacion_Bienes_RegDef_TC**: Importaciones de bienes del régimen definitivo a precios constantes." +
    "- **PIB_Importacion_Bienes_RegEsp_TC**: Importaciones de bienes del régimen especial a precios constantes." +
    "- **PIB_Combustibles_TC**: Valor del consumo de combustibles en la economía a precios constantes." +
    "- **PIB_Sin_Combustibles_TC**: PIB ajustado excluyendo el componente de combustibles." +
    "- **PIB_RegDef_TC**: PIB del régimen definitivo, excluyendo zonas francas y regímenes especiales." +
    "- **PIB_RegEsp_TC**: PIB del régimen especial, que incluye zonas francas y regímenes aduaneros especiales." +
    "- **PIB_Terminos_Intercambio**: Índice de términos de intercambio, relación entre precios de exportación e importación." +
    "- **PIB_USD**: PIB total expresado en dólares estadounidenses corrientes." +
    "\n\n" +
    "Para cada indicador relevante en el análisis, sigue este formato:" +
    "\n" +
    "Indicador de PIB: [Nombre del Indicador] \n" +
    "[Descripción del indicador y un análisis detallado de su comportamiento durante el período y gobierno especificados, incluyendo tendencias, crecimiento, razones, y su impacto]." +
    "\n\n" +
    "Conclusiones: \n" +
    "[Resumen de los hallazgos más importantes y su significado]." +
    "\n" +
    "Recomendaciones: \n" +
    "[Sugerencias o cursos de acción basados en el análisis presentado]." +
    "\n\n" +
    "Prioriza la claridad, la profundidad del análisis y el detalle en la explicación."
)
