"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    df["sexo"] = df["sexo"].str.lower().str.strip()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower().str.strip()
    df["idea_negocio"] = df["idea_negocio"].str.lower().str.replace("_", " ").str.replace("-", " ").str.strip()
    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")
    df["estrato"] = df["estrato"].apply(lambda x: int(x))
    df["comuna_ciudadano"] = df["comuna_ciudadano"].apply(lambda x: int(x))
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
        ).combine_first(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
        )
    df["monto_del_credito"] = df["monto_del_credito"].str.replace("$", "").str.replace(",", "").str.replace(".00", "").str.strip()
    df["línea_credito"] = df["línea_credito"].str.lower().str.strip().str.replace("_", " ").str.replace("-", " ").str.strip()

    df = df.drop_duplicates()
    df = df.dropna()

    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)