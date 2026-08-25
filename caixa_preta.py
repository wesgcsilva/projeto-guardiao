import os
import json
from datetime import datetime
from collections import deque

# Configurações de resiliência e armazenamento
TAMANHO_BUFFER = 10
MAX_LINHAS_LOG = 50
ARQUIVO_LOG = "guardiao_log.json"

# [Seção 6.2 da v1.1] Memória de Curto Prazo (Buffer Cíclico na RAM)
buffer_volatil = deque(maxlen=TAMANHO_BUFFER)

def gerenciar_limpeza_log():
    """
    Gerencia o arquivo de histórico (Memória de Longo Prazo) 
    garantindo que ele não ultrapasse o limite máximo de linhas.
    """
    if not os.path.exists(ARQUIVO_LOG):
        return
        
    try:
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            
        if len(linhas) > MAX_LINHAS_LOG:
            linhas_recentes = linhas[-MAX_LINHAS_LOG:]
            with open(ARQUIVO_LOG, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(linhas_recentes)
    except Exception:
        pass

def salvar_evento_caixa_preta(dados_telemetria):
    """
    Processa os dados coletados:
    1. Adiciona o carimbo de data/hora (timestamp).
    2. Guarda no buffer volátil da RAM.
    3. Persiste de forma estruturada no arquivo JSON local.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados_telemetria["timestamp"] = agora
    
    # 1. Adiciona ao Buffer Cíclico na RAM
    buffer_volatil.append(dados_telemetria)
    
    # 2. Persiste no arquivo JSON (Memória de Longo Prazo)
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(dados_telemetria) + "\n")
        
    # 3. Executa a rotina de limpeza do arquivo
    gerenciar_limpeza_log()
    
    return agora, len(buffer_volatil)