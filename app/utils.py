from app import mongo, app
from random import randint
import re, pdb, string, random, os, requests, base64, datetime, hmac, hashlib, time, imaplib, email
from . import mongo, Session
from datetime import datetime, date
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from PIL import Image
import requests, json
import xlsxwriter
import pandas as pd
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

def xlsx_style(_filename):
    response = {}
    session = Session()
    writer = pd.ExcelWriter(_filename, engine ='xlsxwriter')
    workbook  = writer.book
    name_format=workbook.add_format({'font':24, 'bold': 5})
    header_format=workbook.add_format({'border':1,'align':'left','font': 'Arial','color': '#031B4D','bg_color':'#eeeeee' })
    field_info=workbook.add_format({'border':1,'bg_color':'#36A551','align':'center_across','color' : '#ffffff'})
    row_info=workbook.add_format({'border':1,'font': 'Calibri','bg_color':'#81db9e','color' : '#ffffff','align':'center_across','bold': 1})
    response['name'] = name_format
    response['header'] = header_format
    response['field'] = field_info
    response['record'] = row_info
    return response

def hmac_sha256(key, msg):
    hash_obj = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return hash_obj.hexdigest()

def generateRefca(user_id):
    return str(int(time.time())) + '#' + str(user_id)

class emailService:
    SMTPserver = 'mx-s3.vivawebhost.com'
    SMTPport = 465
    sender = 'hello@hop.cash'
    destination = []
    USERNAME = "hello@hop.cash"
    PASSWORD = "!2345hop5432!"
    text_subtype = 'html'
    content = ''
    subject = ''

    def __init__(self):
        self.SMTPserver = 'mx-s3.vivawebhost.com'
        self.SMTPport = 465
        self.sender = 'hello@hop.cash'
        self.destination = []
        self.username = "hello@hop.cash"
        self.PASSWORD = "!2345hop5432!"
        self.text_subtype = 'html'
        self.content = ''
        self.subject = ''


    def _send(self):
        msg = MIMEText(self.content, self.text_subtype)
        msg['Subject']= self.subject
        msg['From']   = self.sender # some SMTP servers will do this automatically, not all
        conn = SMTP(self.SMTPserver, self.SMTPport)
        conn.set_debuglevel(False)
        conn.login(self.USERNAME, self.PASSWORD)
        try:
            conn.sendmail(self.sender, self.destination, msg.as_string())
        except Exception as e:
            raise e
        finally:
            conn.quit()
