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

# TAXES & SERVICE CHARGES SECTION's API
@api_1.route('/data/tax', methods=['POST', 'GET'])
@_auth.login_required
async def _api_tax(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Hop_Tax()._list(owner_id=user.owner_id)
                response['type'] = Hop_Tax_Type()._list()
                response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                response['data'] = Hop_Tax()._insert(name=apidata['tax_name'], tax_type_id=apidata['tax_type_id'], value=apidata['tax_value'], outlet_list=apidata['outlet_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_Tax()._data(_id=apidata['tax_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_Tax()._update(_id=apidata['tax_id'], name=apidata['tax_name'], tax_type_id=apidata['tax_type_id'], value=apidata['tax_value'], outlet_list=apidata['outlet_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_Tax()._remove(_id=apidata['tax_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 5:
                response['data'] = Hop_Tax()._remove_many(tax_list=apidata['tax_list'], owner_id=user.owner_id)
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
