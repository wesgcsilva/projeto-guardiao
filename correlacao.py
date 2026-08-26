import platform

# Importa a biblioteca de eventos do Windows apenas se o SO for Windows
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import win32evtlog

def obter_eventos_criticos_software():
    """
    [Motor de Correlação] Lê os logs recentes do Windows (System e Application)
    e filtra eventos críticos ou avisos para análise do Guardião.
    """
    eventos_encontrados = []
    
    if not IS_WINDOWS:
        return eventos_encontrados

    servidor = 'localhost'
    tipos_logs = ['System', 'Application']
    
    try:
        for tipo_log in tipos_logs:
            # Abre o visualizador de eventos do Windows de forma segura
            mao = win32evtlog.OpenEventLog(servidor, tipo_log)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            # Lê os registros mais recentes
            registros = win32evtlog.ReadEventLog(mao, flags, 0)
            
            for reg in registros[:3]: # Analisa os 3 mais recentes de cada log para poupar processamento
                codigo_evento = reg.EventID & 0xFFFF
                origem = reg.SourceName
                
                # Traduz o tipo de severidade do Windows
                tipo_str = "INFO"
                if reg.EventType == win32evtlog.EVENTLOG_ERROR_TYPE:
                    tipo_str = "ERRO"
                elif reg.EventType == win32evtlog.EVENTLOG_WARNING_TYPE:
                    tipo_str = "AVISO"
                else:
                    continue # Descarta logs puramente informativos para manter o painel limpo
                
                # Estrutura o evento padronizado para a nossa Caixa-Preta
                eventos_encontrados.append({
                    "origem": str(origem),
                    "codigo": int(codigo_evento),
                    "tipo": str(tipo_str)
                })
                
    except Exception:
        # Evita que falhas de permissão no log do Windows quebrem o ciclo principal
        pass
        
    # Retorna uma lista enxuta contendo apenas os eventos mais relevantes do ciclo
    return eventos_encontrados[:2]