import json
import os

ARQUIVO_LOG = "guardiao_log.json"

def ler_ultimos_eventos(limite=5):
    """
    Lê o arquivo de log JSON estruturado e retorna os últimos eventos registrados.
    """
    if not os.path.exists(ARQUIVO_LOG):
        print("[Aviso]: Nenhum arquivo de log encontrado.")
        return []

    eventos = []
    try:
        # Abre o arquivo para leitura linha por linha (Padrão JSON Lines)
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():
                    # Converte cada linha de texto JSON de volta para um Dicionário Python
                    evento = json.loads(linha.strip())
                    eventos.append(evento)
    except Exception as erro:
        print(f"[Erro]: Não foi possível ler os logs. Detalhes: {erro}")
        return []

    # Retorna apenas a quantidade solicitada dos eventos mais recentes
    return eventos[-limite:]

if __name__ == "__main__":
    print("--- [Projeto Guardião] Módulo Analisador de Logs ---")
    
    # Define quantos eventos recentes deseja consultar
    quantidade = 5
    ultimos_registros = ler_ultimos_eventos(quantidade)
    
    if ultimos_registros:
        print(f"\nExibindo os últimos {len(ultimos_registros)} registros salvos na caixa-preta:\n")
        for ev in ultimos_registros:
            print(f"🕒 [{ev['timestamp']}]")
            print(f"   💻 Sistema: {ev['sistema']}")
            print(f"   🔥 CPU: {ev['cpu_percent']}%")
            print(f"   🧠 RAM: {ev['ram_uso_gb']}GB / {ev['ram_total_gb']}GB ({ev['ram_percent']}%)")
            print(f"   💾 Disco C: {ev['disco_uso_gb']}GB ({ev['disco_percent']}%)")
            print("-" * 50)
    else:
        print("Nenhum dado disponível para análise no momento.")