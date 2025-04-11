import wikipedia
from tools.custom_tool import CustomTool # Classe que encapsula a ferramenta como utilizável em agentes

def wikipedia_search(query: str) -> str:
    wikipedia.set_lang("pt") # Define o idioma da Wikipedia como português
    try:
        return wikipedia.summary(query, sentences=3) # Retorna um resumo com até 3 frases
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Termo ambíguo. Exemplos: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return f"Nenhuma página encontrada para '{query}'."
    except Exception as ex:
        return f"Erro: {str(ex)}"

# Ferramenta customizado para realizar pesquisas
wikipedia_tool = CustomTool(
    name="Wikipedia Search",
    description="Busca resumos da Wikipedia em português sobre o tema fornecido.",
    func=wikipedia_search
) 
