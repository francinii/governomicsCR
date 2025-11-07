from __future__ import annotations
from typing import Dict, Any
import pandas as pd
import re

from .helpers import _concat_by_constants
from .pib_constantes import ConstantesPIB as C


class Demanda:
    """
    Vista de demanda (Demanda) sobre un DataFrame del PIB.
    - Átomos expuestos como propiedades read-only.
    - `dataframe` y `series_type` quedan mutables para integrarse con PIBViews.
    """

    def __init__(self, dataframe: pd.DataFrame, series_type: str = 'TC') -> None:
        self._dataframe = dataframe
        # Normaliza el sufijo (acepta "TC" o "_TC")
        self._series_type = series_type if series_type.startswith("_") else f"_{series_type}"

        self._pib = C.PIB
        self._demanda_interna = C.DEMANDA_INTERNA
        self._gasto_consumo_final = C.GASTO_CONSUMO_FINAL
        self._gasto_consumo_final_hogares = C.GASTO_CONSUMO_FINAL_HOGARES

        self._bienes_consumo_duradero = C.BIENES_CONSUMO_DURADERO
        self._bienes_consumo_semiduradero = C.BIENES_CONSUMO_SEMI_DURADEROS
        self._bienes_consumo_no_duradero = C.BIENES_CONSUMO_NO_DURADEROS

        self._servicios = C.SERVICIOS
        self._gasto_consumo_final_gobierno = C.GASTO_CONSUMO_FINAL_GOBIERNO

        self._formacion_bruta_capital = C.FORMACION_BRUTA_CAPITAL
        self._formacion_bruta_capital_fijo = C.FORMACION_BRUTA_CAPITAL_FIJO
        self._maquinaria_equipo = C.MAQUINARIA_EQUIPO
        self._nuevas_construcciones = C.NUEVAS_CONSTRUCCIONES
        self._variacion_existencias = C.VARIACION_EXISTENCIAS

        self._exportaciones_bienes = C.EXPORTACIONES_BIENES
        self._exportaciones_servicios = C.EXPORTACIONES_SERVICIOS
        self._exportaciones_totales = C.EXPORTACIONES_TOTALES
        self._exportaciones_bienes_reg_def = C.EXPORTACIONES_BIENES_REGDEF
        self._exportaciones_bienes_reg_esp = C.EXPORTACIONES_BIENES_REGESP

        self._importaciones_bienes = C.IMPORTACIONES_BIENES
        self._importaciones_servicios = C.IMPORTACIONES_SERVICIOS
        self._importaciones_totales = C.IMPORTACIONES_TOTALES
        self._importaciones_bienes_reg_def = C.IMPORTACIONES_BIENES_REGDEF
        self._importaciones_bienes_reg_esp = C.IMPORTACIONES_BIENES_REGESP

        self._combustibles_importados = C.COMBUSTIBLES
        self._bienes_no_combustibles_importados = C.SIN_COMBUSTIBLES
        self._terminos_de_intercambio = C.TERMINOS_INTERCAMBIO

    # ---------------------------
    # Dataframe / series_type (mutables)
    # ---------------------------
    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value: pd.DataFrame) -> None:
        self._dataframe = value

    @property
    def series_type(self) -> str:
        return self._series_type

    @series_type.setter
    def series_type(self, value: str) -> None:
        self._series_type = value if value.startswith("_") else f"_{value}"

    # ---------------------------
    # Átomos (read-only)
    # ---------------------------
    @property
    def pib(self) -> str:
        return self._pib

    @property
    def demanda_interna(self) -> str:
        return self._demanda_interna

    @property
    def gasto_consumo_final(self) -> str:
        return self._gasto_consumo_final

    @property
    def gasto_consumo_final_hogares(self) -> str:
        return self._gasto_consumo_final_hogares

    @property
    def bienes_consumo_duradero(self) -> str:
        return self._bienes_consumo_duradero

    @property
    def bienes_consumo_semiduradero(self) -> str:
        return self._bienes_consumo_semiduradero

    @property
    def bienes_consumo_no_duradero(self) -> str:
        return self._bienes_consumo_no_duradero

    @property
    def servicios(self) -> str:
        return self._servicios

    @property
    def gasto_consumo_final_gobierno(self) -> str:
        return self._gasto_consumo_final_gobierno

    @property
    def formacion_bruta_capital(self) -> str:
        return self._formacion_bruta_capital

    @property
    def formacion_bruta_capital_fijo(self) -> str:
        return self._formacion_bruta_capital_fijo

    @property
    def maquinaria_equipo(self) -> str:
        return self._maquinaria_equipo

    @property
    def nuevas_construcciones(self) -> str:
        return self._nuevas_construcciones

    @property
    def variacion_existencias(self) -> str:
        return self._variacion_existencias

    @property
    def exportaciones_bienes(self) -> str:
        return self._exportaciones_bienes

    @property
    def exportaciones_servicios(self) -> str:
        return self._exportaciones_servicios

    @property
    def exportaciones_totales(self) -> str:
        return self._exportaciones_totales

    @property
    def exportaciones_bienes_reg_def(self) -> str:
        return self._exportaciones_bienes_reg_def

    @property
    def exportaciones_bienes_reg_esp(self) -> str:
        return self._exportaciones_bienes_reg_esp

    @property
    def importaciones_bienes(self) -> str:
        return self._importaciones_bienes

    @property
    def importaciones_servicios(self) -> str:
        return self._importaciones_servicios

    @property
    def importaciones_totales(self) -> str:
        return self._importaciones_totales

    @property
    def importaciones_bienes_reg_def(self) -> str:
        return self._importaciones_bienes_reg_def

    @property
    def importaciones_bienes_reg_esp(self) -> str:
        return self._importaciones_bienes_reg_esp

    @property
    def combustibles_importados(self) -> str:
        return self._combustibles_importados

    @property
    def bienes_no_combustibles_importados(self) -> str:
        return self._bienes_no_combustibles_importados

    @property
    def terminos_de_intercambio(self) -> str:
        return self._terminos_de_intercambio
    
    def get_pib(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [self.pib + self.series_type]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    # ---------------------------
    # Métodos que devuelven DataFrames
    # ---------------------------
    def get_categorias_principales(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.pib + self.series_type,
            self.gasto_consumo_final_hogares + self.series_type,
            self.gasto_consumo_final_gobierno + self.series_type,
            self.formacion_bruta_capital_fijo + self.series_type,
            self.exportaciones_totales + self.series_type,
            self.importaciones_totales + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_demanda_interna(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.gasto_consumo_final_hogares + self.series_type,
            self.gasto_consumo_final_gobierno + self.series_type,
            self.formacion_bruta_capital_fijo + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_consumo(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.gasto_consumo_final + self.series_type,
            self.gasto_consumo_final_hogares + self.series_type,
            self.gasto_consumo_final_gobierno + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_consumo_hogares(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.gasto_consumo_final_hogares + self.series_type,
            self.bienes_consumo_duradero + self.series_type,
            self.bienes_consumo_semiduradero + self.series_type,
            self.bienes_consumo_no_duradero + self.series_type,
            rf'^(?:PIB_)?{re.escape(self.servicios)}{re.escape(self.series_type)}$',
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_inversion(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.formacion_bruta_capital_fijo + self.series_type,
            self.maquinaria_equipo + self.series_type,
            self.nuevas_construcciones + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_exportaciones(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.exportaciones_totales + self.series_type,
            self.exportaciones_bienes + self.series_type,
            self.exportaciones_servicios + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_exportaciones_bienes(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.exportaciones_bienes + self.series_type,
            self.exportaciones_bienes_reg_def + self.series_type,
            self.exportaciones_bienes_reg_esp + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_importaciones(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.importaciones_totales + self.series_type,
            self.importaciones_bienes + self.series_type,
            self.importaciones_servicios + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_importaciones_bienes(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.importaciones_bienes + self.series_type,
            self.importaciones_bienes_reg_def + self.series_type,
            self.importaciones_bienes_reg_esp + self.series_type,
        ]
        return _concat_by_constants(self.dataframe, categories, return_dict)

    def get_importaciones_bienes_regimen_def(self, return_dict: bool = False) -> Dict[str, Any] | pd.DataFrame:
        categories = [
            self.importaciones_bienes_reg_def + self.series_type,
            self.combustibles_importados + self.series_type,
            self.bienes_no_combustibles_importados + self.series_type

        ]

        data = _concat_by_constants(self.dataframe, categories, return_dict)

        data = data.loc[:, ~data.columns.duplicated(keep="first")]

        return data