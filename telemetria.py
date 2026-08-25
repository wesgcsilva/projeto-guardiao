import platform
import psutil

# [Seção 6.1 da v1.1] Limiares de criticidade para a Filtragem na Fonte
# Se o uso ultrapassar estes valores, o sistema sinaliza uma anomalia.
LIMIAR_CPU_CRITICO = 80.0    # 80% de uso da CPU
LIMIAR_RAM_CRITICO = 85.0    # 85% de uso da RAM
LIMIAR_DISCO_CRITICO = 90.0  # 90% de uso do Disco

def coletar_dados_sistema():
    """
    [Módulo de Saúde e Diagnóstico - Seção 6.1 da v1.1]
    Realiza a coleta passiva de hardware e aplica a filtragem na fonte 
    para detecção precoce de anomalias de performance.
    """
    sistema = platform.system()
    versao = platform.release()
    
    # Coleta métricas vitais
    uso_cpu = psutil.cpu_percent(interval=1)
    
    memoria = psutil.virtual_memory()
    memoria_total_gb = round(memoria.total / (1024 ** 3), 2)
    memoria_uso_gb = round(memoria.used / (1024 ** 3), 2)
    
    disco_path = "C:\\" if sistema == "Windows" else "/"
    disco = psutil.disk_usage(disco_path)
    disco_total_gb = round(disco.total / (1024 ** 3), 2)
    disco_uso_gb = round(disco.used / (1024 ** 3), 2)
    
    # --- FILTRAGEM NA FONTE (Lógica de Anomalias) ---
    anomalia_detectada = False
    status_alerta = "NORMAL"
    
    if uso_cpu >= LIMIAR_CPU_CRITICO:
        anomalia_detectada = True
        status_alerta = "ALERTA_CPU_CRITICA"
    elif memoria.percent >= LIMIAR_RAM_CRITICO:
        anomalia_detectada = True
        status_alerta = "ALERTA_RAM_CRITICA"
    elif disco.percent >= LIMIAR_DISCO_CRITICO:
        anomalia_detectada = True
        status_alerta = "ALERTA_DISCO_CHEIO"

    # Retorna os dados enriquecidos com o estado de criticidade
    return {
        "sistema": f"{sistema} {versao}",
        "cpu_percent": uso_cpu,
        "ram_uso_gb": memoria_uso_gb,
        "ram_total_gb": memoria_total_gb,
        "ram_percent": memoria.percent,
        "disco_uso_gb": disco_uso_gb,
        "disco_total_gb": disco_total_gb,
        "disco_percent": disco.percent,
        "anomalia": anomalia_detectada,
        "status_alerta": status_alerta
    }