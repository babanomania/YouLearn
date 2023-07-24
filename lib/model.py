
from g4f import Provider, Model
from langchain.chat_models import ChatOpenAI
from lib.G4FLLM import G4FLLM


def get_gpt4f_llm():

    return G4FLLM(
        model=Model.gpt_35_turbo,
        provider=Provider.DeepAi,
    )


def get_openai_llm():

    return ChatOpenAI(
        temperature=0.2,
        model="gpt-3.5-turbo-16k"
    )


def get_llm():
    return get_openai_llm()
