import tkinter as tk

from views.StartWindow import StartWindow
from controllers.Dados import Dados


def main():     
    # 1. Cria a janela principal do Tkinter (o "master")
    root = tk.Tk()
    # 2. Passa essa janela para a classe do outro arquivo
    app = StartWindow(root)
    # 3. Inicia o loop do programa
    root.mainloop()

if __name__ == "__main__":
    main()


Dados.create("tutores.json")
Dados.create("pets.json")