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
@api_1.route('/data/employee', methods=['POST', 'GET'])
@_auth.login_required
async def _api_employee(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Hop_User()._list_all_employee(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                if Hop_User().verify_user(_id=apidata['employee_phone']):
                    if (len(apidata['employee_email']) > 0 and Hop_User().verify_user(_id=apidata['employee_email'])) or len(apidata['employee_email']) == 0:
                        response['data'] = Hop_User()._insert_employee(_name=apidata['employee_name'], _email=apidata['employee_email'], _phonenumber=apidata['employee_phone'], _password=apidata['employee_password'], _role_id=apidata['employee_role_id'], owner_id=user.owner_id)
                        response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                        response['status'] = '00'
                    else:
                        response['status'] = '50'
                        response['message'] = 'This e-mail is already registered'
                else:
                    response['status'] = '50'
                    response['message'] = 'This phone number is already registered'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_User_Outlet()._insert_outlet(_outlet_list=apidata['employee_outlet_list'], _user_id=apidata['employee_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_User_Outlet()._insert_permission(
                    user_id=apidata['employee_id'],
                    outlet_id=apidata['outlet_id'],
                    mobile_order=apidata['employee_mobile_order'],
                    mobile_payment=apidata['employee_mobile_payment'],
                    mobile_void=apidata['employee_mobile_void'],
                    mobile_change_trx=apidata['employee_mobile_change_trx'],
                    mobile_custom_price=apidata['employee_mobile_custom_price'],
                    mobile_custom_discount=apidata['employee_mobile_custom_discount'],
                    mobile_reprint_reciept=apidata['employee_mobile_reprint_reciept'],
                    mobile_reprint_kitchen=apidata['employee_mobile_reprint_kitchen'],
                    mobile_print_invoice=apidata['employee_mobile_print_invoice'],
                    mobile_history=apidata['employee_mobile_history'],
                    mobile_customer=apidata['employee_mobile_customer'],
                    bo_outlet=apidata['employee_bo_outlet'],
                    bo_report=apidata['employee_bo_report'],
                    bo_product=apidata['employee_bo_product'],
                    bo_inventory=apidata['employee_bo_inventory'],
                    bo_tax=apidata['employee_bo_tax'],
                    bo_employee=apidata['employee_bo_employee'],
                    bo_promo=apidata['employee_bo_promo'],
                    bo_customer=apidata['employee_bo_customer'],
                    bo_billing=apidata['employee_bo_billing'],
                    bo_email=apidata['employee_bo_email']
                )
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_User_Outlet()._data(_outlet_id=apidata['outlet_id'], _user_id=apidata['employee_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 5:
                response['data'] = Hop_User()._data(_id=apidata['employee_id'])
                response['outlet_list'] = Hop_User_Outlet()._list(_user_id=user.id)
                response['data_outlet'] = Hop_User_Outlet()._data_list(_user_id=apidata['employee_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 6:
                response['data'] = Hop_User()._data(_id=apidata['employee_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 7:
                response['data'] = Hop_User()._update_employee(_id=apidata['employee_id'], _name=apidata['employee_name'], _email=apidata['employee_email'], _phonenumber=apidata['employee_phone'], _password=apidata['employee_password'], _role_id=apidata['employee_role_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 8:
                response['data'] = Hop_User()._remove_employee(_id=apidata['employee_id'], owner_id=user.owner_id)
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
