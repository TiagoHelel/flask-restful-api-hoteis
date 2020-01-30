from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
import sqlite3

from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params
from resources.filtros import consulta_com_cidade
from resources.filtros import consulta_sem_cidade

# hoteis = [
#     {
#         'hotel_id': 'alpha',
#         'nome': 'Alpha Hotel',
#         'estrelas': 4.3,
#         'diaria': 420.34,
#         'cidade': 'Rio de Janeiro'
#     },
#     {
#         'hotel_id': 'bravo',
#         'nome': 'Bravo Hotel',
#         'estrelas': 4.4,
#         'diaria': 420.34,
#         'cidade': 'Santa Catarina'
#     },
#     {
#         'hotel_id': 'charlie',
#         'nome': 'Charlie Hotel',
#         'estrelas': 3.9,
#         'diaria': 420.34,
#         'cidade': 'São Paulo'
#     }
# ]



path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        # return hoteis
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            filtros = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, filtros)
        else:
            filtros = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, filtros)
        
        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        # return{'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
        return{'hoteis': hoteis}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="This field is required.")
    atributos.add_argument('estrelas', type=float, required=True, help="This field is required.")
    atributos.add_argument('diaria', type=float, required=True, help="This field is required.")
    atributos.add_argument('cidade', type=str, required=True, help="This field is required.")
    atributos.add_argument('site_id', type=int, required=True, help="This field is required.")

    # def find_hotel(hotel_id):
    #     for hotel in hoteis:
    #         if hotel['hotel_id'] == hotel_id:
    #             return hotel
    #     return None



    def get(self, hotel_id):
        # hotel = Hotel.find_hotel(hotel_id)
        hotel = HotelModel.find_hotel(hotel_id)
        # if hotel:
        #     return hotel
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400
        dados = Hotel.atributos.parse_args()
        hotel = (HotelModel(hotel_id, **dados))
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        # novo_hotel = hotel_objeto.json()
        # novo_hotel = {
        #     'hotel_id': hotel_id,
        #     'nome': dados['nome'],
        #     'estrelas': dados['estrelas'],
        #     'diaria': dados['diaria'],
        #     'cidade': dados['cidade']
        # } # igual novo_hotel = { 'hotel_id': hotel_id, **dados }
        # hoteis.append(novo_hotel)
        return hotel.json(), 200

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        # novo_hotel = hotel.json()
        # novo_hotel = { 'hotel_id': hotel_id, **dados }
        # hotel = Hotel.find_hotel(hotel_id)
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            # hotel.update(hotel)
            # return novo_hotel, 200
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = (HotelModel(hotel_id, **dados))
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201
        # return novo_hotel, 201
        # hoteis.append(novo_hotel)

    @jwt_required
    def delete(self, hotel_id):
        # global hoteis
        # hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500
            return {'message': 'Hotel deleted successfully.'}
        return {'message':'Hotel not found.'}, 404