from datetime import date

class Pet:
    def __init__(self, codigo, nome, especie, raca, data_nascimento, peso, tutor_cpf, status="ativo"):
        self.__codigo = codigo
        self.__nome = nome
        self.__especie = especie
        self.__raca = raca
        self.__data_nascimento = data_nascimento
        self.__peso = peso
        self.__tutor_cpf = tutor_cpf
        self.__status = status

    def get_codigo(self): 
        return self.__codigo
    def get_nome(self): 
        return self.__nome
    def get_especie(self): 
        return self.__especie
    def get_raca(self): 
        return self.__raca
    def get_data_nascimento(self): 
        return self.__data_nascimento
    def get_peso(self): 
        return self.__peso
    def get_tutor_cpf(self):
        return self.__tutor_cpf
    def get_status(self): 
        return self.__status

    def to_dict(self):
        return {
            "codigo": self.__codigo,
            "nome": self.__nome,
            "especie": self.__especie,
            "raca": self.__raca,
            "data_nascimento": self.__data_nascimento.isoformat(),
            "peso": self.__peso,
            "tutor_cpf": self.__tutor_cpf,
            "status": self.__status,
        }


class Cachorro(Pet):
    def __init__(self, codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                 porte, vacina_raiva, status="ativo"):
        super().__init__(codigo, nome, "cachorro", raca, data_nascimento, peso, tutor_cpf, status)
        self.__porte = porte
        self.__vacina_raiva = vacina_raiva

    def get_porte(self): return self.__porte
    def get_vacina_raiva(self): return self.__vacina_raiva

    def to_dict(self):
        d = super().to_dict()
        d.update({"porte": self.__porte, "vacina_raiva": self.__vacina_raiva})
        return d


class Gato(Pet):
    def __init__(self, codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                 castrado, tipo_pelo, status="ativo"):
        super().__init__(codigo, nome, "gato", raca, data_nascimento, peso, tutor_cpf, status)
        self.__castrado = castrado
        self.__tipo_pelo = tipo_pelo

    def get_castrado(self): return self.__castrado
    def get_tipo_pelo(self): return self.__tipo_pelo

    def to_dict(self):
        d = super().to_dict()
        d.update({"castrado": self.__castrado, "tipo_pelo": self.__tipo_pelo})
        return d


class Ave(Pet):
    def __init__(self, codigo, nome, raca, data_nascimento, peso, tutor_cpf,
                 anilha, exotica, status="ativo"):
        super().__init__(codigo, nome, "ave", raca, data_nascimento, peso, tutor_cpf, status)
        self.__anilha = anilha
        self.__exotica = exotica

    def get_anilha(self): return self.__anilha
    def get_exotica(self): return self.__exotica

    def to_dict(self):
        d = super().to_dict()
        d.update({"anilha": self.__anilha, "exotica": self.__exotica})
        return d


class Reptil(Pet):
    def __init__(self, codigo, nome, raca, data_nascimento, peso, tutor_cpf, status="ativo"):
        super().__init__(codigo, nome, "réptil", raca, data_nascimento, peso, tutor_cpf, status)


class Roedor(Pet):
    def __init__(self, codigo, nome, raca, data_nascimento, peso, tutor_cpf, status="ativo"):
        super().__init__(codigo, nome, "roedor", raca, data_nascimento, peso, tutor_cpf, status)
