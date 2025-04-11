import os
import re
from crewai import Agent, Task, Crew
from models.article import Article  # Modelo de artigo estruturado
from tools.wikipedia_tool import wikipedia_tool  # Ferramenta de busca na Wikipedia
from langchain_openai import ChatOpenAI  # Wrapper do modelo LLM da OpenAI (aqui usando Groq)

# Configuração do LLM (Groq com LLaMA3-70B)
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = "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"  # Chave de API do Groq

llm_groq = ChatOpenAI(model_name="openai/llama3-70b-8192", temperature=0.7)  # Instancia o modelo com certa criatividade


# AGENTE: Pesquisador
pesquisador = Agent(
    role="Pesquisador",
    goal="Buscar informações relevantes sobre o tema",
    backstory="Especialista em coletar dados da Wikipedia.",
    tools=[wikipedia_tool],  # Ferramenta de busca conectada à Wikipedia
    llm=llm_groq,
    verbose=True,
)


# FUNÇÃO: Extrair seções do artigo gerado em texto
def parse_article(text: str) -> dict:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove formatação em negrito (**texto**)

    # Extrai conteúdo entre títulos de seção com base em padrões
    def extrair(bloco, texto):
        padrao = rf"{bloco}[:\n]?\s*(.*?)(?=\n[A-ZÁÀÉÍÓÚÇ][^\n]*[:\n]|\Z)"
        match = re.search(padrao, texto, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    return {
        "title": text.strip().split("\n")[0],  # Título na primeira linha
        "authors": (
            re.findall(r"Autores?:\s*(.*)", text, re.IGNORECASE)[0].split(",")
            if re.search(r"Autores?:", text, re.IGNORECASE)
            else ["Autor Desconhecido"]
        ),
        "summary": extrair("Resumo", text),
        "keywords": re.findall(r"Palavras-chave[:\n]?\s*(.*)", text, re.IGNORECASE),
        "abstract": extrair("Abstract", text),
        "english_keywords": re.findall(r"Keywords[:\n]?\s*(.*)", text, re.IGNORECASE),
        "introduction": extrair("Introdução", text),
        "materials_and_methods": extrair("Materiais e Métodos", text),
        "results_and_discussion": extrair("Resultados e Discussão", text),
        "conclusions": extrair("Conclusões", text),
        "acknowledgments": extrair("Agradecimentos", text),
        "references": re.findall(r"(?m)^\d+\.\s*(.*)", text),  # Lista numerada de referências
    }


# FUNÇÃO PRINCIPAL: Gera artigo completo a partir de tema

def generate_article(tema: str) -> Article:
    
    # Agente escritor: responsável por gerar o texto do artigo
    escritor = Agent(
        role="escritor",
        goal="Escrever um artigo científico com estrutura e formatação ABNT",
        backstory="escritor experiente que segue normas técnicas. Seu texto tem título, autores, resumo, palavras-chave, introdução, materiais e métodos, resultados e discussão, conclusões, agradecimentos e referências.",
        llm=llm_groq,
        verbose=True,
    )

    # Tarefa 1: O pesquisador coleta informações da Wikipedia
    task1 = Task(
        description=f'Pesquisar o tema "{tema}" na Wikipedia e coletar dados relevantes.',
        expected_output="Texto descritivo com informações úteis sobre o tema.",
        agent=pesquisador,
    )

    # Tarefa 2: O escritor gera o artigo completo com base nas informações anteriores
    task2 = Task(
        description=(
            "Com base nas informações coletadas, escreva um artigo científico completo, estruturado nas normas ABNT. "
            "O artigo deve conter: título, autores fictícios, resumo (até 1500 caracteres), palavras-chave (até 6), "
            "introdução, materiais e métodos, resultados e discussão, conclusões, agradecimentos e referências no padrão NBR 6023. "
            "Evite repetir qualquer seção. Cada seção deve aparecer apenas uma vez no artigo."
        ),
        expected_output="Artigo completo com pelo menos 800 palavras, respeitando as seções da estrutura ABNT.",
        agent=escritor,
    )

    # Criando e rodando a crew (time de agentes com tarefas)
    crew = Crew(agents=[pesquisador, escritor], tasks=[task1, task2], verbose=True)
    result = crew.kickoff()

    # Coletando resultado do texto gerado
    text = result.result if hasattr(result, "result") else str(result)

    # Extração e organização dos dados do artigo
    dados = parse_article(text)

    return Article(
        title=dados["title"],
        english_title=f"{dados['title']} (English)",  # Título traduzido para inglês
        authors=[a.strip() for a in dados["authors"]],
        advisor="Prof. Dr. Exemplo Orientador",  # Pode ser personalizado
        summary=(dados["summary"][:1497] + "...") if len(dados["summary"]) > 1500 else dados["summary"],
        keywords=dados["keywords"],
        abstract=dados["abstract"] or dados["summary"],
        english_keywords=dados["english_keywords"],
        introduction=dados["introduction"],
        materials_and_methods=dados["materials_and_methods"],
        results_and_discussion=dados["results_and_discussion"],
        conclusions=dados["conclusions"],
        acknowledgments=dados["acknowledgments"],
        references=dados["references"] or [
            "SOBRENOME, Nome. Título. Local: Editora, ano.",
            "OUTRO AUTOR. Outro título. Revista XYZ, 2023.",
        ],
    )

# TESTE LOCAL DO SISTEMA

if __name__ == "__main__":
    tema_teste = "Energia Solar"
    artigo = generate_article(tema_teste)
    print("Artigo gerado:")
    print(artigo.model_dump_json(indent=2, ensure_ascii=False))
