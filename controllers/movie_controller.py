from flask import Blueprint, jsonify, request
from serializers import movie_serializer as dynamodb

movie_r = Blueprint("Movi-Route", __name__)


@movie_r.route('/', methods=['GET'])
def home():
    result = {'msg': 'home'}
    return jsonify(result), 200


@movie_r.route('/create_table')
def root_route():
    dynamodb.create_table_movie()
    result = {'msg': 'created table'}
    return jsonify(result), 200


@movie_r.route('/movie', methods=['POST'])
def add_movie():
    data = request.get_json()
    response = dynamodb.write_to_movie(
        data['id'],
        data['title'],
        data['director']
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        result = {'msg': 'Add Movie successful'}
        return jsonify(result), 200
    result = {
        'msg': 'error occurred',
        'response': response
    }
    return jsonify(result)


@movie_r.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    response = dynamodb.read_from_movie(id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if 'Item' in response:
            return {'Item': response['Item']}
        return {'msg': 'Item not found!'}
    return {
        'msg': 'Some error occured',
        'response': response
    }


@movie_r.route('/movie/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    response = dynamodb.update_in_movie(id, data)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'msg': 'Updated successfully',
            'ModifiedAttributes': response['Attributes'],
            'response': response['ResponseMetadata']
        }
    return {
        'msg': 'Some error occured',
        'response': response
    }


@movie_r.route('/upvote/movie/<int:id>', methods=['POST'])
def upvote_movie(id):
    response = dynamodb.upvote_a_movie(id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'msg': 'Upvotes the movie successfully',
            'Upvotes': response['Attributes']['upvotes'],
            'response': response['ResponseMetadata']
        }
    return {
        'msg': 'Some error occured',
        'response': response
    }


@movie_r.route('/movie/<int:id>', methods=['DELETE'])
def delete_movie(id):
    response = dynamodb.delete_from_movie(id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'msg': 'Deleted successfully',
        }
    return {
        'msg': 'Some error occcured',
        'response': response
    }


@movie_r.app_errorhandler(404)
def handle_404(err):
    result = {'error': '404'}
    return jsonify(result), 404


@movie_r.app_errorhandler(500)
def handle_500(err):
    result = {'error': '500'}
    return jsonify(result), 500
