import platform
import psutil

def coletar_dados_sistema():
    """
    [Módulo de Saúde e Diagnóstico - Seção 6.1 da v1.1]
    Responsável pela coleta passiva e não intrusiva dos dados de hardware e sistema.
    """
    sistema = platform.system()
    versao = platform.release()
    
    # Coleta o uso atual da CPU em porcentagem
    uso_cpu = psutil.cpu_percent(interval=1)
    
    # Coleta informações sobre a Memória RAM
    memoria = psutil.virtual_memory()
    memoria_total_gb = round(memoria.total / (1024 ** 3), 2)
    memoria_uso_gb = round(memoria.used / (1024 ** 3), 2)
    
    # Coleta informações sobre o Disco Principal (C: no Windows ou / no Linux)
    disco_path = "C:\\" if sistema == "Windows" else "/"
    disco = psutil.disk_usage(disco_path)
    disco_total_gb = round(disco.total / (1024 ** 3), 2)
    disco_uso_gb = round(disco.used / (1024 ** 3), 2)
    
    # Retorna os dados estruturados em formato de dicionário
    return {
        "sistema": f"{sistema} {versao}",
        "cpu_percent": uso_cpu,
        "ram_uso_gb": memoria_uso_gb,
        "ram_total_gb": memoria_total_gb,
        "ram_percent": memoria.percent,
        "disco_uso_gb": disco_uso_gb,
        "disco_total_gb": disco_total_gb,
        "disco_percent": disco.percent
    }