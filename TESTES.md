# 🧪 Relatório de Testes: Projeto Guardião v1.1

## Teste 01: Captura de Falha Crítica e Caixa-Preta
* **Data:** 25 de Agosto de 2026
* **Objetivo:** Validar se o motor de correlação captura eventos de erro do Windows em tempo real e se a dupla memória salva o histórico volátil (últimos 5 ciclos) durante uma interrupção abrupta.
* **Método (Mocking Profissional):** Utilização de um script paralelo (`simulador_falhas.py`) rodando como Administrador para injetar o Event ID 9999 diretamente no log `System` do Windows, sem alterar o código de produção. O `main.py` foi interrompido manualmente após a injeção.
* **Resultado Esperado:** O módulo analisador deve exibir o erro forjado e o estado da CPU/RAM dos instantes exatos antes da falha.
* **Status:** ✅ SUCESSO. A caixa-preta isolou o evento e gravou o snapshot perfeitamente no arquivo persistente `guardiao_longo_prazo.json`.