import json
import os

ARQUIVO_LOG = "guardiao_log.json"

def ler_ultimos_eventos(limite=5):
    """
    Lê o arquivo de log JSON estruturado e retorna os últimos eventos registrados,
    incluindo os dados de anomalia gerados pela filtragem na fonte.
    """
    if not os.path.exists(ARQUIVO_LOG):
        print("[Aviso]: Nenhum arquivo de log encontrado. Execute o 'main.py' primeiro.")
        return []

    eventos = []
    try:
        # Abre o arquivo de log linha por linha (JSON Lines)
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():
                    # Converte o texto JSON de volta para dicionário Python
                    evento = json.loads(linha.strip())
                    eventos.append(evento)
    except Exception as erro:
        print(f"[Erro]: Não foi possível ler os logs. Detalhes: {erro}")
        return []

<<<<<<< Updated upstream
    # Retorna apenas a quantidade solicitada dos eventos mais recentes
    return eventos[-limite:]
=======
    ultimos = eventos[-limite:]
    print(f"\n================ RELATÓRIO DA CAIXA-PRETA (Longo Prazo) ================")
    print(f"Exibindo os últimos {len(ultimos)} incidentes consolidados:\n")
    
    for inc in ultimos:
        print(f"🕒 Fechamento em: {inc.get('timestamp_fechamento')}")
        print(f"🚨 Motivo: {inc.get('motivo_fechamento')}")
        print(f"📊 Histórico dos últimos momentos antes da falha:")
        
        for reg in inc.get('ultimos_eventos_registrados', []):
            hw = reg.get('hardware', {})
            timestamp_reg = reg.get('timestamp', 'Desconhecido')
            
            # Buscando as métricas no JSON
            cpu = hw.get('cpu_percent', 0)
            ram = hw.get('ram_percent', 0)
            temp = hw.get('temp_cpu_celsius', 'N/A') # Pega a temperatura ou mostra N/A
            motivo = hw.get('motivo_anomalia', 'NORMAL')
            
            # Exibição atualizada e alinhada
            print(f"   - [{timestamp_reg}] CPU: {cpu}% | Temp: {temp}°C | RAM: {ram}% | Status: {motivo}")
        print("-" * 65)
>>>>>>> Stashed changes

if __name__ == "__main__":
    print("--- [Projeto Guardião] Módulo Analisador de Logs & Anomalias ---")
    
    # Define quantos eventos recentes deseja consultar
    quantidade = 5
    ultimos_registros = ler_ultimos_eventos(quantidade)
    
    if ultimos_registros:
        print(f"\nExibindo os últimos {len(ultimos_registros)} registros da caixa-preta:\n")
        for ev in ultimos_registros:
            # Verifica se o evento possui os dados de anomalia (compatibilidade com logs antigos)
            anomalia = ev.get('anomalia', False)
            status = ev.get('status_alerta', 'NORMAL')
            
            # Formata a exibição do status visualmente
            if anomalia:
                status_formatado = f"🚨 ALERTA CRÍTICO: {status}"
            else:
                status_formatado = f"✅ Status: {status}"
            
            print(f"🕒 [{ev['timestamp']}] | {status_formatado}")
            print(f"   💻 Sistema: {ev['sistema']}")
            print(f"   🔥 CPU: {ev['cpu_percent']}%")
            print(f"   🧠 RAM: {ev['ram_uso_gb']}GB / {ev['ram_total_gb']}GB ({ev['ram_percent']}%)")
            print(f"   💾 Disco C: {ev['disco_uso_gb']}GB ({ev['disco_percent']}%)")
            print("-" * 60)
    else:
        print("Nenhum dado disponível para análise no momento.")