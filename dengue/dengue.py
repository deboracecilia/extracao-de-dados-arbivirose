import pandas as pd
import requests
import zipfile
import io
from pathlib import Path

# ==========================================================
# PASTA PARA SALVAR OS DADOS
# ==========================================================

PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)

# ==========================================================
# URLs
# ==========================================================

urls = {
    "Dengue": [
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/csv/DENGBR26.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/csv/DENGBR25.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/csv/DENGBR24.csv.zip",
    ],
    "Chikungunya": [
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Chikungunya/csv/CHIKBR26.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Chikungunya/csv/CHIKBR25.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Chikungunya/csv/CHIKBR24.csv.zip",
    ],
    "Zika": [
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Zikavirus/csv/ZIKABR26.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Zikavirus/csv/ZIKABR25.csv.zip",
        "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Zikavirus/csv/ZIKABR24.csv.zip",
    ],
}

# ==========================================================
# COLUNAS
# ==========================================================

colunas = [
    "DT_NOTIFIC",
    "ID_MUNICIP",
    "CS_SEXO",
    "ANO_NASC",
    "ID_AGRAVO",
    "NU_ANO",
    "SG_UF_NOT",
    "ID_REGIONA",
    "CS_RACA",
    "CS_ESCOL_N",
]

dtype_map = {
    "DT_NOTIFIC": str,
    "ID_MUNICIP": str,
    "CS_SEXO": str,
    "ANO_NASC": "Int64",
    "ID_AGRAVO": str,
    "NU_ANO": "Int64",
    "SG_UF_NOT": str,
    "ID_REGIONA": str,
    "CS_RACA": str,
    "CS_ESCOL_N": str,
}

# ==========================================================
# FUNÇÃO
# ==========================================================

def carregar_zip_sinan(url):
    print(f"\nBaixando {url.split('/')[-1]}")

    resposta = requests.get(url, timeout=120)
    resposta.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resposta.content)) as z:
        nome_csv = [a for a in z.namelist() if a.endswith(".csv")][0]

        with z.open(nome_csv) as arquivo:
            df = pd.read_csv(
                arquivo,
                sep=",",
                encoding="latin-1",
                usecols=lambda x: x in colunas,
                dtype=dtype_map,
                low_memory=False,
                on_bad_lines="skip",
            )

    df["SG_UF_NOT"] = (
        df["SG_UF_NOT"]
        .astype(str)
        .str.strip()
    )

    # Espírito Santo
    df = df[df["SG_UF_NOT"] == "32"].copy()
    print(f"Registros ES: {len(df):,}")
    return df


# ==========================================================
# DOWNLOAD DOS DADOS
# ==========================================================

frames = []

for agravo in urls:
    print("\n" + "=" * 50)
    print(agravo)
    print("=" * 50)

    for url in urls[agravo]:
        try:
            frames.append(carregar_zip_sinan(url))
        except Exception as erro:
            print("Erro:", erro)

df = pd.concat(frames, ignore_index=True)

# ==========================================================
# CORREÇÃO DAS DATAS
# ==========================================================

print("\nExemplo original:")
print(df["DT_NOTIFIC"].head())

df["DT_NOTIFIC"] = (
    df["DT_NOTIFIC"]
    .astype(str)
    .str.strip()
)

df["DT_NOTIFIC"] = df["DT_NOTIFIC"].replace(
    ["", "nan", "<NA>", "00000000", "00/00/0000"],
    pd.NA,
)

df["DT_NOTIFIC"] = pd.to_datetime(
    df["DT_NOTIFIC"],
    format="mixed",
    dayfirst=True,
    errors="coerce",
)

print("\nData corrigida:")
print(df["DT_NOTIFIC"].head())

print("\nDatas vazias:")
print(df["DT_NOTIFIC"].isna().sum())

# ==========================================================
# SALVAR BASE PRINCIPAL
# ==========================================================

arquivo_principal = PASTA_DADOS / "dengue_2024_2026.csv"

df.to_csv(
    arquivo_principal,
    index=False,
    encoding="utf-8-sig",
)

print(f"\nArquivo salvo em:")
print(arquivo_principal.resolve())

# ==========================================================
# TABELAS DE APOIO
# ==========================================================

PASTA_APOIO = Path(r"auxiliares")

tabelas_apoio = {
    "tb_cs_escol_n": "CS_ESCOL.xlsx",
    "tb_id_municip": "ID-MUNICIP.xlsx",
    "tb_id_agravo": "ID_AGRAVO.xlsx",
    "tb_id_regiona": "ID_REGIONA.xlsx",
    "tb_cs_raca": "CS_RACA.xlsx",
}

renomear = {
    "tb_id_agravo": {"ID_AGRAGO": "ID_AGRAVO"},
    "tb_id_regiona": {"Microrregião": "Microrregiao"},
}

print("\n" + "=" * 50)
print("SALVANDO TABELAS DE APOIO")
print("=" * 50)

for nome_tabela, arquivo in tabelas_apoio.items():

    caminho = PASTA_APOIO / arquivo

    print(f"\n{arquivo}")

    try:

        df_apoio = pd.read_excel(caminho)

        for col in df_apoio.columns:
            df_apoio[col] = (
                df_apoio[col]
                .astype(str)
                .str.strip()
            )

        if nome_tabela in renomear:
            df_apoio = df_apoio.rename(
                columns=renomear[nome_tabela]
            )

        destino = PASTA_DADOS / f"{nome_tabela}.csv"

        df_apoio.to_csv(
            destino,
            index=False,
            encoding="utf-8-sig",
        )

        print(f"Salvo em {destino.name}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")

    except Exception as erro:
        print(erro)

print("\nProcesso finalizado!")