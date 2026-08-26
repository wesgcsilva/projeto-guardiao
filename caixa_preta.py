import os
import json
import time

ARQUIVO_LOG_CURTO = "guardiao_log.json"
ARQUIVO_LOG_LONGO = "guardiao_longo_prazo.json"
LIMITE_BUFFER = 5  # Mantém os últimos 5 ciclos em memória antes de uma queda

def inicializar_caixa_preta():
    """
    [Caixa-Preta] Prepara o arquivo de log de curto prazo no início da execução.
    Equivalente a instanciar/limpar o buffer de gravação inicial.
    """
    try:
        with open(ARQUIVO_LOG_CURTO, "w", encoding="utf-8") as arquivo:
            pass  # Cria ou limpa o arquivo deixando-o pronto para receber dados
    except Exception as e:
        print(f"[Erro ao inicializar caixa-preta]: {e}")

def registrar_ciclo_telemetria(telemetria, eventos_software):
    """
    [Caixa-Preta] Salva o ciclo atual de hardware e software no buffer de curto prazo.
    Usa uma lista rotativa para guardar apenas os momentos mais recentes.
    """
    registro = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "hardware": telemetria,
        "eventos_software": eventos_software
    }
    
    # Lê os registros atuais do arquivo curto
    linhas = []
    if os.path.exists(ARQUIVO_LOG_CURTO):
        try:
            with open(ARQUIVO_LOG_CURTO, "r", encoding="utf-8") as f:
                linhas = [json.loads(line.strip()) for line in f if line.strip()]
        except Exception:
            linhas = []
            
    # Adiciona o novo registro no final
    linhas.append(registro)
    
    # Se passar do limite, remove o mais antigo (mantém os últimos N ciclos)
    if len(linhas) > LIMITE_BUFFER:
        linhas = linhas[-LIMITE_BUFFER:]
        
    # Salva de volta no arquivo de curto prazo
    try:
        with open(ARQUIVO_LOG_CURTO, "w", encoding="utf-8") as f:
            for item in linhas:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[Erro ao gravar log curto]: {e}")

def consolidar_fechamento_emergencia(motivo="INTERRUPCAO_MANUAL_OU_QUEDA"):
    """
    [Caixa-Preta] Executado na interrupção (Ctrl+C ou queda). 
    Transfere o buffer volátil para o histórico permanente de longo prazo.
    """
    linhas_curtas = []
    if os.path.exists(ARQUIVO_LOG_CURTO):
        try:
            with open(ARQUIVO_LOG_CURTO, "r", encoding="utf-8") as f:
                linhas_curtas = [json.loads(line.strip()) for line in f if line.strip()]
        except Exception:
            linhas_curtas = []
            
    if not linhas_curtas:
        return
        
    incidente = {
        "timestamp_fechamento": time.strftime('%Y-%m-%d %H:%M:%S'),
        "motivo_fechamento": motivo,
        "ultimos_eventos_registrados": linhas_curtas
    }
    
    # Grava o incidente consolidado no arquivo de longo prazo
    try:
        with open(ARQUIVO_LOG_LONGO, "a", encoding="utf-8") as f:
            f.write(json.dumps(incidente, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[Erro ao consolidar longo prazo]: {e}")