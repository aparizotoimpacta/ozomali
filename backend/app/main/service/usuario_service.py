import uuid
import datetime
import unidecode

from app.main import db
from app.main.model import unaccent
from app.main.model.usuario import Usuario
from app.main.model.perfil import Perfil
from typing import Dict, Tuple
from sqlalchemy.sql import text


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    usuario = Usuario.query.filter(
            Usuario.login == data['login']
    ).first()
    
    perfil = Perfil.query.filter_by(id=data['perfil_id'], ativo=True).first()
    if not perfil:
        response_object = {
            'status': 'Falha',
            'message': 'Perfil não encontrado ou inativo.',
        }
        return response_object, 404

    if not usuario:
        novo_usuario = Usuario(
            login=data['login'],
            senha=data['senha'],
            nome=data['nome'],
            perfil_id=data['perfil_id'],
        )
        save_changes(novo_usuario)
        response_object = {
            'status': 'Sucesso',
            'message': 'Usuário registrado com sucesso.',
            'id' : novo_usuario.id,
        }
        return response_object, 201
        # return generate_token(new_user)
    else:
        response_object = {
            'status': 'Falha',
            'message': 'Login ou nome já existente.',
        }
        return response_object, 409


def update_user(usuario: Usuario,data) -> Tuple[Dict[str, str], int]:
    update_changes(usuario,data)
    response_object = {
            'status': 'Sucesso',
            'message': 'Usuário atualizado com sucesso.',
            'id' : usuario.id,
            'login' : usuario.login,
            'nome' : usuario.nome,
            'ativo' : usuario.ativo,
            'perfil_id' : usuario.perfil_id,
        }
    return response_object, 200


def get_all_users():
    return Usuario.query.join(Perfil).all()

def get_some_user(tipo, id):
    item = '%{}%'.format(id)

    if tipo=='id':
        return Usuario.query.filter_by(id=id).all()
    
    if tipo=='login':
        return Usuario.query.filter(
            unaccent(Usuario.login)
            .ilike( item )
        ).all()

    if tipo=='nome':
        return Usuario.query.filter(
            unaccent(Usuario.nome)
            .ilike( item )
        ).all()

    if tipo=='perfil_id':
        return Usuario.query.filter_by(perfil_id=id).all()
    
    if tipo=='ativo':
        return Usuario.query.filter_by(ativo=id).all()

def get_search_users(data):
    filters = ''    
    if data.get('id',0) != 0:
        filters += "usuario.id = " + str(data.get('id',0))

    if data.get('nome',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(usuario.nome)) like '%" + unidecode.unidecode(data.get('nome','')).lower() + "%'"
    
    if data.get('login',''):
        if filters:
            filters += " AND "
        filters += "LOWER(unaccent(usuario.login)) like '%" + unidecode.unidecode(data.get('login','')) + "%'"

    if data.get('ativo','') == False or data.get('ativo','')== True:
        if filters:
            filters += " AND "
        filters += "usuario.ativo =" 
        filters += "'true'" if data.get('ativo','')== True else "'false'"

    if data.get('perfil_id',0) !=0 :
        if filters:
            filters += " AND "
        filters += "perfil.id = " + str(data.get('perfil_id',0))

    return Usuario.query.join(Perfil).filter(text(filters)).all()


def get_a_user(id):
    return Usuario.query.filter_by(id=id).first()

def generate_token(user: Usuario) -> Tuple[Dict[str, str], int]:
    try:        
        # generate the auth token
        auth_token = Usuario.encode_auth_token(usuario.id, usuario.nome, usuario.login, usurio.perfil.nome)
        response_object = {
            'status': 'Sucesso',
            'message': 'Registrado com sucesso.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'Falha',
            'message': 'Ocorreu um erro. Por favor tente novamente.'
        }
        return response_object, 401


def save_changes(data: Usuario) -> None:
    db.session.add(data)
    db.session.commit()

def update_changes(usuario: Usuario, data) -> None:
    usuario.login = data.get('login' , usuario.login)
    usuario.nome = data.get('nome' , usuario.nome)
    if data.get('senha', 0) != 0:
        usuario.senha = data['senha']
    usuario.ativo = data.get('ativo', usuario.ativo)
    db.session.commit()

def update_password(usuario: Usuario, newpassword: str) -> None:
    if newpassword.__len__() >3:
        usuario.senha = newpassword
    db.session.commit()
