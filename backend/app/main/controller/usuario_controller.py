from flask import request
from flask_restx import Resource

# from app.main.util.decorator import admin_token_required
from ..util.dto import UsuarioDto
from ..service.usuario_service import * 
from typing import Dict, Tuple

api = UsuarioDto.api
_usuarioinsert = UsuarioDto.usuarioinsert
_usuariolist = UsuarioDto.usuariolist
_usuarioupdate = UsuarioDto.usuarioupdate


@api.route('') #,'/')
class UsuarioList(Resource):
    @api.doc('list_of_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_usuariolist, envelope='data')
    def get(self,ativo=True):
        """Lista todos usuários"""
        return get_all_users(ativo)

    @api.expect(_usuarioinsert, validate=True)
    @api.response(201, 'Usuário criado com sucesso.')
    @api.doc('cria um novo usuário')
    def post(self) -> Tuple[Dict[str, str], int]:        
        data = request.json
        return save_new_user(data=data)

@api.route('/inativos')
class UsuarioListas(Resource):
    @api.doc('list_of_inactive_registered_users')
    # @admin_token_required
    @api.marshal_list_with(_usuariolist, envelope='data')
    def get(self,ativo=False):
        """Lista todos usuários inativos"""
        return get_all_users(ativo)


@api.route('/<int:id>')
@api.param('id', 'Identificador do usuário')
@api.response(404, 'Usuário não encontrado.')
class Usuario(Resource):
    @api.doc('get a user')
    @api.marshal_with(_usuariolist)
    def get(self, id):
        """Obtem informações de um usuário com base no seu id"""
        usuario = get_a_user(id)
        if not usuario:
            api.abort(404)
        else:
            return usuario


    @api.doc('Atualiza um usuário')
    @api.expect(_usuarioupdate, validate=True)
    @api.response(201, 'Usuário atualizado com sucesso.')
    #@api.marshal_with(_usuariolist) para retornar o objeto
    def patch(self,id): # -> Tuple[Dict[str, str], int]:        
        """Atualiza um usuário  Obs: para inativar, coloque 'ativo': false """
        
        usuario = get_a_user(id)
        if not usuario:
            api.abort(404)
        else:
            data = request.json        
            return update_user(usuario,data=data)


@api.route('/<string:login>')
@api.param('login', 'parte do login do usuário')
@api.response(404, 'login não encontrado.')
class Usuario(Resource):
    @api.doc('obtem usuario com base no login')
    @api.marshal_with(_usuariolist)
    def get(self, login):
        """Lista de usuário filtrados por login"""
        usuario = get_some_user(login)
        if not usuario:
            api.abort(404)
        else:
            return usuario
