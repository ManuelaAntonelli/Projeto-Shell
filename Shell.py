import sys
import shlex 
import subprocess
import os

def main():
    """Função principal do programa Shell"""
    while True:
        try:

            #Armazena na variável 'comando' a entrada que o usuário fez
            comando = input(">> ")

            #Verifica se o usuário digitou algo
            if not comando.strip():
                continue

            #Irá separar cada palavra escrita na variável "comando" em um array de str
            argumentos = shlex.split(comando)

            if argumentos[0] == 'cd':
                print("['cd']")
                continue 

            elif argumentos[0] in ['history', '!!'] or argumentos[0].startswith('!'):
                print("[comandos de histórico]")
                continue
            
            #Realiza um relatório sobre tudo que ocorreu na função digitada, capture_output=True, torna possível que eu manipule o programa pela variável que eu criei, text=True, converte os bits em str 
            processo = subprocess.run(argumentos, capture_output=True, text=True)

            #Há a saída do que foi requerido ou aviso de erro
            if processo.stdout:
                print(processo.stdout, end="")
            if processo.stderr:
                print(processo.stderr, end="")

        except FileNotFoundError:
            print(f"Comando não encontrado: {argumentos[0]}")
        except KeyboardInterrupt:
            # O usuário ao clicar em "Ctrl + c" sai do programa
            print("Saindo do programa")
            sys.exit(0)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

main()
