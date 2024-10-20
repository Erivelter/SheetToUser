from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import pandas as pd
import json

from model import  user
Diretorio="C:\\Users\\erive\\OneDrive\\Documentos\\programação\\Study\\save_flask\\output"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////user.db'

db.create_all()
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
    return '', 201


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

@app.route("/user", methods=["POST"])
def create_user(json_data):
    data = json.loads(json_data)
    id= data.get('id')
    name = data.get('name')
    password = data.get('password')

    new_user = user(id=id, name=name, password=password)
    db.session.add(new_user)
    db.session.commit()

    return '', 201
    


if __name__ == '__main__':
    app.run(debug=True)