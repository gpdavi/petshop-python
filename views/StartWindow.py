import tkinter as tk
from tkinter import messagebox

from views.TutorCreate import TutorCreate
from views.TutorList import TutorList
from views.PetCreate import PetCreate
from views.PetList import PetList
from views.ServiceCreate import ServiceCreate
from views.ServiceList import ServiceList
from views.ListAgendamento import ListAgendamento


class StartWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de gerenciamento de Petshop")
        self.master.geometry("800x650")

        self.label = tk.Label(master, text="Bem-vindo ao Sistema de Gerenciamento de Petshop!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.tutorcreate_button = tk.Button(master, text="Cadastrar Tutor", bg="#80DD83", command=self.tutorcreate)
        self.tutorcreate_button.pack(pady=10)

        self.tutorlist_button = tk.Button(master, text="Listar Tutores", bg="#80DD83", command=self.tutorlist)
        self.tutorlist_button.pack(pady=10)

        self.petcreate_button = tk.Button(master, text="Cadastrar Pet", bg="#80DD83", command=self.pet_create)
        self.petcreate_button.pack(pady=10)

        self.petlist_button = tk.Button(master, text="Listar Pets", bg="#80DD83", command=self.pet_list)
        self.petlist_button.pack(pady=10)

        self.servicelist_button = tk.Button(master, text="Serviços", bg="#80DD83", command = self.service_list)
        self.servicelist_button.pack(pady=10)

        self.createappointment_button = tk.Button(master, text="Agendamentos", bg="#80DD83", command = self.agendamento_list)
        self.createappointment_button.pack(pady=10)

        self.quit_button = tk.Button(master, text="Finalizar",bg = "#E05454", command=self.confirmar_saida)
        self.quit_button.pack(pady=10)

    def tutorcreate(self):
        self.master.withdraw()
        top = tk.Toplevel()
        TutorCreate(top, parent_window=self.master)
    
    def tutorlist(self):
        self.master.withdraw()
        top = tk.Toplevel()
        TutorList(top, parent_window=self.master)

    def pet_create(self):
        self.master.withdraw()
        top = tk.Toplevel()
        PetCreate(top, parent_window=self.master)

    def pet_list(self):
        self.master.withdraw()
        top = tk.Toplevel()
        PetList(top, parent_window=self.master)

    def create_service(self):
        self.master.withdraw()
        top = tk.Toplevel()
        ServiceCreate(top, parent_window=self.master)
    
    def service_list(self):
        self.master.withdraw()
        top = tk.Toplevel()
        ServiceList(top, parent_window=self.master)
    
    def agendamento_list(self):
        self.master.withdraw()
        top = tk.Toplevel()
        ListAgendamento(top, parent_window=self.master)
    def confirmar_saida(self):
        # Pergunta se quer sair e guarda a resposta (True ou False)
        quer_sair = messagebox.askyesno("Sair", "Tem certeza que deseja fechar o sistema?")
        if quer_sair:
            self.master.quit()
    