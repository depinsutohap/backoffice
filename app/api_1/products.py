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

# PRODUCTS SECTION's API
@api_1.route('/data/products', methods=['POST', 'GET'])
@_auth.login_required
async def _api_products(request):
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        print(request.form)
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        if user is not None and user.verify_token(apidata['token']):
            # PRODUCT CATEGORY
            if int(apidata['status']) == 0:
                response['data'] = Hop_Product_Category()._list(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 1:
                response['data'] = Hop_Product_Category()._insert(category_name=apidata['category_name'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 2:
                response['data'] = Hop_Product_Category()._data(category_id=apidata['category_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 3:
                response['data'] = Hop_Product_Category()._update(category_id=apidata['category_id'], category_name=apidata['category_name'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 4:
                response['data'] = Hop_Product_Category()._remove(category_id=apidata['category_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 5:
                response['data'] = Hop_Product_Category()._remove_many(category_list=apidata['category_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 6:
                response['data'] = Hop_Product_Category()._remove_many(category_list=apidata['category_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 7:
                response['data'] = Hop_Product_Category()._remove_many(category_list=apidata['category_list'], owner_id=user.owner_id)
                response['status'] = '00'
            # PRODUCT ITEM
            elif int(apidata['status']) == 8:
                response['data'] = Hop_Product_Item()._list(owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 9:
                response['data'] = Hop_Product_Item()._insert(product_name=apidata['product_name'], \
                    product_category=apidata['product_category'], product_price=apidata['product_price'], \
                    product_sku=apidata['product_sku'], product_barcode=apidata['product_barcode'], \
                    product_measurement=apidata['product_measurement'], \
                    product_description=apidata['product_description'], product_composed=apidata['product_composed'], \
                    product_sold=apidata['product_sold'], product_variant=apidata['product_variant'], \
                    product_stock=apidata['product_stock'], \
                    data_variant=apidata['data_variant'], \
                    owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 10:
                response['data'] = Hop_Product_Item()._data(_id=apidata['product_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 11:
                response['data'] = Hop_Product_Item()._update_data(product_id=apidata['product_id'], product_name=apidata['product_name'], \
                    product_category=apidata['product_category'], product_sku=apidata['product_sku'], product_barcode=apidata['product_barcode'], \
                    product_measurement=apidata['product_measurement'], product_description=apidata['product_description'], \
                    product_sold=apidata['product_sold'], product_composed=apidata['product_composed'], product_variant=apidata['product_variant'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 12:
                response['data'] = Hop_Product_Item()._remove(product_id=apidata['product_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 13:
                response['data'] = Hop_Product_Item()._remove_many(product_list=apidata['product_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 14:
                response['data'] = Hop_Product_Item()._price(_id=apidata['product_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 15:
                response['data'] = Hop_Product_Item()._update_price(_id=apidata['product_id'], _same_price=apidata['same_price'], _price=apidata['price'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 16:
                response['data'] = Hop_Product_Item()._data_price_outlet(_id=apidata['product_id'], _outlet_id=apidata['outlet_id'], _same_price=apidata['same_price'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 17:
                response['data'] = Hop_Product_Item()._update_outlet_price(_id=apidata['product_id'], _price=apidata['price'], outlet_id=apidata['outlet_id'], owner_id=user.owner_id)
                response['status'] = '00'
            # VARIANT
            elif int(apidata['status']) == 18:
                response['data'] = Hop_Variant_Category()._listbyproduct(_product=apidata['product_id'])
                response['status'] = '00'
            elif int(apidata['status']) == 19:
                response['data'] = Hop_Variant_List()._update(item_id=apidata['product_id'], data_list=apidata['data_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 20:
                response['data'] = Hop_Product_Item()._ingredients(_id=apidata['product_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 21:
                response['data'] = Hop_Composed_Product()._insert(_main_list=apidata['main_data_list'], _list=apidata['product_list'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 22:
                response['data'] = Hop_Composed_Product()._exist_list_item(mpid=apidata['mpid'], mvid=apidata['mvid'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 23:
                response['data'] = Hop_Composed_Product()._exist_list_variant(impid=apidata['import_mpid'], mpid=apidata['mpid'], mvid=apidata['mvid'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 24:
                response['data'] = Hop_Composed_Product()._data(mpid=apidata['import_mpid'], mvid=apidata['import_mvid'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 25:
                response['data'] = Hop_Product_Item()._stock(_id=apidata['product_id'], owner_id=user.owner_id)
                response['status'] = '00'
            elif int(apidata['status']) == 26:
                response['data'] = Hop_Product_Item()._update_stock(_id=apidata['product_id'], _stock=apidata['stock'], owner_id=user.owner_id)
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect(url_for('main.index'))
