import subprocess
import ctypes
import sys

def verificar_admin():
    """Verifica se o script está rodando com privilégios de Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def injetar_erro_sistema_root():
    """
    [Mocking Profissional] Solicita elevação de privilégios e injeta 
    um erro diretamente no log 'System' do Windows sem alterar a produção.
    """
    if not verificar_admin():
        print("⚠️ Requisito Profissional: Para injetar na raiz do log 'System', precisamos de Administrador.")
        print("🔄 Solicitando elevação de privilégios ao Windows...")
        # Reexecuta o próprio script pedindo permissão de Admin (UAC)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print("\n--- [Simulador de Falhas Guardião - Modo ROOT] ---")
    print("⏳ A injetar erro crítico falso diretamente no núcleo do Windows (Log 'System')...")
    
    # PowerShell: Cria a origem de log (se não existir) e injeta o erro 9999
    comando_ps = (
        'New-EventLog -LogName System -Source "GuardiaoMock" -ErrorAction SilentlyContinue; '
        'Write-EventLog -LogName System -Source "GuardiaoMock" -EventId 9999 -EntryType Error -Message "FALHA SIMULADA ROOT: Teste de validacao do MVP."'
    )
    
    try:
        subprocess.run(["powershell", "-Command", comando_ps], capture_output=True)
        print("✅ Log falso injetado com sucesso no 'System'!")
        print("👀 Verifique o terminal onde o Guardião ('main.py') está rodando!")
        input("Pressione ENTER para fechar o simulador...")
    except Exception as erro:
        print(f"❌ Ocorreu um erro ao tentar injetar o log: {erro}")

if __name__ == "__main__":
    injetar_erro_sistema_root()