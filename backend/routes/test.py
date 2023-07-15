from flask import Blueprint, jsonify

test_route = Blueprint('test_route', __name__)

@test_route.route('/api/test', methods=['GET'])
def test_handler():
    try:
        return jsonify({'message': 'API is working successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
