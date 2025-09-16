import sys
import shlex 
import subprocess
import os
import platform

VERMELHO = '\033[31m'
VERDE = '\033[32m'
RESETAR = '\033[0m'
historico = []
Comandos_Internos = ["assoc", "arp", "attrib", "break", "bcdboot", "bcdedit", "cacls", "call", "chcp", "chdir", "chkdsk", "chkntfs", "cmd", "color", "comp", "compact", "convert", "copy", "date", "del", "dir", "diskpart", "doskey", "driverquery", "echo", "endlocal", "erase", "exit", "fc", "find", "findstr", "for", "format", "fsutil", "ftype", "goto", "gpresult", "graftabl", "help", "hostname", "icacls", "if", "label", "md", "mkdir", "mklink", "mode", "more", "move", "openfiles", "path", "pause", "popd", "print", "prompt", "pushd", "rd", "recover", "rem", "ren", "rename", "replace", "rmdir", "robocopy", "route", "runas", "schtasks", "sc", "set", "setlocal", "sfc", "shutdown", "shift", "sort", "start", "subst", "systeminfo", "takeown", "taskkill", "tasklist", "time", "timeout", "title", "tree", "type", "ver", "verify", "vol", "xcopy", "wmic"]

def main():
    """Função principal do programa Shell"""
    print(VERDE)
    global historico
    os.system('cls')
    while True:
        try:

            #Armazena na variável 'comando' a entrada que o usuário fez
            comando = input(f'{os.getcwd()}>')

            #Verifica se o usuário digitou algo
            if not comando.strip():
                continue

            #Irá separar cada palavra escrita na variável "comando" em um array de str
            argumentos = shlex.split(comando)
            historico.append(argumentos)

            if argumentos[0] == "cd":
                try:
                    if len(argumentos) == 1:
                        # Se digitar só 'cd', volta para o diretório home
                        caminho = os.path.expanduser("~")
                    else:
                        # Se especificar um caminho
                        caminho = argumentos[1]
                    
                    # Expande variáveis de ambiente e normaliza o caminho
                    caminho = os.path.expandvars(caminho)  # Ex: %SystemRoot%
                    caminho = os.path.expanduser(caminho)  # Ex: ~
                    caminho = os.path.abspath(caminho)     # Caminho absoluto
                    
                    if os.path.isdir(caminho):
                        os.chdir(caminho)
                    else:
                        print("Diretório não encontrado.")
                        
                except FileNotFoundError:
                    print(VERMELHO + "Diretório não encontrado." + VERDE)
                except PermissionError:
                    print(VERMELHO +"Sem permissão para acessar este diretório." + VERDE)
                except Exception as e:
                    print(f"{VERMELHO}Erro ao mudar de diretório: {e}{VERDE}")
                continue
            
            elif argumentos[0] in ['history', '!!'] or argumentos[0].startswith('!'):
                hist(argumentos[0])
                continue

            elif platform.system() == "Windows" and argumentos[0] == 'cls':
                os.system(argumentos[0])
                continue
            
            #plataform identifica o S.O. e o cmd abre o propmt de comando , com \c para executar o comando e fechar logo em seguida
            elif platform.system() == "Windows" and argumentos[0].lower() in Comandos_Internos:
                argumentos = ['cmd', '/c', comando]

            
            #Realiza um relatório sobre tudo que ocorreu na função digitada, capture_output=True, torna possível que eu manipule o programa pela variável que eu criei, text=True, converte os bits em str 
            processo = subprocess.run(argumentos, capture_output=True, text=True)

            #Há a saída do que foi requerido ou aviso de erro
            if processo.stdout:
                print(processo.stdout, end="")
            if processo.stderr:
                print(processo.stderr, end="")

        except FileNotFoundError:
            print(f"{VERMELHO}Comando não encontrado: {argumentos[0]}{VERDE}")
        except KeyboardInterrupt:
            # O usuário ao clicar em "Ctrl + c" sai do programa
            print( VERMELHO + "Saindo do programa"+VERDE)
            sys.exit(0)
        except Exception as e:
            print(f"{VERMELHO}Ocorreu um erro: {e}{VERDE}")

def hist(comando):
    global historico

    if comando == "history":
        for i, c in enumerate (historico):
            print(f'{i}: {' '.join(c)}')
        return
    
    if comando == '!!':
        if len(comando) < 2:
            print('Nao ha comandos anteriores.')
            return
        cmd = historico[-2]
        print(f'Executando último comando: {historico [-2]}')
        subprocess.run(cmd)
        return
    
    if comando.startswith('!'):
        try:
            index = int(comando[1:])
            cmd = historico[index]
            print(f"Executando comando {index}: {' '.join(cmd)}")
            subprocess.run(cmd)
        except ValueError:
            print(VERMELHO + 'Ocorreu um erro de valor'+ VERDE)
        except IndexError:
            print(VERMELHO + 'Houve um erro de indexacao' + VERDE)
        return   

main()








