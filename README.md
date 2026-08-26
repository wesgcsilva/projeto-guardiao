# 🛡️ Projeto Guardião (v1.1)

O **Projeto Guardião** é um software de monitoramento de hardware, correlação de software e diagnóstico de falhas para computadores pessoais. Atuando como uma verdadeira "caixa-preta", ele registra a saúde do sistema em tempo real e analisa eventos críticos para antecipar problemas.

---

## 🚀 Funcionalidades Principais
- **Telemetria via API Web:** Leitura precisa de temperatura, uso, tensões (VCore) e ventoinhas através do servidor local do *LibreHardwareMonitor*.
- **Correlação de Eventos do Windows:** Captura e categoriza logs do sistema (como erros e avisos do Visualizador de Eventos).
- **Sistema de Caixa-Preta:** Buffer rotativo em memória e persistência de longo prazo para rastrear o exato momento antes de uma falha ou interrupção.
- **Módulo Analisador:** Exibe relatórios detalhados com sumário estatístico dos incidentes e códigos de erro.

---

## 📂 Estrutura Modular do Código
A versão atual está organizada nos seguintes módulos independentes:

```text
projeto-guardiao/
│
├── main.py             # Orquestrador central (loop contínuo e dashboard)
├── telemetria.py       # Coleta de hardware via API JSON do LibreHardwareMonitor
├── correlacao.py       # Leitura e filtragem de eventos do Visualizador do Windows
├── caixa_preta.py      # Gestão do buffer volátil e persistência em JSON
├── analisador.py       # Exibição do relatório pós-falha e sumário estatístico
└── README.md           # Documentação oficial do projeto
```

## Projeto desenvolvido como uma iniciativa de software autoral para gestão proativa e resiliência de sistemas computacionais.
👨‍💻 Autor:  Weslley Gualberto do Carmo Silva
