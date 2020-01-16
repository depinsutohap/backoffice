from sanic import Blueprint

api_1 = Blueprint('api_1', url_prefix='/api', version="v1")

from . import views, report, auths, business, crm, finance, hr, inventory, products
