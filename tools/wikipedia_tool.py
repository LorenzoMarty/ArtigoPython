import wikipedia
from tools.custom_tool import CustomTool

def wikipedia_search(query: str) -> str:
    wikipedia.set_lang("pt")
    try:
        return wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Termo ambíguo. Exemplos: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return f"Nenhuma página encontrada para '{query}'."
    except Exception as ex:
        return f"Erro: {str(ex)}"

wikipedia_tool = CustomTool(
    name="Wikipedia Search",
    description="Busca resumos da Wikipedia em português sobre o tema fornecido.",
    func=wikipedia_search
)
