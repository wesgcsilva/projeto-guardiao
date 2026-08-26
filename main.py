import time
import os
from telemetria import coletar_dados_sistema
from caixa_preta import salvar_evento_caixa_preta, TAMANHO_BUFFER

# Intervalo em segundos entre cada ciclo de monitoramento
INTERVALO_SEGUNDOS = 2

def limpar_tela():
    """Limpa o terminal independentemente do Sistema Operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
<<<<<<< Updated upstream
    print("--- [Projeto Guardião v1.1] Núcleo Modular Iniciado ---")
    print("Pressione Ctrl + C no terminal para encerrar o programa a qualquer momento.\n")
    
    try:
        while True:
            # 1. Executa o Estágio 1: Coleta de Telemetria
            dados_atuais = coletar_dados_sistema()
            
            # 2. Executa a resiliência (Buffer e Persistência na Caixa-Preta)
            timestamp, eventos_no_buffer = salvar_evento_caixa_preta(dados_atuais)
            
            # 3. Exibe o resumo no terminal de forma amigável
            print(f"[{timestamp}] - CPU: {dados_atuais['cpu_percent']}% | RAM: {dados_atuais['ram_uso_gb']}GB ({dados_atuais['ram_percent']}%) | Disco: {dados_atuais['disco_uso_gb']}GB")
            print(f"   [Buffer RAM]: {eventos_no_buffer}/{TAMANHO_BUFFER} eventos estruturados em memória.")
=======
    inicializar_caixa_preta()
    
    try:
        while True:
            telemetria = coletar_dados_sistema()
            eventos_sw = obter_eventos_criticos_software()
            registrar_ciclo_telemetria(telemetria, eventos_sw)
            
            status_txt = f"🚨 {telemetria['motivo_anomalia']}" if telemetria['anomalia'] else "✅ NORMAL"
            hora = time.strftime('%H:%M:%S')
            
            # Limpa a tela e desenha o novo painel
            limpar_tela()
            print("--- [Projeto Guardião v1.1] Dashboard Avançado de Diagnóstico ---")
            print(f"Atualizado às: {hora} | Status do Sistema: {status_txt}")
            print("=" * 65)
            
            print("[🖥️  PROCESSADOR (CPU)]")
            print(f"Uso: {telemetria['cpu_percent']}% | Temp: {telemetria['temp_cpu_celsius']}°C | Fan: {telemetria['fan_cpu_rpm']} RPM | Tensão: {telemetria['tensao_cpu_v']} V")
            print("-" * 65)
            
            print("[🎮 PLACA DE VÍDEO (GPU)]")
            print(f"Uso: {telemetria['uso_gpu_percent']}% | Temp: {telemetria['temp_gpu_celsius']}°C | Fan: {telemetria['fan_gpu_rpm']} RPM")
            print("-" * 65)
            
            print("[🧠 MEMÓRIA E 💾 DISCO]")
            print(f"RAM Uso: {telemetria['ram_percent']}% ({telemetria['ram_uso_gb']} GB / {telemetria['ram_total_gb']} GB)")
            print(f"Disco Uso: {telemetria['disco_percent']}% | S.M.A.R.T: {telemetria['smart_status']}")
            print("=" * 65)
            
            if eventos_sw:
                print(f"⚠️ Alertas do Windows: {len(eventos_sw)} encontrados.")
            
            print("\nPressione Ctrl + C para simular falha e abrir o Relatório da Caixa-Preta.")
>>>>>>> Stashed changes
            
            # Pausa antes da próxima verificação
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
<<<<<<< Updated upstream
        print("\n--- [Projeto Guardião] Monitoramento encerrado pelo usuário. ---")
=======
        limpar_tela()
        print("\n\n--- [Alerta do Sistema]: Interrupção detectada! Salvando caixa-preta... ---")
        consolidar_fechamento_emergencia(motivo="INTERRUPCAO_MANUAL_OU_QUEDA")
        exibir_relatorio_incidentes()
>>>>>>> Stashed changes
