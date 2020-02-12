import time, ast
import json as _json
from . import api_1
from .. import _auth
from decimal import *
from app.models import *
from sqlalchemy import or_
from datetime import datetime
from ..models_mongo import TransLog
from ..utils import *
from sanic.response import json, raw, redirect
from sanic import Sanic, response
from ..models import Hop_User, Hop_Business, Hop_Outlet, Hop_Product_Item, \
    Hop_Role, Hop_Product_Outlet, Hop_Provinces, Hop_Cities,  Hop_Business_Category, \
    Hop_Countries, Hop_Product_Category, Hop_Tax, Hop_Tax_Type, Hop_Special_Promo, Hop_Ap_Detail, \
    Hop_Business, Hop_Num_Emp, Hop_Price, Hop_Measurement_List, Hop_User_Outlet
import pandas as pd
import os
from os import path
from os.path import join, dirname, realpath
import pathlib
from pathlib import Path
import PyPDF2
import urllib.request

app = Sanic(__name__)
excelDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'file_secure\\excels\\')
# image_dir = (os.path.join(os.path.dirname(__file__),'static\\src\\logo.png'))
print('---')
# print(image_dir)

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
                response['data'] = TransLog()._product_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 3:
                response['data'] = TransLog()._daily_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 4:
                response['data'] = TransLog()._data_sales_trx_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 5:
                response['data'] = TransLog()._category_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 6:
                response['data'] = TransLog()._sales_per_outlet_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
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
                response['data'] = TransLog()._dashboard_sales_co(user.owner_id, apidata['outlet'], apidata['dash_on'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 12:
                response['data'] = TransLog()._payment_method_co(user.owner_id,apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 13:
                response['data'] = TransLog()._stock_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 14:
                response['data'] = TransLog()._sales_per_hour_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            if int(apidata['status']) == 15:
                response['data'] = TransLog()._detail_sales_data(apidata['trx_id'])
                response['status'] = '00'
            if int(apidata['status']) == 16:
                filename = 'summary-report.xlsx'
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return json(response)
    else:
        return redirect('/')


@api_1.route('/data/export', methods=['POST', 'GET'])
@_auth.login_required
async def _api_export(request):
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        user = Hop_User().verify_auth(apidata['id'])
        session = Session()
        try:
            int(apidata['status'])
        except:
            response['status'] = 50
            return response
        try:
            if user is not None and user.verify_token(apidata['token']):
                _business = session.query(Hop_Business).filter_by(id = apidata['business_id']).first()
                if _business is not None:
                    business = _business.name
                else:
                    business = 'Semua'
                _outlet = session.query(Hop_Outlet).filter_by(id = apidata['outlet']).first()
                if _outlet is not None:
                    outlet = _outlet.name
                else:
                    outlet = 'Semua'
                if int(apidata['status']) == 1:
                    if int(apidata['export_type']) == 1: #summary
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._summary_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            report_name = pd.DataFrame([['Summary Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            report_detail = pd.DataFrame({'Name': ['Revenue', 'Discount', 'Void', 'Nett Revenue', 'Tax & Service', 'Total Revenue'], 'Amount' : [datas['success_st'],datas['discount_success_st'],datas['void_st'],datas['nettrevenue'],datas['tax_sc_st'],datas['total_revenue']]})
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name.to_excel(writer, sheet_name ='Summary', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Summary', startrow = 2, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Summary', startrow = 5, index=False, header=True)
                            workbook  = writer.book
                            worksheet = writer.sheets['Summary']
                            name_format=workbook.add_format({'font_size':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info=workbook.add_format({'border':1,'bg_color':'#36A551','align':'center_across','color' : '#ffffff'})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#81db9e','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet.conditional_format( 'A1:B1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A7:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 2: #product sales
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._product_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Product Sales Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['product_sales']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue', 'Total Terjual'],[0, 0]])
                            report_detail = pd.DataFrame([[0, 0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Total Terjual'],[datas['total_revenue'], datas['total_sold']]])
                                report_detail.drop('id', axis=1, inplace=True)
                            report_detail.columns = ['Kategori','Produk', 'Revenue', 'SKU', 'Terjual']
                            report_name.to_excel(writer, sheet_name ='Product Sales', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Product Sales', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Product Sales', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Product Sales', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Product Sales']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 3: #daily sales
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._daily_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Daily Sales Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue', 'Total Terjual'],[0, 0]])
                            report_detail = pd.DataFrame([[0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Total Terjual'],[datas['total_revenue'], datas['count_trx']]])
                                report_detail = report_detail[['datePayment', 'sub_total', 'total_trans', 'average']]
                            report_detail.columns= ['Tanggal', 'Total', 'Terjual', 'Rata-Rata']
                            report_name.to_excel(writer, sheet_name ='Daily Sales', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Daily Sales', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Daily Sales', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Daily Sales', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Daily Sales']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 4: #data sales transaction
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._data_sales_trx_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Data Sales Transaction Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue'],[0]])
                            report_detail = pd.DataFrame([[0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue'],[datas['total_revenue']]])
                                report_detail.drop('idtrx', axis=1, inplace=True)
                            report_detail.columns= ['Operator', 'Status', 'Tanggal', 'Total']
                            report_name.to_excel(writer, sheet_name ='Data Sales Transaction', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Data Sales Transaction', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Data Sales Transaction', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Data Sales Transaction', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Data Sales Transaction']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info})
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 5: #sales per category
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._category_sales_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Category Sales Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue', 'Total Terjual', 'Total Rata-Rata'],[0,0,0]])
                            report_detail = pd.DataFrame([[0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Total Terjual', 'Total Rata-Rata'],[datas['total_revenue'], datas['total_sold'], datas['avg']]])
                                report_detail = report_detail[['category', 'revenue', 'sold', 'average']]
                                report_detail.drop('id_product', axis=1, inplace=True)
                            report_detail.columns= ['Kategori', 'Total', 'Terjual', 'Rata-Rata']
                            report_name.to_excel(writer, sheet_name ='Category Sales', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Category Sales', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Category Sales', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Category Sales', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Category Sales']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 6:#sales per outlet
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._sales_per_outlet_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Sales Per Outlet Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue', 'Total Terjual', 'Total Rata-Rata'],[0, 0, 0]])
                            report_detail = pd.DataFrame([[0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Total Terjual', 'Total Rata-Rata'],[datas['total_revenue'], datas['count_trx'], datas['avg_revenue']]])
                                report_detail = report_detail[['outlet', 'revenue', 'sold', 'avg']]
                            report_detail.columns= ['Outlet', 'Total', 'Terjual', 'Rata-Rata']
                            report_name.to_excel(writer, sheet_name ='Sales Per Outlet', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Sales Per Outlet', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Sales Per Outlet', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Sales Per Outlet', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Sales Per Outlet']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 7: # tax
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._tax_revenue_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Tax Revenue Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Tax Revenue'],[0]])
                            report_detail = pd.DataFrame([[0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                            report_detail.columns= ['Tax']
                            report_name.to_excel(writer, sheet_name ='Tax Revenue', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Tax Revenue', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Tax Revenue', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Tax Revenue', startrow = 5, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Tax Revenue']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 8: #discount
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._discount_revenue_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Discount Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Terjual', 'Total Amount'],[0, 0]])
                            report_detail = pd.DataFrame([[0,0,0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                            report_detail.columns= ['Outlet', 'Terjual', 'Total Amount']
                            report_name.to_excel(writer, sheet_name ='Discount', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Discount', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Discount', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Discount', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Discount']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 4, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 9: #Daily Profil
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._daily_profit_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Daily Profit Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Revenue', 'Tax & Service', 'Discount', 'Cost','Total Rata-Rata'],[0, 0, 0, 0, 0]])
                            report_detail = pd.DataFrame([['-',0, 0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Tax & Service', 'Discout', 'Cost', 'Nett Profit'],[datas['total_revenue'], datas['total_tax'], datas['total_discount'], datas['total_cost'], datas['total_profit']]])
                                report_detail = report_detail[['datePayment', 'revenue', 'tax', 'discount', 'cost', 'profit']]
                            report_detail.columns= ['Tanggal',	'Revenue','Tax & Services',	'Discount',	'Cost',	'Nett Profit']
                            report_name.to_excel(writer, sheet_name ='Daily Profit', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Daily Profit', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Daily Profit', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Daily Profit', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Daily Profit']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 5, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 10: #product Profil
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._product_profit_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Product Profit Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Revenue', 'Total Discount', 'Total Cost','Total Nett Revenue'],[0, 0, 0, 0]])
                            report_detail = pd.DataFrame([['-',0, 0, 0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Revenue', 'Total Discount', 'Total Cost','Total Nett Revenue'],[datas['total_revenue'], datas['total_discount'], datas['total_cost'], datas['total_profit']]])
                                report_detail = report_detail[['name', 'sku', 'revenue', 'discount', 'cost', 'profit']]
                            report_detail.columns= ['Product',	'SKU','Revenue',	'Discount',	'Cost',	'Nett Profit']
                            report_name.to_excel(writer, sheet_name ='Product Profit', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Product Profit', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Product Profit', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Product Profit', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Product Profit']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 5, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 11: #sales per hour
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._sales_per_hour_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Sales Per Hour Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['hourly_sales']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Total Transaksi', 'Total Revenue', 'Revenue Rata-Rata'],[0, 0, 0]])
                            report_detail = pd.DataFrame([['-',0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Total Transaction', 'Total Revenue', 'Total Average'],[datas['total_sold'], datas['total_revenue'], datas['total_average']]])
                                report_detail = report_detail[['hour', 'total_trans', 'revenue',  'average']]
                            report_detail.columns= ['Waktu', 'Total Terjual','Revenue',	'Rata-Rata']
                            report_name.to_excel(writer, sheet_name ='Sales Per Hour', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Sales Per Hour', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Sales Per Hour', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Sales Per Hour', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Sales Per Hour']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 5, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 12: #payment method
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._payment_method_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Payment Method Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            # report_total = pd.DataFrame([['Total Transaksi', 'Total Revenue', 'Revenue Rata-Rata'],[0, 0, 0]])
                            report_detail = pd.DataFrame([['-',0, 0, 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                # report_total = pd.DataFrame([['Total Transaction', 'Total Revenue', 'Total Average'],[datas['total_sold'], datas['total_revenue'], datas['total_average']]])
                                report_detail = report_detail[['payment_method', 'subtotal']]
                            report_detail.columns= ['Jenis Pembayaran', 'Total Terjual']
                            report_name.to_excel(writer, sheet_name ='Payment Method', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Payment Method', startrow = 2, index=False, header=False)
                            # report_total.to_excel(writer, sheet_name ='Payment Method', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Payment Method', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Payment Method']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            # worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 5, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
                    elif int(apidata['export_type']) == 13: #stock
                        filename = str(user.owner_id)+"-"+str(apidata['outlet'])+"-"+str(apidata['business_id'])+"-"+str(apidata['export_type'])+"-dari-"+str(apidata['dari'])+"-sampai-"+str(apidata['sampai'])+".xlsx"
                        our_path = excelDir+filename
                        if os.path.isfile(our_path): #Jika file sudah dibuat
                            response['status'] = '00'
                            response['filename'] = filename
                        else:
                            datas = TransLog()._stock_co(user.owner_id, apidata['outlet'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                            writer = pd.ExcelWriter(our_path, engine ='xlsxwriter')
                            report_name = pd.DataFrame([['Stock Report']])
                            report_header = pd.DataFrame([['Bisnis',business,'Dari', apidata['dari']],['Outlet',outlet, 'Sampai',apidata['sampai']]])
                            newdata = [datas['data']]
                            newdata = [x for x in newdata if x != []]
                            report_total = pd.DataFrame([['Grand Total'],[0]])
                            report_detail = pd.DataFrame([['-', '-', '-', '-', 0, '-', 0]])
                            if len(newdata) > 0:
                                for i in range(len(newdata)):
                                    report_detail = pd.DataFrame(newdata[i])
                                report_total = pd.DataFrame([['Grand Total'],[datas['total_grand']]])
                                report_detail = report_detail[['name', 'category', 'sku', 'barcode', 'stock', 'unit', 'revenue']]
                            report_detail.columns= ['Produk', 'Kategori', 'SKU', 'Barcode', 'Stock', 'Unit', 'Revenue']
                            report_name.to_excel(writer, sheet_name ='Stock', startrow = 0, index=False, header=False)
                            report_header.to_excel(writer, sheet_name ='Stock', startrow = 2, index=False, header=False)
                            report_total.to_excel(writer, sheet_name ='Stock', startrow = 5, index=False, header=False)
                            report_detail.to_excel(writer, sheet_name ='Stock', startrow = 8, index=False, header=True)
                            workbook  = writer.book
                            name_format=workbook.add_format({'font':24, 'bold': 5})
                            header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
                            field_info1=workbook.add_format({'border':1,'bg_color':'#fa8231','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            field_info=workbook.add_format({'border':1,'bg_color':'#20bf6b','align':'center_across','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info1=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#fd9644','color' : '#ffffff','align':'center_across','bold': 1})
                            record_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#26de81','color' : '#ffffff','align':'center_across','bold': 1})
                            worksheet = writer.sheets['Stock']
                            worksheet.conditional_format( 'A1:D1' , { 'type' : 'no_blanks' , 'format' : name_format} )
                            worksheet.conditional_format( 'A3:D4' , { 'type' : 'no_blanks' , 'format' : header_format} )
                            worksheet.conditional_format( 'A6:L6' , { 'type' : 'no_blanks' , 'format' : field_info1} )
                            worksheet.conditional_format( 'A7:L7' , { 'type' : 'no_blanks' , 'format' : record_info1} )
                            worksheet.conditional_format( 'A9:L9' , { 'type' : 'no_blanks' , 'format' : field_info} )
                            worksheet.conditional_format( 'A9:M36' , { 'type' : 'no_blanks' , 'format' : record_info} )
                            worksheet.set_column(0, 5, 18)
                            writer.save()
                            response['status'] = '00'
                            response['filename'] = filename
            else:
                response['status'] = '50'
                response['message'] = 'Your credential are invalid.'
            return json(response)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

@api_1.route('/data/dashboard', methods=['POST', 'GET'])
@_auth.login_required
async def _api_dashboard(request):
    if request.method == 'POST':
        apidata = _json.loads(request.form['data'][0])
        response = {}
        print(apidata)
        user = Hop_User().verify_auth(apidata['id'])
        session = Session()
        try:
            if user is not None and user.verify_token(apidata['token']):
                response['data'] = TransLog()._dashboard_sales_co(user.owner_id, apidata['outlet'], apidata['dash_on'], apidata['dari'], apidata['sampai'], apidata['business_id'])
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'Your credential are invalid.'
            return json(response)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

# @api_1.route('/file', methods=['POST', 'GET'])
# @_auth.login_required
# async def handle_request(request):
#     # directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'file_secure\\excels\\')
#     return await response.file('/file_secure/excels/abc.xlsx')

@api_1.route('/data/download', methods=['POST', 'GET'])
async def _download(request):
    if request.method == 'POST':
        # apidata = _json.loads(request.form['data'][0])
        apidata = request.form
        print(apidata)
        respon = {}
        user = Hop_User().verify_auth(apidata['id'][0])
        session = Session()
        try:
            if user is not None and user.verify_token(apidata['token'][0]):
                directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'file_secure\\excels\\')
                # app.static(apidata['filename'], '/file_secure/excels/', stream_large_files=True)
                return await response.file(directory+apidata['filename'][0])
                # return send_file('/file_secure/excels/'+apidata['filename'][0], as_attachment=True)
            else:
                respon['status'] = '50'
                respon['message'] = 'Your credential are invalid.'
            return json(respon)
        except:
            session.rollback()
            raise
        finally:
            session.close()
    return respon
