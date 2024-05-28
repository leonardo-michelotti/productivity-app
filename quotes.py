import random


def get_random_quote():
    quotes = [
        "O único lugar onde o sucesso vem antes do trabalho é no dicionário.",
        "A persistência é o caminho do êxito.",
        "Só se pode alcançar um grande êxito quando nos mantemos fiéis a nós mesmos.",
        "A coragem não é ausência do medo; é a persistência apesar do medo.",
        "O sucesso é a soma de pequenos esforços repetidos dia após dia."
    ]
    return random.choice(quotes)
