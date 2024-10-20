from flask import Flask, jsonify, request, send_from_directory
import os
import pandas as pd
import json
from .database import db
from .model.user import User

Diretorio="C:\\Users\\erive\\OneDrive\\Documentos\\programação\\Study\\save_flask\\output"

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "user.db")}'
db.init_app(app)


csv_file=""

with app.app_context():
    db.create_all()

@app.route("/file", methods=["GET"])
def lista_arquivos():
    arquivos = []

    for name_file in os.listdir(Diretorio):
        endereco_do_arquivo = os.path.join(Diretorio, name_file)

        if(os.path.isfile(endereco_do_arquivo)):
            arquivos.append(name_file)

    return  jsonify(arquivos)
    



@app.route("/file/<name_file>", methods=["GET"])
def get_file(name_file):
    return send_from_directory(Diretorio, name_file, as_attachment=True)

@app.route("/file", methods=["POST"])
def post_arquivo():
    arquivo = request.files.get("uploaderFile")
    global csv_file
    print(arquivo)
    nome_do_arquivo = arquivo.filename
    arquivo.save(os.path.join(Diretorio, nome_do_arquivo ))
    csv_file = nome_do_arquivo
    cadastrar_usuarios(nome_do_arquivo)
    return '', 201
def cadastrar_usuarios(nome_do_arquivo):
    try:
        df = pd.read_csv(os.path.join(Diretorio, nome_do_arquivo))
        for _, row in df.iterrows():
            new_user = User(id=row['id'], name=row['name'], password=row['password'])
            db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao cadastrar usuários: {e}")
        db.session.rollback()


@app.route("/get_csv", methods=["GET"])
def get_user():
    print(csv_file)
    if csv_file is None:
        return jsonify({"error": "Arquivo CSV não especificado"}), 400

    try:
        df = pd.read_csv(os.path.join(Diretorio, csv_file))
        global json_data
        json_data = df.to_json(orient='records')
        return jsonify(json_data)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route("/user", methods=["POST"])
# def create_user():
#     json_data = request.get_json()  # Captura o JSON do corpo da requisição
#     if not json_data:
#         return jsonify({"error": "Dados não fornecidos"}), 400

#     id = json_data.get('id')
#     name = json_data.get('name')
#     password = json_data.get('password')

#     new_user = User(id=id, name=name, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return '', 201
    


if __name__ == '__main__':
    app.run(debug=True)