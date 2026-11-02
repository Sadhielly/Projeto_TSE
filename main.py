import pandas as pd

arquivo = r"C:\Users\sadhi\Downloads\votacao_candidato_munzona_2026\votacao_candidato_munzona_2026_SP.csv"

lista_dados = []

for dados in pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin-1",
    chunksize=100000,
    usecols=[
        "SG_UF",
        "NM_MUNICIPIO",
        "SG_PARTIDO",
        "DS_CARGO",
        "QT_VOTOS_NOMINAIS_VALIDOS"
    ]
):

    uf = dados["SG_UF"].astype("string").str.strip().str.upper()

    municipio = dados["NM_MUNICIPIO"].astype("string").str.strip().str.upper()

    filtro = (uf == "SP") & (municipio == "APARECIDA D OESTE")

    encontrados = dados[filtro].copy()

    lista_dados.append(encontrados)

# Juntar os registros encontrados
dados_municipio = pd.concat(lista_dados, ignore_index=True)

# Garantir que os votos sejam números
dados_municipio["QT_VOTOS_NOMINAIS_VALIDOS"] = pd.to_numeric(
    dados_municipio["QT_VOTOS_NOMINAIS_VALIDOS"],
    errors="coerce"
)

# Média geral
media_geral = dados_municipio["QT_VOTOS_NOMINAIS_VALIDOS"].mean()

# Média por partido
media_partido = dados_municipio.groupby("SG_PARTIDO")[
    "QT_VOTOS_NOMINAIS_VALIDOS"
].mean()

# Partido com maior média
melhor_partido = media_partido.idxmax()
maior_media_partido = media_partido.max()

# Média por cargo
media_cargo = dados_municipio.groupby("DS_CARGO")[
    "QT_VOTOS_NOMINAIS_VALIDOS"
].mean()

# Cargo com maior média
melhor_cargo = media_cargo.idxmax()
maior_media_cargo = media_cargo.max()

# Mostrar resultados
print("\n===== RESULTADOS DE APARECIDA D'OESTE =====")

print("\nTotal de registros:", len(dados_municipio))

print("\nMédia geral de votos:", round(media_geral, 2))

print("\nMÉDIA POR PARTIDO:")
print(media_partido)

print("\nPartido com maior média:", melhor_partido)
print("Maior média:", round(maior_media_partido, 2))

print("\nMÉDIA POR CARGO:")
print(media_cargo)

print("\nCargo com maior média:", melhor_cargo)
print("Maior média:", round(maior_media_cargo, 2))
