import json
import os

ARQUIVO_LOG_LONGO = "guardiao_longo_prazo.json"

def exibir_relatorio_incidentes(limite=3):
    """
    [Módulo de Análise] Lê o log de longo prazo e exibe os incidentes.
    Agora inclui a origem do erro e um resumo estatístico das falhas.
    """
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
        
        # Dicionário para contabilizar os erros
        resumo_alertas = {} 
        
        for reg in inc.get('ultimos_eventos_registrados', []):
            hw = reg.get('hardware', {})
            sw = reg.get('eventos_software', [])
            timestamp_reg = reg.get('timestamp', 'Desconhecido')
            
            cpu = hw.get('cpu_percent', 0)
            temp = hw.get('temp_cpu_celsius', 'N/A')
            ram = hw.get('ram_percent', 0)
            motivo_hw = hw.get('motivo_anomalia', 'NORMAL')
            
            alertas_txt = ""
            if sw:
                lista_alertas = []
                for ev in sw:
                    tipo = ev.get('tipo', 'AVISO').upper()
                    codigo = ev.get('codigo', 'N/A')
                    origem = ev.get('origem', 'N/A')
                    icone = "🔴" if tipo == "ERRO" else "🟡"
                    
                    # Formata a string com Código e Origem
                    alerta_formatado = f"{icone} {tipo} {codigo} ({origem})"
                    lista_alertas.append(alerta_formatado)
                    
                    # Contabiliza no resumo
                    resumo_alertas[alerta_formatado] = resumo_alertas.get(alerta_formatado, 0) + 1
                    
                alertas_txt = f" | Sw_Alerta: {', '.join(lista_alertas)}"
            
            print(f"   - [{timestamp_reg}] CPU: {cpu}% | Temp: {temp}°C | RAM: {ram}% | Hw_Status: {motivo_hw}{alertas_txt}")
        
        # Exibe o Quadro de Resumo se houver alertas
        if resumo_alertas:
            print(f"\n   📋 RESUMO DE ALERTAS DE SOFTWARE NESTE INCIDENTE:")
            for alerta, qtd in resumo_alertas.items():
                print(f"      -> {alerta}: {qtd} ocorrência(s)")
                
        print("-" * 65)

if __name__ == "__main__":
    exibir_relatorio_incidentes()