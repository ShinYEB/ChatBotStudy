from langchain_classic.chains.retrieval import create_retrieval_chain

from component.retriever import getRetriever
from component.generator import getGenerator

class Ragchain:

    def __init__(self):
        retriever = getRetriever()
        generator = getGenerator()

        self.retrieval_chain = create_retrieval_chain(retriever, generator)

    def generate(self, question):
        response = self.retrieval_chain.invoke({"input": question})

        return response["answer"]
