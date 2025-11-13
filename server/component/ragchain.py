from langchain_classic.chains.retrieval import create_retrieval_chain

from .retriever import getRetriever
from .generator import getGenerator

class Ragchain:

    def __init__(self):
        retriever = getRetriever()
        generator = getGenerator()

        self.retrieval_chain = create_retrieval_chain(retriever, generator)

    def generate(self, question):
        response = self.retrieval_chain.invoke({"input": question})

        return response["answer"]

    def testRetriever(self, question, max_content_len=None):
        response = self.retrieval_chain.invoke({"input": question})

        context = response.get("context", [])
        docs_list = []

        for doc in context:
            content = doc.page_content
            if max_content_len:
                content = content[:max_content_len]
            docs_list.append(content)

        return docs_list


