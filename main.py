import time
import os
from telemetria import coletar_dados_sistema
from correlacao import obter_eventos_criticos_software
from caixa_preta import (
    inicializar_caixa_preta, 
    registrar_ciclo_telemetria, 
    consolidar_fechamento_emergencia
)
from analisador import exibir_relatorio_incidentes

INTERVALO_SEGUNDOS = 2

def limpar_tela():
    """Limpa o terminal independentemente do Sistema Operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    inicializar_caixa_preta()
    
    try:
        while True:
            telemetria = coletar_dados_sistema()
            eventos_sw = obter_eventos_criticos_software()
            registrar_ciclo_telemetria(telemetria, eventos_sw)
            
            if telemetria['anomalia']:
                status_txt = f"🔴 CRÍTICO ({telemetria['motivo_anomalia']})"
            elif eventos_sw:
                status_txt = "🟡 ATENÇÃO (Avisos detectados)"
            else:
                status_txt = "🟢 NORMAL"

            hora = time.strftime('%H:%M:%S')
            
            limpar_tela()
            print("--- [Projeto Guardião v1.1] Dashboard Avançado de Diagnóstico ---")
            print(f"Atualizado às: {hora} | Status do Sistema: {status_txt}")
            print("=" * 65)
            
            print("[🖥️  PROCESSADOR (CPU)]")
            print(f"Uso: {telemetria['cpu_percent']}% | Temp: {telemetria['temp_cpu_celsius']}°C | Fan: {telemetria['fan_cpu_rpm']} RPM | Tensão: {telemetria['tensao_cpu_v']} V")
            print("-" * 65)
            
            print("[🎮 PLACA DE VÍDEO (GPU)]")
            print(f"Uso: {telemetria['uso_gpu_percent']}% | Temp: {telemetria['temp_gpu_celsius']}°C | Fan: {telemetria['fan_gpu_rpm']} RPM")
            print("-" * 65)
            
            print("[🧠 MEMÓRIA E 💾 DISCO]")
            print(f"RAM Uso: {telemetria['ram_percent']}% ({telemetria['ram_uso_gb']} GB / {telemetria['ram_total_gb']} GB)")
            print(f"Disco Uso: {telemetria['disco_percent']}% | S.M.A.R.T: {telemetria['smart_status']}")
            print("=" * 65)
            
            # Preview Detalhado de Alertas do Windows
            if eventos_sw:
                print(f"⚠️ Alertas do Windows: {len(eventos_sw)} encontrados.")
                for ev in eventos_sw:
                    tipo_ev = ev.get('tipo', 'AVISO').upper()
                    codigo = ev.get('codigo', 'N/A')
                    origem = ev.get('origem', 'Desconhecida')
                    icone = "🔴" if tipo_ev == "ERRO" else "🟡"
                    print(f"   {icone} [{hora}] {tipo_ev} - Código: {codigo} | Origem: {origem}")
                print("=" * 65)
            else:
                print("✅ Nenhum alerta crítico de software detectado no ciclo atual.")
                print("=" * 65)
            
            print("\nPressione Ctrl + C para simular falha e abrir o Relatório da Caixa-Preta.")
            
            time.sleep(INTERVALO_SEGUNDOS)
            
    except KeyboardInterrupt:
        limpar_tela()
        print("\n\n--- [Alerta do Sistema]: Interrupção detectada! Salvando caixa-preta... ---")
        consolidar_fechamento_emergencia(motivo="INTERRUPCAO_MANUAL_OU_QUEDA")
        exibir_relatorio_incidentes()