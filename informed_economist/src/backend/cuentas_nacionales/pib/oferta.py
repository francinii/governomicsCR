from __future__ import annotations
from typing import Dict, Any
import pandas as pd

from .helpers import _concat_by_constants
from .pib_constantes import ConstantesPIB as C

class Oferta:
    """
    Vista de oferta (Oferta) sobre un DataFrame del PIB.
    """

    def __init__(self, dataframe: pd.DataFrame, series_type: str = "TC") -> None:
        self._dataframe = dataframe
        # Normaliza el sufijo: acepta "TC" o "_TC", "SO" o "_SO", "SD" o "_SD"
        self._series_type = series_type if series_type.startswith("_") else f"_{series_type}"
        self._pib = C.PIB
        self._valor_agregado = C.VALOR_AGREGADO
        self._impuestos = C.IMPUESTOS
        self._industrias: list[str] = list(C.INDUSTRIAS)
        self.agricultura_silvicultura_pesca = C.AGRICULTURA
        self.minas_canteras = C.MINAS_CANTERAS
        self.manufactura = C.MANUFACTURA
        self.electricidad_agua_saneamiento = C.ELECTRICIDAD_AGUA
        self.construccion = C.CONSTRUCCION
        self.comercio = C.COMERCIO
        self.transporte_almacenamiento = C.TRANSPORTE
        self.hoteles_restaurantes = C.HOTELES_RESTAURANTES
        self.informacion_comunicaciones = C.INFORMACION_COMUNICACIONES
        self.financieras_seguros = C.FINANCIERAS_SEGUROS
        self.inmobiliario = C.INMOBILIARIO
        self.actividades_profesionales = C.ACTIVIDADES_PROFESIONALES
        self.administracion_publica = C.ADMINISTRACION_PUBLICA
        self.ense_salud_asistencia_social = C.ENSE_SALUD_ASISTENCIA
        self.otras_actividades = C.OTRAS_ACTIVIDADES
        self._industria_ampliada: list[str] = list(C.INDUSTRIA_AMPLIADA)  
        self._servicios: list[str] = list(C.ACTIVIDADES_SERVICIOS)
    # ---------------------------
    # Atributos mutables
    # ---------------------------
    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe

    @property
    def series_type(self) -> str:
        return self._series_type

    @series_type.setter
    def series_type(self, series_type: str) -> None:
        self._series_type = series_type if series_type.startswith("_") else f"_{series_type}"

    # ---------------------------
    # Atributos read-only
    # ---------------------------
    @property
    def pib(self) -> str:
        return self._pib

    @property
    def valor_agregado(self) -> str:
        return self._valor_agregado

    @property
    def impuestos(self) -> str:
        return self._impuestos

    @property
    def industrias(self) -> list[str]:
        return list(self._industrias)  # se devuelve una copia para evitar mutabilidad
    
    @property
    def industria_ampliada(self) -> list[str]:
        return list(self._industria_ampliada)  # se devuelve una copia para evitar mutabilidad 
    
    @property
    def servicios(self) -> list[str]:
        return list(self._servicios)  # se devuelve una copia para evitar mutabilidad

    @property
    def pib_name(self) -> str:
        return f"{self.pib}{self.series_type}"

    # ---------------------------
    # Atributos read-only (por industria)
    # ---------------------------
    @property
    def agricultura_silvicultura_pesca_(self) -> str:
        return self.agricultura_silvicultura_pesca

    @property
    def minas_canteras_(self) -> str:
        return self.minas_canteras

    @property
    def manufactura_(self) -> str:
        return self.manufactura

    @property
    def electricidad_agua_saneamiento_(self) -> str:
        return self.electricidad_agua_saneamiento

    @property
    def construccion_(self) -> str:
        return self.construccion

    @property
    def comercio_(self) -> str:
        return self.comercio

    @property
    def transporte_almacenamiento_(self) -> str:
        return self.transporte_almacenamiento

    @property
    def hoteles_restaurantes_(self) -> str:
        return self.hoteles_restaurantes

    @property
    def informacion_comunicaciones_(self) -> str:
        return self.informacion_comunicaciones

    @property
    def financieras_seguros_(self) -> str:
        return self.financieras_seguros

    @property
    def inmobiliario_(self) -> str:
        return self.inmobiliario

    @property
    def actividades_profesionales_(self) -> str:
        return self.actividades_profesionales

    @property
    def administracion_publica_(self) -> str:
        return self.administracion_publica

    @property
    def ense_salud_asistencia_social_(self) -> str:
        return self.ense_salud_asistencia_social

    @property
    def otras_actividades_(self) -> str:
        return self.otras_actividades

    # --------------------------------
    # Métodos que devuelven DataFrames
    # --------------------------------
    def get_pib(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [self.pib + self.series_type]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_categorias_principales(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.pib + self.series_type,
            self.valor_agregado + self.series_type,
            self.impuestos + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_industrias(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [base + self.series_type for base in self.industrias]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_valor_agregado(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [self.valor_agregado + self.series_type]
        return _concat_by_constants(self.dataframe, categories, return_dict)
    
    def get_industria_ampliada(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [base + self.series_type for base in self.industria_ampliada]
        df = _concat_by_constants(self.dataframe, categories, return_dict)
        df['Industria_Ampliada' + self.series_type] = df.sum(axis = 1)
        return df

    def get_servicios(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [base + self.series_type for base in self.servicios]
        df = _concat_by_constants(self.dataframe, categories, return_dict)
        df['Servicios' + self.series_type] = df.sum(axis = 1)
        return df

    def get_sectores(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [self.agricultura_silvicultura_pesca + self.series_type]
        df = _concat_by_constants(self.dataframe, categories, return_dict)
        df.columns = ['Agro' + self.series_type]

        servicios = self.get_servicios()
        servicios = pd.DataFrame(servicios['Servicios' + self.series_type])

        industria = self.get_industria_ampliada()
        industria = pd.DataFrame(industria['Industria_Ampliada'+ self.series_type])

        df = pd.concat([df, servicios, industria], axis = 1)
        return df

    def get_impuestos(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [self.impuestos + self.series_type]
        return _concat_by_constants(self.dataframe, categories, return_dict)
