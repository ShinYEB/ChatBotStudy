from component.ragchain import Ragchain
from component.redis import search_cache, add_to_cache

ragchain = Ragchain()

def generate(query):
    #cached_answer = search_cache(query)

    #if cached_answer:
    #    return cached_answer

    llm_answer = ragchain.generate(query)
    add_to_cache(query, llm_answer)

    return llm_answer

def testRetriever(query):
    return ragchain.testRetriever(query)