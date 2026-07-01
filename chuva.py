# =========================
# IMPORTAÇÕES
# =========================

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from time import sleep

# =========================
# PASTA PARA SALVAR DADOS
# =========================

PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)

# =========================
# DATA FINAL
# =========================

data_final = datetime.today().strftime("%Y-%m-%d")

# =========================
# MUNICÍPIOS (ID + LAT + LON)
# =========================

municipios = {
    "Vitoria": (320530, -20.3155, -40.3128),
    "Pancas": (320400, -18.8500, -40.8530),
    "Serra": (320500, -20.1210, -40.3074),
    "Vila Velha": (320520, -20.3297, -40.2925),
    "Colatina": (320150, -19.5387, -40.6306),
    "Cariacica": (320130, -20.2638, -40.4165),
    "Itapemirim": (320280, -21.0094, -40.8347),
    "Boa Esperanca": (320100, -18.5395, -40.3026),
    "Baixo Guandu": (320080, -19.5182, -41.0151),
    "Domingos Martins": (320190, -20.3639, -40.6594),
    "Cachoeiro de Itapemirim": (320120, -20.8485, -41.1124),
    "Anchieta": (320040, -20.8056, -40.6425),
    "Fundao": (320220, -19.9311, -40.4042),
    "Santa Teresa": (320460, -19.9356, -40.5972),
    "Linhares": (320320, -19.3947, -40.0647),
    "Itarana": (320290, -19.8739, -40.8753),
    "Governador Lindenberg": (320225, -19.1864, -40.4598),
    "Brejetuba": (320115, -20.1435, -41.2953),
    "Barra de Sao Francisco": (320090, -18.7548, -40.8965),
    "Muniz Freire": (320370, -20.4658, -41.4156),
    "Piuma": (320420, -20.8378, -40.7218),
    "Sao Mateus": (320490, -18.7201, -39.8589),
    "Vargem Alta": (320503, -20.6695, -41.0065),
    "Viana": (320510, -20.3900, -40.4960),
    "Ponto Belo": (320425, -18.1267, -40.5407),
    "Conceicao da Barra": (320160, -18.5931, -39.7322),
    "Laranja da Terra": (320316, -19.8994, -41.0563),
    "Guacui": (320230, -20.7757, -41.6760),
    "Jaguare": (320305, -18.9070, -40.0757),
    "Mimoso do Sul": (320340, -21.0642, -41.3665),
    "Marataizes": (320332, -21.0426, -40.8249),
    "Aracruz": (320060, -19.8200, -40.2739),
    "Jeronimo Monteiro": (320310, -20.7898, -41.3950),
    "Venda Nova do Imigrante": (320506, -20.3397, -41.1358),
    "Sao Domingos do Norte": (320465, -19.1458, -40.6285),
    "Ibatiba": (320245, -20.2347, -41.5082),
    "Afonso Claudio": (320010, -20.0778, -41.1261),
    "Santa Maria de Jetiba": (320455, -20.0264, -40.7437),
    "Iconha": (320260, -20.7933, -40.8115),
    "Montanha": (320350, -18.1261, -40.3640),
    "Mantenopolis": (320330, -18.8622, -41.1236),
    "Bom Jesus do Norte": (320110, -21.1181, -41.6731),
    "Castelo": (320140, -20.6036, -41.2023),
    "Sao Gabriel da Palha": (320470, -19.0177, -40.5356),
    "Alto Rio Novo": (320035, -19.0614, -41.0177),
    "Alfredo Chaves": (320030, -20.6396, -40.7548),
    "Ibitirama": (320255, -20.5461, -41.6665),
    "Ibiracu": (320250, -19.8325, -40.3732),
    "Aguia Branca": (320013, -18.9841, -40.7418),
    "Apiaca": (320050, -21.1516, -41.5680),
    "Itaguacu": (320270, -19.8019, -40.8554),
    "Guarapari": (320240, -20.6770, -40.5095),
    "Alegre": (320020, -20.7637, -41.5336),
    "Marilandia": (320335, -19.4117, -40.5452),
    "Nova Venecia": (320390, -18.7157, -40.4053),
    "Divino de Sao Lourenco": (320180, -20.6227, -41.6948),
    "Rio Bananal": (320435, -19.2608, -40.3366),
    "Atilio Vivacqua": (320070, -20.9134, -41.1985),
    "Vila Pavao": (320515, -18.6189, -40.6098),
    "Pedro Canario": (320405, -18.2985, -40.5418),
    "Sao Jose do Calcado": (320480, -21.0277, -41.6541),
    "Mucurici": (320360, -18.0949, -40.5150),
    "Ecoporanga": (320210, -18.3735, -40.8308),
    "Irupi": (320265, -20.3508, -41.6448),
    "Vila Valerio": (320517, -18.9962, -40.3847),
    "Sooretama": (320501, -19.1882, -40.0975),
    "Conceicao do Castelo": (320170, -20.3686, -41.2431),
    "Joao Neiva": (320313, -19.7578, -40.3853),
    "Santa Leopoldina": (320450, -20.1001, -40.5298),
    "Presidente Kennedy": (320430, -21.0959, -41.0460),
    "Muqui": (320380, -20.9519, -41.3463),
    "Sao Roque do Canaa": (320495, -19.7411, -40.6524),
    "Marechal Floriano": (320334, -20.4120, -40.6833),
    "Pinheiros": (320410, -18.4151, -40.2176),
    "Iuna": (320300, -20.3471, -41.5354),
    "Rio Novo do Sul": (320440, -20.8556, -40.9383),
    "Dores do Rio Preto": (320200, -20.6931, -41.8418),
    "Agua Doce do Norte": (320016, -18.5484, -40.9785)
}

# =========================
# COLETA DOS DADOS
# =========================

frames = []

for municipio, (id_municip, latitude, longitude) in municipios.items():

    print(f"\nColetando {municipio}...")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&start_date=2024-01-01"
        f"&end_date={data_final}"
        "&daily=precipitation_sum,"
        "precipitation_hours,"
        "temperature_2m_mean,"
        "temperature_2m_max,"
        "temperature_2m_min"
        "&timezone=America/Sao_Paulo"
    )

    try:

        resposta = requests.get(url, timeout=60)
        resposta.raise_for_status()
        dados = resposta.json()

        df_temp = pd.DataFrame({
            "data": pd.to_datetime(dados["daily"]["time"]),
            "id_municipio": id_municip,
            "municipio": municipio,
            "chuva_mm": dados["daily"]["precipitation_sum"],
            "horas_chuva": dados["daily"]["precipitation_hours"],
            "temp_media": dados["daily"]["temperature_2m_mean"],
            "temp_max": dados["daily"]["temperature_2m_max"],
            "temp_min": dados["daily"]["temperature_2m_min"]
        })

        frames.append(df_temp)

        print(f"{len(df_temp)} registros")

    except Exception as erro:
        print(f"Erro em {municipio}")
        print(erro)

    sleep(1)

# =========================
# JUNTA TODOS OS DADOS
# =========================

if len(frames) == 0:
    print("Nenhum dado foi coletado.")
    exit()

df = pd.concat(frames, ignore_index=True)

print(f"\nTotal de registros: {len(df):,}")

# =========================
# SALVAR CSV
# =========================

arquivo_saida = PASTA_DADOS / "clima_espirito_santo_2024_2026.csv"

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo salvo com sucesso em:")
print(arquivo_saida.resolve())

print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos das colunas:")
print(df.dtypes)