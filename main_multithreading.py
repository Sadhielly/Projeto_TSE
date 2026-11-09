import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def processar_bloco(dados):

    uf = dados["SG_UF"].astype("string").str.strip().str.upper()
    municipio = dados["NM_MUNICIPIO"].astype("string").str.strip().str.upper()

    filtro = (uf == "SP") & (municipio == "APARECIDA D OESTE")

    encontrados = dados[filtro].copy()

    encontrados["QT_VOTOS_NOMINAIS_VALIDOS"] = pd.to_numeric(
        encontrados["QT_VOTOS_NOMINAIS_VALIDOS"],
        errors="coerce"
    )

    encontrados = encontrados.dropna(
        subset=["QT_VOTOS_NOMINAIS_VALIDOS"]
    )

    soma_geral = encontrados["QT_VOTOS_NOMINAIS_VALIDOS"].sum()
    quantidade = len(encontrados)

    soma_partido = encontrados.groupby("SG_PARTIDO")[
        "QT_VOTOS_NOMINAIS_VALIDOS"
    ].sum().to_dict()

    quantidade_partido = encontrados.groupby("SG_PARTIDO")[
        "QT_VOTOS_NOMINAIS_VALIDOS"
    ].count().to_dict()

    soma_cargo = encontrados.groupby("DS_CARGO")[
        "QT_VOTOS_NOMINAIS_VALIDOS"
    ].sum().to_dict()

    quantidade_cargo = encontrados.groupby("DS_CARGO")[
        "QT_VOTOS_NOMINAIS_VALIDOS"
    ].count().to_dict()

    return (
        soma_geral,
        quantidade,
        soma_partido,
        quantidade_partido,
        soma_cargo,
        quantidade_cargo
    )


if __name__ == "__main__":

    inicio = time.perf_counter()

    arquivo = r"C:\Users\sadhi\Downloads\votacao_candidato_munzona_2026\votacao_candidato_munzona_2026_SP.csv"

    dados_csv = pd.read_csv(
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
    quantidade_partidos = {}

    soma_cargos = {}
    quantidade_cargos = {}

    with ThreadPoolExecutor(max_workers=4) as threads:

        resultados = threads.map(processar_bloco, dados_csv)

        for resultado in resultados:

            soma, quantidade, partidos, qtd_partidos, cargos, qtd_cargos = resultado

            soma_total += soma
            quantidade_total += quantidade

            for partido, valor in partidos.items():
                soma_partidos[partido] = soma_partidos.get(partido, 0) + valor
                quantidade_partidos[partido] = quantidade_partidos.get(partido, 0) + qtd_partidos[partido]

            for cargo, valor in cargos.items():
                soma_cargos[cargo] = soma_cargos.get(cargo, 0) + valor
                quantidade_cargos[cargo] = quantidade_cargos.get(cargo, 0) + qtd_cargos[cargo]

    media_geral = soma_total / quantidade_total

    print("MÉDIA GERAL DO MUNICÍPIO:")
    print(round(media_geral, 2))

    print("\nMÉDIA POR PARTIDO:")

    medias_partidos = {
        partido: soma_partidos[partido] / quantidade_partidos[partido]
        for partido in soma_partidos
    }

    for partido, media in medias_partidos.items():
        print(partido, round(media, 2))

    maior_partido = max(medias_partidos, key=medias_partidos.get)

    print("\nPartido com maior média:", maior_partido)
    print("Maior média:", round(medias_partidos[maior_partido], 2))

    print("\nMÉDIA POR CARGO:")

    medias_cargos = {
        cargo: soma_cargos[cargo] / quantidade_cargos[cargo]
        for cargo in soma_cargos
    }

    for cargo, media in medias_cargos.items():
        print(cargo, round(media, 2))

    maior_cargo = max(medias_cargos, key=medias_cargos.get)

    print("\nCargo com maior média:", maior_cargo)
    print("Maior média:", round(medias_cargos[maior_cargo], 2))

    fim = time.perf_counter()

    print("\nTempo de execução com multithreading:", round(fim - inicio, 2), "segundos")


    console = Console()

    tabela = Table(title="Resultados da Apuração - Multithreading", title_style="bold magenta", border_style="cyan")
    tabela.add_column("Métrica / Categoria", style="bold yellow", no_wrap=True)
    tabela.add_column("Detalhe / Vencedor", style="cyan")
    tabela.add_column("Valor / Média", justify="right", style="bold green")

    tabela.add_row("Total de Registros", "Aparecida d'Oeste - SP", f"{quantidade_total:,}".replace(",", "."))
    tabela.add_row("Média Geral de Votos", "Geral", f"{media_geral:.2f}")
    tabela.add_row("Partido com Maior Média", str(maior_partido), f"{medias_partidos[maior_partido]:.2f}")
    tabela.add_row("Cargo com Maior Média", str(maior_cargo), f"{medias_cargos[maior_cargo]:.2f}")
    tabela.add_row("Desempenho", "Tempo de Execução", f"{tempo_execucao} segundos", style="dim")

    console.print("\n")
    console.print(Panel(tabela, title="[bold green]Relatório de Desempenho (Multithreading)[/]", expand=False))
    console.print("\n")
