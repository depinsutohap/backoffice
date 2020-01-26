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


async def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

# ==============================================================================
# SPECIFICS DATA [API]
# ==============================================================================

# THIS IS THE API FOR SEARCH LIST

@api_1.route('/data/search', methods=['POST', 'GET'])
@_auth.login_required
async def _api_search(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                session = Session()
                try:
                    _query = session.query(Hop_Product_Outlet).filter_by(owner_id=user.owner_id, status=True).filter(Hop_Product_Item.name.like('%' + apidata['q'] + '%')).order_by(Hop_Product_Item.name).limit(5).all()
                    response['q'] = []
                    for i in _query:
                        response['q'].append([i.id, i.name])
                        response['status'] = '00'
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            elif int(apidata['status']) == 1:
                session = Session()
                try:
                    _query = session.query(Hop_Product_Item).filter(Hop_Product_Item.owner_id==user.owner_id, Hop_Product_Item.id!=apidata['pid'], Hop_Product_Item.composed_type==False, Hop_Product_Item.status==True, Hop_Product_Item.name.like('%' + apidata['q'] + '%'), ~Hop_Product_Item.id.in_(apidata['except'])).order_by(Hop_Product_Item.name).limit(3).all()
                    response['q'] = []
                    for i in _query:
                        response['q'].append([i.id, i.name, i.variant_type])
                        response['status'] = '00'
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            elif int(apidata['status']) == 2:
                response['q'] = Hop_Variant_List()._list(apidata['ipid'])
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                session = Session()
                try:
                    _query = session.query(Hop_Measurement_List).filter(Hop_Measurement_List.id!=apidata['except'], Hop_Measurement_List.owner_id==user.owner_id, Hop_Measurement_List.status==True, Hop_Measurement_List.name.like('%' + apidata['q'] + '%')).order_by(Hop_Measurement_List.name).limit(3).all()
                    response['q'] = []
                    response['status'] = '50'
                    for i in _query:
                        response['q'].append([i.id, i.name])
                    if len(response['q']) > 0:
                        response['status'] = '00'
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            elif int(apidata['status']) == 4:
                session = Session()
                try:
                    _query = session.query(Hop_Measurement_List).filter(Hop_Measurement_List.owner_id==user.owner_id, Hop_Measurement_List.status==True, Hop_Measurement_List.name ==  apidata['q'] ).order_by(Hop_Measurement_List.name).first()
                    response['status'] = '50'
                    if _query is not None:
                        response['q'] = [_query.id, _query.name]
                        response['status'] = '00'
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            elif int(apidata['status']) == 5:
                _except = []
                session = Session()
                try:
                    for i in apidata['except']:
                        if i[1] == 'false':
                            _except.append(i[0])
                        else:
                            _variant_count = session.query(Hop_Variant_List).filter(Hop_Variant_List.product_item_id==i[0], Hop_Variant_List.status==True, ~Hop_Variant_List.id.in_(i[2])).count()
                            if _variant_count == 0:
                                _except.append(i[0])
                    _query = session.query(Hop_Product_Item).filter(Hop_Product_Item.owner_id==user.owner_id,
                    Hop_Product_Item.status==True, Hop_Product_Item.composed_type==False,
                    Hop_Product_Item.name.like('%' + apidata['q'] + '%'), or_(Hop_Product_Item.invent_type==True, Hop_Product_Item.variant_type==True),
                    ~Hop_Product_Item.id.in_(_except)).order_by(Hop_Product_Item.name).limit(3).all()
                    response['q'] = []
                    for i in _query:
                        _variant_count = session.query(Hop_Variant_List).filter(Hop_Variant_List.product_item_id==i.id, Hop_Variant_List.invent_type==True, Hop_Variant_List.status==True).count()
                        if i.variant_type == True and _variant_count > 0:
                            response['q'].append([i.id, i.name, i.variant_type])
                        elif i.variant_type == False:
                            response['q'].append([i.id, i.name, i.variant_type])
                        response['status'] = '00'
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            elif int(apidata['status']) == 6:
                response['q'] = Hop_Variant_List()._list_except(apidata['ipid'], apidata['except'])
                response['status'] = '00'
        return json(response)
    else:
        return redirect(url_for('main.index'))

# THIS IS THE API FOR GENERAL LIST

@api_1.route('/data/general', methods=['POST', 'GET'])
@_auth.login_required
async def _api_general(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Hop_Business_Category()._list()
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                response['data'] = Hop_Num_Emp()._list()
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_User_Outlet()._list(user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_Business()._listbyownerid(user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_User_Outlet()._listbybusinessid(apidata['business'])
                response['status'] = '00'

            else:
                response['status'] = '50'
                response['message'] = 'Your credential are invalid.'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))

# THIS IS THE API FOR GENERAL LOCATION LIST

@api_1.route('/data/location', methods=['POST', 'GET'])
@_auth.login_required
async def _api_location(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        if int(apidata['status']) == 0:
            response['data'] = Hop_Countries()._list()
            response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))

# THIS IS THE API FOR GENERAL USER DATA

@api_1.route('/data/user', methods=['POST', 'GET'])
@_auth.login_required
async def _api_users(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                # OWNER DATA
                response['data'] = Hop_User()._owner_data(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                # OWNER DATA
                response['data'] = Hop_User()._data(_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                # OWNER DATA
                response['data'] = Hop_User()._update(_id=user.id, _name=apidata['name'], _email=apidata['email'], _phone=apidata['phone'])
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                # OWNER DATA
                if user.verify_password(apidata['cur_pass']):
                    if apidata['cur_pass'] != apidata['new_pass']:
                        if len(apidata['new_pass'].strip()) >= 8:
                            if apidata['new_pass'] == apidata['pass_ver']:
                                response['data'] = Hop_User()._update_password(_id=user.id, _new_pass=apidata['new_pass'])
                                response['status'] = '00'
                            else:
                                response['status'] = '50'
                                response['message'] = 'Password and confirm password does not match'
                        else:
                            response['status'] = '50'
                            response['message'] = 'Password must be at least 8 characters in length.'
                    else:
                        response['status'] = '50'
                        response['message'] = 'Your new password must be different from your previous password.'
                else:
                    response['status'] = '50'
                    response['message'] = 'The password is incorrect'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))

# PROMO SECTION's API
@api_1.route('/data/billing', methods=['POST', 'GET'])
@_auth.login_required
async def _api_billing(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            # PRODUCT CATEGORY
            if int(apidata['status']) == 0:
                response['data'] = Hop_User_Outlet()._list(user.id)
                response['package'] = Hop_Billing_Package_Item()._list(1)
                response['count'] = Hop_Billing_Invoice()._invoice_trx_count(user.id)
                response['ongoing'] = Hop_Billing_Invoice()._check_ongoing_payment(user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                response['data'] = Hop_Billing_Invoice()._add_order_overview(
                    user_id=user.id, package_id=apidata['package_id'],
                    outlet_list=apidata['outlet_list'], owner_id=user.owner_id
                )
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_Billing_Invoice()._exist_order(
                    user_id=user.id
                )
                response['payment'] = Hop_Billing_Payment()._list()
                response['ongoing'] = Hop_Billing_Invoice()._check_ongoing_payment(user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_Billing_Invoice()._remove_order(
                    user_id=user.id, trx_list=apidata['trx_list'], owner_id=user.owner_id
                )
                response['list'] = Hop_Billing_Invoice()._exist_order(user_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_Billing_Invoice()._proceed_payment(
                    user_id=user.id, payment_id=apidata['payment_id']
                )
                response['count'] = Hop_Billing_Invoice()._invoice_trx_count(user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 5:
                response['data'] = Hop_Billing_Invoice()._history_list(user_id=user.id)
                response['status'] = '00'
            elif int(apidata['status']) == 6:
                response['data'] = Hop_Billing_Invoice()._data_ongoing(user_id=user.id)
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
