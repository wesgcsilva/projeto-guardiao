import time
from telemetria import coletar_dados_sistema
from caixa_preta import salvar_evento_caixa_preta, TAMANHO_BUFFER

# Intervalo em segundos entre cada ciclo de monitoramento
INTERVALO_SEGUNDOS = 2

if __name__ == "__main__":
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
            
            # Pausa antes da próxima verificação
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
        print("\n--- [Projeto Guardião] Monitoramento encerrado pelo usuário. ---")