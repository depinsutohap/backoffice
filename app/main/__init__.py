from sanic import Blueprint

main = Blueprint('main')

from . import views, auth, errors
