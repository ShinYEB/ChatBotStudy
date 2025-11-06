from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("""
당신은 질문-답변(QA) 봇입니다. 
오직 제공된 <context> 안의 내용을 근거로만 답변해야 합니다.
만약 <context> 안에 답변의 근거가 없다면, "제공된 정보로는 알 수 없습니다."라고 답하세요.

<context>
{context}
</context>

Question: {input}
""")

def getGenerator():

    model = ChatOpenAI(model="gpt-4o-mini")

    document_chain = create_stuff_documents_chain(model, prompt)

    return document_chain