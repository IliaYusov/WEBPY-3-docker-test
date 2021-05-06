from app import app, auth
from app.models import User, Advert
from app.schema import USER_CREATE, ADVERT_CREATE
from app.validator import validate
from flask import jsonify, request, g
from flask.views import MethodView


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True


class UserView(MethodView):

    def get(self, user_id):
        user = User.by_id(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())


class AdvertView(MethodView):

    def get(self, advert_id):
        advert = Advert.by_id(advert_id)
        return jsonify(advert.to_dict())

    @validate('json', ADVERT_CREATE)
    @auth.login_required
    def post(self):
        advert = Advert(**request.json)
        advert.user_id = g.user.id
        advert.add()
        return jsonify(advert.to_dict())

    @auth.login_required
    def delete(self, advert_id):
        advert = Advert.by_id(advert_id)
        if advert.user_id == g.user.id:
            advert.remove()
            return jsonify({'message': f'advert id:{advert_id} - deleted'})
        else:
            return jsonify({'message': "Can't delete someone else's ad"})


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', ])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])
app.add_url_rule('/adverts/<int:advert_id>', view_func=AdvertView.as_view('adverts_get'), methods=['GET', ])
app.add_url_rule('/adverts/', view_func=AdvertView.as_view('adverts_create'), methods=['POST', ])
app.add_url_rule('/adverts/<int:advert_id>', view_func=AdvertView.as_view('adverts_delete'), methods=['DELETE', ])
