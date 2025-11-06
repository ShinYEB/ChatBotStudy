from component.ragchain import Ragchain

ragchain = Ragchain()

def generate(question):
    return ragchain.generate(question)
