"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd
def pregunta_01():
    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    data = pd.read_csv(
        os.path.join(input_dir, "solicitudes_de_credito.csv"),
        sep=";",
        index_col=0,
    )

    data.dropna(inplace=True)

    columnas_numericas = ["estrato", "comuna_ciudadano", "monto_del_credito"]
    columnas_texto = [
        "tipo_de_emprendimiento",
        "idea_negocio",
        "línea_credito",
    ]

    data['sexo'] = data['sexo'].str.lower().astype('category')

    for col in columnas_texto:
        if col in data.columns:
            data[col] = (data[col]
                         .str.lower()
                        .str.replace(r'[_-]', ' ', regex=True)
                        .str.strip()
            )
    data["barrio"] = data["barrio"].str.lower().str.replace(r'[_-]', ' ', regex=True)
            
    if "fecha_de_beneficio" in data.columns:

        def limpiar_fecha(x):
            parts = str(x).strip().split("/")
            if len(parts) == 3:
                if len(parts[0]) == 4:  # YYYY/MM/DD
                    return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                if len(parts[2]) == 4:  # DD/MM/YYYY
                    return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
            return x

        data["fecha_de_beneficio"] = data["fecha_de_beneficio"].apply(
            limpiar_fecha
        )

    if "monto_del_credito" in data.columns:
        data["monto_del_credito"] = (
            data["monto_del_credito"]
            .astype(str)
            .str.strip()
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(".00", "", regex=False)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    for col in columnas_numericas:
        if col in data.columns:
            # Primero quitamos el .0 si viene como float en texto para que no altere la conversión
            data[col] = data[col].astype(str).str.replace(r"\.0$", "", regex=True)
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data.dropna(inplace=True)
    for col in columnas_numericas:
        data[col] = data[col].astype(int)

    data.drop_duplicates(inplace=True)


    for col in data.columns:
        print(f'{col}: {data[col].value_counts().to_list()}')
    
    output_file = os.path.join(output_dir, "solicitudes_de_credito.csv")
    data.to_csv(output_file, index=False, sep=";")