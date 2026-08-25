import os
import json
from datetime import datetime
from collections import deque

TAMANHO_BUFFER = 5  # Estritamente os últimos 5 eventos
ARQUIVO_TEMPO_REAL = "guardiao_log.json"
ARQUIVO_LONGO_PRAZO = "guardiao_longo_prazo.json"

# Buffer volátil na RAM para manter os últimos ciclos
buffer_volatil = deque(maxlen=TAMANHO_BUFFER)

def inicializar_caixa_preta():
    """Limpa o log de curto prazo ao iniciar o programa (começa do zero)."""
    if os.path.exists(ARQUIVO_TEMPO_REAL):
        try:
            os.remove(ARQUIVO_TEMPO_REAL)
        except Exception:
            pass

def registrar_ciclo_telemetria(dados_telemetria, eventos_software):
    """
    Grava a telemetria atual no buffer volátil da RAM 
    e atualiza o arquivo de curto prazo em tempo real.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    registro = {
        "timestamp": timestamp,
        "hardware": dados_telemetria,
        "eventos_software": eventos_software
    }
    
    # Adiciona ao buffer da RAM
    buffer_volatil.append(registro)
    
    # Escreve no log temporário de curto prazo
    with open(ARQUIVO_TEMPO_REAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro) + "\n")

def consolidar_fechamento_emergencia(motivo="ENCERRAMENTO_ABRUPTO"):
    """
    Chamado quando o sistema é interrompido ou detecta falha.
    Salva estritamente os últimos 5 eventos do buffer no Longo Prazo.
    """
    if not buffer_volatil:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    snapshot_incidente = {
        "timestamp_fechamento": timestamp,
        "motivo_fechamento": motivo,
        "ultimos_eventos_registrados": list(buffer_volatil)
    }
    
    # Salva no cofre de Longo Prazo
    with open(ARQUIVO_LONGO_PRAZO, "a", encoding="utf-8") as f:
        f.write(json.dumps(snapshot_incidente) + "\n")