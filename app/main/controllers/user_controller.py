from flask_restful import  Api
from app.main.services.user_service import (
    save_new_user, 
    get_a_user,
    get_all_users,
    get_a_user_by_email,
    encode_auth_token
)
from flask import (
    current_app as app,
    Blueprint,
    jsonify,
    request,
    make_response,
)
from app.main.config import key 
from app.main.util.decorator import auth_required
import base64

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/')
@auth_required
def get_user_list():
    all_user = get_all_users()
    return jsonify(all_user)


@user_controller.route('/auth/register', methods=['POST'])
def register():
    """Creates a new User """
    data = request.json
    if save_new_user(data=data) == True:
        response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


@user_controller.route('/auth/login', methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = get_a_user_by_email(post_data.get('email'))
        print(user['password'])
        if user != None and user['password'] == base64.b64encode(post_data.get('password').encode()):
            auth_token = encode_auth_token(user['_id'], user['email'])
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(responseObject), 200

        else:
            responseObject = {
                    'status': 'fail',
                    'message': 'email or password is wrong.',
                }
            return jsonify(responseObject), 200
                
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'server error'
        }
        return jsonify(responseObject), 500