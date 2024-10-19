from flask import Flask, jsonify, request, send_from_directory, render_template
import os
from flask_sqlalchemy import SQLAlchemy
Diretorio="C:\\Users\\erive\\OneDrive\\Documentos\\programação\\Study\\save_flask\\output"
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////user.db'
# db = SQLAlchemy(app)
# db.create_all()
@app.route("/user",methods=["GET"])
def mostar_user():
    pass



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

    print(arquivo)
    nome_do_arquivo = arquivo.filename
    arquivo.save(os.path.join(Diretorio, nome_do_arquivo ))

    return '', 201

if __name__ == '__main__':
    app.run(debug=True)

