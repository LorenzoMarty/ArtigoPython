from crewai_tools import BaseTool
import requests

class WikipediaTool(BaseTool):
    name = "Wikipedia Search Tool"
    description = "Busca informações da Wikipedia em português"

    def _run(self, query: str) -> str:
        url = f"https://pt.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "extracts",
            "exlimit": 1,
            "explaintext": 1,
            "titles": query,
            "format": "json",
            "utf8": 1,
            "redirects": 1
        }
        response = requests.get(url, params=params)
        pages = response.json().get("query", {}).get("pages", {})
        return next(iter(pages.values())).get("extract", "Nada encontrado.")