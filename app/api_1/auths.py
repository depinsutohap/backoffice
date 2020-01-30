import ast
from app import app
from . import api_1
import json as _json
from .. import _auth, jinja
from decimal import *
from app.models import *
from sanic.response import json, raw, redirect
from ..models import Hop_User, Hop_Business, Hop_Outlet, Hop_Business, Hop_Login_Log, Hop_User_Outlet

#===================================================================
# SPECIFICS DATA [API]
# ==============================================================================

# THIS IS API FOR LOGIN
# /api-v1/backoffice/auth/login
@api_1.route('/auth/login', methods=['GET', 'POST'])
async def request_login(request):
    if request.method == 'POST':
        response = {}
        response['status'] = '00'
        response['message'] = 'Welcome to Hop\'s backoffice'
        apidata = _json.loads(request.form['data'][0])
        if len(apidata['email']) > 0:
            user_email = Hop_User().verify_auth(apidata['email'])
            if user_email is not None:
                if user_email.verify_password(apidata['password']):
                    if user_email.role_id != 3:
                        response['user_id'] = user_email.id
                        response['role_id'] = user_email.role_id
                        response['token'] = user_email.generate_token()
                        response['name'] = user_email.name
                        response['phone_number'] = user_email.phone_number
                        # response['lang'] = user_email.language_id if user_email.language_id != None else 1
                        response['lang'] = 1
                        response['email'] = user_email.email if user_email.email != None else '-'
                        response['permission'] = None
                        if user_email.role_id != 1:
                            response['permission'] = Hop_User_Outlet()._permission(user_email.id)
                        Hop_Login_Log()._insert(user_email.id, 2)
                        _auth.login_user(request, user_email)
                    else:
                        response['status'] = '50'
                        response['message'] = 'Your credential are invalid.'
                else:
                    response['status'] = '50'
                    response['message'] = 'The username or password is incorrect'

            else:
                response['status'] = '50'
                response['message'] = 'The username or password is incorrect'
        else:
            response['status'] = '50'
            response['message'] = 'Please fill out all required fields.'
        return json(response)
    else:
        return redirect('/')

@api_1.route('/auth/register', methods=['GET', 'POST'])
async def _add_register(request):
    if request.method == "POST":
        response = {}
        apidata = _json.loads(request.form['data'][0])
        if(len(apidata['name']) > 0 and len(apidata['email']) > 0 and len(apidata['phone']) > 0):
            check_email = Hop_User().verify_auth(apidata['email'])
            check_phone = Hop_User().verify_auth(apidata['phone'])
            if check_email is None and check_phone is None:
                if len(apidata['password'].strip()) >= 8:
                    response['data'] = Hop_User()._insertowner(apidata['name'],apidata['phone'],apidata['email'], apidata['password'], apidata['refferal'])
                    response['status'] = '00'
                    response['message'] = 'Welcome to Hop! Be ready to Hop and Grow!'
                    user = Hop_User().verify_auth(response['data']['id'])
                    _auth.login_user(request, user)
                    Hop_Login_Log()._insert(user.id, 2)

                    subject = "Hey, " + user.name + "! Awalilah perjalanan usahamu dengan Hop sekarang."
                    content = jinja.env.get_template('mail/register.html').render(
                        name=user.name, subject=subject
                    )
                    await app.send_email(
                        targetlist=user.email,
                        subject=subject,
                        content=content,
                        html=True,
                        # attachments=attachments
                    )
                else:
                    response['status'] = '50'
                    response['message'] = 'Password must be at least 8 characters in length.'
            else:
                response['status'] = '50'
                response['message'] = 'This Email or Phone Number has been registered.'
        else:
            response['status'] = '50'
            field = 'name'
            if len(apidata['phone']) == 0:
                field = 'phone number'
            elif len(apidata['email']) == 0:
                field = 'E-mail'
            response['message'] = 'Please fill your ' + field + ' to register to hop.cash.'
        return json(response)
    else:
        return redirect('/')

@api_1.route('/auth/detail', methods=['POST', 'GET'])
@_auth.login_required
async def _add_detail(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            if len(apidata['business_name'].strip()) > 0 and len(apidata['outlet_name'].strip()) > 0 and \
                len(apidata['outlet_phone_number'].strip()) > 0 and len(apidata['outlet_address'].strip()) > 0:
                _business = Hop_Business()._insert(apidata['business_name'], apidata['business_category'], user.owner_id)
                _outlet = Hop_Outlet()._insert(apidata['outlet_name'], apidata['outlet_num_emp'], apidata['outlet_phone_number'], apidata['outlet_address'], apidata['outlet_country'], _business['id'], user.owner_id)
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'Please fill all required fields.'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect('/')


# @api_1.route('/auth/reset_password', methods=['GET', 'POST'])
# async def _reset_password(request):
#     if request.method == "POST":
#         response = {}
#         apidata = _json.loads(request.form['data'][0])
#         print(apidata)
#         if len(apidata['email']) > 0:
#             Hop_User()._insertowner(apidata['email'])
#             response['status'] = '00'
#             response['messages'] = 'success'
#         else:
#             response['status'] = '50'
#             response['messages'] = 'email sudah ada yang pakai'
#         return json(response)
#     else:
#         return redirect('/')
