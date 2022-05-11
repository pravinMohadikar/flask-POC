from flask import Blueprint, make_response, jsonify,request
from app.models.model import Users

user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/user', methods=['GET'])
def user_profile():
    username = request.json['username']
    user = Users.objects.get(username=username)
    return make_response(jsonify({
        'name': user.name,
        'email': user.email,
        'dob': user.dob
        }), 200)


@user_blueprint.route('/getalluser', methods=['GET'])
def get_alluser():
    user = Users.objects.all()

    output = []
    for a in user:
        output.append({
            'username':a.username,
            'name':a.name,
            'email':a.email,
            'dob':a.dob
        })
    return jsonify({'user': output})
