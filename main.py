import os
from crewai import Agent, Task, Crew
from models.article import Article
from tools.wikipedia_tool import wikipedia_tool
from langchain_openai import ChatOpenAI

# Configurar Groq (OpenAI compatible)
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = "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"  # Substitua pela sua chave

# Instanciar o LLM via Groq
llm_groq = ChatOpenAI(
    model_name="openai/llama3-70b-8192",
    temperature=0.7
)

# Criar o agente pesquisador
pesquisador = Agent(
    role='Pesquisador',
    goal='Buscar informações relevantes sobre o tema',
    backstory='Especialista em coletar dados da Wikipedia.',
    tools=[wikipedia_tool],
    llm=llm_groq,
    verbose=True
)

def generate_article(tema: str) -> Article:
    redator = Agent(
        role='Redator',
        goal='Escrever um artigo com pelo menos 300 palavras',
        backstory='Redator experiente com ótima habilidade de síntese e escrita.',
        llm=llm_groq,
        verbose=True
    )

    task1 = Task(
        description=f'Pesquisar o tema "{tema}" na Wikipedia e coletar dados relevantes.',
        expected_output='Texto descritivo com informações úteis sobre o tema.',
        agent=pesquisador
    )

    task2 = Task(
        description='Com base nas informações coletadas, redigir um artigo de no mínimo 300 palavras.',
        expected_output='Artigo formatado como JSON, contendo título, conteúdo e número de palavras.',
        agent=redator
    )

    crew = Crew(
        agents=[pesquisador, redator],
        tasks=[task1, task2],
        verbose=True
    )

    result = crew.kickoff()

    # Corrigido aqui:
    article_text = result.result if hasattr(result, "result") else str(result)

    article = Article(
        title=tema,
        content=article_text,
        word_count=len(article_text.split())
    )

    return article

# Teste rápido se rodar main.py diretamente
if __name__ == "__main__":
    tema_teste = "Futebol"
    artigo = generate_article(tema_teste)
    print(artigo.json(indent=2, ensure_ascii=False))
