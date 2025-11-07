import pandas as pd
from .oferta import Oferta
from .demanda import Demanda


class PIBViews:
    def __init__(self, dataframe: pd.DataFrame, series_type: str = "TC") -> None:
        self._dataframe = dataframe
        self._oferta = Oferta(dataframe, series_type=series_type)
        self._demanda = Demanda(dataframe, series_type=series_type)

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe

    @dataframe.setter
    def dataframe(self, new_dataframe: pd.DataFrame) -> None:
        self._dataframe = new_dataframe
        self._oferta.dataframe = new_dataframe
        self._demanda.dataframe = new_dataframe

    @property
    def oferta(self) -> "Oferta":
        return self._oferta

    @property
    def demanda(self) -> "Demanda":
        return self._demanda

    @property
    def series_type(self) -> str:
        # Fuente única de la verdad; ambas deben estar sincronizadas
        return self._oferta.series_type

    @series_type.setter
    def series_type(self, value: str) -> None:
        self._oferta.series_type = value
        self._demanda.series_type = value
