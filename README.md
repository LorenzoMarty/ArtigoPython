# 🧠 ArtigoPython — Geração Automática de Artigos com CrewAI

Este projeto utiliza **agentes inteligentes** com a biblioteca [CrewAI] para **gerar artigos que seguem as Normas ABNT automaticamente a partir de um tema**, consultando informações da Wikipedia e redigindo textos com um modelo de linguagem grande (LLM).

---

## 🚀 Tecnologias Utilizadas

| Tecnologia             | Descrição |
|------------------------|-----------|
| **Python**             | Linguagem principal do projeto |
| **Flask**              | Framework web usado para criar a API (`app.py`) |
| **Pydantic**           | Modelagem dos artigos como objetos estruturados |
| **CrewAI**             | Orquestração multiagente inteligente |
| **CrewAI Tools**       | Ferramentas personalizadas integradas à CrewAI |
| **LangChain**          | Camada de integração com LLMs compatíveis |
| **Groq API**           | Plataforma de execução dos LLMs (LLaMA 3) |
| **Wikipedia Tool**     | Ferramenta customizada que pesquisa na Wikipedia |
| **JSON**               | Formato de retorno dos artigos |

---

## 📁 Estrutura do Projeto

```
.
├── app.py                      # API Flask
├── main.py                     # Geração do artigo com CrewAI
├── models/
│   └── article.py              # Modelo do artigo usando Pydantic
├── tools/
│   └── wikipedia_tool.py       # Ferramenta personalizada para busca na Wikipedia
├── requirements.txt            # Dependências do projeto
```

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/LorenzoMarty/ArtigoPython.git
cd artigopython
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Configure a API da Groq

Você precisa ter uma conta em [groq.com](https://console.groq.com/). Em seguida, configure suas variáveis de ambiente:

```bash
export OPENAI_API_KEY=sua_chave_groq
export OPENAI_API_BASE=https://api.groq.com/openai/v1
```

No Windows (cmd):

```cmd
set OPENAI_API_KEY=sua_chave_groq
set OPENAI_API_BASE=https://api.groq.com/openai/v1
```

---

## 🧪 Executando o Projeto

### Opção 1: Rodar diretamente via terminal

```bash
python main.py
```

Esse script irá executar o sistema multiagente, pesquisar na Wikipedia e gerar um artigo completo com título, conteúdo e contagem de palavras.

---

### Opção 2: Usar via API Flask

```bash
python app.py
```

Acesse via navegador ou ferramentas como Postman em:

```
http://127.0.0.1:5000
```

**Exemplo de requisição (POST)**:
```json
{
  "tema": "Energia solar"
}
```

---

## 📌 Exemplo de Execução via Terminal

```bash
python main.py
```

---

## 👨‍💻 Autor

Desenvolvido por Lorenzo dos Reis Marty