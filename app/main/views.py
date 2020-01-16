from . import main
from ..models import *
from .. import jinja, _auth
from sanic.response import json, raw, text, redirect
from sanic.views import HTTPMethodView
from sanic.exceptions import ServerError
import jinja2_sanic

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Setup jinja2 environment


async def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @main.route('/google273b4a5af9f9bf98.html')
# async def google():
#     return jinja.render('google273b4a5af9f9bf98.html')

# @main.route("/")
# async def hello(request):
#     return text("Hello World!")

@main.route('/')
async def index(request):
    cur_user = _auth.current_user(request)
    if cur_user is not None:
        if cur_user is not None and Hop_User().verify_detail(cur_user.id) is False:
            return redirect('/detail')
        return jinja.render("main/index.html", request, cur_user=cur_user)
    return redirect('/login')


@main.route('/page/<sector>')
@_auth.login_required
async def _page(request, sector):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if sector not in [
        'dashboard', 'report', 'business', 'product-item', 'product-category',
        'inventory','tax', 'employee', 'promo', 'account', 'billing'
    ]:
        abort(404)
    if sector == 'product-item':
        cur_user = _auth.current_user(request)
        if Hop_Product_Category()._check_validation(owner_id=Hop_User()._user_owner(cur_user.id)) is False:
            sector = 'product-category'
    return jinja.render('main/user/' + sector + '/index.html', request)

@main.route('/page/<sector>/<subpage>')
@_auth.login_required
async def _subreport(request, sector, subpage):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if sector in ['report', 'business', 'product-item', 'inventory', 'employee', 'promo', 'billing']:
        if subpage not in [
        # Report Data
            'summary', 'product-sales', 'daily-sales', 'data-sales-transactions', 'sales-per-category',
            'sales-per-outlet', 'tax-revenue', 'discount', 'daily-profit', 'product-profit',
            'sales-per-hour', 'payment-method', 'stock', 'cash-recap', 'customer',
        # New Business & Outlet
            'new', 'new-outlet',
        # Products Item & Employee
            'add', 'edit', 'manage-price', 'manage-ingredients', 'manage-stock', 'manage-access',
        # Promo
            'special-promo', 'auto-promo', 'add-auto-promo', 'edit-auto-promo',
        # Inventory
            'stock-card', 'stock-entry', 'stock-exit', 'transfer-stock', 'stock-opname',
            'add-stock-entry', 'add-stock-exit', 'add-transfer-stock', 'add-stock-opname',
        # Billing
            'detail-payment'
        ]:
            abort(404)
        return jinja.render('main/user/' + sector + '/sub/' + subpage + '.html', request)
    else:
        abort(404)

@main.route('/page/<sector>/section/<page>')
@_auth.login_required
async def _section_business(request, sector, page):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if sector not in ['business', 'billing']:
        abort(404)
    if page not in ['overview', 'activity', 'settings', 'bundling', 'order', 'history']:
        abort(404)
    return jinja.render('main/user/' + sector + '/section/' + page + '.html', request)
