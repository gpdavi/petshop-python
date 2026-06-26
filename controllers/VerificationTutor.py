class VerificationTutor:
    @staticmethod
    def verify_cpf(CPF):
        # Verifica se o CPF tem 11 dígitos
        if len(CPF) != 11:
            return False
        
        # Verifica se todos os caracteres são dígitos
        if not CPF.isdigit():
            return False
        return True

    @staticmethod  
    def verify_email(email):
        # Verifica se o email contém "@" e "."
        if "@" not in email or "." not in email:
            return False
        return True
    
    @staticmethod
    def verify_number(numero):
        if not numero.isdigit():
            return False
        return True