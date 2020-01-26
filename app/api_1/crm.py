import time, ast
import json as _json
from . import api_1
from .. import _auth, Session
from decimal import *
from app.models import *
from sqlalchemy import or_
from datetime import datetime
from sanic.response import json, raw, redirect
from ..models import Hop_User, Hop_Business, Hop_Outlet, Hop_Product_Item, \
    Hop_Role, Hop_Product_Outlet, Hop_Provinces, Hop_Cities,  Hop_Business_Category, \
    Hop_Countries, Hop_Product_Category, Hop_Tax, Hop_Tax_Type, Hop_Special_Promo, Hop_Ap_Detail, \
    Hop_Business, Hop_Num_Emp, Hop_Price, Hop_Measurement_List, Hop_User_Outlet, Hop_Variant_List, \
    Hop_Variant_Category, Hop_Composed_Product, Hop_Inventory, Hop_Inventory_List, \
    Hop_Billing_Package_Item, Hop_Billing_Invoice, Hop_Billing_Payment

# PROMO SECTION's API
@api_1.route('/data/promo', methods=['POST', 'GET'])
@_auth.login_required
async def _api_promo(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            # PRODUCT CATEGORY
            if int(apidata['status']) == 0:
                response['data_sp'] = Hop_Special_Promo()._count(owner_id=user.owner_id)
                response['data_ap'] = Hop_Ap_Detail()._count(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                response['data'] = Hop_Special_Promo()._list(owner_id=user.owner_id)
                response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_Special_Promo()._insert(
                    name=apidata['promo_name'], percent=apidata['promo_percent_type'],
                    value=apidata['promo_value'], promo_date_status=apidata['promo_date_status'],
                    startdate=apidata['promo_start_date'], enddate=apidata['promo_end_date'],
                    starttime=apidata['promo_start_time'], endtime=apidata['promo_end_time'],
                    apply_time_status=apidata['promo_applied_time_status'], applied_day=apidata['applied_day'],
                    outlet_list=apidata['promo_outlet'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_Special_Promo()._data(_id=apidata['promo_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_Special_Promo()._update(
                    id=apidata['promo_id'], name=apidata['promo_name'], percent=apidata['promo_percent_type'],
                    value=apidata['promo_value'], promo_date_status=apidata['promo_date_status'],
                    startdate=apidata['promo_start_date'], enddate=apidata['promo_end_date'],
                    starttime=apidata['promo_start_time'], endtime=apidata['promo_end_time'],
                    apply_time_status=apidata['promo_applied_time_status'], applied_day=apidata['applied_day'],
                    outlet_list=apidata['promo_outlet'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 5:
                response['data'] = Hop_Special_Promo()._remove(_id=apidata['promo_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 6:
                response['data'] = Hop_Special_Promo()._remove_many(promo_list=apidata['promo_list'], owner_id=user.owner_id)
                response['status'] = '00'
            # PRODUCT ITEM
            elif int(apidata['status']) == 7:
                response['data'] = Hop_Ap_Detail()._list(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 8:
                response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                response['item_list'] = Hop_Product_Item()._list_sold(owner_id=user.owner_id)
                response['category_list'] = Hop_Product_Category()._list(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 9:
                if len(apidata['type_id']) > 0 and  apidata['requirement_id'] != '' \
                and apidata['requirement_value'] != '' and apidata['reward_id'] != '' \
                and apidata['reward_value'] != '':
                    response['data'] = Hop_Ap_Detail()._insert(
                        ap_type_id=apidata['type_id'], ap_requirement_id=apidata['requirement_id'],
                        requirement_value=apidata['requirement_value'], requirement_relation=apidata['requirement_relation'],
                        ap_reward_id=apidata['reward_id'], reward_value=apidata['reward_value'],
                        reward_relation=apidata['reward_relation'], multiple=apidata['multiple'],
                        promo_date_status=apidata['promo_date_status'], startdate=apidata['promo_start_date'],
                        enddate=apidata['promo_end_date'], starttime=apidata['promo_start_time'],
                        endtime=apidata['promo_end_time'], apply_time_status=apidata['promo_applied_time_status'],
                        applied_day=apidata['applied_day'], outlet_list=apidata['promo_outlet'],
                        owner_id=user.owner_id)
                    response['status'] = '00'
                else:
                    response['status'] = '50'
                    response['message'] = 'Please fill all required fields'
            elif int(apidata['status']) == 10:
                response['data'] = Hop_Ap_Detail()._data(promo_id=apidata['promo_id'], owner_id=user.owner_id)
                response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                response['item_list'] = Hop_Product_Item()._list_sold(owner_id=user.owner_id)
                response['category_list'] = Hop_Product_Category()._list(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 11:
                if len(apidata['type_id']) > 0 and  apidata['requirement_id'] != '' \
                and apidata['requirement_value'] != '' and apidata['reward_id'] != '' \
                and apidata['reward_value'] != '':
                    response['data'] = Hop_Ap_Detail()._update( promo_id=apidata['promo_id'],
                        ap_type_id=apidata['type_id'], ap_requirement_id=apidata['requirement_id'],
                        requirement_value=apidata['requirement_value'], requirement_relation=apidata['requirement_relation'],
                        ap_reward_id=apidata['reward_id'], reward_value=apidata['reward_value'],
                        reward_relation=apidata['reward_relation'], multiple=apidata['multiple'],
                        promo_date_status=apidata['promo_date_status'], startdate=apidata['promo_start_date'],
                        enddate=apidata['promo_end_date'], starttime=apidata['promo_start_time'],
                        endtime=apidata['promo_end_time'], apply_time_status=apidata['promo_applied_time_status'],
                        applied_day=apidata['applied_day'], outlet_list=apidata['promo_outlet'],
                        owner_id=user.owner_id)
                    response['status'] = '00'
                else:
                    response['status'] = '50'
                    response['message'] = 'Please fill all required fields'
            elif int(apidata['status']) == 12:
                response['data'] = Hop_Ap_Detail()._basic_data(_id=apidata['promo_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 13:
                response['data'] = Hop_Ap_Detail()._remove(_id=apidata['promo_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 14:
                response['data'] = Hop_Ap_Detail()._remove_many(promo_list=apidata['promo_list'], owner_id=user.owner_id)
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
