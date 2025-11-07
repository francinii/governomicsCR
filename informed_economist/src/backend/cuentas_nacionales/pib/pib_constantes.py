# -*- coding: utf-8 -*-

class ConstantesPIB:
    """Define constantes para la clase PIB."""

    # Tipos de datos dentro de cada categor�a
    PRECIOS_BASICOS = "precios_basicos"
    VOLUMEN = "volumen"
    INDICE_PRECIOS_IMPLICITOS = "indice_precios_implicitos"

    # Variables clave
    PIB = "PIB"
    PIB_USD = "PIB_USD"
    IMPUESTOS = "Impuestos"
    VALOR_AGREGADO = "Valor_Agregado"

    # Actividades econ�micas
    AGRICULTURA = "Agricultura_Silvicultura_Pesca"
    MINAS_CANTERAS = "Minas_Canteras"
    MANUFACTURA = "Manufactura"
    ELECTRICIDAD_AGUA = "Electricidad_Agua_Saneamiento"
    CONSTRUCCION = "Construccion"
    COMERCIO = "Comercio"
    TRANSPORTE = "Transporte_Almacenamiento"
    HOTELES_RESTAURANTES = "Hoteles_Restaurantes"
    INFORMACION_COMUNICACIONES = "Informacion_Comunicaciones"
    FINANCIERAS_SEGUROS = "Financieras_Seguros"
    INMOBILIARIO = "Inmobiliario"
    ACTIVIDADES_PROFESIONALES = "Actividades_Profesionales"
    ADMINISTRACION_PUBLICA = "Administracion_Publica"
    ENSE_SALUD_ASISTENCIA = "Ense_Salud_Asistencia_Social"
    OTRAS_ACTIVIDADES = "Otras_Actividades"

    INDUSTRIAS = [
        AGRICULTURA, MINAS_CANTERAS, MANUFACTURA, ELECTRICIDAD_AGUA,
        CONSTRUCCION, COMERCIO, TRANSPORTE, HOTELES_RESTAURANTES,
        INFORMACION_COMUNICACIONES, FINANCIERAS_SEGUROS, INMOBILIARIO,
        ACTIVIDADES_PROFESIONALES, ADMINISTRACION_PUBLICA,
        ENSE_SALUD_ASISTENCIA, OTRAS_ACTIVIDADES,
    ]

    INDUSTRIA_AMPLIADA = [MINAS_CANTERAS, MANUFACTURA, ELECTRICIDAD_AGUA, CONSTRUCCION]

    ACTIVIDADES_SERVICIOS = [COMERCIO, TRANSPORTE, HOTELES_RESTAURANTES,
                 INFORMACION_COMUNICACIONES, FINANCIERAS_SEGUROS, INMOBILIARIO,
                 ACTIVIDADES_PROFESIONALES, ADMINISTRACION_PUBLICA,
                 ENSE_SALUD_ASISTENCIA, OTRAS_ACTIVIDADES
    ]

    # Componentes del PIB
    DEMANDA_INTERNA = "Demanda_Interna"
    GASTO_CONSUMO_FINAL = "Gasto_Consumo_Final"
    GASTO_CONSUMO_FINAL_HOGARES = "Gasto_Consumo_Final_Hogares"
    BIENES_CONSUMO_DURADERO = "Bienes_Consumo_Duradero"
    BIENES_CONSUMO_SEMI_DURADEROS = "Bienes_Consumo_Semi_Duraderos"
    BIENES_CONSUMO_NO_DURADEROS = "Bienes_Consumo_No_Duraderos"
    SERVICIOS = "Servicios"
    GASTO_CONSUMO_FINAL_GOBIERNO = "Gasto_Consumo_Final_Gobierno_General"
    FORMACION_BRUTA_CAPITAL = "Formacion_Bruta_Capital"
    FORMACION_BRUTA_CAPITAL_FIJO = "Formacion_Bruta_Capital_Fijo"
    MAQUINARIA_EQUIPO = "Maquinaria_Equipo"
    NUEVAS_CONSTRUCCIONES = "Nuevas_Construcciones"
    VARIACION_EXISTENCIAS = "Variacion_Existencias"

    # Exportaciones e Importaciones
    EXPORTACIONES_BIENES = "Exportaciones_Bienes"
    EXPORTACIONES_SERVICIOS = "Exportaciones_Servicios"
    EXPORTACIONES_TOTALES = "Exportaciones_Bienes_Servicios"
    EXPORTACIONES_BIENES_REGDEF = "Exportacion_Bienes_RegDef"
    EXPORTACIONES_BIENES_REGESP = "Exportacion_Bienes_RegEsp"

    IMPORTACIONES_BIENES = "Importaciones_Bienes"
    IMPORTACIONES_SERVICIOS = "Importaciones_Servicios"
    IMPORTACIONES_TOTALES = "Importaciones_Bienes_Servicios"
    IMPORTACIONES_BIENES_REGDEF = "Importacion_Bienes_RegDef"
    IMPORTACIONES_BIENES_REGESP = "Importacion_Bienes_RegEsp"

    # Regimen constantes faltantes
    PIB_REGDEF = "RegDef"
    PIB_REGESP = "RegEsp"

    # Otros
    COMBUSTIBLES = "Combustibles"
    SIN_COMBUSTIBLES = "Sin_Combustibles"
    TERMINOS_INTERCAMBIO = "Terminos_Intercambio"
