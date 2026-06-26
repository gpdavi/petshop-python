class Tutor:
    def __init__(self, CPF, name, telefone, email, address,tipo):
        self.__CPF = CPF
        self.__name = name
        self.__telefone = telefone
        self.__email = email
        self.__address = address
        self.__tipo = tipo
    
    def get_CPF(self):
        return self.__CPF
    
    def get_name(self):
        return self.__name
    def get_telefone(self):
        return self.__telefone
    def get_email(self):
        return self.__email
    def get_address(self):
        return self.__address
    def get_tipo(self):
        return self.__tipo

    def to_dict(self):
        return {
            "CPF": self.__CPF,
            "name": self.__name,
            "telefone": self.__telefone,
            "email": self.__email,
            "address": self.__address,  
            "tipo": self.__tipo
        }