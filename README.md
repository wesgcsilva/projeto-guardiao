# 🛡️ Projeto Guardião (v1.1)

O **Projeto Guardião** é um software de monitoramento avançado, diagnóstico e segurança para computadores pessoais. Sua missão é desmistificar as falhas de hardware e software, oferecendo aos usuários uma compreensão clara e acionável sobre a saúde de seus sistemas, atuando como uma verdadeira "caixa-preta" para o PC.

---

## 🚀 Sobre o Projeto
Computadores modernos são ecossistemas complexos propensos a reinicializações inesperadas, telas azuis (BSOD) e degradação de performance. Ferramentas nativas costumam ser crípticas e focadas em dados brutos e difíceis de interpretar. O Guardião preenche essa lacuna unificando:
- **Monitoramento Passivo de Saúde:** Acompanhamento contínuo de CPU, Memória RAM e Armazenamento.
- **Resiliência de Dados (Caixa-Preta):** Buffer em memória volátil (RAM) e persistência estruturada em formato JSON com rotação automática de logs.
- **Arquitetura Modular:** Separação limpa entre a coleta de dados, a gestão da caixa-preta e a execução principal.

---

## 📂 Estrutura Modular do Código
A versão atual (`v1.1`) está organizada em módulos independentes para garantir alta manutenibilidade e escalabilidade:

```text
projeto-guardiao/
│
├── main.py             # Orquestrador central (executa o loop contínuo)
├── telemetria.py       # Módulo de coleta passiva de dados de hardware
├── caixa_preta.py      # Gestão do buffer volátil (RAM) e logs JSON
├── .gitignore          # Arquivos e pastas ignoradas pelo Git
└── README.md           # Documentação oficial do projeto
```

