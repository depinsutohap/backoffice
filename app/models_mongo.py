from . import mongo, Session
import pymongo, requests, time
import pandas as pd
from sqlalchemy import func
from datetime import datetime, timedelta
from itertools import groupby
from .models import Hop_Product_Item, Hop_Ap_Detail, Hop_Special_Promo, \
Hop_Product_Item, Hop_Outlet, Hop_User, Hop_Business, Hop_Product_Outlet, \
Hop_Product_Category, Hop_Tax, Hop_Special_Promo, Hop_Price, Hop_Ap_Detail, \
Hop_Payment_Detail, Hop_Variant_List, Hop_Variant_Item, Hop_Inventory, Hop_Measurement_List, \
Hop_Cost, Hop_Log_Inventory, Hop_Composed_Product
from flask import current_app, request, url_for, Flask, make_response
from openpyxl import Workbook
from openpyxl import load_workbook
from flask import send_from_directory
import os
from os.path import join, dirname, realpath
import pathlib
from hop_core.bo import Report

app = Flask(__name__)

def _to_converted(sources):
    response = {}
    k = sources.split('-')
    response['sampai'] = datetime(year=int(k[0]), month=int(k[1]), day=int(k[2]), hour=23, minute=59, second=59)
    return response

def _from_converted(sources):
    response = {}
    k = sources.split('-')
    response['dari'] = datetime(year=int(k[0]), month=int(k[1]), day=int(k[2]), hour=00, minute=00, second=00)
    return response

class TransLog:
    name = None
    kasir_id = None
    outlet_id = None
    refno = None
    list_item = {
        'item_id' : None,
        'quantity' : None,
        'price_id' : None
    }
    auto_promo = []
    special_promo = None
    sub_total = None
    total = None
    paymen_method = None
    status = None
    added_time = datetime.now()

    def _insert(self, _name, _kasirid, _outletid, _idtransaction, _codestruk, _noorder, _statustransaction, _datesaved, _datepayment, _total, _discount, _tax, _subtotal, _tableid, _product, _autopromo, _reward, _subpayment, _specialpromo, _paymentstruk):
        _data_ = {}
        _data_['name'] = _name
        _data_['kasir_id'] = _kasirid
        _data_['outlet_id'] = _outletid
        _data_['id_transaction'] = _idtransaction
        _data_['code_struk'] = _codestruk
        _data_['no_order'] = _noorder
        _data_['status_transaction'] = _statustransaction
        _data_['dateSaved'] = _datesaved
        _data_['datePayment'] = _datepayment
        _data_['total'] = _total
        _data_['discount'] = _discount
        _data_['tax'] = _tax
        _data_['sub_total'] = _subtotal
        _data_['table_id'] = _tableid
        _data_['product'] = _product
        _data_['auto_promo'] = _autopromo
        _data_['reward'] = _reward
        _data_['sub_payment'] = _subpayment
        _data_['special_promo_id'] = _specialpromo
        _data_['payment_struk'] = _paymentstruk
        _data_['added_time'] = datetime.now()
        mongo.trx_log.insert(_data_)
        return _data_

    def _update(self, _name, _kasirid, _outletid, _idtransaction, _codestruk, _noorder, _statustransaction, _datesaved, _datepayment, _total, _discount, _tax, _subtotal, _tableid, _product, _autopromo, _reward, _subpayment, _specialpromo, _paymentstruk):
        _data_ = {}
        _data_['name'] = _name
        _data_['kasir_id'] = _kasirid
        _data_['outlet_id'] = _outletid
        _data_['code_struk'] = _codestruk
        _data_['no_order'] = _noorder
        _data_['status_transaction'] = _statustransaction
        _data_['dateSaved'] = _datesaved
        _data_['datePayment'] = _datepayment
        _data_['total'] = _total
        _data_['discount'] = _discount
        _data_['tax'] = _tax
        _data_['sub_total'] = _subtotal
        _data_['table_id'] = _tableid
        _data_['product'] = _product
        _data_['auto_promo'] = _autopromo
        _data_['reward'] = _reward
        _data_['sub_payment'] = _subpayment
        _data_['special_promo_id'] = _specialpromo
        _data_['payment_struk'] = _paymentstruk
        _data_['added_time'] = datetime.now()
        return mongo.trx_log.find_and_modify({"id_transaction": _idtransaction},{"$set":_data_})

    def _listbyoutlet(self, _outletid):
        response = {}
        response['data'] = []
        session = Session()
        try:
            for i in mongo.trx_log.find({'outlet_id' : int(_outletid)}):
                _detailproduct = []
                for p in i['product']:
                    session = Session()
                    try:
                        for prod in session.query(Hop_Product_Outlet).filter_by(id = p['id']).all():
                            _prod = Hop_Product_Item()._data(prod.product_item_id)
                            _prod.update({"quantity" : p["quantity"]})
                            _detailproduct.append(_prod)
                    except:
                        session.rollback()
                        raise
                    finally:
                        session.close()
                _detailap = None
                if i['auto_promo'] is not None:
                    _detailap = []
                    for ap in i['auto_promo']:
                        _autopromo = Hop_Ap_Detail()._data(ap['id'])
                        _autopromo.update({"take_it" : ap["take_it"]})
                        _detailproduct.append(_autopromo)
                _detailsp = None
                if i['special_promo_id'] is not None:
                    _detailsp = []
                    for sp in i['special_promo_id']:
                        _specialpromo = Hop_Special_Promo()._data(sp['id'])
                        _detailsp.append(_specialpromo)

                response['data'].append({
                    'id_transaction' : i['id_transaction'],
                    'code_struk' : i['code_struk'],
                    'payment_struk' : i['payment_struk'],
                    'no_order' : i['no_order'],"no_order": "01",
                    "status_transaction": i['status_transaction'],
                    "name": i['name'],
                    "dateSaved": i['dateSaved'],
                    "datePayment": i['datePayment'],
                    "total": i['total'],
                    "discount": i['discount'],
                    "tax": i['tax'],
                    "sub_total": i['sub_total'],
                    "table_id": i['table_id'],
                    "product": _detailproduct,
                    "auto_promo": _detailap,
                    "reward": i['reward'],
                    "sub_payment": i['sub_payment'],
                    "outlet_id": i['outlet_id'],
                    "special_promo_id": _detailsp,
                    'added_time': str(i['added_time']).replace('GMT', '').strip()
                })
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _find_outlet(self, _business_id, _outletid, _ownerid):
        response = []
        session = Session()
        try:
            if int(_outletid) == 0 and int(_business_id) == 0:
                for o in session.query(Hop_Outlet).filter_by(owner_id = _ownerid).all():
                    response.append({'id':o.id, 'name' :o.name})
            elif int(_outletid) == 0 and int(_business_id) != 0:
                _business = session.query(Hop_Business).filter_by(id=_business_id).first()
                for o in session.query(Hop_Outlet).filter_by(business_id = _business.id).all():
                    response.append({'id':o.id, 'name' :o.name})
            elif int(_outletid) != 0:
                _o_name = session.query(Hop_Outlet).filter_by(id=_outletid).first()
                response.append({'id':_outletid, 'name': _o_name.name})
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    # def _find_product(self, _business_id, _outletid, _ownerid):
    #     response = []
    #     session = Session()
    #     try:
    #         if int(_outletid) == 0 and int(_business_id) == 0:
    #             for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
    #                 for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, owner_id=_ownerid).all():
    #                     response.append({'id':o.id, 'name' :o.name})
    #         elif int(_outletid) == 0 and int(_business_id) != 0:
    #             for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
    #                 for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, outlet_id=_outletid).all():
    #                     response.append({'id':o.id, 'name' :o.name})
    #         elif int(_outletid) != 0:
    #             _o_name = session.query(Hop_Outlet).filter_by(id=_outletid).first()
    #             response.append({'id':_outletid, 'name': _o_name.name})
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()
    #
    #     return response


    def _dashboard_sales_co(self, _ownerid, _outletid, _dashon, _dari, _sampai, _business_id): #dashboard dan report - sales per hour
        response = {}
        sales_data = []
        per_hour = []
        hours = []
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        df2 = pd.DataFrame()
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try :
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    sales_data = {}
                    if i is not None and i['status_transaction'] == 3:
                        sales_data.update({'hourPayment' : i['datePayment'].strftime("%H{}").format(':00'), 'discount' : i['discount'], 'sub_total' : i['sub_total']})
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedia
                if int(_dashon) == 0: #jika typenya untuk dashboard
                    category = TransLog()._category_sales_co(_ownerid, _outletid, _dari, _sampai, _business_id)
                    product = TransLog()._product_sales_co(_ownerid, _outletid, _dari, _sampai, _business_id)
                    if len(category['data']) > 0:
                        response['category_sales'] = category['data']
                    else:
                        response['category_sales'] = 0
                    if len(product['product_sales']) > 0:
                        response['product_sales'] = product['product_sales']
                    else:
                        response['product_sales'] = 0
                    response['total_business'] = session.query(Hop_Business).filter_by(owner_id = _ownerid).count()
                for i in range(len(merge_sales)): #hanya sales per hour
                    df = pd.DataFrame(merge_sales[i])
                    df['trans'] = 1
                    df = df.groupby('hourPayment', as_index=False).sum()
                    df['average'] = df['sub_total'] / df['trans']
                    df['average'].round(2)
                    df2 = df2.append(df)
                data_map = df2.groupby('hourPayment', as_index=False).sum()
                master_data = data_map.to_dict('r')
                counter = 0
                avg = 0
                temp_data = []
                for i in range(24):
                    x = len(str(i))
                    if x < 2:
                        y = '{}{}{}'.format('0',i,':00')
                    else:
                        y = '{}{}'.format(i,':00')
                    hours.append(y)
                for i in hours:
                    try: #ketika indexing data ada
                        temp_hour = master_data[counter]['hourPayment'] #penampungan sementara jam dari data source
                        temp_revenue = master_data[counter]['sub_total'] #penampungan revenue dari data source
                        temp_trans = master_data[counter]['trans']
                        temp_average = master_data[counter]['average']
                        hour = i #penampungan jam dari data template
                    except IndexError: #ketika indexxing out of range
                        temp_hour = temp_hour
                        temp_revenue = 0 #ketika tidak ada data maka revenue 0
                        temp_trans = 0
                        temp_average = 0
                        hour = i #penampungan jam dari data template
                    if temp_hour == i: #ketika jam dari data source setara dengan jam dari data template
                        revenue = temp_revenue #revenue diisi dengan penampungan revenue
                        total_trans = temp_trans
                        average = temp_average
                        hour = temp_hour #jam diisi penampungan jam
                        counter +=1
                    else:
                        revenue = 0
                        total_trans = 0
                        average = 0
                        hour = i
                    avg += average
                    temp_data.append({'hour' : hour, 'revenue':revenue , 'total_trans':total_trans, 'average':round(average, 2)})
                total_revenue = sum(get_revenue['revenue'] for get_revenue in temp_data)
                total_sold = sum(get_total['total_trans'] for get_total in temp_data)
                response['average'] = avg
                response['hourly_sales'] = temp_data
                response['total_sold'] = total_sold
                response['total_revenue'] = total_revenue
                response['total_average'] = round(avg, 2)
            else:
                response['hourly_sales'] = []
                response['total_sold'] = 0
                response['total_revenue'] = 0
                response['total_average'] = 0
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _summary_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        summary = []
        sales = []
        merge_sales = []
        outlet_list = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        revenue = 0
        total_revenue = 0
        total_discount = 0
        total_void = 0
        total_tax = 0
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try :
            for o in findOutlet:
                oid = int(o['id'])
                outlet_list.append(oid)
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    if i is not None and i['status_transaction'] == 3:
                        revenue += i['sub_total']
                        total_discount += i['discount']
                    elif i is not None and i['status_transaction'] == 4:
                        total_void += i['sub_total']
            netrevenue = revenue - total_discount - total_void
            total_revenue = netrevenue + total_tax
            response['success_st'] = revenue
            response['void_st'] = total_void
            response['discount_success_st'] = total_discount
            response['nettrevenue'] = netrevenue
            response['tax_sc_st'] = total_tax
            response['total_revenue'] = total_revenue
            # response['cogs'] = Report()._cogs(date_from, date_to, outlet_list, _ownerid)
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    def _product_sales_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['sales'] = []
        response['profit'] = []
        source_data = []
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        product_sales = [] #temporary pecahan data pertama
        product_data = [] #temporary pecahan data kedua
        product_price = []
        df2 = pd.DataFrame()
        session = Session()
        try:
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    sales_data = {}
                    if i is not None and i['status_transaction'] == 3:
                        sales_data.update({'datePayment' : i['datePayment'], 'product': i['product']})
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedia
                for i in range(len(merge_sales)):
                    df = pd.DataFrame(merge_sales[i])
                    df2 = df2.append(df)
                data_map = df2.groupby('datePayment', as_index=False).sum()
                master_data = data_map.to_dict('r')
                for k,v in groupby(master_data,key=lambda x:x['datePayment']): #dikelompokan berdasarkan date payment
                    for d in v:
                        for i in d['product']:
                            id_price = i['price'][0]['id']
                            get_price =  session.query(Hop_Price).filter_by(id=int(id_price)).first()
                            total = i['quantity'] * get_price.value
                            product_data.append({'id': str(i['id']), 'price':int(total), 'quantity': i['quantity'], 'id_price': id_price})
                product_data.sort(key=lambda x:x['id'])
                for k,v in groupby(product_data,key=lambda x:x['id']): #dikelomopkan berdasarkan id product
                    total = 0
                    sold = 0
                    for d in v:
                        sold += d['quantity']
                        get_variant = session.query(Hop_Price).filter_by(id=int(d['id_price'])).first()
                        po = session.query(Hop_Product_Item).filter_by(id=int(k)).first()
                        if get_variant.variant_type is True:
                            vid = get_variant.vid
                            var = session.query(Hop_Variant_List).filter_by(id=vid).first()
                            var_item_1 = session.query(Hop_Variant_Item).filter_by(id=var.variant_item_1).first()
                            var_item_2 = session.query(Hop_Variant_Item).filter_by(id=var.variant_item_2).first()
                            var_item_3 = session.query(Hop_Variant_Item).filter_by(id=var.variant_item_3).first()
                            var_item_4 = session.query(Hop_Variant_Item).filter_by(id=var.variant_item_4).first()
                            if var_item_2 is None:
                                variant2 = ''
                            else:
                                 variant2 = var_item_2.name
                            if var_item_3 is None:
                                variant3 = ''
                            else:
                                variant3 = var_item_3.name
                            if var_item_4 is None:
                                variant4= ''
                            else:
                                variant4 = var_item_4.name
                            product = '{} {} {}'.format(po.name, var_item_1.name, variant2, variant3, variant4)
                        else:
                            product = po.name
                        cat = session.query(Hop_Product_Category).filter_by(id = po.product_category_id).first()
                        total += d['price']
                    product_price.append({'id':int(k),'name':product,'category':cat.name, 'sku':po.sku if po.sku != None else '-','sold_item':sold, 'revenue':total})
                    response['profit'].append({'id':int(k),'name':product,'sku':po.sku if po.sku != None else '-','revenue':total, 'sold_item':sold})
                    total_revenue = sum(get_revenue['revenue'] for get_revenue in product_price)
                    count_text = sum(get_total['sold_item'] for get_total in product_price)
                response['total_revenue'] = total_revenue
                response['total_sold'] = count_text
                response['product_sales'] = product_price
            else:
                response['product_sales'] = []
                response['total_revenue'] = 0
                response['total_sold'] = 0
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _daily_sales_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        df2 = pd.DataFrame()
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        df2 = pd.DataFrame()
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        response['data'] = []
        response['profit'] = []
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    sales_data = {}
                    if i is not None and i['status_transaction'] == 3:
                        sales_data.update({
                            'datePayment' : i['datePayment'].strftime("%Y-%m-%d"),
                            'sub_total': i['sub_total'],
                            'tax': i['tax'],
                            'discount': i['discount'],
                        })
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedia
                for i in range(len(merge_sales)): #hanya sales per hour
                    df = pd.DataFrame(merge_sales[i])
                    df['total_trans'] = 1
                    df2 = df2.append(df)
                data_map = df2.groupby('datePayment', as_index=False).sum()
                data_map['average'] = data_map['sub_total'] / data_map['total_trans']
                master_data = data_map.to_dict('r')
                print('------')
                print(master_data)
                response['data'] = master_data
                response['profit'] = master_data
                total_revenue = sum(get_revenue['sub_total'] for get_revenue in response['data'])
                total_trans = sum(get_total['total_trans'] for get_total in response['data'])
                avg = int(total_revenue) / int(total_trans)
                response['avg_revenue'] = round(avg, 2)
                response['total_revenue'] = total_revenue
                response['count_trx'] = total_trans
            else:
                response['data'] = []
                response['avg_revenue'] = 0
                response['total_revenue'] = 0
                response['count_trx'] = 0
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _detail_sales_data(self, _id_trans):
        response = {}
        response['data']=[]
        product_list = []
        product_price = []
        quantity = []
        log_transaction = []
        total_price = 0
        sub_total = 0
        counter = 0
        session = Session()
        try:
            my_data = mongo.trx_log.find_one({"id_transaction": _id_trans})
            if my_data['status_transaction'] == 1:
                status = 'On Going'
            elif my_data['status_transaction'] == 2:
                status = 'Cancel'
            elif my_data['status_transaction'] == 3:
                status = 'Success'
            elif my_data['status_transaction'] == 4:
                status = 'Void'
            for i in my_data['product']:
                price_id = i['price'][0]['id']
                j = session.query(Hop_Price).filter_by(id = price_id).first()
                total_price = int(i['quantity']) * int(j.value)
                sub_total += total_price
                product_price.append({"total" : total_price})
                k = session.query(Hop_Product_Item).filter_by(id = i['id']).first()
                product_list.append({"product": k.name, "price": j.value, "quantity" : i['quantity']})
            for z in my_data['log_transaction']:
                for x in z['product']:
                    log_prod_item = session.query(Hop_Product_Item).filter_by(id = x['id']).first()
                    log_transaction.append({"date": z['date'], "product_item": log_prod_item.name,"quantity": x['quantity']})
            kasir = session.query(Hop_User).filter_by(id =my_data['kasir_id']).first()
            operator = kasir.name
            discount = my_data['discount']
            tax = my_data['tax']
            total = sub_total - discount - tax
            change = my_data['payment_amount'] - total
            response['data'].append({"no_order": my_data['no_order'], "order_name": my_data['name'], "operator": operator, "table": my_data['table_id'], "code_struk": my_data['code_struk'], "transaction_time" : my_data['log_transaction'][0]['date'], "payment_cashier": my_data['payment_cashier'], "payment" :my_data['payment_name'], "status_transaction": status, "product_list": product_list, "discount": discount, "tax": tax, "product_price": product_price, "sub_total": my_data['sub_total'], "total": total, 'payment_amount': my_data['payment_amount'], "change": change, "log_transaction": log_transaction})
            print(response)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data_sales_trx_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            trx = TransLog()._summary_co(_ownerid, _outletid, _dari, _sampai, _business_id)['success_st']
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    sales_data = {}
                    if i is not None:
                        operator = session.query(Hop_User).filter_by(id=i['kasir_id']).first()
                        if i['status_transaction'] == 1:
                            status = 'On Going'
                        elif i['status_transaction'] == 2:
                            status = 'Cancelled'
                        elif i['status_transaction'] == 3:
                            status = 'Successful'
                        elif i['status_transaction'] == 4:
                            status = 'void'
                        response['data'].append({'time': i['dateSaved'],'operator': operator.name,'idtrx': i['id_transaction'],'statustrx' : status,'total': i['sub_total']})
            response['total_revenue'] = trx
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response #done

    def _category_sales_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        df2 = pd.DataFrame()
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            for o in findOutlet:
                all_sales = []
                trx = TransLog()._product_sales_co(_ownerid, _outletid, _dari, _sampai, _business_id)
                for i in trx['product_sales']:
                    sales_data = {}
                    if i is not None:
                        sales_data.update({'id_product': i['id'],'category': i['category'].lower(),'revenue': i['revenue'],'sold' : i['sold_item']})
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedia
                for i in range(len(merge_sales)): #hanya sales per hour
                    df = pd.DataFrame(merge_sales[i])
                    df = df.groupby('category', as_index=False).sum()
                    df['average'] = df['revenue'] / df['sold']
                    df['average'] = round(df['average'],2)
                data_map = df.groupby('category', as_index=False).sum()
                master_data = data_map.to_dict('r')
                revenue_all = sum(get_revenue['revenue'] for get_revenue in master_data)
                sold_all = sum(get_total['sold'] for get_total in master_data)
                avg = int(revenue_all) / int(sold_all)
                response['data'] = master_data
                response['avg'] = round(avg,2)
                response['total_revenue'] = revenue_all
                response['total_sold'] = sold_all
            else:
                response['data'] = []
                response['avg'] = 0
                response['total_revenue'] = 0
                response['total_sold'] = 0
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _sales_per_outlet_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        response['avg_revenue'] = 0
        response['total_revenue'] = 0
        response['count_trx'] = 0
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            for o in findOutlet:
                all_sales = []
                total = 0
                trans = 0
                avg = 0
                all_data = mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]})
                for i in all_data:
                    _oname = session.query(Hop_Outlet).filter_by(id=i['outlet_id']).first()
                    total += i['sub_total']
                    outlet = _oname.name
                if all_data.count() != 0:
                    avg = total / all_data.count()
                response['data'].append({
                    'outlet': o['name'],
                    'sold': all_data.count(),
                    'revenue': total,
                    'avg': round(avg)
                })
            total_revenue = sum(get_revenue['revenue'] for get_revenue in response['data'])
            total_trans = sum(get_total['sold'] for get_total in response['data'])
            response['avg_revenue'] = round(avg, 2)
            response['total_revenue'] = total_revenue
            response['count_trx'] = total_trans
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response #done

    def _tax_revenue_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            trx = TransLog()._summary_co(_ownerid, _outletid, _dari, _sampai, _business_id)
            for o in findOutlet:
                product_sales = []
                product_data = []
                for i in mongo.trx_log.find({"$and" :[{"outlet_id": int(o['id'])},{"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    x = i['datePayment']
                    product_sales.append({
                        'datePayment' : x,
                        'tax': i['tax_list']
                    })
                for k,v in groupby(product_sales,key=lambda x:x['datePayment']):
                    for d in v:
                        for i in d['tax']:
                            product_data.append({'id': str(i['id'])})
                product_data.sort(key=lambda x:x['id'][0:])
                for k,v in groupby(product_data,key=lambda x:x['id']):
                    po = session.query(Hop_Tax).filter_by(id = int(k)).first()
                    end_price = 0
                    end_price = (po.value/100) * trx['nettrevenue']
                    response['data'].append({'id':int(k),
                            'name':po.name,
                            'value':str(po.value),
                            'total_tax': round(int(end_price)),
                            'grand_total': trx['tax_sc_st']
                    })
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    def _discount_revenue_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        app = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        response['data'] = []
        response['nominal_disc'] = []
        response['nominal_ap'] = []
        response['count_trx'] = 0
        response['total_amount'] = 0
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try :
            for o in findOutlet:
                product_sales = [] #temporary pecahan data pertama
                product_data = [] #temporary pecahan data kedua
                auto_promo = []
                for i in mongo.trx_log.find({ "$and": [{"outlet_id": int(o['id'])} ,{"status_transaction":3} , {"datePayment" : { "$gte" :  dari, "$lte" : sampai}}]}):
                    x = i['datePayment']
                    product_sales.append({
                        'datePayment' : x,
                        'discount': i['special_promo'],
                        'autopromo': i['auto_promo'],
                        'disc_total': i['discount'],
                        'subtotal': i['sub_total']
                    })
                for k,v in groupby(product_sales,key=lambda x:x['datePayment']):
                    for d in v:
                        for i in d['discount']:
                            product_data.append({'id': str(i['id']), 'disc_total':d['disc_total'], 'subtotal': d['subtotal']})
                        for j in d['autopromo']:
                            if j['take_it']==True:
                                auto_promo.append({'id': str(j['id']), 'status': j['take_it'], 'subtotal': d['subtotal']})
                auto_promo.sort(key=lambda x:x['id'][0:])
                product_data.sort(key=lambda x:x['id'][0:])
                disc_total = 0
                nominal = 0
                value = 0
                for k,v in groupby(product_data,key=lambda x:x['id']):
                    count = 0
                    for d in v:
                      po = session.query(Hop_Special_Promo).filter_by(id = int(k)).first()
                      if po.percent is True:
                          nominal = (int(d['subtotal'])/100) * int(po.value)
                          count += int(k)
                          total = count/int(k)
                          value = str(po.value) + '%'
                          response['nominal_disc'].append({'id': str(i['id']), 'nominal':nominal})
                          disc_total = sum(get_revenue['nominal'] for get_revenue in response['nominal_disc'])
                      elif po.percent is False:
                          count += int(k)
                          total = count/int(k)
                          value = 'Rp. ' + str(po.value)
                          disc_total = int(total)*po.value
                          response['nominal_disc'].append({'id': str(i['id']), 'nominal':int(disc_total)})
                    response['data'].append({'id':int(k),
                            'name':po.name,
                            'value': value,
                            'count': total,
                            'total_disc': int(disc_total),
                    })
                for k,v in groupby(auto_promo,key=lambda x:x['id']):
                    count = 0
                    for d in v:
                        ap = session.query(Hop_Ap_Detail).filter_by(id = int(k)).first()
                        if (ap.ap_reward_id == 4):
                            nominal = (int(d['subtotal'])/100) * int(ap.reward_value)
                            count += int(k)
                            total = count/int(k)
                            value = str(ap.reward_value) + '%'
                            response['nominal_ap'].append({'id': str(i['id']), 'nominal': round(nominal)})
                            disc_total = sum(get_revenue['nominal'] for get_revenue in response['nominal_ap'])
                        elif (ap.ap_reward_id == 3):
                            count += int(k)
                            total = count/int(k)
                            value = 'Rp. ' + str(ap.reward_value)
                            disc_total = int(total)*ap.reward_value
                    if(ap.ap_reward_id ==4 or ap.ap_reward_id ==3):
                        response['data'].append({'id':int(k),
                                'name':ap.name,
                                'value': value,
                                'count': total,
                                'total_disc': int(disc_total),
                        })
                response['count_trx'] = sum(get_total['count'] for get_total in response['data'])
                response['total'] = sum(get_amount['total_disc'] for get_amount in response['data'])
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _daily_profit_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        app = []
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            trx = TransLog()._daily_sales_co(_ownerid, _outletid, _dari, _sampai, _business_id)
            product_cost = TransLog()._product_profit_co(_ownerid, _outletid, _dari, _sampai, _business_id)
            for xy in trx['profit']:
                app.append({
                    'datePayment': xy['datePayment'],
                    'discount': xy['discount'],
                    'revenue': xy['sub_total'],
                    'tax' : xy['tax']
                })
            app.sort(key=lambda x:x['datePayment'])
            for k,v in groupby(app,key=lambda x:x['datePayment']):
                total_profit = 0
                cost = product_cost['cost']
                for d in v:
                    total_profit = (int(d['revenue']) + int(d['tax'])) - int(d['discount']) - cost
                    response['data'].append({'datePayment': d['datePayment'],
                    'discount': d['discount'],
                    'revenue': d['revenue'],
                    'tax' : d['tax'],
                    'cost' : cost,
                    'profit': total_profit
                    })
            response['total_trans'] = trx['count_trx']
            response['total_tax'] = sum(get_tax['tax'] for get_tax in response['data'])
            response['total_discount'] = sum(get_discount['discount'] for get_discount in response['data'])
            response['total_cost'] = sum(get_cost['cost'] for get_cost in response['data'])
            response['total_profit'] = sum(get_profit['profit'] for get_profit in response['data'])
            response['total_revenue'] = sum(get_revenue['revenue'] for get_revenue in response['data'])

        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    def _product_profit_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        response['cost'] = []
        app = []
        c_cost = []
        total_cost = []
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            trx = TransLog()._product_sales_co(_ownerid, _outletid, _dari, _sampai, _business_id)
            for xy in trx['profit']:
                app.append({
                    'id': xy['id'],
                    'name': xy['name'],
                    'revenue': xy['revenue'],
                    'sold' : xy['sold_item'],
                    'sku' : xy['sku']
                })
            app.sort(key=lambda x:x['id'])
            for k,v in groupby(app,key=lambda x:x['id']):
                basic = 0
                for c in session.query(Hop_Composed_Product).filter_by(main_product_id = int(k)).all():
                    for a in session.query(Hop_Cost).filter_by(pid = c.ingredients_product_id).all():
                        c_cost.append({'basic': int(a.value) * c.amount})
                total_profit = 0
                discount = 0
                total_cost = sum(get_cost['basic'] for get_cost in c_cost)
                for d in v:
                    cost = int(total_cost) * int(d['sold'])
                    response['cost'] = cost
                    total_profit = int(d['revenue']) - discount - cost
                    response['data'].append({'name': d['name'],
                    'revenue': d['revenue'],
                    'sku': d['sku'],
                    'discount': discount,
                    'cost' : cost,
                    'profit': total_profit
                    })
            response['total_revenue'] = sum(get_revenue['revenue'] for get_revenue in response['data'])
            response['total_discount'] = sum(get_discount['discount'] for get_discount in response['data'])
            response['total_cost'] = sum(get_cost['cost'] for get_cost in response['data'])
            response['total_profit'] = sum(get_profit['profit'] for get_profit in response['data'])
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _sales_per_hour_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        sales_data = []
        per_hour = []
        hours = []
        source_data = []
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        df2 = pd.DataFrame()
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try :
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({ "$and": [ {"outlet_id":int(o['id'])}, {"datePayment": {'$gte': dari, '$lte': sampai}}]}):
                    sales_data = {}
                    if i is not None and i['status_transaction'] == 3:
                        sales_data.update({'hourPayment' : i['datePayment'].strftime("%H{}").format(':00'), 'discount' : i['discount'], 'sub_total' : i['sub_total']})
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedia
                for i in range(len(merge_sales)):
                    df = pd.DataFrame(merge_sales[i])
                    df['trans'] = 1
                    df = df.groupby('hourPayment', as_index=False).sum()
                    df['average'] = df['sub_total'] / df['trans']
                    df['average'].round(2)
                    df2 = df2.append(df)
                data_map = df2.groupby('hourPayment', as_index=False).sum()
                master_data = data_map.to_dict('r')
                counter = 0
                avg = 0
                temp_data = []
                for i in range(24):
                    x = len(str(i))
                    if x < 2:
                        y = '{}{}{}'.format('0',i,':00')
                    else:
                        y = '{}{}'.format(i,':00')
                    hours.append(y)
                for i in hours:
                    try: #ketika indexing data ada
                        temp_hour = master_data[counter]['hourPayment'] #penampungan sementara jam dari data source
                        temp_revenue = master_data[counter]['sub_total'] #penampungan revenue dari data source
                        temp_trans = master_data[counter]['trans']
                        temp_average = master_data[counter]['average']
                        hour = i #penampungan jam dari data template
                    except IndexError: #ketika indexxing out of range
                        temp_hour = temp_hour
                        temp_revenue = 0 #ketika tidak ada data maka revenue 0
                        temp_trans = 0
                        temp_average = 0
                        hour = i #penampungan jam dari data template
                    if temp_hour == i: #ketika jam dari data source setara dengan jam dari data template
                        revenue = temp_revenue #revenue diisi dengan penampungan revenue
                        total_trans = temp_trans
                        average = temp_average
                        hour = temp_hour #jam diisi penampungan jam
                        counter +=1
                    else:
                        revenue = 0
                        total_trans = 0
                        average = 0
                        hour = i
                    avg += average
                    temp_data.append({'hour' : hour, 'revenue':revenue , 'total_trans':total_trans, 'average':average})
                total_revenue = sum(get_revenue['revenue'] for get_revenue in temp_data)
                total_sold = sum(get_total['total_trans'] for get_total in temp_data)
                response['average'] = avg
                response['hourly_sales'] = temp_data
                response['total_sold'] = total_sold
                response['total_revenue'] = total_revenue
                response['total_average'] = round(avg, 2)
            else:
                response['hourly_sales'] = []
                response['total_sold'] = 0
                response['total_revenue'] = 0
                response['total_average'] = 0
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _payment_method_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        product_sales = [] #temporary pecahan data pertama
        product_data = [] #temporary pecahan data kedua
        merge_sales = []
        findOutlet = TransLog()._find_outlet(_business_id, _outletid, _ownerid)
        df2 = pd.DataFrame()
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try :
            for o in findOutlet:
                all_sales = []
                for i in mongo.trx_log.find({ "$and": [ {"outlet_id":int(o['id'])}, {"datePayment": {'$gte': dari, '$lte': sampai}}]}):
                    sales_data = {}
                    if i is not None and i['status_transaction'] == 3:
                        x = i['datePayment']
                        po = session.query(Hop_Payment_Detail).filter_by(id = int(i['sub_payment'])).first()
                        sales_data.update({
                            'datePayment' : x,
                            'payment_id': i['sub_payment'],
                            'payment_method': po.name,
                            'subtotal': i['sub_total']
                        })
                    all_sales.append(sales_data)
                merge_sales.append(all_sales)
            merge_sales = [x for x in merge_sales if x != []]
            if len(merge_sales) > 0: #jika data tersedi
                for i in range(len(merge_sales)):
                    df = pd.DataFrame(merge_sales[i])
                    df2 = df2.append(df)
                data_map = df2.groupby('payment_method', as_index=False).sum()
                master_data = data_map.to_dict('r')
                print(master_data)
                response['data'] = master_data
            else:
                response['data'] = []
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    def _stock(self, _outletid, _ownerid, _dari, _sampai):
        response = {}
        response['data'] = []
        count = []
        total = 0
        arb = []
        session = Session()
        try:
            for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
                for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, outlet_id=_outletid).all():
                    if (c.type_id==2):
                        cost = session.query(Hop_Cost).filter_by(id = c.cost_id).first()
                        total = int(c.quantity) * int(cost.value)
                        # print(total)
                    elif (c.type_id ==3):
                        cost2 = session.query(Hop_Cost).filter_by(pid = c.pid).first()
                        total = int(c.quantity) * int(cost2.value)
                        # print(total)
                    count.append({
                        'id': c.pid,
                        'total': total,
                    })
            count.sort(key=lambda x:x['id'])
            for k,v in groupby(count, key=lambda x:x['id']):
                for i in session.query(func.max(Hop_Inventory.added_time), Hop_Inventory.pid).group_by(Hop_Inventory.pid).filter_by(pid=int(k)).all():
                    item = session.query(Hop_Inventory).filter(Hop_Inventory.pid == i[1]).filter(Hop_Inventory.added_time == i[0]).first()
                    sums = 0
                    for d in v:
                        sums += int(d['total'])
                    for z in session.query(Hop_Product_Item).filter_by(id=int(k), composed_type=False, status=True).all():
                        measurement = '-'
                        if z.measurement_id is not None :
                            measurement = session.query(Hop_Measurement_List).filter_by(id = z.measurement_id).first()
                            measurement = measurement.name
                        category = session.query(Hop_Product_Category).filter_by(id = z.product_category_id).first()
                        response['data'].append({
                            'name': z.name,
                            'sku': z.sku if j.sku != None else '-',
                            'barcode': z.barcode if z.barcode != None else '-',
                            'unit': measurement,
                            'category': category.name,
                            'stock': int(item.fs),
                            'revenue': sums
                        })
            response['total_grand'] = sum(get_revenue['revenue'] for get_revenue in response['data'])
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _find_product(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = []
        session = Session()
        try:
            if int(_outletid) == 0 and int(_business_id) == 0:
                for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
                    for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, owner_id=_ownerid).filter(Hop_Log_Inventory.added_time.between(_dari,_sampai)).all():
                        response.append({'type_id':c.type_id, 'cost_id':c.cost_id, 'quantity':c.quantity, 'pid':c.pid})
            if int(_outletid) != 0 and int(_business_id) == 0:
                for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
                    for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, owner_id=_ownerid).filter(Hop_Log_Inventory.added_time.between(_dari,_sampai)).all():
                        response.append({'type_id':c.type_id, 'cost_id':c.cost_id, 'quantity':c.quantity, 'pid':c.pid})
            else:
                for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
                    for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, outlet_id=_outletid).filter(Hop_Log_Inventory.added_time.between(_dari,_sampai)).all():
                        response.append({'type_id':c.type_id, 'cost_id':c.cost_id, 'quantity':c.quantity, 'pid':c.pid})
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return response

    def _stock_co(self, _ownerid, _outletid, _dari, _sampai, _business_id):
        response = {}
        response['data'] = []
        count = []
        total = 0
        arb = []
        date_from = _from_converted(_dari)
        date_to = _to_converted(_sampai)
        dari = date_from['dari']
        sampai = date_to['sampai']
        findProduct = TransLog()._find_product(_ownerid, _outletid, dari, sampai, _business_id)
        session = Session()
        try:
            int(_outletid)
            int(_business_id)
        except:
            response['status'] = 50
            return response
        try:
            for c in findProduct:
                if (int(c['type_id'])==2):
                    cost = session.query(Hop_Cost).filter_by(id = int(c['cost_id'])).first()
                    total = int(c['quantity']) * int(cost.value)
                elif (int(c['type_id']) ==3):
                    cost2 = session.query(Hop_Cost).filter_by(pid = int(c['pid'])).first()
                    total = int(c['quantity']) * int(cost2.value)
                count.append({
                    'id': int(c['pid']),
                    'total': total,
                })
            count.sort(key=lambda x:x['id'])
            for k,v in groupby(count, key=lambda x:x['id']):
                for i in session.query(func.max(Hop_Inventory.added_time), Hop_Inventory.pid).group_by(Hop_Inventory.pid).filter_by(pid=int(k)).all():
                    item = session.query(Hop_Inventory).filter(Hop_Inventory.pid == i[1]).filter(Hop_Inventory.added_time == i[0]).first()
                    sums = 0
                    for d in v:
                        sums += d['total']
                    for z in session.query(Hop_Product_Item).filter_by(id=int(k), composed_type=False, status=True).all():
                        measurement = ''
                        if z.measurement_id is not None :
                            measurement = session.query(Hop_Measurement_List).filter_by(id = z.measurement_id).first()
                            measurement = measurement.name
                        category = session.query(Hop_Product_Category).filter_by(id = z.product_category_id).first()
                        response['data'].append({
                            'name': z.name,
                            'sku': z.sku if z.sku != None else '-',
                            'barcode': z.barcode if z.barcode != None else '-',
                            'unit': measurement,
                            'category': category.name,
                            'stock': int(item.fs),
                            'revenue': sums
                        })
            response['total_grand'] = sum(get_revenue['revenue'] for get_revenue in response['data'])
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _stock_all(self, _ownerid, _dari, _sampai):
        response = {}
        response['data'] = []
        count = []
        total = 0
        arb = []
        session = Session()
        try:
            for j in session.query(Hop_Product_Item).filter_by(owner_id=_ownerid, composed_type=False, status=True).all():
                for c in session.query(Hop_Log_Inventory).filter_by(pid = j.id, status=True, owner_id=_ownerid).all():
                    if (c.type_id==2):
                        cost = session.query(Hop_Cost).filter_by(id = c.cost_id).first()
                        total = int(c.quantity) * int(cost.value)
                        # print(total)
                    elif (c.type_id ==3):
                        cost2 = session.query(Hop_Cost).filter_by(pid = c.pid).first()
                        total = int(c.quantity) * int(cost2.value)
                        # print(total)
                    count.append({
                        'id': c.pid,
                        'total': total,
                    })
            count.sort(key=lambda x:x['id'])
            for k,v in groupby(count, key=lambda x:x['id']):
                for i in session.query(func.max(Hop_Inventory.added_time), Hop_Inventory.pid).group_by(Hop_Inventory.pid).filter_by(pid=int(k)).all():
                    item = session.query(Hop_Inventory).filter(Hop_Inventory.pid == i[1]).filter(Hop_Inventory.added_time == i[0]).first()
                    sums = 0
                    for d in v:
                        sums += d['total']
                    for z in session.query(Hop_Product_Item).filter_by(id=int(k), composed_type=False, status=True).all():
                        measurement = ''
                        if z.measurement_id is not None :
                            measurement = session.query(Hop_Measurement_List).filter_by(id = z.measurement_id).first()
                            measurement = measurement.name
                        category = session.query(Hop_Product_Category).filter_by(id = z.product_category_id).first()
                        response['data'].append({
                            'name': z.name,
                            'sku': z.sku if j.sku != None else '-',
                            'barcode': z.barcode if z.barcode != None else '-',
                            'unit': measurement,
                            'category': category.name,
                            'stock': int(item.fs),
                            'revenue': sums
                        })
            response['total_grand'] = sum(get_revenue['revenue'] for get_revenue in response['data'])
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _count(self, _ownerid):
        response = {}
        session = Session()
        try:
            v = 0
            w = 0
            x = 0
            y = 0
            z = 0
            business = session.query(Hop_Business).filter_by(owner_id= _ownerid).all()
            for b in business:
                for o in session.query(Hop_Outlet).filter_by(business_id = b.id).all():
                    outlet = session.query(Hop_Outlet).filter_by(id = o.id).first()
                    a = mongo.trx_log.find({ "outlet_id" : outlet.id }).count()
                    b = mongo.trx_log.find({"$and": [{ "outlet_id" : outlet.id },{ "status_transaction": 3 }]}).count()
                    c = mongo.trx_log.find({"$and": [{ "outlet_id" : outlet.id },{ "status_transaction": 1 }]}).count()
                    d = mongo.trx_log.find({"$and": [{ "outlet_id" : outlet.id },{ "status_transaction": 2 }]}).count()
                    e = mongo.trx_log.find({"$and": [{ "outlet_id" : outlet.id },{ "status_transaction": 4 }]}).count()
                    v += a
                    w += b
                    x += c
                    y += d
                    z += e
            response['total_trans'] = v
            response['success_trans'] = w
            response['ongoing_trans'] = x
            response['cancelled_trans'] = y
            response['void_trans'] = z
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, _outletid):
        response = {}
        _trxlog = mongo.trx_log.find_one({'outlet_id' : _outletid})
        if _trxlog is not None:
            response["id_transaction"] =  _trxlog["id_transaction"]
            response["code_struk"] =  _trxlog["code_struk"]
            response["payment_struk"] =  _trxlog["payment_struk"]
            response["no_order"] =  _trxlog["no_order"]
            response["status_transaction"] =  _trxlog["status_transaction"]
            response["name"] =  _trxlog["name"]
            response["dateSaved"] =  _trxlog["dateSaved"]
            response["datePayment"] =  _trxlog["datePayment"]
            response["total"] =  _trxlog["total"]
            response["discount"] =  _trxlog["discount"]
            response["tax"] =  _trxlog["tax"]
            response["sub_total"] =  _trxlog["sub_total"]
            response["table_id"] =  _trxlog["table_id"]
            response["product"] =  []
            for di in _trxlog['product']:
                response['product'].append({
                    'id' : Hop_Product_Item()._data(di['id']),
                    'quantity' : di['quantity'],
                })
            response["auto_promo"] =  _trxlog["auto_promo"]
            response["reward"] =  _trxlog["reward"]
            response["sub_payment"] =  _trxlog["sub_payment"]
            response["outlet_id"] =  _trxlog["outlet_id"]
            response["special_promo_id"] =  _trxlog["special_promo_id"]
            response["added_time"] =  str(_trxlog["added_time"]).replace("GMT", "").strip()

        return response
