import platform
import psutil

IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import wmi

# Limiares de criticidade (Filtragem na Fonte)
LIMIAR_CPU_CRITICO = 85.0
LIMIAR_RAM_CRITICO = 90.0

def coletar_dados_sistema():
    """
    [Módulo de Saúde] Coleta métricas de CPU, RAM, Discos e status S.M.A.R.T. via WMI.
    """
    sistema = platform.system()
    versao = platform.release()
    
    uso_cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    
    disco_path = "C:\\" if sistema == "Windows" else "/"
    disco = psutil.disk_usage(disco_path)
    
    # Consulta de Hardware Avançada (S.M.A.R.T. via WMI)
    smart_status = "NÃO_SUPORTADO_OU_NAO_WINDOWS"
    if IS_WINDOWS:
        try:
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                if hasattr(disk, 'Status') and disk.Status:
                    smart_status = disk.Status
                    break
        except Exception:
            smart_status = "INDISPONIVEL_WMI"

    # Lógica de anomalia na fonte
    anomalia = False
    motivo = "NORMAL"
    
    if uso_cpu >= LIMIAR_CPU_CRITICO:
        anomalia = True
        motivo = "CPU_CRITICA"
    elif memoria.percent >= LIMIAR_RAM_CRITICO:
        anomalia = True
        motivo = "RAM_CRITICA"
    elif smart_status not in ["OK", "NÃO_SUPORTADO_OU_NAO_WINDOWS"]:
        anomalia = True
        motivo = "ALERTA_SMART_DISCO"

    return {
        "sistema": f"{sistema} {versao}",
        "cpu_percent": uso_cpu,
        "ram_uso_gb": round(memoria.used / (1024 ** 3), 2),
        "ram_total_gb": round(memoria.total / (1024 ** 3), 2),
        "ram_percent": memoria.percent,
        "disco_percent": disco.percent,
        "smart_status": smart_status,
        "anomalia": anomalia,
        "motivo_anomalia": motivo
    }