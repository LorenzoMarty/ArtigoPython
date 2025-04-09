from flask import Flask, request, jsonify, render_template
from main import generate_article

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/gerar-artigo", methods=["POST"])
def gerar_artigo():
    tema = request.form.get("tema") or (request.json or {}).get("tema")
    if not tema:
        return jsonify({"erro": "Tema não fornecido"}), 400

    artigo = generate_article(tema)
    
    if request.form:
        return f"""
        <h1>Artigo Gerado</h1>
        <h2>{artigo.title}</h2>
        <p>{artigo.content}</p>
        <p><strong>Total de palavras:</strong> {artigo.word_count}</p>
        <a href="/">Voltar</a>
        """
    else:
        return jsonify(artigo.dict())

if __name__ == "__main__":
    app.run(debug=True)
