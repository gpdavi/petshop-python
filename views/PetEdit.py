import tkinter as tk
from tkinter import messagebox

from controllers.Dados import Dados


class PetEdit:
    def __init__(self, master, pet, parent_list):
        self.master = master
        self.pet = pet
        self.parent_list = parent_list
        self.master.title("Editar Pet")
        self.master.geometry("300x200")

        tk.Label(master, text="Editar Pet", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(master)
        frame.pack(padx=20, pady=5)

        tk.Label(frame, text="Peso (kg):").grid(row=0, column=0, sticky="e", pady=5)
        self.peso_entry = tk.Entry(frame)
        self.peso_entry.insert(0, pet.get("peso", ""))
        self.peso_entry.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Status:").grid(row=1, column=0, sticky="e", pady=5)
        self.status_var = tk.StringVar(value=pet.get("status", "ativo"))
        frame_status = tk.Frame(frame)
        frame_status.grid(row=1, column=1)
        tk.Radiobutton(frame_status, text="Ativo", variable=self.status_var, value="ativo").pack(side="left")
        tk.Radiobutton(frame_status, text="Inativo", variable=self.status_var, value="inativo").pack(side="left")

        tk.Button(master, text="Salvar", bg="#80DD83", command=self.salvar).pack(pady=15)

    def salvar(self):
        try:
            peso = float(self.peso_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Peso deve ser um número.")
            self.master.lift()
            return

        pets = Dados.load("animais.json")
        for i, a in enumerate(pets):
            if a["codigo"] == self.pet["codigo"]:
                pets[i]["peso"] = peso
                pets[i]["status"] = self.status_var.get()
                break

        Dados.save("animais.json", pets)
        messagebox.showinfo("Sucesso", "Pet atualizado com sucesso!")
        self.parent_list.carregar()
        self.master.destroy()