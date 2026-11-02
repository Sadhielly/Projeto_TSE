import subprocess
import sys
import re

print("===== EXECUTANDO MULTIPROCESSING =====\n")

resultado_processos = subprocess.run(
    [sys.executable, "main_multiprocessing.py"],
    capture_output=True,
    text=True
)

print(resultado_processos.stdout)

if resultado_processos.returncode != 0:
    print("Erro ao executar multiprocessing:")
    print(resultado_processos.stderr)
    sys.exit(1)


print("\n===== EXECUTANDO MULTITHREADING =====\n")

resultado_threads = subprocess.run(
    [sys.executable, "main_multithreading.py"],
    capture_output=True,
    text=True
)

print(resultado_threads.stdout)

if resultado_threads.returncode != 0:
    print("Erro ao executar multithreading:")
    print(resultado_threads.stderr)
    sys.exit(1)


tempo_processos = float(
    re.search(
        r"Tempo de execução com multiprocessing:\s*([\d.]+)",
        resultado_processos.stdout
    ).group(1)
)

tempo_threads = float(
    re.search(
        r"Tempo de execução com multithreading:\s*([\d.]+)",
        resultado_threads.stdout
    ).group(1)
)


print("\n===== COMPARAÇÃO DE DESEMPENHO =====")

print("Multiprocessing:", tempo_processos, "segundos")
print("Multithreading:", tempo_threads, "segundos")

if tempo_processos < tempo_threads:
    print("\nMelhor desempenho: Multiprocessing")

elif tempo_threads < tempo_processos:
    print("\nMelhor desempenho: Multithreading")

else:
    print("\nAs duas abordagens tiveram o mesmo tempo.")
