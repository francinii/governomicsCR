import pandasai as pai
import pandas as pd
from pandasai import SmartDataframe

_pib_schema_cache = None

#  Excel file charging
def create_pib_schema(llm, file_path: str = "app/data/raw/Variables_PIB_TC.xlsx"):
    global _pib_schema_cache
    if _pib_schema_cache is not None:
        print("Returning cached PIB schema.")
        return _pib_schema_cache

    print("Dataset 'costa-rica/pib-gobiernos' not found in cache, creating new dataset.")
    
    file_df = pd.read_excel(file_path, sheet_name="pibQ")

    smart_df = SmartDataframe(
        file_df,
        config={
            "llm": llm, 
            "verbose": True,
            "enable_cache": False,
            "save_charts_path": "charts"
        }
    )

    smart_df.description = "PIB trimestral de Costa Rica, desagregado por sectores económicos y componentes, con valores a precios constantes."
    smart_df.columns = [
        {"name": "fecha", "type": "datetime", "description": "Fecha del trimestre correspondiente al dato del PIB."},
        {"name": "PIB_TC", "type": "float", "description": "PIB total a precios constantes, indicador del valor total de los bienes y servicios producidos en la economía."},
        {"name": "PIB_Impuestos_TC", "type": "float", "description": "Valor de los impuestos netos de subsidios sobre los productos, a precios constantes."},
        {"name": "PIB_Valor_Agregado_TC", "type": "float", "description": "Valor agregado bruto total de la economía, a precios constantes."},
        {"name": "PIB_Agricultura_Silvicultura_Pesca_TC", "type": "float", "description": "Producción económica del sector Agricultura, Silvicultura y Pesca ajustada por inflación."},
        {"name": "PIB_Minas_Canteras_TC", "type": "float", "description": "Producción del sector de Minería y Canteras a precios constantes."},
        {"name": "PIB_Manufactura_TC", "type": "float", "description": "Producción industrial manufacturera ajustada por inflación."},
        {"name": "PIB_Electricidad_Agua_Saneamiento_TC", "type": "float", "description": "Valor agregado del sector de suministro de electricidad, agua y saneamiento."},
        {"name": "PIB_Construccion_TC", "type": "float", "description": "Producción del sector de construcción a precios constantes."},
        {"name": "PIB_Comercio_TC", "type": "float", "description": "Valor agregado del comercio al por mayor y al por menor a precios constantes."},
        {"name": "PIB_Transporte_Almacenamiento_TC", "type": "float", "description": "Producción del sector transporte y almacenamiento, ajustado por inflación."},
        {"name": "PIB_Informacion_Comunicaciones_TC", "type": "float", "description": "Actividad económica de información y comunicaciones a precios constantes."},
        {"name": "PIB_Intermediacion_Financiera_Seguros_TC", "type": "float", "description": "Valor agregado de la intermediación financiera y seguros."},
        {"name": "PIB_Servicios_Inmobiliarios_TC", "type": "float", "description": "Actividad del sector inmobiliario a precios constantes."},
        {"name": "PIB_Servicios_Empresariales_TC", "type": "float", "description": "Servicios profesionales, científicos y de apoyo empresarial ajustados por inflación."},
        {"name": "PIB_Administracion_Publica_TC", "type": "float", "description": "Gasto y producción del sector público en administración, defensa y servicios sociales."},
        {"name": "PIB_Educacion_TC", "type": "float", "description": "Valor agregado de los servicios educativos, públicos y privados."},
        {"name": "PIB_Salud_TC", "type": "float", "description": "Producción del sector de salud humana y asistencia social."},
        {"name": "PIB_Otros_Servicios_TC", "type": "float", "description": "Otros servicios personales, culturales y de esparcimiento a precios constantes."},
        {"name": "PIB_Demanda_Interna_TC", "type": "float", "description": "Demanda interna total, suma del consumo e inversión doméstica ajustada por inflación."},
        {"name": "PIB_Consumo_Final_TC", "type": "float", "description": "Consumo final total, incluyendo hogares y gobierno, a precios constantes."},
        {"name": "PIB_Consumo_Hogares_TC", "type": "float", "description": "Consumo final de los hogares a precios constantes."},
        {"name": "PIB_Consumo_Gobierno_TC", "type": "float", "description": "Consumo final del gobierno general ajustado por inflación."},
        {"name": "PIB_Formacion_Brut-Capital_TC", "type": "float", "description": "Formación bruta de capital, inversión total en activos fijos a precios constantes."},
        {"name": "PIB_Exportaciones_TC", "type": "float", "description": "Exportaciones totales de bienes y servicios a precios constantes."},
        {"name": "PIB_Importaciones_TC", "type": "float", "description": "Importaciones totales de bienes y servicios a precios constantes."},
        {"name": "PIB_Servicios_Alimentos_Alojamiento_TC", "type": "float", "description": "Servicios de alojamiento y de comida a precios constantes."},
        {"name": "PIB_Actividades_Financieras_TC", "type": "float", "description": "Actividades financieras y de seguros a precios constantes."},
        {"name": "PIB_Profesionales_Cientificas_TC", "type": "float", "description": "Actividades profesionales, científicas y técnicas a precios constantes."},
        {"name": "PIB_Actividades_Inmobiliarias_TC", "type": "float", "description": "Actividades inmobiliarias a precios constantes."},
        {"name": "PIB_Informacion_Comunicaciones_TC", "type": "float", "description": "Información y comunicaciones a precios constantes."},
        {"name": "PIB_Actividades_Servicios_Adm_TC", "type": "float", "description": "Actividades de servicios administrativos y de apoyo a precios constantes."},
        {"name": "PIB_Defens-Adm_Pub_TC", "type": "float", "description": "Administración pública y defensa a precios constantes."},
        {"name": "PIB_Educacion_TC", "type": "float", "description": "Educación a precios constantes."},
        {"name": "PIB_Salud_Asistencia_TC", "type": "float", "description": "Actividades de atención de la salud humana y de asistencia social a precios constantes."},
        {"name": "PIB_Actividades_Artisticas_TC", "type": "float", "description": "Actividades artísticas, de entretenimiento y recreativas a precios constantes."},
        {"name": "PIB_Hogares_Privados_TC", "type": "float", "description": "Actividades de los hogares como empleadores; actividades no diferenciadas de los hogares productores de bienes y servicios para uso propio a precios constantes."},
        {"name": "PIB_Organizaciones_Extraterritoriales_TC", "type": "float", "description": "Actividades de organizaciones y organismos extraterritoriales a precios constantes."},
        {"name": "PIB_Exportaciones_Bienes_TC", "type": "float", "description": "Exportaciones de bienes a precios constantes."},
        {"name": "PIB_Exportaciones_Servicios_TC", "type": "float", "description": "Exportaciones de servicios a precios constantes."},
        {"name": "PIB_Importaciones_Bienes_TC", "type": "float", "description": "Importaciones de bienes a precios constantes."},
        {"name": "PIB_Importaciones_Servicios_TC", "type": "float", "description": "Importaciones de servicios a precios constantes."},
        {"name": "PIB_Exportacion_Bienes_RegDef_TC", "type": "float", "description": "Exportaciones de bienes del régimen definitivo a precios constantes."},
        {"name": "PIB_Exportacion_Bienes_RegEsp_TC", "type": "float", "description": "Exportaciones de bienes del régimen especial a precios constantes."},
        {"name": "PIB_Importacion_Bienes_RegDef_TC", "type": "float", "description": "Importaciones de bienes del régimen definitivo a precios constantes."},
        {"name": "PIB_Importacion_Bienes_RegEsp_TC", "type": "float", "description": "Importaciones de bienes del régimen especial a precios constantes."},
        {"name": "PIB_Combustibles_TC", "type": "float", "description": "Valor del consumo de combustibles en la economía a precios constantes."},
        {"name": "PIB_Sin_Combustibles_TC", "type": "float", "description": "PIB ajustado excluyendo el componente de combustibles."},
        {"name": "PIB_RegDef_TC", "type": "float", "description": "PIB del régimen definitivo, excluyendo zonas francas y regímenes especiales."},
        {"name": "PIB_RegEsp_TC", "type": "float", "description": "PIB del régimen especial, que incluye zonas francas y regímenes aduaneros especiales."},
        {"name": "PIB_Terminos_Intercambio", "type": "float", "description": "Índice de términos de intercambio, relación entre precios de exportación e importación."},
        {"name": "PIB_USD", "type": "float", "description": "PIB total expresado en dólares estadounidenses corrientes."}
    ]

    _pib_schema_cache = smart_df
    return smart_df


