import time
from telemetria import coletar_dados_sistema
from correlacao import obter_eventos_criticos_software
from caixa_preta import inicializar_caixa_preta, registrar_ciclo_telemetria, consolidar_fechamento_emergencia
from analisador import exibir_relatorio_incidentes

INTERVALO_SEGUNDOS = 2

if __name__ == "__main__":
    # Limpa o log temporário da sessão anterior
    inicializar_caixa_preta()
    
    print("--- [Projeto Guardião v1.1] Núcleo Ativo ---")
    print(f"Coletando telemetria a cada {INTERVALO_SEGUNDOS}s. Pressione Ctrl + C para simular falha/encerramento.\n")
    
    try:
        while True:
            telemetria = coletar_dados_sistema()
            eventos_sw = obter_eventos_criticos_software()
            
            # Registra no buffer e no arquivo de curto prazo
            registrar_ciclo_telemetria(telemetria, eventos_sw)
            
            status_txt = f"ALERTA ({telemetria['motivo_anomalia']})" if telemetria['anomalia'] else "OK"
            print(f"[{time.strftime('%H:%M:%S')}] Status: {status_txt} | CPU: {telemetria['cpu_percent']}% | RAM: {telemetria['ram_percent']}%", end="\r")
            
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
        print("\n\n--- [Alerta do Sistema]: Interrupção detectada! Salvando caixa-preta... ---")
        
        # Consolida os últimos 5 eventos no longo prazo antes de morrer
        consolidar_fechamento_emergencia(motivo="INTERRUPCAO_MANUAL_OU_QUEDA")
        
        # Chama o analisador para exibir o relatório gerado
        exibir_relatorio_incidentes()