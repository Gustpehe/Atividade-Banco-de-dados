from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from Modelo_tabelas import Base, Cliente, Especialistas, Agendamentos
import os
from dotenv import load_dotenv
from CriarSession import roda_essa_bomba

load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app)

Session = roda_essa_bomba("DATABASE_URL")

# Definição das rotas
@app.route("/")
def pag_null():
    return redirect('/home')


# Redireciona para a home quando a URL não existir
@app.errorhandler(404)
def pag_not_found(batata_que_segura_a_realidade_nao_remover_de_maneira_alguma):
    return redirect('/home')


@app.route("/home")
def pag_home():
    return render_template("home.html")


@app.route("/login")
def pag_login():
    return render_template("login.html")


@app.route("/cadastro")
def pag_cadastro():
    return render_template("cadastro.html")


@app.route("/crudUser")
def pag_crud_user():
    return render_template("crudUser.html")


@app.route("/crudEspecialistas")
def pag_crud_esp():
    return render_template("crudEspecialistas.html")


@app.route("/crudAgendamentos")
def pag_crud_agend():
    return render_template("crudAgendamentos.html")


@app.route("/sobre")
def pag_sobre():
    return render_template("sobre.html")


@app.route("/contato")
def pag_contato():
    return render_template("contato.html")


@app.route("/agendamentos")
def pag_agendamentos():
    return render_template("agendamentos.html")


@app.route("/perfil")
def pag_perfil():
    return render_template("perfil.html")


# Partes da API

# API - Clientes
# Lista todos os clientes
@app.route("/api/clientes", methods=["GET"])
def listar_clientes():
    session = Session()
    clientes = session.query(Cliente).all()
    data = [{"id": c.id, "nome": c.nome, "CPF": c.CPF, "idade": c.idade, "senha": c.senha, "classe": c.classe} for c in clientes]
    session.close()
    return jsonify(data)

# Cria um novo cliente
@app.route("/api/clientes", methods=["POST"])
def criar_cliente():
    session = Session()
    data = request.json
    novo = Cliente(nome=data["nome"], CPF=data["CPF"], idade=data["idade"], senha=data["senha"])
    # Verifica se já existe esse CPF no banco
    checar_cpf = session.query(Cliente).filter_by(CPF=data["CPF"]).first()
    if checar_cpf:
        session.close()
        return jsonify({"error": "Ja existe um cliente com este CPF."}), 400
    session.add(novo)
    session.commit()
    session.close()
    return jsonify({"message": "Cliente criado com sucesso"}), 201

# Atualiza um cliente
@app.route("/api/clientes/<int:id>", methods=["PUT"])
def atualizar_cliente(id):
    session = Session()
    cliente = session.query(Cliente).get(id)
    if not cliente:
        session.close()
        return jsonify({"error": "Cliente não encontrado"}), 404

    data = request.json
    # Atualiza apenas os campos enviados
    cliente.nome = data.get("nome", cliente.nome)
    cliente.CPF = data.get("CPF", cliente.CPF)
    cliente.idade = data.get("idade", cliente.idade)
    cliente.senha = data.get("senha", cliente.senha)
    cliente.classe = data.get("classe", cliente.classe)
    session.commit()
    session.close()
    return jsonify({"message": "Cliente atualizado com sucesso"})

# Deleta um cliente
@app.route("/api/clientes/<int:id>", methods=["DELETE"])
def deletar_cliente(id):
    session = Session()
    cliente = session.query(Cliente).get(id)
    if not cliente:
        session.close()
        return jsonify({"error": "Cliente não encontrado"}), 404
    session.delete(cliente)
    session.commit()
    session.close()
    return jsonify({"message": "Cliente removido com sucesso"})



# API - Especialistas
# Lista os especialistas
@app.route("/api/especialistas", methods=["GET"])
def listar_especialistas():
    session = Session()
    especialistas = session.query(Especialistas).all()
    data = [{"id": e.id, "nome": e.nome, "CRM": e.CRM, "CPF": e.CPF, "area": e.area, "senha": e.senha}
            for e in especialistas]
    session.close()
    return jsonify(data)

# Cria um novo especialista
@app.route("/api/especialistas", methods=["POST"])
def criar_especialista():
    session = Session()
    data = request.json

    # Verifica CRM ou CPF repetido
    if session.query(Especialistas).filter(
        (Especialistas.CRM == data["CRM"]) | (Especialistas.CPF == data["CPF"])
    ).first():
        session.close()
        return jsonify({"error": "Já existe um especialista com este CRM ou CPF."}), 400

    novo = Especialistas(
        nome=data["nome"],
        CRM=data["CRM"],
        CPF=data["CPF"],
        area=data["area"],
        senha=data["senha"]
    )

    session.add(novo)
    session.commit()
    session.close()
    return jsonify({"message": "Especialista criado com sucesso"}), 201

# Atualiza o especialista
@app.route("/api/especialistas/<int:id>", methods=["PUT"])
def atualizar_especialista(id):
    session = Session()
    especialista = session.query(Especialistas).get(id)
    if not especialista:
        session.close()
        return jsonify({"error": "Especialista não encontrado"}), 404

    data = request.json
    especialista.nome = data.get("nome", especialista.nome)
    especialista.CRM = data.get("CRM", especialista.CRM)
    especialista.CPF = data.get("CPF", especialista.CPF)
    especialista.area = data.get("area", especialista.area)
    especialista.senha = data.get("senha", especialista.senha)
    session.commit()
    session.close()
    return jsonify({"message": "Especialista atualizado com sucesso"})

# Deleta especialista
@app.route("/api/especialistas/<int:id>", methods=["DELETE"])
def deletar_especialista(id):
    session = Session()
    especialista = session.query(Especialistas).get(id)
    if not especialista:
        session.close()
        return jsonify({"error": "Especialista não encontrado"}), 404
    if especialista.agendamentos:
        return jsonify({"error": "Não é possível deletar, existem agendamentos associados."}), 400

    session.delete(especialista)
    session.commit()
    session.close()
    return jsonify({"message": "Especialista removido com sucesso"})

# API - Agendamentos
# Lista os agendamentos
@app.route("/api/agendamentos", methods=["GET"])
def listar_agendamentos():
    session = Session()
    agendamentos = session.query(Agendamentos).all()
    # monta dados com informações de cliente e especialista
    data = [{
        "id": a.id,
        "cliente_id": a.cliente_id,
        "cliente_nome": a.cliente.nome,
        "especialista_id": a.especialista_id,
        "especialista_nome": a.especialista.nome,
        "data": a.data.isoformat(),
        "local": a.local
    } for a in agendamentos]
    session.close()
    return jsonify(data)

# Cria agendamento novo
@app.route("/api/agendamentos", methods=["POST"])
def criar_agendamento():
    session = Session()
    data = request.json

    # Verifica se cliente e o especialista existem
    cliente = session.query(Cliente).get(data["cliente_id"])
    especialista = session.query(Especialistas).get(data["especialista_id"])
    if not cliente or not especialista:
        session.close()
        return jsonify({"error": "Cliente ou especialista não encontrado."}), 400

    novo = Agendamentos(
        cliente_id=data["cliente_id"],
        especialista_id=data["especialista_id"],
        data=data["data"],
        local=data["local"]
    )

    session.add(novo)
    session.commit()
    session.close()
    return jsonify({"message": "Agendamento criado com sucesso"}), 201

# Atualiza o agendamento
@app.route("/api/agendamentos/<int:id>", methods=["PUT"])
def atualizar_agendamento(id):
    session = Session()
    agendamento = session.query(Agendamentos).get(id)
    if not agendamento:
        session.close()
        return jsonify({"error": "Agendamento não encontrado"}), 404

    data = request.json
    agendamento.cliente_id = data.get("cliente_id", agendamento.cliente_id)
    agendamento.especialista_id = data.get("especialista_id", agendamento.especialista_id)
    agendamento.data = data.get("data", agendamento.data)
    agendamento.local = data.get("local", agendamento.local)
    session.commit()
    session.close()
    return jsonify({"message": "Agendamento atualizado com sucesso"})

# Deleta o agendamento
@app.route("/api/agendamentos/<int:id>", methods=["DELETE"])
def deletar_agendamento(id):
    session = Session()
    agendamento = session.query(Agendamentos).get(id)
    if not agendamento: 
        session.close()
        return jsonify({"error": "Agendamento não encontrado"}), 404
    session.delete(agendamento)
    session.commit()
    session.close()
    return jsonify({"message": "Agendamento removido com sucesso"})

# API - Login
@app.route("/api/login", methods=["POST"])
def login():
    session = Session()
    data = request.json
    cpf = data.get("CPF")
    senha = data.get("senha")

    # verifica se CPF e senha foram enviados
    if not cpf or not senha:
        session.close()
        return jsonify({"error": "CPF e senha são obrigatórios."}), 400

    cliente = session.query(Cliente).filter_by(CPF=cpf, senha=senha).first()
    session.close()

    if cliente:
        return jsonify({
            "message": "Login realizado com sucesso!",
            "cliente": {"id": cliente.id, "nome": cliente.nome, "CPF": cliente.CPF, "classe": cliente.classe}}), 200
    else:
        return jsonify({"error": "CPF ou senha incorretos."}), 401

# Roda essa !incrível API
if __name__ == "__main__":
    app.run(debug=True)
