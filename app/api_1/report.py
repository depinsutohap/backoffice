import time, ast
import json as _json
from . import api_1
from .. import _auth
from decimal import *
from app.models import *
from sqlalchemy import or_
from datetime import datetime
from ..models_mongo import TransLog
from sanic.response import json, raw, redirect
from ..models import Hop_User, Hop_Business, Hop_Outlet, Hop_Product_Item, \
    Hop_Role, Hop_Product_Outlet, Hop_Provinces, Hop_Cities,  Hop_Business_Category, \
    Hop_Countries, Hop_Product_Category, Hop_Tax, Hop_Tax_Type, Hop_Special_Promo, Hop_Ap_Detail, \
    Hop_Business, Hop_Num_Emp, Hop_Price, Hop_Measurement_List, Hop_User_Outlet



@api_1.route('/data/report', methods=['POST', 'GET'])
@_auth.login_required
async def _api_report(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        # app = current_app._get_current_object()
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = TransLog()._count(user.owner_id)
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect('/')

@api_1.route('/data/subreport', methods=['POST', 'GET'])
@_auth.login_required
async def _api_summary(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        # app = current_app._get_current_object()
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 1:
                response['data'] = TransLog()._summary_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 2:
                response['data'] = TransLog()._product_sales_all(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 3:
                response['data'] = TransLog()._daily_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 4:
                response['data'] = TransLog()._data_sales_trx_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 5:
                response['data'] = TransLog()._per_category_sales(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 6:
                response['data'] = TransLog()._sales_per_outlet_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
                # if (int(apidata['business_id']) == 0 or int(apidata['outlet']) == 0):
                #     response['data'] = TransLog()._sales_per_outlet_all(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                #     response['status'] = '00'
                # elif int(apidata['outlet']) != 0:
                #     response['data'] = TransLog()._sales_per_outlet(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                #     response['status'] = '00'
            if int(apidata['status']) == 7:
                response['data'] = TransLog()._tax_revenue_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 8:
                response['data'] = TransLog()._discount_revenue_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 9:
                response['data'] = TransLog()._daily_profit_co(user.owner_id,apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 10:
                response['data'] = TransLog()._product_profit_co(user.owner_id,apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 11:
                print('dksoaasdkoasdko')
                response['data'] = TransLog()._dashboard_sales_all(user.owner_id, apidata['outlet'], apidata['dash_on'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 12:
                if (int(apidata['business_id']) == 0 or int(apidata['outlet']) == 0):
                    response['data'] = TransLog()._payment_method_all(user.owner_id, apidata['dari'], apidata['sampai'])
                    response['status'] = '00'
                elif int(apidata['outlet']) != 0:
                    response['data'] = TransLog()._payment_method(apidata['outlet'], apidata['dari'], apidata['sampai'])
                    response['status'] = '00'
            if int(apidata['status']) == 13:
                if (int(apidata['business_id']) == 0 or int(apidata['outlet']) == 0):
                    response['data'] = TransLog()._stock_all(user.owner_id, apidata['dari'], apidata['sampai'])
                    response['status'] = '00'
                elif int(apidata['outlet']) != 0:
                    response['data'] = TransLog()._stock(apidata['outlet'], user.owner_id, apidata['dari'], apidata['sampai'])
                    response['status'] = '00'
            if int(apidata['status']) == 14:
                response['data'] = TransLog()._sales_per_hour_all(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 15:
                response['data'] = TransLog()._detail_sales_data(apidata['trx_id'])
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect('/')

@api_1.route('/data/dashboard', methods=['POST', 'GET'])
@_auth.login_required
async def _api_dashboard(request):
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            response['data'] = TransLog()._dashboard_sales_all(user.owner_id, apidata['outlet'], apidata['dash_on'], apidata['dari'], apidata['sampai'], apidata['business_id'])
            response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
