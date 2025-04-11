from flask import Flask, request, jsonify, render_template
from main import generate_article # Importa a função principal que gera o artigo

app = Flask(__name__) # Cria a aplicação Flask


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html") # Retorna uma página HTML com um formulário (não fornecido aqui)


@app.route("/gerar-artigo", methods=["POST"]) 
def gerar_artigo():
    tema = request.form.get("tema") # Tenta pegar o tema de um formulário HTML
    if not tema and request.is_json:
        tema = request.json.get("tema") # Alternativa: pegar tema de uma requisição JSON
    if not tema:
        return jsonify({"erro": "Tema não fornecido"}), 400 # Retorna erro se tema não foi enviado

    artigo = generate_article(tema) # Chama a função que usa a CrewAI para gerar o artigo

    if request.is_json:
        return jsonify(artigo.dict()) # Retorna o artigo como JSON
    else:
        return f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{artigo.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 12pt;
            background: #fdfdfd;
            color: #222;
            margin: 40px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
        }}

        h1 {{
            font-size: 24pt;
            margin-bottom: 10px;
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
            color: #333;
        }}

        h2 {{
            font-size: 16pt;
            margin-top: 30px;
            color: #2c3e50;
        }}

        p {{
            text-align: justify;
            margin-top: 10px;
        }}

        .keywords {{
            font-style: italic;
            color: #555;
        }}

        .section {{
            margin-top: 30px;
        }}

        .references {{
            margin-top: 20px;
            padding-left: 20px;
        }}

        .references p {{
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{artigo.title}</h1>

        <div class="section">
            <h2>Resumo</h2>
            <p>{artigo.summary}</p>
        </div>

        <div class="section">
            <h2>Palavras-chave</h2>
            <p class="keywords">{", ".join(artigo.keywords)}</p>
        </div>

        <div class="section">
            <h2>Introdução</h2>
            <p>{artigo.introduction}</p>
        </div>

        <div class="section">
            <h2>Materiais e Métodos</h2>
            <p>{artigo.materials_and_methods}</p>
        </div>

        <div class="section">
            <h2>Resultados e Discussão</h2>
            <p>{artigo.results_and_discussion}</p>
        </div>

        <div class="section">
            <h2>Conclusões</h2>
            <p>{artigo.conclusions}</p>
        </div>

        <div class="section">
            <h2>Agradecimentos</h2>
            <p>{artigo.acknowledgments}</p>
        </div>

        <div class="section">
            <h2>Referências</h2>
            <div class="references">
                {"".join(f"<p>{ref}</p>" for ref in artigo.references)}
            </div>
        </div>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True) # Executa o app localmente com modo de depuração
