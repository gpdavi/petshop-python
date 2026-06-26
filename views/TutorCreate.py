import tkinter as tk
from tkinter import messagebox

from models.Tutor import Tutor
from controllers.Dados import Dados
from controllers.VerificationTutor import VerificationTutor

class TutorCreate:
    def __init__(self, master, parent_window=None):
        self.master = master
        self.parent_window = parent_window
        self.master.title("Cadastro de Tutor")
        self.master.geometry("700x400")

        self.label = tk.Label(master, text="Cadastro de Tutor", font=("Arial", 16))
        self.label.grid(row=0, column=2, columnspan=2, pady=10)

        self.back_button = tk.Button(master, text="Voltar", bg="#d3d3d3", command=self.voltar)
        self.back_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.CPF_label = tk.Label(master, text="CPF:")
        self.CPF_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.CPF_entry = tk.Entry(master)
        self.CPF_entry.grid(row=1, column=1, padx=10, pady=5)

        self.name_label = tk.Label(master, text="Nome:")
        self.name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)

        self.last_name_label = tk.Label(master, text="Sobrenome:")
        self.last_name_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(master)
        self.last_name_entry.grid(row=2, column=3, padx=10, pady=5)

        self.telefone_label = tk.Label(master, text="Telefone:")
        self.telefone_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.telefone_entry = tk.Entry(master)
        self.telefone_entry.grid(row=3, column=1, padx=10, pady=5)

        self.email_label = tk.Label(master, text="Email:")
        self.email_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        self.cidade_label = tk.Label(master, text="Cidade:")
        self.cidade_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.cidade_entry = tk.Entry(master)
        self.cidade_entry.grid(row=6, column=1, padx=10, pady=5)

        self.bairro_label = tk.Label(master, text="Bairro:")
        self.bairro_label.grid(row=6, column=2, padx=10, pady=5, sticky="e")
        self.bairro_entry = tk.Entry(master)
        self.bairro_entry.grid(row=6, column=3, padx=10, pady=5)

        self.tutortype_label = tk.Label(master, text="Função:")
        self.tutortype_label.grid(row=5, column=0, padx=10, pady=5)
        self.tipo_var = tk.StringVar()
        frame_tutortype = tk.Frame(master)
        frame_tutortype.grid(row=5, column=1, columnspan=4, pady=5)

        for tutortype in ["BanhoTosa", "Consulta", "Vacinação", "Hospedagem"]:
            tk.Radiobutton(frame_tutortype, text=tutortype, variable=self.tipo_var, value=tutortype,
                   font=("Arial", 10),
                   activebackground="#ffffff", cursor="hand2").pack(side="left", padx=10)
        
        
        
        self.rua_label = tk.Label(master, text="Rua:")
        self.rua_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.rua_entry = tk.Entry(master)
        self.rua_entry.grid(row=7, column=1, padx=10, pady=5)

        self.numero_label = tk.Label(master, text="Número:")
        self.numero_label.grid(row=7, column=2, padx=10, pady=5, sticky="e")
        self.numero_entry = tk.Entry(master)
        self.numero_entry.grid(row=7, column=3, padx=10, pady=5)

        self.submit_button = tk.Button(master, text="Cadastrar", bg="#80DD83", command=self.submit)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=10)
    
    def submit(self):
        CPF = self.CPF_entry.get()
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        cidade = self.cidade_entry.get()
        bairro = self.bairro_entry.get()
        rua = self.rua_entry.get()
        numero = self.numero_entry.get()
        tipo = self.tipo_var.get()
        

        if not all([CPF, name, last_name, telefone, email, cidade, bairro, rua, numero, tipo]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            self.master.lift()
            return
        if not self.checkCPF():
            self.master.lift()                                                                                                                                                                                                              
            return
        if not VerificationTutor.verify_email(email):
            messagebox.showerror("Erro", "Email inválido. Por favor, insira um email válido.")
            self.master.lift()
            return
        if not VerificationTutor.verify_number(numero):
            messagebox.showerror("Erro", "Número Invalido. Por Favor, insira um número válido!")
            self.master.lift()
            return
        
        address = f"{rua}, {numero}, {bairro}, {cidade}"
        nome = f"{name} {last_name}"
        tutor = Tutor(CPF, nome, telefone, email, address, tipo)


        tutores = Dados.load("tutores.json")
        tutores_objs = tutores
        tutores_objs.append(tutor.to_dict())
        Dados.save("tutores.json", tutores_objs)
        
        messagebox.showinfo("Sucesso", "Tutor cadastrado com sucesso!")
        self.master.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

    def voltar(self):
        if self.parent_window:
            self.parent_window.deiconify() # Redesenha/reexibe a tela anterior caso tenha sido escondida
        self.master.destroy()
    
    def checkCPF(self):
        CPF = self.CPF_entry.get()
        if not VerificationTutor.verify_cpf(CPF):
            messagebox.showerror("Erro", "CPF inválido. Por favor, insira um CPF válido.")
            return False
        return True