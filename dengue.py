import pandas as pd
import requests
import zipfile
import io
import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# URLs organizadas por agravo
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


# Colunas desejadas
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


# Tipos
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


def carregar_zip_sinan(url):

    print(f"\nBaixando {url.split('/')[-1]}")

    resposta = requests.get(url, timeout=120)
    resposta.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resposta.content)) as z:

        nome_csv = [
            arq
            for arq in z.namelist()
            if arq.endswith(".csv")
        ][0]

        with z.open(nome_csv) as arquivo:

            df = pd.read_csv(
                arquivo,
                sep=",",
                encoding="latin-1",
                usecols=lambda x: x in colunas,
                dtype=dtype_map,
                low_memory=False,
                on_bad_lines="skip"
            )

    # filtra Espírito Santo
    df["SG_UF_NOT"] = (
        df["SG_UF_NOT"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["SG_UF_NOT"] == "32"
    ].copy()

    print(f"Registros ES: {len(df):,}")

    return df


frames = []


for agravo in urls:

    print("\n" + "=" * 50)
    print(agravo)
    print("=" * 50)

    for url in urls[agravo]:

        try:

            df_temp = carregar_zip_sinan(url)

            frames.append(df_temp)

        except Exception as erro:

            print("Erro:", erro)


# junta tudo
df = pd.concat(
    frames,
    ignore_index=True
)


# ==========================
# CORREÇÃO DA DATA
# ==========================

print("\nExemplo original:")
print(df["DT_NOTIFIC"].head())


df["DT_NOTIFIC"] = (
    df["DT_NOTIFIC"]
    .astype(str)
    .str.strip()
)

# remove valores inválidos
df["DT_NOTIFIC"] = df["DT_NOTIFIC"].replace(
    [
        "",
        "nan",
        "<NA>",
        "00000000",
        "00/00/0000"
    ],
    pd.NA
)

# converte automaticamente
df["DT_NOTIFIC"] = pd.to_datetime(
    df["DT_NOTIFIC"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

print("\nData corrigida:")
print(df["DT_NOTIFIC"].head())

print("\nDatas vazias:")
print(df["DT_NOTIFIC"].isna().sum())


# ==========================
# MYSQL
# ==========================

HOST = "10.61.47.64"
PORTA = 3306
USUARIO = "admin"
SENHA = "Senac@2026"
BANCO = "doencas_arbivirose_2026_2024"


try:

    conexao = pymysql.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
        port=PORTA
    )

    print("\nConectado!")

    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dengue_2022_2026 (

        DT_NOTIFIC DATE,
        ID_MUNICIP VARCHAR(50),
        CS_SEXO VARCHAR(10),
        ANO_NASC INT,
        ID_AGRAVO VARCHAR(50),
        NU_ANO INT,
        SG_UF_NOT VARCHAR(10),
        ID_REGIONA VARCHAR(50),
        CS_RACA VARCHAR(50),
        CS_ESCOL_N VARCHAR(50)

    )
    """)

    conexao.commit()

    cursor.close()
    conexao.close()

    print("Tabela pronta!")

except Exception as erro:

    print("Erro MySQL:")
    print(erro)

    exit()


# ==========================
# ENVIA MYSQL
# ==========================

senha_mysql = quote_plus(SENHA)

engine = create_engine(
    f"mysql+pymysql://{USUARIO}:{senha_mysql}@{HOST}:{PORTA}/{BANCO}"
)

try:

    df.to_sql(
        "dengue_2022_2026",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=50000
    )

    print("\nDados enviados!")

except Exception as erro:

    print("\nErro:")
    print(erro)


# conferência final
print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos:")
print(df.dtypes)

# ==========================
# TABELAS DE APOIO
# ==========================
 
PASTA = r"C:\Users\debora.cofaria\Documents\Débora Cecília - IA\code\dengue"
 
tabelas_apoio = {
    "tb_cs_escol_n": {
        "arquivo": "CS_ESCOL.xlsx",
        "ddl": """
            CREATE TABLE IF NOT EXISTS tb_cs_escol_n (
                CS_ESCOL_N   VARCHAR(10)  NOT NULL,
                Escolaridade VARCHAR(100),
                PRIMARY KEY (CS_ESCOL_N)
            )
        """,
    },
    "tb_id_municip": {
        "arquivo": "ID-MUNICIP.xlsx",
        "ddl": """
            CREATE TABLE IF NOT EXISTS tb_id_municip (
                ID_MUNICIP VARCHAR(20)  NOT NULL,
                Municipio  VARCHAR(150),
                PRIMARY KEY (ID_MUNICIP)
            )
        """,
    },
    "tb_id_agravo": {
        "arquivo": "ID_AGRAVO.xlsx",
        "ddl": """
            CREATE TABLE IF NOT EXISTS tb_id_agravo (
                ID_AGRAVO VARCHAR(10)  NOT NULL,
                DOENCA    VARCHAR(100),
                PRIMARY KEY (ID_AGRAVO)
            )
        """,
        "rename": {"ID_AGRAGO": "ID_AGRAVO"},
    },
    "tb_id_regiona": {
        "arquivo": "ID_REGIONA.xlsx",
        "ddl": """
            CREATE TABLE IF NOT EXISTS tb_id_regiona (
                ID_REGIONA   VARCHAR(10)  NOT NULL,
                Microrregiao VARCHAR(150),
                PRIMARY KEY (ID_REGIONA)
            )
        """,
        "rename": {"Microrregião": "Microrregiao"},
    },
    "tb_cs_raca": {
        "arquivo": "CS_RACA.xlsx",
        "ddl": """
            CREATE TABLE IF NOT EXISTS tb_cs_raca (
                CS_RACA VARCHAR(5)  NOT NULL,
                Raca    VARCHAR(50),
                PRIMARY KEY (CS_RACA)
            )
        """,
    },
}
 
 
print("\n" + "=" * 50)
print("TABELAS DE APOIO")
print("=" * 50)
 
try:
 
    conexao = pymysql.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
        port=PORTA
    )
 
    cursor = conexao.cursor()
 
    for nome_tabela, cfg in tabelas_apoio.items():
        cursor.execute(cfg["ddl"])
 
    conexao.commit()
    cursor.close()
    conexao.close()
 
    print("Tabelas de apoio criadas!")
 
except Exception as erro:
 
    print("Erro ao criar tabelas de apoio:")
    print(erro)
 
    exit()
 
 
for nome_tabela, cfg in tabelas_apoio.items():
 
    caminho = rf"{PASTA}\{cfg['arquivo']}"
 
    print(f"\n{cfg['arquivo']}  →  {nome_tabela}")
 
    try:
 
        df_apoio = pd.read_excel(caminho)
 
        for col in df_apoio.columns:
            df_apoio[col] = df_apoio[col].astype(str).str.strip()
 
        if "rename" in cfg:
            df_apoio = df_apoio.rename(columns=cfg["rename"])
 
        print(f"  Colunas: {list(df_apoio.columns)}")
        print(f"  Registros lidos: {len(df_apoio)}")
 
        df_apoio.to_sql(
            nome_tabela,
            con=engine,
            if_exists="replace",
            index=False
        )
 
        print(f"  Enviado com sucesso!")
 
    except FileNotFoundError:
        print(f"  Arquivo não encontrado: {caminho}")
 
    except Exception as erro:
        print(f"  Erro: {erro}")
 
 
print("\nTabelas de apoio finalizadas!")