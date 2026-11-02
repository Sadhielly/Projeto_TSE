import pandas as pd
import time
import multiprocessing


arquivo = r"C:\Users\sadhi\Downloads\votacao_candidato_munzona_2026\votacao_candidato_munzona_2026_SP.csv"


def processar_bloco(dados):
    uf = dados["SG_UF"].astype("string").str.strip().str.upper()
    municipio = dados["NM_MUNICIPIO"].astype("string").str.strip().str.upper()

    filtro = (uf == "SP") & (municipio == "APARECIDA D OESTE")
    dados = dados[filtro].copy()

    dados["QT_VOTOS_NOMINAIS_VALIDOS"] = pd.to_numeric(
        dados["QT_VOTOS_NOMINAIS_VALIDOS"], errors="coerce"
    )

    dados = dados.dropna(subset=["QT_VOTOS_NOMINAIS_VALIDOS"])

    soma_geral = dados["QT_VOTOS_NOMINAIS_VALIDOS"].sum()
    quantidade = dados["QT_VOTOS_NOMINAIS_VALIDOS"].count()

    partidos = dados.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS_VALIDOS"].agg(["sum", "count"])
    cargos = dados.groupby("DS_CARGO")["QT_VOTOS_NOMINAIS_VALIDOS"].agg(["sum", "count"])

    return soma_geral, quantidade, partidos.to_dict("index"), cargos.to_dict("index")


if __name__ == "__main__":
    inicio = time.perf_counter()

    arquivo_csv = pd.read_csv(
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
    )

    soma_total = 0
    quantidade_total = 0
    soma_partidos = {}
    soma_cargos = {}

    with multiprocessing.Pool() as processos:
        resultados = processos.imap(processar_bloco, arquivo_csv)

        for soma, quantidade, partidos, cargos in resultados:
            soma_total += soma
            quantidade_total += quantidade

            for partido, valores in partidos.items():
                if partido not in soma_partidos:
                    soma_partidos[partido] = [0, 0]

                soma_partidos[partido][0] += valores["sum"]
                soma_partidos[partido][1] += valores["count"]

            for cargo, valores in cargos.items():
                if cargo not in soma_cargos:
                    soma_cargos[cargo] = [0, 0]

                soma_cargos[cargo][0] += valores["sum"]
                soma_cargos[cargo][1] += valores["count"]

    media_geral = soma_total / quantidade_total

    medias_partidos = {
        partido: soma / quantidade
        for partido, (soma, quantidade) in soma_partidos.items()
    }

    medias_cargos = {
        cargo: soma / quantidade
        for cargo, (soma, quantidade) in soma_cargos.items()
    }

    maior_partido = max(medias_partidos, key=medias_partidos.get)
    maior_cargo = max(medias_cargos, key=medias_cargos.get)

    fim = time.perf_counter()

print("\n===== RESULTADOS COM MULTIPROCESSING =====")
print("Total de registros:", quantidade_total)
print("Média geral:", round(media_geral, 2))
print("Partido com maior média:", maior_partido)
print("Maior média:", round(medias_partidos[maior_partido], 2))
print("Cargo com maior média:", maior_cargo)
print("Maior média:", round(medias_cargos[maior_cargo], 2))
print("Tempo de execução com multiprocessing:", round(fim - inicio, 2), "segundos")