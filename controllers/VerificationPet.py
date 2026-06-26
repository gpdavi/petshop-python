class VerificationTutor:
    @staticmethod
    def verify_chip(chip):
        # Verifica se o chip tem 15 dígitos
        if len(chip) != 15:
            return False
        
        # Verifica se todos os caracteres são dígitos
        if not chip.isdigit():
            return False
        return True