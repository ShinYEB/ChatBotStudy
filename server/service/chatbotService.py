from component.ragchain import Ragchain

ragchain = Ragchain()

def generate(query):

    llm_answer = ragchain.generate(query)

    return llm_answer
