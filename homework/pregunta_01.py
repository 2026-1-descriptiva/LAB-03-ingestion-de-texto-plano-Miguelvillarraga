"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

from pathlib import Path
import re


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    import pandas as pd

    file_path = (
      Path(__file__).resolve().parent.parent
      / "files"
      / "input"
      / "clusters_report.txt"
    )

    rows = []
    current_row = None

    with file_path.open("r", encoding="utf-8") as file:
      for raw_line in file:
        line = raw_line.rstrip("\n")

        match = re.match(
          r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%\s+(.*)$",
          line,
        )
        if match is not None:
          if current_row is not None:
            rows.append(current_row)

          current_row = {
            "cluster": int(match.group(1)),
            "cantidad_de_palabras_clave": int(match.group(2)),
            "porcentaje_de_palabras_clave": float(
              match.group(3).replace(",", ".")
            ),
            "principales_palabras_clave": match.group(4).strip(),
          }
          continue

        if current_row is not None and line.strip():
          current_row["principales_palabras_clave"] += " " + line.strip()

    if current_row is not None:
      rows.append(current_row)

    dataframe = pd.DataFrame(rows)
    dataframe["principales_palabras_clave"] = dataframe[
      "principales_palabras_clave"
    ].map(_normalize_keywords)

    return dataframe


def _normalize_keywords(value):
    value = value.strip().rstrip(".")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*,\s*", ", ", value)
    return value
