import json
import os

class Dados:
    PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")  # pasta onde os JSONs serão salvos

    def create(nome_arquivo):
        caminho = os.path.join(Dados.PASTA, nome_arquivo)
        os.makedirs(Dados.PASTA, exist_ok=True)  # cria a pasta se não existir
        try:
            with open(caminho, "x", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
        except FileExistsError:
            pass

    def save(nome_arquivo, dados):
        caminho = os.path.join(Dados.PASTA, nome_arquivo)
        serializavel = []
        for item in dados:
            if hasattr(item, "to_dict"):    
                serializavel.append(item.to_dict())
            elif hasattr(item, "__dict__"):
                serializavel.append(item.__dict__)
            else:
                serializavel.append(item)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(serializavel, f, indent=4, ensure_ascii=False)

    def load(nome_arquivo):
        caminho = os.path.join(Dados.PASTA, nome_arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    return []
                return json.loads(conteudo)
        except FileNotFoundError:
            print(f"Arquivo '{caminho}' não encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"Arquivo '{caminho}' corrompido, recriando...")
            Dados.create(nome_arquivo)
            return []