import platform

IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import win32evtlog

def obter_eventos_criticos_software():
    """
    [Motor de Correlação] Lê o Log de Eventos do Windows (System) 
    para correlacionar falhas de software com o estado do hardware.
    """
    eventos_recentes = []
    if not IS_WINDOWS:
        return eventos_recentes

    try:
        hand = win32evtlog.OpenEventLog('localhost', 'System')
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        
        contador = 0
        for event in events:
            # EventType 1 = Erro, 2 = Aviso
            if event.EventType in [1, 2]:
                eventos_recentes.append({
                    "origem": event.SourceName,
                    "codigo": event.EventID & 0xFFFF,
                    "tipo": "ERRO" if event.EventType == 1 else "AVISO"
                })
            contador += 1
            if contador >= 3:  # Limita aos 3 mais recentes
                break
    except Exception:
        pass

    return eventos_recentes