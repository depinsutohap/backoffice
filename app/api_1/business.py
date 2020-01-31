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
    Hop_Billing_Package_Item, Hop_Billing_Invoice, Hop_Billing_Payment, Hop_Product_Category_Outlet

# BUSINESS SECTION's API
@api_1.route('/data/business', methods=['POST', 'GET'])
@_auth.login_required
async def _api_business(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
            # BUSINESS LIST BASED ON OWNER ID
                response['data'] = Hop_Business()._listbyownerid(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
            # LIST DATA AND OUTLET
                _business = Hop_Business().verify_auth(apidata['bid'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Business()._basicdata(_id=_business.id)
                    response['status'] = '00'
            elif int(apidata['status']) == 2:
            # LIST DATA AND OUTLET
                _business = Hop_Business().verify_auth(apidata['bid'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Business()._basicdata(_id=_business.id)
                    response['list'] = Hop_Outlet()._list(business_id=_business.id, user_id=user.id)
                    response['status'] = '00'
            elif int(apidata['status']) == 3:
            # OUTLET LIST BASED ON BUSINESS ID AND OWNER ID
                _business = Hop_Business().verify_auth(apidata['bid'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['list'] = Hop_Outlet()._list(business_id=_business.id, user_id=user.id)
                    response['category_list'] = Hop_Product_Category()._list(owner_id=user.owner_id)
                    response['item_list'] = Hop_Product_Item()._list_sold(owner_id=user.owner_id)
                    response['tax_list'] = Hop_Tax()._list(owner_id=user.owner_id)
                    response['status'] = '00'
            elif int(apidata['status']) == 4:
            # SUBMIT NEW BUSINESS AND GET EXISTING OUTLET BASED ON OWNER ID
                response['data'] = Hop_Business()._insert_detail(_name=apidata['business_name'], _businesscategory=apidata['business_category'], _description=apidata['business_description'], owner_id=user.owner_id)
                response['data_outlet'] = Hop_Business()._listbyownerid_all(user_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 5:
            # MOVE BUSINESS LIST INTO NEW BUSINESS
                _business = Hop_Business().verify_auth(apidata['business_id'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Business()._move_business_list(new_business_id=_business.id, data_outlet_list=apidata['outlet_list'], owner_id=user.owner_id)
                    response['business_id'] = _business.id
                    response['status'] = '00'
            elif int(apidata['status']) == 6:
            # INSERT NEW OUTLET
                _business = Hop_Business().verify_auth(apidata['business_id'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Outlet()._insert(_name=apidata['outlet_name'], _numempid=apidata['outlet_num_emp'], _phonenumber=apidata['outlet_phone_number'], _address=apidata['outlet_address'], _country_id=apidata['outlet_country'], _business_id=apidata['business_id'], owner_id=user.owner_id)
                    response['status'] = '00'
                else:
                    response['status'] = '50'
            elif int(apidata['status']) == 7:
            # UPDATE BUSINESS SETTINGS
                _business = Hop_Business().verify_auth(apidata['business_id'])
                if _business is not None and _business.owner_id == user.owner_id:
                    if len(apidata['business_name'].strip()) > 0:
                        response['data'] = Hop_Business()._update(_id=_business.id, _name=apidata['business_name'], _businesscategory=apidata['business_category'], _description=apidata['business_description'], owner_id=user.owner_id)
                        response['status'] = '00'
                    else:
                        response['status'] = '50'
                        response['message'] = 'Please fill all required fields'
                else:
                    response['status'] = '50'
            elif int(apidata['status']) == 8:
            # REMOVE BUSINESS
                _business = Hop_Business().verify_auth(apidata['business_id'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Business()._remove(_id=_business.id, owner_id=user.owner_id)
                    response['status'] = '00'
                else:
                    response['status'] = '50'
            elif int(apidata['status']) == 9:
            # GET ALL OUTLET LIST BASED ON OWNER WITH CURRENT BUSINESS ID AS THE EXCEPTION
                _business = Hop_Business().verify_auth(apidata['business_id'])
                if _business is not None and _business.owner_id == user.owner_id:
                    response['data'] = Hop_Business()._outlet_list_exception(business_id=_business.id, user_id=user.id)
                    response['status'] = '00'
                else:
                    response['status'] = '50'
            elif int(apidata['status']) == 10:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Outlet()._data(_id=apidata['outlet_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 11:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Outlet()._update(
                    _id=apidata['outlet_id'], _name=apidata['outlet_name'],
                    _numempid=apidata['outlet_numemp'], _phonenumber=apidata['outlet_phone'],
                    _address=apidata['outlet_address'], _country_id=apidata['outlet_country'],
                    _tax_list=apidata['outlet_tax'], _table_status=apidata['table_status'])
                response['status'] = '00'
            elif int(apidata['status']) == 12:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Outlet()._remove(_id=apidata['outlet_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 13:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Outlet()._data(_id=apidata['outlet_id'])
                response['list'] = Hop_Product_Category_Outlet()._list(outlet_id=apidata['outlet_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 14:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Product_Category_Outlet()._update(
                    outlet_id=apidata['outlet_id'], _list=apidata['list'],
                    owner_id=user.owner_id
                )
                response['status'] = '00'
            elif int(apidata['status']) == 15:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Outlet()._data(_id=apidata['outlet_id'])
                response['list'] = Hop_Product_Outlet()._list(outlet_id=apidata['outlet_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 16:
            # GET THE DATA FOR THE OUTLET
                response['data'] = Hop_Product_Outlet()._update(
                    outlet_id=apidata['outlet_id'], _list=apidata['list'],
                    owner_id=user.owner_id
                )
                response['status'] = '00'

        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
