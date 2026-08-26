import urllib.request
import json

def buscar_sensores_lhm_json(no, caminho=""):
    """
    Função recursiva para navegar na árvore de dados JSON do LHM.
    Se encontrar um valor numérico, imprime na tela.
    """
    nome = no.get("Text", "")
    valor = no.get("Value", "")
    
    # Se o nó tiver um valor, é um sensor final! Vamos imprimir de forma legível.
    if valor:
        print(f"👉 {caminho} {nome:<20} | VALOR: {valor}")
        
    # Se tiver "filhos" (Children), entra neles para continuar a busca (Recursão)
    for filho in no.get("Children", []):
        # Vai guardando o caminho (ex: Desktop > Placa-Mãe > Fan)
        novo_caminho = f"{caminho} [{nome}] >" if nome else caminho
        buscar_sensores_lhm_json(filho, novo_caminho)

def rastrear_servidor_web():
    """Conecta ao servidor web embutido do LibreHardwareMonitor."""
    print("🔍 TESTANDO CONEXÃO COM O SERVIDOR WEB DO LHM...\n")
    print("=" * 80)
    
    url = "http://localhost:8085/data.json"
    
    try:
        # Faz a requisição GET para a porta 8085
        resposta = urllib.request.urlopen(url, timeout=3)
        
        # Converte a resposta de texto puro para um Dicionário Python
        dados_json = json.loads(resposta.read().decode('utf-8'))
        
        print("✅ Conexão Web bem-sucedida! Lendo a árvore de hardware:\n")
        buscar_sensores_lhm_json(dados_json)
        
    except Exception as e:
        print("❌ Falha de conexão com o Servidor Web do LHM.")
        print(f"Detalhe do erro: {e}")
        print("\nSolução: No LHM, vá em 'Options' e marque a opção 'Run Web Server'.")
        
    print("=" * 80)

if __name__ == "__main__":
    rastrear_servidor_web()