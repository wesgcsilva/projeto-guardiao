import json
import os

ARQUIVO_LOG_LONGO = "guardiao_longo_prazo.json"

def exibir_relatorio_incidentes(limite=3):
    if not os.path.exists(ARQUIVO_LOG_LONGO):
        print("\n[Analisador]: Nenhum incidente registrado no longo prazo.")
        return

    eventos = []
    try:
        with open(ARQUIVO_LOG_LONGO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():
                    eventos.append(json.loads(linha.strip()))
    except Exception as e:
        print(f"[Erro ao ler longo prazo]: {e}")
        return

    ultimos = eventos[-limite:]
    print(f"\n================ RELATÓRIO DA CAIXA-PRETA (Longo Prazo) ================")
    print(f"Exibindo os últimos {len(ultimos)} incidentes consolidados:\n")
    
    for inc in ultimos:
        print(f"🕒 Fechamento em: {inc.get('timestamp_fechamento')}")
        print(f"🚨 Motivo: {inc.get('motivo_fechamento')}")
        print(f"📊 Histórico dos últimos momentos antes da falha:")
        
        for reg in inc.get('ultimos_eventos_registrados', []):
            hw = reg.get('hardware', {})
            # CORREÇÃO APLICADA AQUI: Uso de string simples 'timestamp' em vez de lista
            timestamp_reg = reg.get('timestamp', 'Desconhecido')
            cpu = hw.get('cpu_percent', 0)
            ram = hw.get('ram_percent', 0)
            motivo = hw.get('motivo_anomalia', 'NORMAL')
            
            print(f"   - [{timestamp_reg}] CPU: {cpu}% | RAM: {ram}% | Status: {motivo}")
        print("-" * 65)

if __name__ == "__main__":
    exibir_relatorio_incidentes()