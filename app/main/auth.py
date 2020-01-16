from . import main
from ..models import *
from .. import jinja, _auth
from sanic.response import json, raw, text, redirect
from sanic.views import HTTPMethodView
from sanic.exceptions import ServerError
from sanic_jwt import protected
import jinja2_sanic

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

async def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/<sector>', methods=["GET", "POST"])
async def login(request, sector):
    cur_user = _auth.current_user(request)
    if cur_user is not None:
        return redirect('/')
    else:
        if sector in ['login', 'register', 'forgot']:
            return jinja.render("auth/" + sector + ".html", request, cur_user=cur_user)

@main.route('/detail')
@_auth.login_required
async def detail(request):
    cur_user = _auth.current_user(request)
    if cur_user is not None and Hop_User().verify_detail(cur_user.id):
        return redirect('/')
    return jinja.render("auth/detail.html", request, cur_user=cur_user)

# @main.before_app_request
# async def before_request(request):
#     if current_user.is_authenticated:
#         print(current_user.verify_detail())
#         if current_user.is_authenticated and current_user.verify_detail() is False and  request.endpoint[:5] == 'auth.':
#             return redirect(url_for('auth.detail'))
#         current_user.ping()
        # if current_user.is_authenticated \
        #         and not current_user.confirmed \
        #         and request.endpoint[:5] != 'auth.':
        #     return redirect(url_for('auth.unconfirmed'))
#
# @main.before_request
# async def make_session_permanent(request):
#     session.permanent = True
#
# @main.route('/unconfirmed')
# async def unconfirmed(request):
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

@main.route('/logout')
@_auth.login_required
async def logout(request):
    _auth.logout_user(request)
    return redirect('/')
