import platform
import psutil

<<<<<<< Updated upstream
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
=======
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import wmi

LIMIAR_CPU_CRITICO = 85.0
LIMIAR_RAM_CRITICO = 90.0
LIMIAR_TEMP_CRITICO = 85.0

def obter_sensores_avancados_ohm():
    """Busca inteligente de sensores, lidando com variações de nomes das Placas-Mãe."""
    dados_ohm = {
        "temp_cpu": "N/A", "temp_gpu": "N/A",
        "fan_cpu_rpm": 0, "fan_gpu_rpm": 0,
        "tensao_cpu_v": "N/A", "uso_gpu": "N/A"
    }
    
    if not IS_WINDOWS:
        return dados_ohm
        
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        for sensor in w.Sensor():
            nome = sensor.Name.upper()
            tipo = sensor.SensorType.upper()
            
            # 1. Temperaturas
            if tipo == "TEMPERATURE":
                if "CPU" in nome and dados_ohm["temp_cpu"] == "N/A":
                    dados_ohm["temp_cpu"] = round(sensor.Value, 1)
                elif "GPU" in nome and dados_ohm["temp_gpu"] == "N/A":
                    dados_ohm["temp_gpu"] = round(sensor.Value, 1)
                    
            # 2. Ventoinhas (Ampliamos a busca para FAN #1, FAN #2, etc.)
            elif tipo == "FAN":
                if ("CPU" in nome or "FAN #1" in nome or "FAN #2" in nome) and dados_ohm["fan_cpu_rpm"] == 0:
                    dados_ohm["fan_cpu_rpm"] = int(sensor.Value)
                elif "GPU" in nome and dados_ohm["fan_gpu_rpm"] == 0:
                    dados_ohm["fan_gpu_rpm"] = int(sensor.Value)
                    
            # 3. Voltagem (Buscando por VCORE além de CPU)
            elif tipo == "VOLTAGE":
                if ("CPU" in nome or "VCORE" in nome) and dados_ohm["tensao_cpu_v"] == "N/A":
                    dados_ohm["tensao_cpu_v"] = round(sensor.Value, 3)
            
            # 4. Uso da GPU (LOAD)
            elif tipo == "LOAD":
                if "GPU CORE" in nome and dados_ohm["uso_gpu"] == "N/A":
                    dados_ohm["uso_gpu"] = round(sensor.Value, 1)
                    
    except Exception:
        pass

    return dados_ohm

def coletar_dados_sistema():
    """Compila todos os dados para a futura Inteligência Artificial."""
>>>>>>> Stashed changes
    sistema = platform.system()
    versao = platform.release()
    
    # Coleta métricas vitais
    uso_cpu = psutil.cpu_percent(interval=1)
    
    memoria = psutil.virtual_memory()
<<<<<<< Updated upstream
    memoria_total_gb = round(memoria.total / (1024 ** 3), 2)
    memoria_uso_gb = round(memoria.used / (1024 ** 3), 2)
    
=======
>>>>>>> Stashed changes
    disco_path = "C:\\" if sistema == "Windows" else "/"
    disco = psutil.disk_usage(disco_path)
    disco_total_gb = round(disco.total / (1024 ** 3), 2)
    disco_uso_gb = round(disco.used / (1024 ** 3), 2)
    
<<<<<<< Updated upstream
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
=======
    smart_status = "NAO_SUPORTADO"
    if IS_WINDOWS:
        try:
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                if hasattr(disk, 'Status') and disk.Status:
                    smart_status = disk.Status
                    break
        except Exception:
            smart_status = "INDISPONIVEL"

    # Injetando o radar OHM
    sensores = obter_sensores_avancados_ohm()

    anomalia = False
    motivo = "NORMAL"
    
    if uso_cpu >= LIMIAR_CPU_CRITICO:
        anomalia = True
        motivo = "CPU_CRITICA"
    elif isinstance(sensores["temp_cpu"], (int, float)) and sensores["temp_cpu"] >= LIMIAR_TEMP_CRITICO:
        anomalia = True
        motivo = "TEMPERATURA_CRITICA"
    elif memoria.percent >= LIMIAR_RAM_CRITICO:
        anomalia = True
        motivo = "RAM_CRITICA"
    elif smart_status not in ["OK", "NAO_SUPORTADO"]:
        anomalia = True
        motivo = "ALERTA_SMART_DISCO"
>>>>>>> Stashed changes

    # Retorna os dados enriquecidos com o estado de criticidade
    return {
        "sistema": f"{sistema} {versao}",
        "cpu_percent": uso_cpu,
<<<<<<< Updated upstream
        "ram_uso_gb": memoria_uso_gb,
        "ram_total_gb": memoria_total_gb,
        "ram_percent": memoria.percent,
        "disco_uso_gb": disco_uso_gb,
        "disco_total_gb": disco_total_gb,
        "disco_percent": disco.percent,
        "anomalia": anomalia_detectada,
        "status_alerta": status_alerta
=======
        "ram_percent": memoria.percent,
        "ram_uso_gb": round(memoria.used / (1024 ** 3), 2),
        "ram_total_gb": round(memoria.total / (1024 ** 3), 2),
        "disco_percent": disco.percent,
        "smart_status": smart_status,
        "temp_cpu_celsius": sensores["temp_cpu"],
        "fan_cpu_rpm": sensores["fan_cpu_rpm"],
        "tensao_cpu_v": sensores["tensao_cpu_v"],
        "uso_gpu_percent": sensores["uso_gpu"],
        "temp_gpu_celsius": sensores["temp_gpu"],
        "fan_gpu_rpm": sensores["fan_gpu_rpm"],
        "anomalia": anomalia,
        "motivo_anomalia": motivo
>>>>>>> Stashed changes
    }