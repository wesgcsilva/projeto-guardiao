import platform
import psutil
import urllib.request
import json

IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import wmi

LIMIAR_CPU_CRITICO = 85.0
LIMIAR_RAM_CRITICO = 90.0
LIMIAR_TEMP_CRITICO = 85.0

def obter_sensores_avancados_lhm_web():
    """Consome a API Web JSON do LibreHardwareMonitor para altíssima precisão."""
    dados = {
        "temp_cpu": "N/A", "temp_gpu": "N/A",
        "fan_cpu_rpm": 0, "fan_gpu_rpm": 0,
        "tensao_cpu_v": "N/A", "uso_gpu": "N/A"
    }
    
    if not IS_WINDOWS:
        return dados
        
    try:
        # Acessa o Servidor Web nativo do LHM (Porta 8085)
        url = "http://localhost:8085/data.json"
        req = urllib.request.urlopen(url, timeout=2)
        json_data = json.loads(req.read().decode('utf-8'))
        
        # Função recursiva para vasculhar as "pastas" da árvore JSON
        def navegar_json(node, caminho=""):
            nome = node.get("Text", "")
            valor_str = node.get("Value", "")
            novo_caminho = f"{caminho} > [{nome}]" if nome else caminho

            # Se encontrou um valor numérico válido (ex: "520 RPM", "1,550 V")
            if valor_str and " " in valor_str:
                try:
                    # Limpa a formatação (tira unidades e troca vírgula por ponto para o Python ler)
                    val_limpo = valor_str.split(" ")[0].replace(",", ".")
                    valor_num = float(val_limpo)
                    
                    # 1. Ventoinhas (Fans)
                    if "[Fans]" in novo_caminho:
                        # Se o caminho citar Placa de Vídeo, vai pra GPU
                        if "RTX" in novo_caminho or "GeForce" in novo_caminho or "GPU" in novo_caminho:
                            if valor_num > 0 and dados["fan_gpu_rpm"] == 0:
                                dados["fan_gpu_rpm"] = int(valor_num)
                        # Caso contrário, é a ventoinha da Placa-Mãe (Processador)
                        else:
                            if valor_num > 0 and dados["fan_cpu_rpm"] == 0:
                                dados["fan_cpu_rpm"] = int(valor_num)
                                
                    # 2. Temperaturas
                    elif "[Temperatures]" in novo_caminho:
                        # Pega a temperatura central da arquitetura Ryzen
                        if "Core (Tctl/Tdie)" in nome or "CPU Package" in nome:
                            dados["temp_cpu"] = round(valor_num, 1)
                        # Pega a temperatura da GPU
                        elif "GPU Core" in nome and ("RTX" in novo_caminho or "GeForce" in novo_caminho):
                            dados["temp_gpu"] = round(valor_num, 1)
                            
                    # 3. Tensões (Voltagem)
                    elif "[Voltages]" in novo_caminho:
                        # Pega exatamente a tensão de núcleo exposta pelo chip Ryzen
                        if "Core (SVI2 TFN)" in nome or "CPU VCore" in nome:
                            dados["tensao_cpu_v"] = round(valor_num, 3)
                            
                    # 4. Uso da Placa de Vídeo (Load)
                    elif "[Load]" in novo_caminho:
                        if "GPU Core" in nome and ("RTX" in novo_caminho or "GeForce" in novo_caminho):
                            dados["uso_gpu"] = round(valor_num, 1)
                            
                except ValueError:
                    pass # Ignora caso não consiga converter para número
                    
            # Continua a busca nos sub-níveis
            for filho in node.get("Children", []):
                navegar_json(filho, novo_caminho)

        # Inicia a varredura
        navegar_json(json_data)
        
    except Exception as e:
        # Silencia erros de conexão caso o LHM seja fechado
        pass
        
    return dados

def coletar_dados_sistema():
    """Compila todos os dados para a futura Inteligência Artificial."""
    sistema = platform.system()
    versao = platform.release()
    
    uso_cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    disco_path = "C:\\" if sistema == "Windows" else "/"
    disco = psutil.disk_usage(disco_path)
    
    # Avaliação do S.M.A.R.T. via WMI (Mantido pois funciona independentemente do LHM)
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

    # Chama a nossa nova API de altíssima precisão
    sensores = obter_sensores_avancados_lhm_web()

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

    return {
        "sistema": f"{sistema} {versao}",
        "cpu_percent": uso_cpu,
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
    }