from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import hmac_sha256
from . import mongo, Base, Session
import pymongo, requests, time, itertools, ast, jwt
from sqlalchemy import *
from itertools import permutations
from decimal import *
from bson.objectid import ObjectId
from time import time
from app import app

# CLASS FOR USER

class Hop_Role(Base):
    __tablename__ = 'role'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        session = Session()
        try:
           _role = session.query(Hop_Role).filter_by(id=_id, status=True).first()
           if _role is not None:
               response['id'] = _role.id
               response['name'] = _role.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    phone_number = Column(String(50),index=True)
    password_hash = Column(String(128), default=None)
    pin_hash = Column(String(128), default=None)
    email = Column(String(100),index=True, default=None)
    role_id = Column(Integer,ForeignKey('role.id'), default=3)
    sales_id = Column(Integer,ForeignKey('sales.id'), default=None)
    owner_id = Column(Integer, default=None)
    address = Column(Text, default=None)
    gender_id = Column(String(15), default=None)
    birthdate = Column(DateTime, default=None)
    confirmed = Column(Boolean,default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    # USER BASIC DATA
    def _basic_data(self, _id):
        response = {}
        session = Session()
        try:
           user = session.query(Hop_User).filter_by(id=_id, status=True).first()
           response['id'] = user.id
           response['name'] = user.name
           response['phone_number'] = user.phone_number
           response['role_id'] = user.role_id
           response['email'] = user.email
           response['token'] = user.generate_token()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
           user = session.query(Hop_User).filter_by(id=_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if user is not None:
            response['id'] = user.id
            response['name'] = user.name
            response['email'] = user.email
            response['phone_number'] = user.phone_number
            response['token'] = user.generate_token()
            response['register_date'] = str(user.added_time)
            response['role'] = Hop_Role()._data(user.role_id)
            response['outlet_list'] = Hop_User_Outlet()._listbyuserid(user.id)
            response['log_time'] = str(Hop_Login_Log()._data(user.id))
        return response

    def _list_all_employee(self, owner_id):
        response = []
        session = Session()
        try:
            _users = session.query(Hop_User).filter_by(owner_id=owner_id, status=True).filter(Hop_User.id!=owner_id).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _users:
            response.append(Hop_User()._data(_id=i.id))
        return response

    def _insert_employee(self, _name, _phonenumber, _email, _password, _role_id, owner_id):
        response = None
        session = Session()
        try:
            insert = Hop_User()
            insert.name = _name
            insert.phone_number = _phonenumber
            insert.email = _email
            insert.password_hash = generate_password_hash(_password)
            insert.role_id = _role_id
            insert.owner_id = owner_id
            session.add(insert)
            session.commit()
            response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_User()._basic_data(response)

    def _update_employee(self, _id, _name, _phonenumber, _email, _password, _role_id, owner_id):
        response = None
        session = Session()
        try:
            insert = session.query(Hop_User).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if insert is not None:
                insert.name = _name
                insert.phone_number = _phonenumber
                insert.email = _email
                if _password is not None:
                    insert.password_hash = generate_password_hash(_password)
                insert.role_id = _role_id
                session.add(insert)
                session.commit()
                response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_User()._basic_data(response)

    def _remove_employee(self, _id, owner_id):
        session = Session()
        try:
            insert = session.query(Hop_User).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if insert is not None:
                insert.status = False
                session.add(insert)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # OWNER DATA
    def _owner_data(self, owner_id):
        response = {}
        session = Session()
        try:
            user = session.query(Hop_User).filter_by(owner_id=owner_id, status=True).first()
            response['id'] = user.id
            response['name'] = user.name
            response['phone_number'] = user.phone_number
            response['email'] = user.email
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _insertowner(self, _name, _phonenumber, _email, _password, _refferal):
        response = None
        session = Session()
        try:
            insert = Hop_User()
            insert.name = _name
            insert.phone_number = _phonenumber
            insert.email = _email
            insert.password_hash = generate_password_hash(_password)
            insert.role_id = 1
            if _refferal is not None:
                _sales = Hop_Sales()._data(_refferal)
                insert.sales_id = _sales['id']
            session.add(insert)
            session.commit()
            insert.owner_id = insert.id
            session.add(insert)
            session.commit()
            response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return Hop_User()._basic_data(response)

    def _update(self, _id, _name, _email, _phone):
        response = {}
        response['status'] = '50'
        response['message'] = 'You credential is invalid'
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=_id, status=True).first()
            if _user is not None:
                _user.name = _name
                if Hop_User().verify_user(_id=_email) or _user.email == _email:
                    _user.email = _email
                if Hop_User().verify_user(_id=_phone) or _user.phone_number == _phone:
                    _user.phone_number = _phone
                session.add(_user)
                session.commit()
                response = Hop_User()._basic_data(_user.id)
                response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _update_password(self, _id, _new_pass):
        response = None
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=_id, status=True).first()
            if _user is not None:
                _user.password_hash = generate_password_hash(_new_pass)
                session.add(_user)
                session.commit()
            response = _user.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_User()._basic_data(response)

    def _user_owner(self, id):
        response = None
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=id, status=True).first()
            if _user is not None:
                response = _user.owner_id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response


    # VERIFICATION USER AS THE OWNER
    def verify_detail(self, id):
        response = False
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=id).first()
            if _user is not None:
                if session.query(Hop_Business).filter_by(owner_id=_user.owner_id, status=True).count() > 0:
                    response = True
        except:
            session.rollback()
            raise
        finally:
            session.close()
        print(response)
        return response

    # ALL AUTHENTICION METHODS

    def verify_user(self, _id):
        response = True
        session = Session()
        try:
            if session.query(Hop_User).filter_by(phone_number=_id, status=True).count() > 0:
                response = False
            if session.query(Hop_User).filter_by(email=_id, status=True).count() > 0:
                response = False
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_token(self):
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':' + str(self.email)+ ':' + str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        return hmac_sha256(key, msg)

    def verify_token(self, token):
        response = False
        key = str.encode(self.phone_number)
        msg = str.encode(str(self.id) + ':'+ str(self.email) + ':'+ str(self.phone_number) + ':' + str(self.password_hash) + ':' + str(self.pin_hash))
        if token == hmac_sha256(key, msg):
            response = True
        return response

    def verify_auth(self, username):
        response = None
        session = Session()
        try:
            check_id = session.query(Hop_User).filter_by(id=username, status=True).first()
            check_email = session.query(Hop_User).filter_by(email=username, status=True).first()
            check_phone = session.query(Hop_User).filter_by(phone_number=username, status=True).first()
            if check_id is not None:
                response = check_id
            elif check_email is not None:
                response = check_email
            elif check_phone is not None:
                response = check_phone
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def verify_reg(self, email, phone):
        response = False
        session = Session()
        try:
            check_email = session.query(Hop_User).filter_by(email=email, status=True).count()
            check_phone = session.query(Hop_User).filter_by(phone_number=phone, status=True).count()
            if check_email == 0 and check_phone == 0:
                response = True
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def get_reset_password_token(self, expires_in=3600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Hop_User().verify_auth(id)


class Hop_Gender(Base):
    __tablename__ = 'gender'

    id = Column(Integer,primary_key=True)
    name = Column(Text)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self,_id):
        response = {}
        session = Session()
        try:
            _gender = session.query(Hop_Gender).filter_by(id = _id).first()
            if _gender is not None:
                response['id'] =  _gender.id
                response['name'] =  _gender.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _list(self):
        response = []
        session = Session()
        try:
            _gender = session.query(Hop_Gender).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _gender:
            response.append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

# CLASS FOR BUSINESS

class Hop_Business_Category(Base):
    __tablename__ = 'business_category'

    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self):
        response = []
        session = Session()
        try:
            _business_category = session.query(Hop_Business_Category).filter_by(status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _business_category:
            response.append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _business_category = session.query(Hop_Business_Category).filter_by(id = _id, status = True).first()
            if _business_category is not None:
                response['id'] = _business_category.id
                response['name'] = _business_category.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Business(Base):
    __tablename__ = 'business'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    business_category_id = Column(Integer,ForeignKey('business_category.id'))
    description = Column(Text)
    owner_id = Column(Integer,ForeignKey('user.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def verify_auth(self, bid):
        response = None
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(id=bid, status=True).first()
            if _business is not None:
                response = _business
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response


    def _insert(self, _name, _businesscategory, _owner_id):
        response = None
        session = Session()
        try:
            insert = Hop_Business()
            insert.name = _name
            insert.business_category_id = _businesscategory
            insert.owner_id = _owner_id
            insert.added_time = datetime.now()
            session.add(insert)
            session.commit()
            response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Business()._data(response)

    def _insert_detail(self, _name, _businesscategory, _description, owner_id):
        response = None
        session = Session()
        try:
            insert = Hop_Business()
            insert.name = _name
            insert.business_category_id = _businesscategory
            insert.description = _description
            insert.owner_id = owner_id
            session.add(insert)
            session.commit()
            response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Business()._data(response)

    def _update(self, _id, _name, _businesscategory, _description, owner_id):
        response = None
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(id=_id, owner_id=owner_id, status=True).first()
            _business.name = _name
            _business.business_category_id = _businesscategory
            _business.description = _description
            _business.owner_id = owner_id
            session.add(_business)
            session.commit()
            response = _business.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Business()._data(response)

    def _remove(self, _id, owner_id):
        response = None
        response_id = None
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(id=_id, owner_id=owner_id, status=True).first()
            _business.status = False
            session.add(_business)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_User().verify_detail(owner_id)

    def _basicdata(self, _id):
        response = {}
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _business is not None:
            response['id'] = _business.id
            response['name'] = _business.name
            response['description'] = _business.description
            response['business_category_id'] = Hop_Business_Category()._data(_business.business_category_id)
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _business is not None:
            response['id'] = _business.id
            response['name'] = _business.name
            response['description'] = _business.description
            response['business_category_id'] = Hop_Business_Category()._data(_business.business_category_id)
        return response

    def _checkbyuserid(self, _userid):
        response = True
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(owner_id = _userid).first()
            if _business is None:
                response = False
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response


    def _listbyownerid(self, owner_id):
        response = []
        session = Session()
        try:
            _business = session.query(Hop_Business).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _business:
            response.append({
                'id' : i.id,
                'name' : i.name,
                # 'outlet' : Hop_Outlet()._list(i.id)
            })
        return response

    def _listbyownerid_all(self, user_id):
        response = []
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=user_id, status=True).first()
            _business = session.query(Hop_Business).filter_by(owner_id=_user.owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _business:
            response += Hop_Outlet()._list(i.id, _user.id)
        return response

    def _outlet_list_exception(self, business_id, user_id):
        response = []
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=user_id, status=True).first()
            _business = session.query(Hop_Business).filter_by(owner_id=_user.owner_id, status=True).filter(Hop_Business.id!=business_id).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _business:
            response += Hop_Outlet()._list(i.id, user_id)
        return response

    def _move_business_list(self, new_business_id, data_outlet_list, owner_id):
        response = []
        if data_outlet_list is not None:
            for i in data_outlet_list:
                response.append(Hop_Outlet()._move_business(new_business_id, i, owner_id))
        return response

class Hop_Outlet(Base):
    __tablename__ = 'outlet'

    id = Column(Integer,primary_key=True)
    name = Column(Text, default=None)
    email = Column(String(100),index=True, default=None)
    phone_number = Column(String(50),index=True, default=None)
    address = Column(Text, default=None)
    business_id = Column(Integer,ForeignKey('business.id'), default=None)
    owner_id = Column(Integer,ForeignKey('user.id'), default=None)
    num_emp_id = Column(Integer,ForeignKey('num_emp.id'), default=1)
    countries_id = Column(Integer,ForeignKey('countries.id'), default=None)
    provinces_id = Column(Integer,ForeignKey('provinces.id'), default=None)
    cities_id = Column(Integer,ForeignKey('cities.id'), default=None)
    postal_code = Column(String(6),index=True, default=None)
    table_status = Column(Boolean,default=True)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, _name, _numempid, _phonenumber, _address, _country_id, _business_id, owner_id):
        response = None
        session = Session()
        try:
            insert = Hop_Outlet()
            insert.name = _name
            insert.num_emp_id = _numempid
            insert.phone_number = _phonenumber
            insert.address = _address
            insert.countries_id = _country_id
            insert.business_id = _business_id
            insert.owner_id = owner_id
            session.add(insert)
            session.commit()
            _business = session.query(Hop_Business).filter_by(id=insert.business_id, status=True).first()
            response = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        Hop_Product_Category_Outlet()._insertall(response, _business.owner_id)
        Hop_Product_Outlet()._insertall(response, _business.owner_id)
        return Hop_Outlet()._data(response)

    def _update(self, _id, _name, _numempid, _phonenumber, _address, _country_id, _tax_list, _table_status):
        response = {}
        response['status'] = '50'
        response['message'] = 'Your credential is invalid'
        response_id = None
        session = Session()
        try:
            insert = session.query(Hop_Outlet).filter_by(id=_id).first()
            if insert is not None:
                insert.name = _name
                insert.phone_number = _phonenumber
                insert.num_emp_id = _numempid
                insert.address = _address
                insert.countries_id = _country_id
                insert.table_status = True if _table_status == True else False
                session.add(insert)
                session.commit()
                response_id = insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if response_id is not None:
            Hop_Outlet_Tax()._remove(response_id)
            for i in _tax_list:
                Hop_Outlet_Tax()._insert(response_id, i)
            response = Hop_Outlet()._data(response_id)
        return response

    def _data(self,_id):
        response = {}
        _outlet = None
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _outlet is not None:
            response['id'] =  _outlet.id
            response['name'] =  _outlet.name
            response['address'] =  _outlet.address
            response['phone_number'] = _outlet.phone_number
            response['region'] = _outlet.provinces_id
            response['city'] = _outlet.cities_id
            response['table_status'] = _outlet.table_status
            response['business_id'] = Hop_Business()._data(_outlet.business_id)
            response['num_emp'] = Hop_Num_Emp()._data(_outlet.num_emp_id)
            response['country'] = Hop_Countries()._data(_outlet.countries_id)
            response['tax_list'] = Hop_Outlet_Tax()._list(_outlet.id)
            response['billing'] = Hop_Billing_Outlet()._checkbillingoutlet(_outlet.id)
            response['total_category'] = Hop_Product_Category_Outlet()._count(_outlet.id, _outlet.owner_id)
            response['total_item'] = Hop_Product_Outlet()._count(_outlet.id, _outlet.owner_id)
        return response

    def _basic_data(self,_id):
        response = {}
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _outlet is not None:
            response['id'] =  _outlet.id
            response['business_id'] = Hop_Business()._data(_outlet.business_id)
            response['name'] =  _outlet.name
            response['billing'] = Hop_Billing_Outlet()._checkbillingoutlet(_outlet.id)
        return response

    def _list(self, business_id, user_id):
        response = []
        _exist = []
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=user_id, status=True).first()
            _outlet = session.query(Hop_Outlet).filter_by(business_id=business_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _user is not None:
            if _user.role_id == 1:
                for i in _outlet:
                    response.append(Hop_Outlet()._data(i.id))
            elif _user.role_id == 2:
                for i in _outlet:
                    _exist.append(i.id)
                response = Hop_Outlet()._listbyuserid(_user.id, _exist)
        return response

    def _listbyuserid(self, _userid=None, _exist=[]):
        response = []
        session = Session()
        try:
            _user_outlet = session.query(Hop_User_Outlet).filter_by(user_id = _userid, status = True).filter(Hop_User_Outlet.outlet_id.in_(_exist)).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _user_outlet:
            response.append(Hop_Outlet()._data(i.outlet_id))
        return response

    def _listbyownerid(self, owner_id=None, _except=[]):
        response = []
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(owner_id=owner_id, status=True).filter(~Hop_Outlet.id.in_(_except)).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _outlet:
            response.append(Hop_Outlet()._basic_data(i.id))
        return response

    def _move_business(self, new_business_id, outlet_id, owner_id):
        response = None
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(id=outlet_id, status=True).first()
            _business = session.query(Hop_Business).filter_by(id=_outlet.business_id, status=True).first()
            if _business.owner_id == owner_id:
                _outlet.business_id = new_business_id
                session.add(_outlet)
                session.commit()
                response = _outlet.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Outlet()._data(response)

    def _remove(self, _id, owner_id):
        response = {}
        response['status'] = '50'
        response['message'] = 'Your credential is invalid'
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _outlet is not None:
                response = Hop_Outlet()._data(_outlet.id)
                _outlet.status = False
                session.add(_outlet)
                response['status'] = '00'
                response['message'] = 'Your Outlet has been removed'

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_User_Outlet(Base):
    __tablename__ = 'user_outlet'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    outlet_id = Column(Integer,ForeignKey('outlet.id'))
    business_id = Column(Integer,ForeignKey('business.id'),default=None)
    mob_order = Column(Boolean,default=False)
    mob_payment = Column(Boolean,default=False)
    mob_void = Column(Boolean,default=False)
    mob_change_transaction = Column(Boolean,default=False)
    mob_custom_price = Column(Boolean,default=False)
    mob_custom_discount = Column(Boolean,default=False)
    mob_reprint_reciept = Column(Boolean,default=False)
    mob_reprint_kitchen_reciept = Column(Boolean,default=False)
    mob_print_invoice_reciept = Column(Boolean,default=False)
    mob_history_transaction = Column(Boolean,default=False)
    mob_customer_management = Column(Boolean,default=False)
    bo_outlet_management = Column(Boolean,default=False)
    bo_report = Column(Boolean,default=False)
    bo_management_product = Column(Boolean,default=False)
    bo_management_inventory = Column(Boolean,default=False)
    bo_management_tax = Column(Boolean,default=False)
    bo_management_employee = Column(Boolean,default=False)
    bo_management_promo = Column(Boolean,default=False)
    bo_customer_management = Column(Boolean,default=False)
    bo_billing = Column(Boolean,default=False)
    bo_daily_report = Column(Boolean,default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _permission(self, user_id):
        response = {}
        response['user_id'] = user_id
        response['business_list'] = []
        response['bo_outlet_management'] = []
        response['bo_report'] = []
        response['bo_management_product'] = []
        response['bo_management_inventory'] = []
        response['bo_management_tax'] = []
        response['bo_management_employee'] = []
        response['bo_management_promo'] = []
        response['bo_customer_management'] = []
        response['bo_billing'] = []
        response['bo_daily_report'] = []
        session = Session()
        try:
            _huo = session.query(Hop_User_Outlet).filter_by(user_id=user_id, status=True).all()
            for i in _huo:
                if _huo is not None:
                    _business = session.query(Hop_Business).filter_by(id=i.outlet_id, status=True).first()
                    if _business.id not in response['business_list']:
                        response['business_list'].append(_business.id)
                    if i.bo_outlet_management is not False:
                        response['bo_outlet_management'].append(i.outlet_id)
                    if i.bo_report is not False:
                        response['bo_report'].append(i.outlet_id)
                    if i.bo_management_product is not False:
                        response['bo_management_product'].append(i.outlet_id)
                    if i.bo_management_inventory is not False:
                        response['bo_management_inventory'].append(i.outlet_id)
                    if i.bo_management_tax is not False:
                        response['bo_management_tax'].append(i.outlet_id)
                    if i.bo_management_employee is not False:
                        response['bo_management_employee'].append(i.outlet_id)
                    if i.bo_management_promo is not False:
                        response['bo_management_promo'].append(i.outlet_id)
                    if i.bo_customer_management is not False:
                        response['bo_customer_management'].append(i.outlet_id)
                    if i.bo_billing is not False:
                        response['bo_billing'].append(i.outlet_id)
                    if i.bo_daily_report is not False:
                        response['bo_daily_report'].append(i.outlet_id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _insert_outlet(self, _user_id, _outlet_list):
        session = Session()
        try:
            _outlet = session.query(Hop_User_Outlet).filter_by(user_id=_user_id, status=True).all()
            for o in _outlet:
                o.status = False
                session.add(o)
            for o in _outlet_list:
                _huo = session.query(Hop_User_Outlet).filter_by(user_id=_user_id, outlet_id=o).first()
                if _huo is not None:
                    _huo.status = True
                    session.add(_huo)
                else:
                    _new_huo = Hop_User_Outlet()
                    _new_huo.user_id = _user_id
                    _new_huo.outlet_id = o
                    _new_huo.business_id = Hop_Outlet()._data(o)['business_id']['id']
                    session.add(_new_huo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _insert_permission(self, user_id, outlet_id,
        mobile_order, mobile_payment, mobile_void, mobile_change_trx, mobile_custom_price, mobile_custom_discount,
        mobile_reprint_reciept, mobile_reprint_kitchen, mobile_print_invoice, mobile_history, mobile_customer,
        bo_outlet, bo_report, bo_product, bo_inventory, bo_tax, bo_employee, bo_promo, bo_customer, bo_billing,
        bo_email
    ):
        session = Session()
        try:
            _huo = session.query(Hop_User_Outlet).filter_by(user_id=user_id, outlet_id=outlet_id).first()
            if _huo is not None:
                _huo.mob_order = True if mobile_order == True else False
                _huo.mob_payment = True if mobile_payment == True else False
                _huo.mob_void = True if mobile_void == True else False
                _huo.mob_change_transaction = True if mobile_change_trx == True else False
                _huo.mob_custom_price = True if mobile_custom_price == True else False
                _huo.mob_custom_discount = True if mobile_custom_discount == True else False
                _huo.mob_reprint_reciept = True if mobile_reprint_reciept == True else False
                _huo.mob_reprint_kitchen_reciept = True if mobile_reprint_kitchen == True else False
                _huo.mob_print_invoice_reciept = True if mobile_print_invoice == True else False
                _huo.mob_history_transaction = True if mobile_history == True else False
                _huo.mob_customer_management = True if mobile_customer == True else False
                _huo.bo_outlet_management = True if bo_outlet == True else False
                _huo.bo_report = True if bo_report == True else False
                _huo.bo_management_product = True if bo_product == True else False
                _huo.bo_management_inventory = True if bo_inventory == True else False
                _huo.bo_management_tax = True if bo_tax == True else False
                _huo.bo_management_employee = True if bo_employee == True else False
                _huo.bo_management_promo = True if bo_promo == True else False
                _huo.bo_customer_management = True if bo_customer == True else False
                _huo.bo_billing = True if bo_billing == True else False
                _huo.bo_daily_report = True if bo_email == True else False
                session.add(_huo)
            else:
                _new_huo = Hop_User_Outlet()
                _new_huo.user_id = user_id
                _new_huo.outlet_id = outlet_id
                _new_huo.business_id = Hop_Outlet()._data(outlet_id)['business_id']['id']
                _new_huo.mob_order = True if mobile_order == True else False
                _new_huo.mob_payment = True if mobile_payment == True else False
                _new_huo.mob_void = True if mobile_void == True else False
                _new_huo.mob_change_transaction = True if mobile_change_trx == True else False
                _new_huo.mob_custom_price = True if mobile_custom_price == True else False
                _new_huo.mob_custom_discount = True if mobile_custom_discount == True else False
                _new_huo.mob_reprint_reciept = True if mobile_reprint_reciept == True else False
                _new_huo.mob_reprint_kitchen_reciept = True if mobile_reprint_kitchen == True else False
                _new_huo.mob_print_invoice_reciept = True if mobile_print_invoice == True else False
                _new_huo.mob_history_transaction = True if mobile_history == True else False
                _new_huo.mob_customer_management = True if mobile_customer == True else False
                _new_huo.bo_outlet_management = True if bo_outlet == True else False
                _new_huo.bo_report = True if bo_report == True else False
                _new_huo.bo_management_product = True if bo_product == True else False
                _new_huo.bo_management_inventory = True if bo_inventory == True else False
                _new_huo.bo_management_tax = True if bo_tax == True else False
                _new_huo.bo_management_employee = True if bo_employee == True else False
                _new_huo.bo_management_promo = True if bo_promo == True else False
                _new_huo.bo_customer_management = True if bo_customer == True else False
                _new_huo.bo_billing = True if bo_billing == True else False
                _new_huo.bo_daily_report = True if bo_email == True else False
                _new_huo.status = False
                session.add(_new_huo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _data(self, _user_id, _outlet_id):
        response = {}
        session = Session()
        try:
            _huo = session.query(Hop_User_Outlet).filter_by(user_id=_user_id, outlet_id=_outlet_id).first()
            if _huo is not None:
                response['user_id'] = _huo.user_id
                response['outlet_id'] = _huo.outlet_id
                response['mob_order'] = _huo.mob_order
                response['mob_payment'] = _huo.mob_payment
                response['mob_void'] = _huo.mob_void
                response['mob_change_transaction'] = _huo.mob_change_transaction
                response['mob_custom_price'] = _huo.mob_custom_price
                response['mob_custom_discount'] = _huo.mob_custom_discount
                response['mob_reprint_reciept'] = _huo.mob_reprint_reciept
                response['mob_reprint_kitchen_reciept'] = _huo.mob_reprint_kitchen_reciept
                response['mob_print_invoice_reciept'] = _huo.mob_print_invoice_reciept
                response['mob_history_transaction'] = _huo.mob_history_transaction
                response['mob_customer_management'] = _huo.mob_customer_management
                response['bo_outlet_management'] = _huo.bo_outlet_management
                response['bo_report'] = _huo.bo_report
                response['bo_management_product'] = _huo.bo_management_product
                response['bo_management_inventory'] = _huo.bo_management_inventory
                response['bo_management_tax'] = _huo.bo_management_tax
                response['bo_management_employee'] = _huo.bo_management_employee
                response['bo_management_promo'] = _huo.bo_management_promo
                response['bo_customer_management'] = _huo.bo_customer_management
                response['bo_billing'] = _huo.bo_billing
                response['bo_daily_report'] = _huo.bo_daily_report
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data_list(self, _user_id):
        response = []
        session = Session()
        try:
            _huo = session.query(Hop_User_Outlet).filter_by(user_id=_user_id, status=True).all()
            for i in _huo:
                response.append(i.outlet_id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _listbyuserid(self, _userid=None, _except=[]):
        response = []
        session = Session()
        try:
            _user_outlet = session.query(Hop_User_Outlet).filter_by(user_id = _userid, status = True).filter(~Hop_User_Outlet.outlet_id.in_(_except)).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _user_outlet:
            response.append(Hop_Outlet()._data(i.outlet_id))
        return response

    def _listbybusinessid(self, business_id):
        response = []
        session = Session()
        try:
            _outlet = session.query(Hop_Outlet).filter_by(business_id=business_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _outlet:
            response.append(Hop_Outlet()._basic_data(i.id))
        return response

    def _list(self, _user_id):
        response = None
        session = Session()
        try:
            _user = session.query(Hop_User).filter_by(id=_user_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _user is not None:
            _except = Hop_Billing_Invoice()._order_trx_service(_user.id)
            if _user.role_id == 1:
                response = Hop_Outlet()._listbyownerid(_user.owner_id, _except)
            elif _user.role_id == 2:
                response = Hop_User_Outlet()._listbyuserid(_user.id, _except)
        return response

class Hop_Table_Outlet(Base):
    __tablename__ = 'table_outlet'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    outlet_id = Column(Integer,ForeignKey('outlet.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, _name, _outletid):
        session = Session()
        try:
            insert = Hop_Table_Outlet()
            insert.name = _name
            insert.outlet_id = _outletid
            insert.added_time = datetime.now()
            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update(self,_id, _name, _outletid):
        session = Session()
        try:
            update = session.query(Hop_Table_Outlet).filter_by(id = _id).first()
            update.name = _name
            update.outlet_id = _outletid
            session.add(update)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove(self, _id):
        session = Session()
        try:
            update = session.query(Hop_Table_Outlet).filter_by(id = _id).first()
            update.status = False
            session.add(update)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def _listbyoutlet(self, _outletid):
        response = []
        session = Session()
        try:
            _table_outlet = session.query(Hop_Table_Outlet).filter_by(outlet_id = _outletid, status = True).all()
            for i in _table_outlet:
                response.append({
                    'id' : i.id,
                    'name' : i.name
                })
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _table_outlet = session.query(Hop_Table_Outlet).filter_by(id = _id).filter_by(status = True).first()
            if _table_outlet is not None:
                response['id'] = _table_outlet.id
                response['name'] = _table_outlet.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _checkname(self, _name, _outletid):
        response = False
        session = Session()
        try:
            _table_outlet = session.query(Hop_Table_Outlet).filter_by(name = _name, status = True, outlet_id = _outletid).first()
            if _table_outlet is not None:
              response = True
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Num_Emp(Base):
    __tablename__ = 'num_emp'

    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self):
        response = []
        session = Session()
        try:
            _num_emp = session.query(Hop_Num_Emp).filter_by(status = True).all()
            for i in _num_emp:
                response.append({
                    'id' : i.id ,
                    'name' : i.name
                })
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _num_emp = session.query(Hop_Num_Emp).filter_by(id = _id, status = True).first()
            if _num_emp is not None:
                response['id'] = _num_emp.id
                response['name'] = _num_emp.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

# CLASS FOR PRODUCTS

class Hop_Product_Category(Base):
    __tablename__ = 'product_category'

    id = Column(Integer,primary_key=True)
    owner_id = Column(Integer,ForeignKey('user.id'))
    name = Column(Text)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self, owner_id):
        response = []
        session = Session()
        try:
            _category = session.query(Hop_Product_Category).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _category:
            response.append({
                'id' : i.id ,
                'name' : i.name,
                'list': Hop_Product_Item()._count(category_id=i.id, owner_id=owner_id)
            })
        return response

    def _insert(self, category_name, owner_id):
        response = {}
        response_id = None
        session = Session()
        try:
            _exist_category = session.query(Hop_Product_Category).filter_by(name = category_name, owner_id=owner_id, status=True).first()
            if _exist_category is None:
                _category = Hop_Product_Category()
                _category.name = category_name
                _category.owner_id = owner_id
                session.add(_category)
                session.commit()
                response_id = _category.id
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'This category name has been used in your category list'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if response_id != None:
            for i in Hop_Outlet()._listbyownerid(owner_id):
                Hop_Product_Category_Outlet()._insert(i['id'], response_id)
            response.update(Hop_Product_Category()._data(response_id, owner_id))
        return response

    def _basicdata(self, category_id, owner_id):
        response = {}
        session = Session()
        try:
            _category = session.query(Hop_Product_Category).filter_by(id=category_id, owner_id=owner_id, status=True).first()
            if _category is not None:
                response['id'] = _category.id
                response['name'] = _category.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, category_id, owner_id):
        response = {}
        session = Session()
        try:
            _category = session.query(Hop_Product_Category).filter_by(id=category_id, status=True).first()
            if _category is not None:
                response['id'] = _category.id
                response['name'] = _category.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _category is not None:
            response['list'] = Hop_Product_Item()._listbycategory(category_id=response['id'], owner_id=owner_id)
        return response

    def _update(self, category_id, category_name, owner_id):
        response = {}
        session = Session()
        try:
            _exist_category = session.query(Hop_Product_Category).filter_by(name=category_name, owner_id=owner_id, status=True).filter(Hop_Product_Category.id!=category_id).first()
            if _exist_category is None:
                _category = session.query(Hop_Product_Category).filter_by(id=category_id, owner_id=owner_id, status=True).first()
                if _category is not None:
                    _category.name = category_name
                    session.add(_category)
                    session.commit()
                    response['id'] = _category.id
                    response['status'] = '00'
                else:
                    response['status'] = '50'
                    response['message'] = 'Your credential is invalid'
            else:
                response['status'] = '50'
                response['message'] = 'This category name has been used in your category list'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _category is not None:
            response.update(Hop_Product_Category()._data(response['id'], owner_id))
        return response

    def _remove(self, category_id, owner_id):
        response = {}
        session = Session()
        try:
            _category = session.query(Hop_Product_Category).filter_by(id=category_id, owner_id=owner_id, status=True).first()
            if _category is not None:
                total_item = Hop_Product_Item()._count(_category.id, owner_id)
                if total_item == 0:
                    response['status'] = '00'
                    response['name'] = _category.name
                    response['id'] = _category.id
                    _category.status = False
                    session.add(_category)
                    session.commit()

                    Hop_Product_Category_Outlet()._remove_many(_category.id)
                else:
                    response['status'] = '50'
                    response['id'] = _category.id
                    response['name'] = _category.name
                    response['total_item'] = total_item
                    response['message'] = 'To remove a category, you must move or remove all item within it.'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _remove_many(self, category_list, owner_id):
        response = []
        for i in category_list:
            response.append(Hop_Product_Category()._remove(category_id=i, owner_id=owner_id))
        return response

    def _check_validation(self, owner_id):
        response = False
        session = Session()
        try:
            _cat = session.query(Hop_Product_Category).filter_by(owner_id=owner_id).count()
            if _cat > 0:
                response = True
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Product_Item(Base):
    __tablename__ = 'product_item'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    product_category_id = Column(Integer,ForeignKey('product_category.id'))
    owner_id = Column(Integer,ForeignKey('user.id'))
    measurement_id = Column(Integer,ForeignKey('measurement_list.id'))
    description = Column(Text)
    sku = Column(Text)
    barcode = Column(Text)
    composed_type = Column(Boolean,default=False)
    sold_type = Column(Boolean,default=True)
    variant_type = Column(Boolean,default=False)
    invent_type = Column(Boolean,default=False)
    invent_min_stock = Column(Integer,default=0)
    invent_alert_type = Column(Boolean,default=False)
    same_price = Column(Boolean,default=True)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, product_name, product_category, product_price, \
        product_sku, product_barcode, product_measurement, product_description, \
        product_sold, product_variant, product_composed, product_stock, data_variant, owner_id):
        response = {}
        session = Session()
        try:
            _exist_item = session.query(Hop_Product_Item).filter_by(name=product_name, owner_id=owner_id, status=True).first()
            if _exist_item is None:
                insert = Hop_Product_Item()
                insert.name = product_name
                insert.product_category_id = product_category
                insert.sku = product_sku if len(product_sku) > 0 else None
                insert.barcode = product_barcode if len(product_barcode) > 0 else None
                measurement = None
                if len(product_measurement['name']) > 0:
                    _em = session.query(Hop_Measurement_List).filter_by(id=product_measurement['id'], owner_id=owner_id, status=True).first()
                    if _em is not None:
                        measurement = _em.id
                    else:
                        _m = Hop_Measurement_List()
                        _m.name = product_measurement['name']
                        _m.owner_id = owner_id
                        session.add(_m)
                        session.commit()
                        measurement = _m.id
                insert.measurement_id = measurement
                insert.description = product_description if len(product_description) > 0 else None
                if len(data_variant) > 0:
                    insert.variant_type = True if product_variant == True else False
                insert.sold_type = True if product_sold == True else False
                print(product_composed)
                insert.composed_type = True if product_composed == True else False
                print(product_stock)
                insert.invent_type = True if product_stock == True else False
                insert.owner_id = owner_id
                session.add(insert)
                session.commit()
                response['id'] = insert.id
                response['variant_type'] = insert.variant_type
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'This item name has been used in your product item'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _exist_item is None:
            if len(product_price) > 0:
                Hop_Price()._insert(pid=response['id'], value=product_price)
            else:
                Hop_Price()._insert(pid=response['id'], value=0)

            if response['variant_type'] == True:
                Hop_Variant_List()._update(item_id=response['id'], data_list=data_variant, owner_id=owner_id)
                Hop_Variant_List()._add_invent_all(item_id=response['id'])

            for i in Hop_Outlet()._listbyownerid(owner_id):
                Hop_Product_Outlet()._insert(i['id'], response['id'])
            response.update(Hop_Product_Item()._data(response['id'], owner_id))
        return response

    def _update_data(self, product_id, product_name, product_category, \
        product_sku, product_barcode, product_measurement, product_description, \
        product_sold, product_composed, product_variant, owner_id):
        response = None
        session = Session()
        try:
            item = session.query(Hop_Product_Item).filter_by(id=product_id, owner_id=owner_id, status=True).first()
            item.name = product_name
            item.product_category_id = product_category
            item.sku = product_sku if len(product_sku) > 0 else None
            item.barcode = product_barcode if len(product_barcode) > 0 else None
            measurement = None
            if len(product_measurement['name']) > 0:
                _em = session.query(Hop_Measurement_List).filter_by(id=product_measurement['id'], owner_id=owner_id, status=True).first()
                if _em is not None:
                    measurement = _em.id
                else:
                    _m = Hop_Measurement_List()
                    _m.name = product_measurement['name']
                    _m.owner_id = owner_id
                    session.add(_m)
                    session.commit()
                    measurement = _m.id
            item.measurement_id = measurement
            item.description = product_description if len(product_description) > 0 else None
            item.sold_type = True if product_sold == True else False
            item.composed_type = True if product_composed == True else False
            _variant = session.query(Hop_Variant_List).filter_by(product_item_id=product_id, status=True).count()
            if _variant > 0:
                item.variant_type = True if product_variant == True else False
            else:
                item.variant_type = False
            item.owner_id = owner_id
            session.add(item)
            session.commit()
            response = item.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return Hop_Product_Item()._data(response, owner_id)

    def _list(self, owner_id):
        response = []
        session = Session()
        try:
            _products = session.query(Hop_Product_Item).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _products:
            response.append(Hop_Product_Item()._data(i.id, owner_id))
        return response

    def _list_sold(self, owner_id):
        response = []
        session = Session()
        try:
            _products = session.query(Hop_Product_Item).filter_by(owner_id=owner_id, sold_type=True, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _products:
            response.append(Hop_Product_Item()._data(i.id, owner_id))
        return response


    def _listbycategory(self, category_id, owner_id):
        response = []
        session = Session()
        try:
            _products = session.query(Hop_Product_Item).filter_by(product_category_id=category_id, owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _products:
            response.append(Hop_Product_Item()._data(i.id, owner_id))
        return response

    def _count(self, category_id, owner_id):
        response = 0
        session = Session()
        try:
            response = session.query(Hop_Product_Item).filter_by(product_category_id=category_id, owner_id=owner_id, status=True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _basic_data(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['cat_id'] = _item.product_category_id
            response['measurement'] = Hop_Measurement_List()._data(_item.measurement_id, owner_id)
            response['variant_type'] = _item.variant_type
        return response

    def _data(self, _id, owner_id, outlet_id=None):
        response = {}
        session = Session()
        try:
            _itemdetail = session.query(Hop_Product_Item).filter_by(id=_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _itemdetail is not None:
            response['id'] = _itemdetail.id
            response['name'] = _itemdetail.name
            response['description'] = _itemdetail.description
            response['sku'] = _itemdetail.sku
            response['barcode'] = _itemdetail.barcode
            response['sold_type'] = _itemdetail.sold_type
            response['composed_type'] = _itemdetail.composed_type
            response['invent_type'] = _itemdetail.invent_type
            response['variant_type'] = _itemdetail.variant_type
            response['category'] = Hop_Product_Category()._basicdata(_itemdetail.product_category_id, owner_id)
            response['measurement'] = Hop_Measurement_List()._data(_itemdetail.measurement_id, owner_id) if _itemdetail.measurement_id is not None else None
            response['price'] = Hop_Price()._check_list_price(pid=_itemdetail.id, variant_type=_itemdetail.variant_type, same_type=_itemdetail.same_price, outlet_id=outlet_id)
        return response

    def _data_price_outlet(self, _id, _outlet_id, _same_price, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['sku'] = _item.sku
            response['price'] = Hop_Price()._check_detail_price(pid=_item.id, variant_type=_item.variant_type, same_type=False, outlet_id=_outlet_id)
        return response

    def _price(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['same_price'] = _item.same_price
            response['sku'] = _item.sku if _item.sku is not None else '-'
            response['variant_type'] = _item.variant_type
            response['sold'] = _item.sold_type
            response['variant_list'] = []
            if _item.variant_type is False:
                response['price'] = Hop_Price()._check_detail_price(pid=_item.id)
            else:
                response['variant_list'] = Hop_Variant_List()._list(item_id=_item.id)
                response['price'] = Hop_Price()._check_detail_price(pid=_item.id, variant_type=True)
            response['outlet_list'] = []
            _outlet = session.query(Hop_Outlet).filter_by(owner_id=owner_id, status=True).all()
            for o in _outlet:
                response['outlet_list'].append({
                    'id': o.id,
                    'name': o.name
                })
        return response

    def _ingredients(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['same_price'] = _item.same_price
            response['sku'] = _item.sku if _item.sku is not None else '-'
            response['variant_type'] = _item.variant_type
            response['sold'] = _item.sold_type
            response['variant_list'] = []
            response['ingredients_list'] = []
            if _item.variant_type is False:
                response['ingredients_list'].append(Hop_Composed_Product()._list(mpid=_item.id, mvid=None, owner_id=owner_id))
            else:
                response['variant_list'] = Hop_Variant_List()._list(item_id=_item.id)
                for i in response['variant_list']:
                    response['ingredients_list'].append(Hop_Composed_Product()._list(mpid=_item.id, mvid=i['id'], owner_id=owner_id))
        return response

    def _stock(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['sku'] = _item.sku if _item.sku is not None else '-'
            response['variant_type'] = _item.variant_type
            response['invent_type'] = _item.invent_type
            response['invent_min_stock'] = _item.invent_min_stock
            response['invent_alert_type'] = _item.invent_alert_type
            response['variant_list'] = []
            if _item.variant_type is True:
                response['variant_list'] = Hop_Variant_List()._list_stock(item_id=_item.id)
        return response

    def _update_price(self, _id, _same_price, _price, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _item is not None:
                if _same_price == True:
                    _item.same_price = True
                    if _item.variant_type == False:
                        for i in _price:
                            _item.sold_type = True if i['sold'] == True else False
                            Hop_Price()._insert(pid=_item.id, value=i['value'])
                    else:
                        Hop_Price()._insert(pid=_item.id, variant_type=True, same_type=True, price_list=_price)
                else:
                    _item.same_price = False
                session.add(_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _update_stock(self, _id, _stock, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _item is not None:
                print(_stock)
                if _item.variant_type == False:
                    _item.invent_type = True if _stock[0]['invent_type'] == True else False
                    _item.invent_min_stock = _stock[0]['value']
                    _item.invent_alert_type = True if _stock[0]['alert_type'] == True else False
                    session.add(_item)
                    session.commit()
                else:
                    Hop_Variant_List()._update_stock(_stock=_stock)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _update_outlet_price(self, _id, _price, outlet_id, owner_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _item is not None:
                if _item.variant_type == False:
                    for i in _price:
                        Hop_Price()._insert(pid=_item.id, value=i['value'], same_type=False, outlet_id=outlet_id)
                else:
                    Hop_Price()._insert(pid=_item.id, variant_type=True, same_type=False, outlet_id=outlet_id, price_list=_price)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _remove(self, product_id, owner_id):
        response = {}
        response
        session = Session()
        try:
            _itemdetail = session.query(Hop_Product_Item).filter_by(id=product_id, owner_id=owner_id, status=True).first()
            if _itemdetail is not None:
                response['status'] = '00'
                response['name'] = _itemdetail.name
                response['id'] = _itemdetail.id
                _itemdetail.status = False
                session.add(_itemdetail)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        Hop_Product_Outlet()._remove_many(response['id'])
        return response

    def _remove_many(self, product_list, owner_id):
        response = []
        for i in product_list:
            response.append(Hop_Product_Item()._remove(product_id=i, owner_id=owner_id))
        return response

    def _checkbyuserid(self,_userid):
        response = True
        session = Session()
        try:
            _itemdetail = session.query(product_item).filter_by(owner_id = _userid, status = True).first()
            if _itemdetail is None:
                response = False
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return True

class Hop_Product_Outlet(Base):
    __tablename__ = 'product_outlet'

    id = Column(Integer,primary_key=True)
    outlet_id = Column(Integer,ForeignKey('outlet.id'))
    product_item_id = Column(Integer,ForeignKey('product_item.id'))
    product_category_id = Column(Integer,ForeignKey('product_category.id'),default=None)
    favourite = Column(Boolean,default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insertall(self, outlet_id, owner_id):
        session = Session()
        try:
            product_item = session.query(Hop_Product_Item).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in product_item:
            Hop_Product_Outlet()._insert(outlet_id, i.id)

    def _insert(self, _outletid, _productitem):
        session = Session()
        try:
            insert = Hop_Product_Outlet()
            insert.outlet_id = _outletid
            insert.product_item_id = _productitem
            insert.product_category_id = _productitem
            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update(self, outlet_id, _list, owner_id):
        Hop_Product_Outlet()._remove_many_by_outlet(outlet_id)
        session = Session()
        try:
            for i in _list:
                hpo = session.query(Hop_Product_Outlet).filter_by(outlet_id=outlet_id, product_item_id=i).first()
                hpo.status = True
                session.add(hpo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Product_Outlet()._count(outlet_id, owner_id)

    def _remove(self, _outletid, product_item_id):
        session = Session()
        try:
            hpo = session.query(Hop_Product_Outlet).filter_by(outlet_id=_outletid, product_item_id=product_item_id, status=True).first()
            hpo.status = False
            session.add(hpo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_many(self, product_item_id):
        session = Session()
        try:
            hpo = session.query(Hop_Product_Outlet).filter_by(product_item_id=product_item_id, status=True).all()
            for i in hpo:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_many_by_outlet(self, outlet_id):
        session = Session()
        try:
            hpo = session.query(Hop_Product_Outlet).filter_by(outlet_id=outlet_id, status=True).all()
            for i in hpo:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _list(self, outlet_id, owner_id):
        response = []
        session = Session()
        try:
            _products = session.query(Hop_Product_Outlet).filter_by(outlet_id=outlet_id, status=True).all()
            for i in _products:
                _item = session.query(Hop_Product_Item).filter_by(id=i.product_item_id, sold_type=True, owner_id=owner_id, status=True).first()
                if _item is not None:
                    response.append({
                        'id': _item.id,
                        'name': _item.name,
                    })
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _count(self, outlet_id, owner_id):
        response_list = []
        response = 0
        session = Session()
        try:
            _product = session.query(Hop_Product_Outlet).filter_by(outlet_id=outlet_id, status=True).all()
            for i in _product:
                _item = session.query(Hop_Product_Item).filter_by(id=i.product_item_id, sold_type=True, owner_id=owner_id, status=True).first()
                if _item is not None:
                    response_list.append({
                        'id': _item.id,
                        'name': _item.name,
                    })
            response = len(response_list)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Product_Category_Outlet(Base):
    __tablename__ = 'product_category_outlet'

    id = Column(Integer,primary_key=True)
    outlet_id = Column(Integer,ForeignKey('outlet.id'))
    product_category_id = Column(Integer,ForeignKey('product_category.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insertall(self, outlet_id, owner_id):
        session = Session()
        try:
            product_category = session.query(Hop_Product_Category).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for pc in product_category:
            Hop_Product_Category_Outlet()._insert(outlet_id, pc.id)

    def _insert(self, _outletid, _productcategory):
        session = Session()
        try:
            insert = Hop_Product_Category_Outlet()
            insert.outlet_id = _outletid
            insert.product_category_id = _productcategory
            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update(self, outlet_id, _list, owner_id):
        Hop_Product_Category_Outlet()._remove_many_by_outlet(outlet_id)
        session = Session()
        try:
            for i in _list:
                hpo = session.query(Hop_Product_Category_Outlet).filter_by(outlet_id=outlet_id, product_category_id=i).first()
                hpo.status = True
                session.add(hpo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Product_Category_Outlet()._count(outlet_id, owner_id)

    def _remove(self, _outletid, _productcategory):
        session = Session()
        try:
            hpco = session.query(Hop_Product_Category_Outlet).filter_by(outlet_id=_outletid, product_category_id=_productcategory, status=True).first()
            hpco.status = False
            session.add(hpco)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_many(self, _productcategory):
        session = Session()
        try:
            hpco = session.query(Hop_Product_Category_Outlet).filter_by(product_category_id=_productcategory, status=True).all()
            for i in hpco:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_many_by_outlet(self, outlet_id):
        session = Session()
        try:
            hpo = session.query(Hop_Product_Category_Outlet).filter_by(outlet_id=outlet_id, status=True).all()
            for i in hpo:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _list(self, outlet_id, owner_id):
        response = []
        session = Session()
        try:
            _products = session.query(Hop_Product_Category_Outlet).filter_by(outlet_id=outlet_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _products:
            print(i.id)
            response.append(Hop_Product_Category()._basicdata(i.product_category_id, owner_id))
        return response

    def _count(self, outlet_id, owner_id):
        response = 0
        session = Session()
        try:
            response = session.query(Hop_Product_Category_Outlet).filter_by(outlet_id=outlet_id, status=True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Measurement_List(Base):
    __tablename__ = 'measurement_list'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    owner_id = Column(Integer,ForeignKey('user.id'),default=None)
    default = Column(Boolean,default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self, q, owner_id):
        response = []
        session = Session()
        try:
            _measurement_list = session.query(Hop_Measurement_List).filter_by(owner_id=owner_id, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _measurement_list:
            response.append({
                'id' : i.id,
                'name' : i.name
            })
        return response

    def _data(self, _id, owner_id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _measurement_list = session.query(Hop_Measurement_List).filter_by(id=_id, owner_id=owner_id).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _measurement_list is not None:
            response['id'] = _measurement_list.id
            response['name'] = _measurement_list.name
            response['status'] = '00'
        return response

class Hop_Price(Base):
    __tablename__ = 'price'

    id = Column(Integer,primary_key=True)
    pid = Column(Integer,ForeignKey('product_item.id'), default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'), default=None)
    value = Column(Numeric(36,2), default=0)
    variant_type = Column(Boolean,default=False)
    same_type = Column(Boolean,default=True)
    outlet_id = Column(Integer,ForeignKey('outlet.id'), default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _check_list_price(self, pid=None, vid=None, value=0, variant_type=False, same_type=True, outlet_id=None):
        response = {}
        response['value'] = 0
        response['status'] = '50'
        session = Session()
        try:
            if same_type == True:
                if variant_type == False:
                    price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                    if price is not None:
                        response['value'] = str(price.value)
                        response['status'] = '00'
                else:
                    cp = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=True, status=True).count()
                    if cp > 0:
                        _max_price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=True, status=True).order_by(desc(Hop_Price.value)).first()
                        _min_price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=True, status=True).order_by(asc(Hop_Price.value)).first()
                        response['value'] = str(_min_price.value)
                        response['status'] = '00'
                        if _min_price.value != _max_price.value:
                            response['value'] = str(int(_min_price.value)) + ' - ' + str(int(_max_price.value))
                    else:
                        price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                        response['value'] = str(price.value)
                        response['status'] = '00'
            else:
                if variant_type == False:
                    _max_price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=False, status=True).order_by(desc(Hop_Price.value)).first()
                    _min_price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=False, status=True).order_by(asc(Hop_Price.value)).first()
                    response['value'] = str(_min_price.value)
                    response['status'] = '00'
                    if _min_price.value != _max_price.value:
                        response['value'] = str(int(_min_price.value)) + ' - ' + str(int(_max_price.value))
                        response['status'] = '00'
                else:
                    cp = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=True, status=True).count()
                    if cp > 0:
                        _max_price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=True, status=True).order_by(desc(Hop_Price.value)).first()
                        _min_price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=True, status=True).order_by(asc(Hop_Price.value)).first()
                        response['value'] = str(_min_price.value)
                        response['status'] = '00'
                        if _min_price.value != _max_price.value:
                            response['value'] = str(int(_min_price.value)) + ' - ' + str(int(_max_price.value))
                    else:
                        price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                        response['value'] = str(price.value)
                        response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _check_detail_price(self, pid=None, variant_type=False, same_type=True, outlet_id=None):
        response = {}
        response['price_list'] = []
        response['status'] = '50'
        session = Session()
        try:
            if same_type == True:
                if variant_type == False:
                    price_data = {}
                    price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                    price_data['id'] = price.id
                    price_data['pid'] = price.pid
                    price_data['vid'] = price.vid
                    price_data['value'] = int(price.value)
                    response['status'] = '50'
                    response['price_list'].append(price_data)
                else:
                    price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=True, status=True).all()
                    response['status'] = '00'
                    if len(price) > 0:
                        for i in price:
                            if session.query(Hop_Variant_List).filter_by(id=i.vid, status=True).first() is not None:
                                price_data = {}
                                price_data['id'] = i.id
                                price_data['pid'] = i.pid
                                price_data['vid'] = i.vid
                                price_data['value'] = int(i.value)
                                response['price_list'].append(price_data)
                        if len(response['price_list']) == 0:
                            price_data = {}
                            price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                            price_data['id'] = price.id
                            price_data['pid'] = price.pid
                            price_data['vid'] = price.vid
                            price_data['value'] = int(price.value)
                            response['price_list'].append(price_data)
                            response['status'] = '50'
                    else:
                        price_data = {}
                        price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                        price_data['id'] = price.id
                        price_data['pid'] = price.pid
                        price_data['vid'] = price.vid
                        price_data['value'] = int(price.value)
                        response['price_list'].append(price_data)
                        response['status'] = '50'
            else:
                if variant_type == False:
                    price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=False, outlet_id=outlet_id, status=True).all()
                    if len(price) > 0:
                        for i in price:
                            price_data = {}
                            price_data['id'] = i.id
                            price_data['pid'] = i.pid
                            price_data['vid'] = i.vid
                            price_data['value'] = int(i.value)
                            response['price_list'].append(price_data)
                        response['status'] = '00'
                    else:
                        price_data = {}
                        price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                        price_data['id'] = price.id
                        price_data['pid'] = price.pid
                        price_data['vid'] = price.vid
                        price_data['value'] = int(price.value)
                        response['price_list'].append(price_data)
                        response['status'] = '50'
                else:
                    if outlet_id is not None:
                        # single_price = Hop_Price.query.filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                        price = session.query(Hop_Price).filter_by(pid=pid, same_type=False, variant_type=True, outlet_id=outlet_id, status=True).all()
                        response['status'] = '00'
                        if len(price) > 0:
                            for i in price:
                                if session.query(Hop_Variant_List).filter_by(id=i.vid, status=True).first() is not None:
                                    price_data = {}
                                    price_data['id'] = i.id
                                    price_data['pid'] = i.pid
                                    price_data['vid'] = i.vid
                                    price_data['value'] = int(i.value)
                                    response['price_list'].append(price_data)
                            if len(response['price_list']) == 0:
                                price_data = {}
                                price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                                price_data['id'] = price.id
                                price_data['pid'] = price.pid
                                price_data['vid'] = price.vid
                                price_data['value'] = int(price.value)
                                response['price_list'].append(price_data)
                                response['status'] = '50'
                        else:
                            price_data = {}
                            price = session.query(Hop_Price).filter_by(pid=pid, same_type=True, variant_type=False, status=True).first()
                            price_data['id'] = price.id
                            price_data['pid'] = price.pid
                            price_data['vid'] = price.vid
                            price_data['value'] = int(price.value)
                            response['price_list'].append(price_data)
                            response['status'] = '50'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _insert(self, pid=None, vid=None, value=0, variant_type=False, same_type=True, outlet_id=None, price_list=None):
        session = Session()
        try:
            if same_type == True:
                if variant_type == False:
                    _exist_price = session.query(Hop_Price).filter_by(pid=pid, variant_type=False, same_type=True).all()
                    for i in _exist_price:
                        i.status = False
                        session.add(i)
                    insert = Hop_Price()
                    insert.pid = pid
                    insert.value = value
                    session.add(insert)
                else:
                    for i in price_list:
                        vi = None
                        if type(i['vi']) == int:
                            vi = i['vi']
                        if vi is not None:
                            variant = session.query(Hop_Variant_List).filter_by(id=vi, status=True).first()
                            variant.sold_type = True if i['sold'] == True else False
                            session.add(variant)
                            _exist_price = session.query(Hop_Price).filter_by(pid=pid, vid=vi, variant_type=True, same_type=True).all()
                            for m in _exist_price:
                                m.status = False
                                session.add(m)
                            insert = Hop_Price()
                            insert.pid = pid
                            insert.vid = vi
                            insert.variant_type = True
                            insert.value = i['value']
                            session.add(insert)
            else:
                if variant_type == False:
                    _exist_price = session.query(Hop_Price).filter_by(pid=pid, variant_type=False, same_type=False, outlet_id=outlet_id).all()
                    for i in _exist_price:
                        i.status = False
                        session.add(i)
                    insert = Hop_Price()
                    insert.pid = pid
                    insert.vid = vid
                    insert.value = value
                    insert.same_type = False
                    insert.outlet_id = outlet_id
                    session.add(insert)
                else:
                    for i in price_list:
                        vi = None
                        if type(i['vi']) == int:
                            vi = i['vi']
                        if vi is not None and outlet_id is not None:
                            _exist_price = session.query(Hop_Price).filter_by(pid=pid, vid=vi, variant_type=True, same_type=False, outlet_id=outlet_id).all()
                            for m in _exist_price:
                                m.status = False
                                session.add(m)
                            insert = Hop_Price()
                            insert.pid = pid
                            insert.vid = vi
                            insert.variant_type = True
                            insert.same_type = False
                            insert.outlet_id = outlet_id
                            insert.value = i['value']
                            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_many_variant(self, pid=None):
        session = Session()
        try:
            _price = session.query(Hop_Price).filter_by(pid=pid, variant_type=True, status=True).all()
            for i in _price:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _data(self, outlet_id, pid, vid, variant_type, same_type):
        session = Session()
        try:
            response = {}
            _price = session.query(Hop_Price).filter_by(outlet_id=outlet_id, pid=pid, vid=vid, variant_type=variant_type, same_type=same_type, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        response['id'] = _id
        response['value'] = 0
        if _price is not None:
            response['value'] = _price.value
        return response

class Hop_Variant_Category(Base):
    __tablename__ = 'variant_category'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    product_item_id = Column(Integer,ForeignKey('product_item.id'))
    owner_id = Column(Integer,ForeignKey('user.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _remove_all(self, item_id, owner_id):
        session = Session()
        try:
            _exist_variant = session.query(Hop_Variant_Category).filter_by(product_item_id=item_id, owner_id=owner_id, status=True).all()
            for i in _exist_variant:
                Hop_Variant_Item()._remove_all(variant_category_id=i.id, item_id=item_id, owner_id=owner_id)
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update(self, id, name, item_id, owner_id):
        response = {}
        session = Session()
        try:
            _exist_variant = session.query(Hop_Variant_Category).filter_by(id=id, product_item_id=item_id, owner_id=owner_id).first()
            if _exist_variant is not None and id != 0:
                _exist_variant.status = True
                session.add(_exist_variant)
                session.commit()
                response = {
                    'id': _exist_variant.id,
                    'name': _exist_variant.name,
                }
            else:
                _variant = Hop_Variant_Category()
                _variant.name = name
                _variant.product_item_id = item_id
                _variant.owner_id = owner_id
                session.add(_variant)
                session.commit()
                response =  {
                    'id': _variant.id,
                    'name': _variant.name,
                }
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _listbyproduct(self, _product):
        response = []
        session = Session()
        try:
            _variant_category = session.query(Hop_Variant_Category).filter_by(product_item_id = _product, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _variant_category:
            response.append({
                'id' : i.id,
                'name' : i.name,
                'sub_variant' : Hop_Variant_Item()._listbyvariantcategory(i.id)
            })
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _variant_category = session.query(Hop_Variant_Category).filter_by(id = _id, status = True).first()
            if _variant_category is not None:
                response['id'] = _variant_category.id
                response['name'] = _variant_category.name
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Variant_Item(Base):
    __tablename__ = 'variant_item'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    variant_category_id = Column(Integer,ForeignKey('variant_category.id'))
    product_item_id = Column(Integer,ForeignKey('product_item.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _remove_all(self, variant_category_id, item_id, owner_id):
        session = Session()
        try:
            _exist_variant = session.query(Hop_Variant_Item).filter_by(variant_category_id=variant_category_id, product_item_id=item_id, status=True).all()
            for i in _exist_variant:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def _update(self, id, name, variant_category_id, item_id, owner_id):
        response = {}
        session = Session()
        try:
            _exist_variant = session.query(Hop_Variant_Item).filter_by(id=id, variant_category_id=variant_category_id, product_item_id=item_id).first()
            if _exist_variant is not None and id != 0:
                _exist_variant.status = True
                session.add(_exist_variant)
                session.commit()
                response = {
                    'id': _exist_variant.id,
                    'name': _exist_variant.name,
                }
            else:
                _variant = Hop_Variant_Item()
                _variant.name = name
                _variant.variant_category_id = variant_category_id
                _variant.product_item_id = item_id
                _variant.owner_id = owner_id
                session.add(_variant)
                session.commit()
                response = Hop_Variant_Item()._data(_variant.id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _listbyvariantcategory(self, _variantcategory):
        response = []
        session = Session()
        try:
            _variant_item = session.query(Hop_Variant_Item).filter_by(variant_category_id = _variantcategory, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _variant_item:
            response.append({
                'id' : i.id,
                'text' : i.name,
                'name' : i.name,
            })
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _variant_item = session.query(Hop_Variant_Item).filter_by(id=_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _variant_item is not None:
            response['id'] = _variant_item.id
            response['name'] = _variant_item.name
        return response

class Hop_Variant_List(Base):
    __tablename__ = 'variant_list'

    id = Column(Integer,primary_key=True)
    product_item_id = Column(Integer,ForeignKey('product_item.id'),default=None)
    variant_item_1 = Column(Integer,ForeignKey('outlet.id'),default=None)
    variant_item_2 = Column(Integer,ForeignKey('variant_item.id'),default=None)
    variant_item_3 = Column(Integer,ForeignKey('variant_item.id'),default=None)
    variant_item_4 = Column(Integer,ForeignKey('variant_item.id'),default=None)
    sku = Column(Text)
    sold_type = Column(Boolean,default=True)
    invent_type = Column(Boolean,default=False)
    invent_min_stock = Column(Integer,default=0)
    invent_alert_type = Column(Boolean,default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _add_invent_all(self, item_id):
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter_by(product_item_id=item_id, status=True).all()
            for i in _variant:
                i.invent_type = True
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update(self, item_id, data_list, owner_id):
        response = {}
        _data = []
        _cat_list = []
        Hop_Variant_Category()._remove_all(item_id, owner_id)
        for x in data_list:
            _category = Hop_Variant_Category()._update(id=x['id'], name=x['name'], item_id=item_id, owner_id=owner_id)
            _cat_list.append(_category['id'])
            _detail = []
            Hop_Variant_Item()._remove_all(variant_category_id=_category['id'], item_id=item_id, owner_id=owner_id)
            for y in x['sub_variant']:
                _item = Hop_Variant_Item()._update(id=y['id'], name=y['name'], variant_category_id=_category['id'], item_id=item_id, owner_id=owner_id)
                _detail.append(_item['id'])
            _data.append(_detail)
        _matrix = list(itertools.product(*_data))

        Hop_Variant_List()._remove_all(product_item_id=item_id)
        Hop_Price()._remove_many_variant(pid=item_id)
        session = Session()
        try:
            if len(_matrix) > 0 and len(_cat_list) > 0:
                for i in _matrix:
                    _variant = session.query(Hop_Variant_List).filter_by(
                        product_item_id=item_id,
                        variant_item_1=i[0],
                        variant_item_2=None,
                        variant_item_3=None,
                        variant_item_4=None).first()
                    if len(_cat_list) == 2:
                        _variant = session.query(Hop_Variant_List).filter_by(
                            product_item_id=item_id,
                            variant_item_1=i[0],
                            variant_item_2=i[1],
                            variant_item_3=None,
                            variant_item_4=None).first()
                    elif len(_cat_list) == 3:
                        _variant = session.query(Hop_Variant_List).filter_by(
                            product_item_id=item_id,
                            variant_item_1=i[0],
                            variant_item_2=i[1],
                            variant_item_3=i[2],
                            variant_item_4=None).first()
                    elif len(_cat_list) == 4:
                        _variant = session.query(Hop_Variant_List).filter_by(
                            product_item_id=item_id,
                            variant_item_1=i[0],
                            variant_item_2=i[1],
                            variant_item_3=i[2],
                            variant_item_4=i[3]).first()
                    if _variant is not None:
                        _variant.status = True
                        session.add(_variant)
                        single_price = session.query(Hop_Price).filter_by(pid=item_id, vid=_variant.id).order_by(desc(Hop_Price.id)).limit(1).all()
                        for i in single_price:
                            i.status = True
                            session.add(i)
                        _outlet = session.query(Hop_Outlet).filter_by(owner_id=owner_id, status=True).all()
                        for o in _outlet:
                            outlet_price = session.query(Hop_Price).filter_by(pid=item_id, vid=_variant.id, outlet_id=o.id).order_by(desc(Hop_Price.id)).limit(1).all()
                            for v in outlet_price:
                                v.status = True
                                session.add(v)
                    else:
                        _insert = Hop_Variant_List()
                        _insert.product_item_id = item_id
                        _insert.variant_item_1 = i[0]
                        if len(_cat_list) >= 2:
                            _insert.variant_item_2 = i[1]
                        if len(_cat_list) >= 3:
                            _insert.variant_item_3 = i[2]
                        if len(_cat_list) >= 4:
                            _insert.variant_item_4 = i[3]
                        session.add(_insert)
                session.commit()
            response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _list(self, item_id):
        response = []
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter_by(product_item_id=item_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _variant:
            _data = {}
            _data['id'] = i.id
            _data['product_item_id'] = i.product_item_id
            _data['invent_type'] = i.invent_type
            _data['sold'] = i.sold_type
            _data['sku'] = i.sku if i.sku is not None else '-'
            _data['variant_item_1'] = Hop_Variant_Item()._data(i.variant_item_1)
            if i.variant_item_2 != None:
                _data['variant_item_2'] = Hop_Variant_Item()._data(i.variant_item_2)
            else:
                _data['variant_item_2'] = None
            if i.variant_item_3 != None:
                _data['variant_item_3'] = Hop_Variant_Item()._data(i.variant_item_3)
            else:
                _data['variant_item_3'] = None
            if i.variant_item_4 != None:
                _data['variant_item_4'] = Hop_Variant_Item()._data(i.variant_item_4)
            else:
                _data['variant_item_4'] = None
            response.append(_data)
        return response

    def _list_stock(self, item_id):
        response = []
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter_by(product_item_id=item_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _variant:
            _data = {}
            _data['id'] = i.id
            _data['product_item_id'] = i.product_item_id
            _data['invent_type'] = i.invent_type
            _data['invent_min_stock'] = i.invent_min_stock
            _data['invent_alert_type'] = i.invent_alert_type
            _data['sku'] = i.sku if i.sku is not None else '-'
            _data['variant_item_1'] = Hop_Variant_Item()._data(i.variant_item_1)
            if i.variant_item_2 != None:
                _data['variant_item_2'] = Hop_Variant_Item()._data(i.variant_item_2)
            else:
                _data['variant_item_2'] = None
            if i.variant_item_3 != None:
                _data['variant_item_3'] = Hop_Variant_Item()._data(i.variant_item_3)
            else:
                _data['variant_item_3'] = None
            if i.variant_item_4 != None:
                _data['variant_item_4'] = Hop_Variant_Item()._data(i.variant_item_4)
            else:
                _data['variant_item_4'] = None
            response.append(_data)
        return response

    def _list_except(self, item_id, except_list):
        response = []
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter(Hop_Variant_List.product_item_id==item_id, Hop_Variant_List.invent_type==True, Hop_Variant_List.status==True, ~Hop_Variant_List.id.in_(except_list)).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _variant:
            _data = {}
            _data['id'] = i.id
            _data['product_item_id'] = i.product_item_id
            _data['invent_type'] = i.invent_type
            _data['sold'] = i.sold_type
            _data['sku'] = i.sku if i.sku is not None else '-'
            _data['variant_item_1'] = Hop_Variant_Item()._data(i.variant_item_1)
            if i.variant_item_2 != None:
                _data['variant_item_2'] = Hop_Variant_Item()._data(i.variant_item_2)
            else:
                _data['variant_item_2'] = None
            if i.variant_item_3 != None:
                _data['variant_item_3'] = Hop_Variant_Item()._data(i.variant_item_3)
            else:
                _data['variant_item_3'] = None
            if i.variant_item_4 != None:
                _data['variant_item_4'] = Hop_Variant_Item()._data(i.variant_item_4)
            else:
                _data['variant_item_4'] = None
            response.append(_data)
        return response

    def _data(self, pid, vid):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter_by(id=vid, product_item_id=pid, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _variant is not None:
            response['id'] = _variant.id
            response['product_item_id'] = _variant.product_item_id
            response['invent_type'] = _variant.invent_type
            response['sold'] = _variant.sold_type
            response['sku'] = _variant.sku if _variant.sku is not None else '-'
            response['variant_item_1'] = Hop_Variant_Item()._data(_variant.variant_item_1)
            if _variant.variant_item_2 != None:
                response['variant_item_2'] = Hop_Variant_Item()._data(_variant.variant_item_2)
            else:
                response['variant_item_2'] = None
            if _variant.variant_item_3 != None:
                response['variant_item_3'] = Hop_Variant_Item()._data(_variant.variant_item_3)
            else:
                response['variant_item_3'] = None
            if _variant.variant_item_4 != None:
                response['variant_item_4'] = Hop_Variant_Item()._data(_variant.variant_item_4)
            else:
                response['variant_item_4'] = None
            response['status'] = '00'
        return response

    def _data_no_status(self, pid, vid):
        response = {}
        response['status'] = '50'
        session = Session()
        print(vid)
        try:
            _variant = session.query(Hop_Variant_List).filter_by(id=vid, product_item_id=pid).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _variant is not None:
            response['id'] = _variant.id
            response['product_item_id'] = _variant.product_item_id
            response['invent_type'] = _variant.invent_type
            response['sold'] = _variant.sold_type
            response['sku'] = _variant.sku if _variant.sku is not None else '-'
            response['variant_item_1'] = Hop_Variant_Item()._data(_variant.variant_item_1)
            if _variant.variant_item_2 != None:
                response['variant_item_2'] = Hop_Variant_Item()._data(_variant.variant_item_2)
            else:
                response['variant_item_2'] = None
            if _variant.variant_item_3 != None:
                response['variant_item_3'] = Hop_Variant_Item()._data(_variant.variant_item_3)
            else:
                response['variant_item_3'] = None
            if _variant.variant_item_4 != None:
                response['variant_item_4'] = Hop_Variant_Item()._data(_variant.variant_item_4)
            else:
                response['variant_item_4'] = None
            response['status'] = '00'
        return response

    def _remove_all(self, product_item_id):
        response = {}
        session = Session()
        try:
            _variant = session.query(Hop_Variant_List).filter_by(product_item_id=product_item_id, status=True).all()
            for i in _variant:
                i.status=False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _update_stock(self, _stock):
        session = Session()
        try:
            for i in _stock:
                _variant = session.query(Hop_Variant_List).filter_by(product_item_id=i['pi'], id=i['vi'], status=True).first()
                if _variant is not None:
                    _variant.invent_type = True if i['invent_type'] == True else False
                    _variant.invent_min_stock = i['value']
                    _variant.invent_alert_type = True if i['alert_type'] == True else False
                    session.add(_variant)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

class Hop_Variant_Price_Outlet(Base):
    __tablename__ = 'variant_price_outlet'

    id = Column(Integer,primary_key=True)
    variant_list_id = Column(Integer,ForeignKey('variant_list.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    price = Column(Integer,default=0)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Composed_Product(Base):
    __tablename__ = 'composed_product'

    id = Column(Integer,primary_key=True)
    main_product_id = Column(Integer,ForeignKey('product_item.id'),default=None)
    main_variant_list_id = Column(Integer,ForeignKey('variant_list.id'),default=None)
    ingredients_product_id = Column(Integer,ForeignKey('product_item.id'),default=None)
    ingredients_variant_list_id = Column(Integer,ForeignKey('variant_list.id'),default=None)
    amount = Column(Numeric(10,2),default=0)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, _main_list, _list, owner_id):
        session = Session()
        try:
            for i in _main_list['vid']:
                Hop_Composed_Product()._remove(_main_list['pid'], i)
            for i in _list:
                _exist = session.query(Hop_Composed_Product).filter_by(
                    main_product_id=i['mpid'],
                    main_variant_list_id=i['mvid'] if i['mvid'] != None else None,
                    ingredients_product_id=i['ipid'],
                    ingredients_variant_list_id=None,
                )
                if i['ivariant'] == True:
                    _exist = session.query(Hop_Composed_Product).filter_by(
                        main_product_id=i['mpid'],
                        main_variant_list_id=i['mvid'] if i['mvid'] != None else None,
                        ingredients_product_id=i['ipid'],
                        ingredients_variant_list_id=i['ivid'],
                    )
                if _exist.count() > 0:
                    _exist_q = None
                    for x in _exist.order_by(desc(Hop_Composed_Product.id)).limit(1).all():
                        if float(i['value']) == float(x.amount):
                            x.status = True
                            session.add(x)
                        else:
                            _composed = Hop_Composed_Product()
                            _composed.main_product_id=i['mpid']
                            _composed.main_variant_list_id=i['mvid'] if i['mvid'] != None else None
                            _composed.ingredients_product_id=i['ipid']
                            if i['ivariant'] == True:
                                _composed.ingredients_variant_list_id=i['ivid']
                            _composed.amount=Decimal(i['value'])
                            session.add(_composed)
                else:
                    _composed = Hop_Composed_Product()
                    _composed.main_product_id=i['mpid']
                    _composed.main_variant_list_id=i['mvid'] if i['mvid'] != None else None
                    _composed.ingredients_product_id=i['ipid']
                    if i['ivariant'] == True:
                        _composed.ingredients_variant_list_id=i['ivid']
                    _composed.amount=Decimal(i['value'])
                    session.add(_composed)
                session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove(self, mpid, mvid):
        session = Session()
        try:
            _exist = session.query(Hop_Composed_Product).filter_by(
                main_product_id=mpid,
                main_variant_list_id=mvid,
                status=True
            )
            for i in _exist.all():
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _list(self, mpid=None, mvid=None, owner_id=None):
        response = {}
        response['mpid'] = mpid
        response['mvid'] = mvid
        response['list'] = []
        session = Session()
        try:
            print(mpid)
            print(mvid)
            _composed = session.query(Hop_Composed_Product).filter_by(main_product_id=mpid, main_variant_list_id=mvid, status=True).all()
            print(len(_composed))
        except:
            session.rollback()
            raise
        finally:
            session.close()
        print(len(_composed))
        for i in _composed:
            print(i.id)
            _data = {}
            _data['ipid'] = Hop_Product_Item()._basic_data(i.ingredients_product_id, owner_id)
            _data['amount'] = str(i.amount)
            _data['ivid'] =  None
            if i.ingredients_variant_list_id is not None:
                _data['ivid'] = Hop_Variant_List()._data(i.ingredients_product_id, i.ingredients_variant_list_id)
            response['list'].append(_data)
        return response

    def _exist_list_item(self, mpid=None, mvid=None, owner_id=None):
        response = {}
        response['status'] = '50'
        response['list'] = []
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=mpid, owner_id=owner_id, status=True).first()
            if _item is not None:
                response['name'] = _item.name
                _item_list = session.query(Hop_Product_Item).filter_by(owner_id=owner_id, status=True).all()
                if _item.variant_type == False:
                    _item_list = session.query(Hop_Product_Item).filter(Hop_Product_Item.id != mpid).filter_by(owner_id=owner_id, status=True).all()
                for i in _item_list:
                    if i.variant_type == True:
                        _ic = session.query(Hop_Composed_Product).filter(Hop_Composed_Product.main_variant_list_id != None, Hop_Composed_Product.main_variant_list_id != mvid).filter_by(main_product_id=i.id, status=True).count()
                    else:
                        _ic = session.query(Hop_Composed_Product).filter_by(main_product_id=i.id, status=True).count()
                    if _ic > 0:
                        response['list'].append({
                            'id' : i.id,
                            'name' : i.name,
                        })
                if len(response['list']) > 0:
                    response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _exist_list_variant(self, impid=None, mpid=None, mvid=None, owner_id=None):
        response = {}
        response['status'] = '50'
        response['variant'] = False
        response['list'] = []
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=impid, owner_id=owner_id, status=True).first()
            if _item is not None and _item.variant_type == True:
                _variant_list = session.query(Hop_Variant_List).filter(Hop_Variant_List.id != mvid).filter_by(product_item_id=impid, status=True).all()
                for i in _variant_list:
                    _vc = session.query(Hop_Composed_Product).filter_by(main_product_id=impid, main_variant_list_id=i.id, status=True).count()
                    if _vc > 0:
                        response['list'].append(Hop_Variant_List()._data(impid, i.id))
                if len(response['list']) > 0:
                    response['variant'] = False
                    response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, mpid, mvid, owner_id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(id=mpid, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['variant_type'] = _item.variant_type
            response['status'] = '00'
            response['ingredients_list'] = []
            if _item.variant_type is False:
                response['ingredients_list'] = Hop_Composed_Product()._list(mpid=_item.id, mvid=None, owner_id=owner_id)
            else:
                response['ingredients_list'] = Hop_Composed_Product()._list(mpid=_item.id, mvid=mvid, owner_id=owner_id)
        return response

# CLASS FOR inventory

class Hop_Inventory_Type(Base):

    __tablename__ = 'inventory_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, id):
        response = {}
        session = Session()
        try:
            _invent = session.query(Hop_Inventory_Type).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _invent is not None:
            response['id'] = _invent.id
            response['name'] = _invent.name
        return response

class Hop_Inventory_List(Base):
    __tablename__ = 'inventory_list'

    id = Column(Integer,primary_key=True)
    name = Column(Text,default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'), default=None)
    to_outlet_id = Column(Integer,ForeignKey('outlet.id'), default=None)
    type_id = Column(Integer,ForeignKey('inventory_type.id'),default=None)
    description = Column(Text,default=None)
    owner_id = Column(Integer,ForeignKey('user.id'))
    date = Column(Date,default=datetime.now().date())
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _name(self, type_id, outlet_id):
        name_id = '0000000000001'
        session = Session()
        try:
            _invent = session.query(Hop_Inventory_List).filter_by(type_id=type_id, outlet_id=outlet_id, status=True).order_by(desc(Hop_Inventory_List.id)).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _invent is not None:
            _id = int(_invent.name.split('-')[2])
            name_id_len = len(str(int(_id) + 1))
            name_id = ''
            for i in range(13 - name_id_len):
                name_id += '0'
            name_id += str(int(_id) + 1)
        name = 'SM-'
        if type_id == 3:
            name = 'SK-'
        elif type_id == 6:
            name = 'TR-'
        elif type_id == 7:
            name = 'SO-'
        name += str(outlet_id) + '-' + name_id
        return name

    def _insert_sm(self, date, outlet_id, description, data_list, owner_id):
        response = {}
        response['status'] = '00'
        session = Session()
        try:
            _invent_list = Hop_Inventory_List()
            _invent_list.name = Hop_Inventory_List()._name(2, outlet_id)
            _invent_list.outlet_id = outlet_id
            _invent_list.type_id = 2
            _invent_list.date = date
            _invent_list.description = description
            _invent_list.owner_id = owner_id
            session.add(_invent_list)
            session.commit()
            response['id'] = _invent_list.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in data_list:
            pid = i[0]
            vid = None
            _item = Hop_Product_Item()._basic_data(_id=pid, owner_id=owner_id)
            cid = _item['cat_id']
            if _item['variant_type'] == True:
                vid = i[2]
            _cost = Hop_Cost()._insert(pid=pid, vid=vid, outlet_id=outlet_id, value=i[4])
            _invent = Hop_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, outlet_id=outlet_id, owner_id=owner_id, sm=i[3])
            _log_invent = Hop_Log_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], inventory_id=_invent, outlet_id=outlet_id, owner_id=owner_id, type_id=2, cost_id=_cost['id'], quantity=i[3])
        return response

    def _insert_se(self, date, outlet_id, description, data_list, owner_id):
        response = {}
        response['status'] = '00'
        session = Session()
        try:
            _invent_list = Hop_Inventory_List()
            _invent_list.name = Hop_Inventory_List()._name(3, outlet_id)
            _invent_list.outlet_id = outlet_id
            _invent_list.type_id = 3
            _invent_list.date = date
            _invent_list.description = description
            _invent_list.owner_id = owner_id
            session.add(_invent_list)
            session.commit()
            response['id'] = _invent_list.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in data_list:
            print(i)
            pid = i[0]
            vid = None
            _item = Hop_Product_Item()._basic_data(_id=pid, owner_id=owner_id)
            cid = _item['cat_id']
            if _item['variant_type'] == True:
                vid = i[2]
            _invent = Hop_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, outlet_id=outlet_id, owner_id=owner_id, sk=-1 * int(i[3]))
            _log_invent = Hop_Log_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], inventory_id=_invent, outlet_id=outlet_id, owner_id=owner_id, type_id=3, cost_id=None, quantity=-1 * int(i[3]))
        return response

    def _insert_ts(self, date, from_outlet_id, to_outlet_id, description, data_list, owner_id):
        response = {}
        response['status'] = '00'
        session = Session()
        try:
            _invent_list = Hop_Inventory_List()
            _invent_list.name = Hop_Inventory_List()._name(6, from_outlet_id)
            _invent_list.outlet_id = from_outlet_id
            _invent_list.to_outlet_id = to_outlet_id
            _invent_list.type_id = 6
            _invent_list.date = date
            _invent_list.description = description
            _invent_list.owner_id = owner_id
            session.add(_invent_list)
            session.commit()
            response['id'] = _invent_list.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in data_list:
            print(i)
            pid = i[0]
            vid = None
            _item = Hop_Product_Item()._basic_data(_id=pid, owner_id=owner_id)
            cid = _item['cat_id']
            if _item['variant_type'] == True:
                vid = i[2]
            _invent = Hop_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, outlet_id=from_outlet_id, owner_id=owner_id, tr=-1 * int(i[3]))
            _log_invent = Hop_Log_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], inventory_id=_invent, outlet_id=from_outlet_id, owner_id=owner_id, type_id=6, cost_id=None, quantity=-1 * int(i[3]))
            _to_invent = Hop_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, outlet_id=to_outlet_id, owner_id=owner_id, tr=int(i[3]))
            _to_log_invent = Hop_Log_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], inventory_id=_invent, outlet_id=to_outlet_id, owner_id=owner_id, type_id=6, cost_id=None, quantity=int(i[3]))
        return response

    def _insert_so(self, date, outlet_id, description, data_list, owner_id):
        response = {}
        response['status'] = '00'
        session = Session()
        try:
            _invent_list = Hop_Inventory_List()
            _invent_list.name = Hop_Inventory_List()._name(7, outlet_id)
            _invent_list.outlet_id = outlet_id
            _invent_list.type_id = 7
            _invent_list.date = date
            _invent_list.description = description
            _invent_list.owner_id = owner_id
            session.add(_invent_list)
            session.commit()
            response['id'] = _invent_list.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in data_list:
            pid = i[0]
            vid = None
            _item = Hop_Product_Item()._basic_data(_id=pid, owner_id=owner_id)
            cid = _item['cat_id']
            if _item['variant_type'] == True:
                vid = i[2]
            _invent = Hop_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, outlet_id=outlet_id, owner_id=owner_id, ad=int(i[4]))
            _log_invent = None
            if int(i[4]) != 0:
                _log_invent = Hop_Log_Inventory()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], inventory_id=_invent, outlet_id=outlet_id, owner_id=owner_id, type_id=7, cost_id=None, quantity=int(i[4]))
            _invent_adj = Hop_Inventory_Adj()._insert(pid=pid, vid=vid, cid=cid, date=date, inventory_list_id=response['id'], log_id=_log_invent, inventory_id=_invent, outlet_id=outlet_id, owner_id=owner_id, quantity_system=int(i[3]), quantity_deviation=int(i[4]))
        return response

    def _list(self, type_id, from_date, to_date, outlet_id, owner_id):
        response = {}
        response['status'] = '50'
        response['list'] = []
        session = Session()
        _invent_list = []
        try:
            if int(outlet_id) == 0:
                _invent_list = session.query(Hop_Inventory_List).filter_by(type_id=type_id, owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _invent_list:
            _data = {
                'id': i.id,
                'name': i.name,
                'outlet': Hop_Outlet()._basic_data(i.outlet_id),
                'type': Hop_Inventory_Type()._data(i.type_id),
                'date': str(i.date),
            }
            if i.type_id == 6:
                _data['to_outlet'] = Hop_Outlet()._basic_data(i.to_outlet_id)
            response['list'].append(_data)

        if len(response['list']) > 0:
            response['status'] = '00'
        return response

    def _data(self, type_id, stock_id, outlet_id, owner_id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _invent = session.query(Hop_Inventory_List).filter_by(id=stock_id, type_id=type_id, outlet_id=outlet_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _invent is not None:
            response['status'] = '00'
            response['id'] =  _invent.id
            response['name'] =  _invent.name
            response['outlet'] =  Hop_Outlet()._basic_data(_invent.outlet_id)
            if _invent.type_id == 6:
                response['to_outlet'] = Hop_Outlet()._basic_data(_invent.to_outlet_id)
            response['type'] =  Hop_Inventory_Type()._data(_invent.type_id)
            response['date'] =  str(_invent.date)
            if type_id !=  7:
                response['list'] = Hop_Log_Inventory()._list_by_sli(_invent.id, _invent.outlet_id, owner_id)
            else:
                response['list'] = Hop_Inventory_Adj()._list_by_sli(_invent.id, _invent.outlet_id, owner_id)
        return response

class Hop_Log_Inventory(Base):

    __tablename__ = 'log_inventory'

    id = Column(Integer,primary_key=True)
    pid = Column(Integer,ForeignKey('product_item.id'),default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'),default=None)
    cid = Column(Integer,ForeignKey('product_category.id'),default=None)
    inventory_list_id = Column(Integer,ForeignKey('inventory_list.id'),default=None)
    inventory_id = Column(Integer,ForeignKey('inventory.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    owner_id = Column(Integer,ForeignKey('user.id'),default=None)
    type_id = Column(Integer,ForeignKey('inventory_type.id'),default=None)
    cost_id = Column(Integer,ForeignKey('cost.id'),default=None)
    quantity = Column(DECIMAL(36,2), default=0)
    date = Column(Date,default=None)
    expire = Column(Date,default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, pid, vid, cid, date, inventory_list_id, inventory_id, outlet_id, owner_id, type_id, cost_id, quantity):
        response = None
        session = Session()
        try:
            _log = Hop_Log_Inventory()
            _log.pid = pid
            _log.vid = vid
            _log.cid = cid
            _log.date = date
            _log.owner_id = owner_id
            _log.inventory_list_id = inventory_list_id
            _log.inventory_id = inventory_id
            _log.outlet_id = outlet_id
            _log.type_id = type_id
            _log.cost_id = cost_id
            _log.quantity = quantity
            session.add(_log)
            session.commit()
            response = _log.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _list_by_sli(self, inventory_list_id, outlet_id, owner_id):
        response = []
        session = Session()
        try:
            _invent_list = session.query(Hop_Log_Inventory).filter_by(inventory_list_id=inventory_list_id, outlet_id=outlet_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _invent_list:
            response.append({
                'pid': Hop_Product_Item()._basic_data(i.pid, owner_id),
                'vid': Hop_Variant_List()._data_no_status(i.pid, i.vid),
                'quantity': int(i.quantity),
                'cost': Hop_Cost()._data(i.cost_id)
            })
        return response

class Hop_Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer,primary_key=True)
    pid = Column(Integer,ForeignKey('product_item.id'),default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'),default=None)
    cid = Column(Integer,ForeignKey('product_category.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    owner_id = Column(Integer,ForeignKey('user.id'),default=None)
    sa = Column(Numeric(36,2),default=0)
    sm = Column(Numeric(36,2),default=0)
    sk = Column(Numeric(36,2),default=0)
    sp = Column(Numeric(36,2),default=0)
    pi = Column(Numeric(36,2),default=0)
    tr = Column(Numeric(36,2),default=0)
    ad = Column(Numeric(36,2),default=0)
    fs = Column(Numeric(36,2),default=0)
    date = Column(Date,default=datetime.now().date())
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, pid=None, vid=None, cid=None, date=None, outlet_id=None, owner_id=None, sm=0 ,sk=0 ,tr=0 ,ad=0):
        response = None
        _exist_fs = 0
        session = Session()
        try:
            if session.query(Hop_Inventory).filter(Hop_Inventory.date >= datetime.now().date(), Hop_Inventory.date <= datetime.now().date()+timedelta(days=1)).filter_by(pid=pid, vid=vid, outlet_id=outlet_id).first() is None:
                for i in session.query(Hop_Inventory).filter(Hop_Inventory.date < datetime.now().date()).filter_by(pid=pid, vid=vid, outlet_id=outlet_id).order_by(desc(Hop_Inventory.id)).limit(1).all():
                    _exist_fs = i.fs
                _invent = Hop_Inventory()
                _invent.owner_id = owner_id
                _invent.pid = pid
                _invent.vid = vid
                _invent.cid = cid
                _invent.date=date
                _invent.outlet_id = outlet_id
                # STOCK CARD
                _invent.sa = _exist_fs
                _invent.sm = sm
                _invent.sk = sk
                _invent.sp = 0
                _invent.pi = 0
                _invent.tr = tr
                _invent.ad = ad
                _invent.fs = _invent.sa + _invent.sm + _invent.sk + _invent.sp + _invent.pi + _invent.tr + _invent.ad
                session.add(_invent)
                session.commit()

            else:
                _invent = session.query(Hop_Inventory).filter(Hop_Inventory.date >= datetime.now().date(), Hop_Inventory.date <= datetime.now().date()+timedelta(days=1)).filter_by(pid=pid, vid=vid, outlet_id=outlet_id).first()
                _invent.sm = _invent.sm + sm
                _invent.sk = _invent.sk + sk
                _invent.tr = _invent.tr + tr
                _invent.ad = _invent.ad + ad
                _invent.fs = _invent.sa + _invent.sm + _invent.sk + _invent.sp + _invent.pi + _invent.tr + _invent.ad
                session.add(_invent)
                session.commit()
            response = _invent.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _list(self, from_date, to_date, outlet_id, owner_id):
        _from_date = from_date.split('-')
        _to_date = to_date.split('-')
        _from = datetime(year=int(_from_date[0]),month=int(_from_date[1]),day=int(_from_date[2]))
        _to = datetime(year=int(_to_date[0]),month=int(_to_date[1]),day=int(_to_date[2]))
        response = {}
        response['status'] = '50'
        response['list'] = []
        session = Session()
        try:
            _item = session.query(Hop_Product_Item).filter_by(owner_id=owner_id, composed_type=False, status=True).all()
            for i in _item:
                if i.variant_type == False:
                    _invent_count = session.query(Hop_Inventory).filter_by(pid=i.id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).count()
                    if outlet_id != '0':
                        _invent_count = session.query(Hop_Inventory).filter_by(pid=i.id, outlet_id=outlet_id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).count()
                    if _invent_count > 0:
                        _invent_list = session.query(Hop_Inventory).filter(Hop_Inventory.date >= _from, Hop_Inventory.date <= _to).filter_by(pid=i.id, vid=None, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).all()
                        if outlet_id != '0':
                            _invent_list = session.query(Hop_Inventory).filter(Hop_Inventory.date >= _from, Hop_Inventory.date <= _to).filter_by(pid=i.id, vid=None, outlet_id=outlet_id, owner_id=owner_id, status=True).all()
                        _append_detail = {}
                        _append_detail['pid'] = Hop_Product_Item()._basic_data(i.id, owner_id=owner_id)
                        _append_detail['vid'] = None
                        _append_detail['sa'] = 0
                        _invent_before = session.query(Hop_Inventory).filter(Hop_Inventory.date < _from).filter_by(pid=i.id, vid=None, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).limit(1).all()
                        if outlet_id != '0':
                            _invent_before = session.query(Hop_Inventory).filter(Hop_Inventory.date < _from).filter_by(pid=i.id, vid=None, outlet_id=outlet_id, owner_id=owner_id, status=True).order_by(desc(Hop_Inventory.id)).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).limit(1).all()
                        for x in _invent_before:
                            _append_detail['sa'] = int(x.fs)
                        _append_detail['sm'] = 0
                        _append_detail['sk'] = 0
                        _append_detail['sp'] = 0
                        _append_detail['pi'] = 0
                        _append_detail['tr'] = 0
                        _append_detail['ad'] = 0
                        _append_detail['fs'] = 0
                        for x in _invent_list:
                            _append_detail['sm'] += int(x.sm)
                            _append_detail['sk'] += int(x.sk)
                            _append_detail['sp'] += int(x.sp)
                            _append_detail['pi'] += int(x.pi)
                            _append_detail['tr'] += int(x.tr)
                            _append_detail['ad'] += int(x.ad)
                        _append_detail['fs'] = _append_detail['sa'] + _append_detail['sm'] + _append_detail['sk'] + _append_detail['sp'] + _append_detail['pi'] + _append_detail['tr'] + _append_detail['ad'] + _append_detail['fs']
                        response['list'].append(_append_detail)
                else:
                    _variant = session.query(Hop_Variant_List).filter_by(product_item_id=i.id, status=True).all()
                    for v in _variant:
                        _invent_count = session.query(Hop_Inventory).filter_by(pid=i.id, vid=v.id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).count()
                        if outlet_id != '0':
                            _invent_count = session.query(Hop_Inventory).filter_by(pid=i.id, vid=v.id, outlet_id=outlet_id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).count()
                        if _invent_count > 0:
                            _invent_list = session.query(Hop_Inventory).filter(Hop_Inventory.date >= _from, Hop_Inventory.date <= _to).filter_by(pid=i.id, vid=v.id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).all()
                            if outlet_id != '0':
                                _invent_list = session.query(Hop_Inventory).filter(Hop_Inventory.date >= _from, Hop_Inventory.date <= _to).filter_by(pid=i.id, vid=v.id, outlet_id=outlet_id, owner_id=owner_id, status=True).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).all()
                            _append_detail = {}
                            _append_detail['pid'] = Hop_Product_Item()._basic_data(i.id, owner_id=owner_id)
                            _append_detail['vid'] = Hop_Variant_List()._data(i.id, v.id)
                            _append_detail['sa'] = 0
                            _invent_before = session.query(Hop_Inventory).filter(Hop_Inventory.date < _from).filter_by(pid=i.id, vid=v.id, owner_id=owner_id, status=True).order_by(desc(Hop_Inventory.id)).order_by(asc(Hop_Inventory.date)).order_by(desc(Hop_Inventory.id)).limit(1).all()
                            for x in _invent_before:
                                _append_detail['sa'] = int(x.fs)
                            _append_detail['sm'] = 0
                            _append_detail['sk'] = 0
                            _append_detail['sp'] = 0
                            _append_detail['pi'] = 0
                            _append_detail['tr'] = 0
                            _append_detail['ad'] = 0
                            _append_detail['fs'] = 0
                            for x in _invent_list:
                                _append_detail['sm'] += int(x.sm)
                                _append_detail['sk'] += int(x.sk)
                                _append_detail['sp'] += int(x.sp)
                                _append_detail['pi'] += int(x.pi)
                                _append_detail['tr'] += int(x.tr)
                                _append_detail['ad'] += int(x.ad)
                            _append_detail['fs'] = _append_detail['sa'] + _append_detail['sm'] + _append_detail['sk'] + _append_detail['sp'] + _append_detail['pi'] + _append_detail['tr'] + _append_detail['ad'] + _append_detail['fs']
                            response['list'].append(_append_detail)
            if len(response['list']) > 0:
                response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Inventory_Adj(Base):

    __tablename__ = 'inventory_adjusment'

    id = Column(Integer,primary_key=True)
    pid = Column(Integer,ForeignKey('product_item.id'),default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'),default=None)
    cid = Column(Integer,ForeignKey('product_category.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    owner_id = Column(Integer,ForeignKey('user.id'),default=None)
    quantity_system = Column(Numeric(36,2), default=0)
    quantity_deviation = Column(Numeric(36,2), default=0)
    inventory_list_id = Column(Integer,ForeignKey('inventory_list.id'),default=None)
    log_id = Column(Integer,ForeignKey('log_inventory.id'),default=None)
    inventory_id = Column(Integer,ForeignKey('inventory.id'),default=None)
    date = Column(Date,default=datetime.now().date())
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self,
        pid, vid, cid, outlet_id, date, quantity_system,
        quantity_deviation, inventory_list_id, log_id, inventory_id, owner_id
    ):
        response = None
        session = Session()
        try:
            _invent = Hop_Inventory_Adj()
            _invent.pid = pid
            _invent.vid = vid
            _invent.cid = cid
            _invent.outlet_id = outlet_id
            _invent.owner_id = owner_id
            _invent.quantity_system = quantity_system
            _invent.quantity_deviation = quantity_deviation
            _invent.inventory_id = inventory_id
            _invent.inventory_list_id = inventory_list_id
            _invent.log_id = log_id
            _invent.date = date
            session.add(_invent)
            session.commit()
            response = _invent.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _list_by_sli(self, _list_id, outlet_id, owner_id):
        response = []
        session = Session()
        try:
            _invent_list = session.query(Hop_Inventory_Adj).filter_by(inventory_list_id=_list_id, outlet_id=outlet_id, owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _invent_list:
            _append_detail = {}
            _append_detail['pid'] = Hop_Product_Item()._basic_data(i.pid, owner_id=owner_id)
            _append_detail['vid'] = Hop_Variant_List()._data(i.pid, i.vid) if i.vid is not None else None
            _append_detail['outlet'] = Hop_Outlet()._basic_data(i.outlet_id)
            _append_detail['date'] = i.date
            _append_detail['quantity_system'] = int(i.quantity_system)
            _append_detail['quantity_deviation'] = int(i.quantity_deviation)
            response.append(_append_detail)
        return response

class Hop_Cost(Base):
    __tablename__ = 'cost'
    id = Column(Integer,primary_key=True)
    pid = Column(Integer,ForeignKey('product_item.id'),default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'), default=None)
    value = Column(Numeric(36,2),default=0)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, pid, vid, outlet_id, value):
        response = None
        session = Session()
        try:
            _cost = Hop_Cost()
            _cost.pid = pid
            _cost.vid = vid
            _cost.outlet_id = outlet_id
            _cost.value = value
            session.add(_cost)
            session.commit()
            response = _cost.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return Hop_Cost()._data(response)

    def _data(self, id):
        response = {}
        session = Session()
        try:
            _cost = session.query(Hop_Cost).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _cost is not None:
            response['id'] = _cost.id
            response['pid'] = _cost.pid
            response['vid'] = _cost.vid
            response['outlet_id'] = _cost.outlet_id
            response['value'] = int(_cost.value)
        return response

# CLASS FOR TAXES

class Hop_Tax(Base):
    __tablename__ = 'tax'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    owner_id = Column(Integer,ForeignKey('user.id'))
    tax_type_id = Column(Integer,ForeignKey('tax_type.id'))
    value = Column(Numeric(3,1))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self, owner_id):
        response = []
        session = Session()
        try:
            _tax = session.query(Hop_Tax).filter_by(owner_id=owner_id, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _tax:
            response.append(Hop_Tax()._data(i.id, owner_id))
        return response

    def _insert(self, name, tax_type_id, value, outlet_list, owner_id):
        response = {}
        session = Session()
        try:
            _tax = Hop_Tax()
            _tax.name = name
            _tax.tax_type_id = tax_type_id
            _tax.value = value
            _tax.owner_id = owner_id
            session.add(_tax)
            session.commit()
            response['id'] = _tax.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        Hop_Outlet_Tax()._remove_all(tax_id=response['id'])
        for i in outlet_list:
            Hop_Outlet_Tax()._insert(outlet_id = i, tax_id=response['id'])
        return Hop_Tax()._data(response['id'], owner_id)

    def _update(self, _id, name, tax_type_id, value, outlet_list, owner_id):
        response = {}
        session = Session()
        try:
            _tax = session.query(Hop_Tax).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _tax is not None:
                _tax.name = name
                _tax.tax_type_id = tax_type_id
                _tax.value = value
                session.add(_tax)
            session.commit()
            response['id'] = _tax.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        Hop_Outlet_Tax()._remove_all(tax_id=response['id'])
        for i in outlet_list:
            Hop_Outlet_Tax()._insert(outlet_id = i, tax_id=response['id'])
        return Hop_Tax()._data(response['id'], owner_id)

    def _data(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _tax = session.query(Hop_Tax).filter_by(id=_id, owner_id=owner_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _tax is not None:
            response['id'] = _tax.id
            response['name'] = _tax.name
            response['tax_type'] = Hop_Tax_Type()._data(_tax.tax_type_id)
            response['value'] = str(_tax.value)
            response['outlet_list'] = Hop_Outlet_Tax()._list_outlet(_tax.id)
        return response

    def _remove(self, _id, owner_id):
        response = {}
        response_id = None
        session = Session()
        try:
            _tax = session.query(Hop_Tax).filter_by(id=_id, owner_id=owner_id, status=True).first()
            if _tax is not None:
                response_id = _tax.id
                _tax.status = False
                session.add(_tax)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if response_id is not None:
            Hop_Outlet_Tax()._remove_all(tax_id=response_id)
            response['status'] = '00'
        return response

    def _remove_many(self, tax_list, owner_id):
        response = []
        for i in tax_list:
            response.append(Hop_Tax()._remove(_id=i, owner_id=owner_id))
        return response

class Hop_Tax_Type(Base):
    __tablename__ = 'tax_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self):
        response = []
        session = Session()
        try:
            _tax = session.query(Hop_Tax_Type).filter_by(status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _tax:
            response.append(Hop_Tax_Type()._data(i.id))
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _tax_type = session.query(Hop_Tax_Type).filter_by(id=_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _tax_type is not None:
            response['id'] = _tax_type.id
            response['name'] = _tax_type.name
        return response

class Hop_Outlet_Tax(Base):
    __tablename__ = 'outlet_tax'

    id = Column(Integer,primary_key=True)
    tax_id = Column(Integer,ForeignKey('tax.id'))
    outlet_id = Column(Integer,ForeignKey('outlet.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, outlet_id, tax_id):
        session = Session()
        try:
            _exist_tax = session.query(Hop_Outlet_Tax).filter_by(outlet_id=outlet_id, tax_id=tax_id).first()
            if _exist_tax is None:
                _tax = Hop_Outlet_Tax()
                _tax.outlet_id = outlet_id
                _tax.tax_id = tax_id
                session.add(_tax)
                print(_tax.id)
            else:
                _exist_tax.status = True
                session.add(_exist_tax)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_all(self, tax_id):
        session = Session()
        try:
            _tax = session.query(Hop_Outlet_Tax).filter_by(tax_id=tax_id).all()
            for i in _tax:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _list_outlet(self, tax_id):
        response = []
        session = Session()
        try:
            _tax = session.query(Hop_Outlet_Tax).filter_by(tax_id=tax_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _tax:
            response.append(Hop_Outlet()._basic_data(i.outlet_id))
        return response

    def _remove(self, outlet_id):
        session = Session()
        try:
            _old_outlet_tax = session.query(Hop_Outlet_Tax).filter_by(outlet_id=outlet_id, status=True).all()
            for i in _old_outlet_tax:
                i.status=False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def _list(self, outlet_id):
        response = []
        session = Session()
        try:
            _outlet_tax = session.query(Hop_Outlet_Tax).filter_by(outlet_id=outlet_id, status=True).all()
            for i in _outlet_tax:
                response.append(i.tax_id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _sumtax(self, _outletid):
        response = 0
        session = Session()
        try:
            _outlet_tax = session.query(Hop_Outlet_Tax).filter_by(outlet_id = _outletid, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _outlet_tax:
            _tax = Hop_Tax()._data(i.tax_id)
            response = response + _tax['value']
        return str(response)

# CLASS FOR PAYMENT

class Hop_Payment_Type(Base):
    __tablename__ = 'payment_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Payment_Name(Base):
    __tablename__ = 'payment_name'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    type_id = Column(Integer,ForeignKey('payment_type.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Payment_Detail(Base):
    __tablename__ = 'payment_detail'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    payment_name_id = Column(Integer,ForeignKey('payment_name.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _payment_detail = session.query(payment_detail).filter_by(id = _id).filter_by(status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _payment_detail is not None:
            response['id'] = _payment_detail.id
            response['name'] = _payment_detail.name
            response['payment_name_id'] = _payment_detail.payment_name_id
        return response

    def _listbypayment(self, _paymentid):
        response = []
        session = Session()
        try:
            _payment_detail = session.query(payment_detail).filter_by(payment_name_id = _paymentid, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _payment_detail:
            response.append({
                'id' : i.id ,
                'name' : i.name
            })
        return response

# CLASS FOR PROMO
class Hop_Special_Promo(Base):
    __tablename__ = 'special_promo'

    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    percent = Column(Boolean,default=True)
    value = Column(Numeric(65,1))
    description = Column(String(200))
    promo_date_status = Column(Boolean,default=False)
    startdate = Column(DateTime, default=None)
    enddate = Column(DateTime, default=None)
    apply_time_status = Column(Boolean,default=False)
    starttime = Column(Time, default=None)
    endtime = Column(Time, default=None)
    senin = Column(Boolean,default=False)
    selasa = Column(Boolean,default=False)
    rabu = Column(Boolean,default=False)
    kamis = Column(Boolean,default=False)
    jumat = Column(Boolean,default=False)
    sabtu = Column(Boolean,default=False)
    minggu = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey('user.id'), default=None)
    activate = Column(DateTime,default=True)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _count(self, owner_id):
        response = 0
        session = Session()
        try:
            response = session.query(Hop_Special_Promo).filter_by(owner_id=owner_id, status=True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _insert(
        self, name, percent, value, promo_date_status, startdate, enddate,
        starttime, endtime, apply_time_status, applied_day, outlet_list, owner_id):
        response = {}
        response_id = None
        if len(name.strip()) > 0 and len(value.strip()) >0:
            if int(percent) == 0 and int(value) > 100:
                response['status'] = '50'
                response['message'] = 'Value of the promo has to be less than 100%'
                return response
            session = Session()
            try:
                    promo = Hop_Special_Promo()
                    promo.name = name
                    promo.percent = True if int(percent) == 0 else False
                    promo.value = value
                    promo.promo_date_status = False
                    if promo_date_status == True:
                        promo.promo_date_status = True
                        promo.startdate = startdate
                        promo.enddate = enddate
                    promo.apply_time_status = False
                    if apply_time_status == True:
                        promo.apply_time_status = True
                        promo.starttime = starttime
                        promo.endtime = endtime
                    for i in applied_day:
                        if i == 'sunday':
                            promo.minggu = True
                        elif i == 'monday':
                            promo.senin = True
                        elif i == 'tuesday':
                            promo.selasa = True
                        elif i == 'wednesday':
                            promo.rabu = True
                        elif i == 'thursday':
                            promo.kamis = True
                        elif i == 'friday':
                            promo.jumat = True
                        elif i == 'saturday':
                            promo.sabtu = True
                    promo.owner_id = owner_id
                    session.add(promo)
                    session.commit()
                    response_id = promo.id
                    response['status'] = '00'
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            response['status'] = '50'
            response['message'] = 'Please fill all required fields'
        if response_id is not None:
            Hop_Promo_Outlet()._remove_all(promo_id=response_id, type_promo=2)
            for i in outlet_list:
                Hop_Promo_Outlet()._insert(outlet_id = i, promo_id=response_id, type_promo=2)
            response.update(Hop_Special_Promo()._basic_data(response_id, owner_id))
        return response

    def _update(
        self, id, name, percent, value, promo_date_status, startdate, enddate,
        starttime, endtime, apply_time_status, applied_day, outlet_list, owner_id):
        response = {}
        response_id = None
        if len(name.strip()) > 0 and len(value.strip()) >0:
            if int(percent) == 0 and float(value) > 100:
                response['status'] = '50'
                response['message'] = 'Value of the promo has to be less than 100%'
                return response
            session = Session()
            try:

                promo = session.query(Hop_Special_Promo).filter_by(id=id, owner_id=owner_id, status=True).first()
                promo.name = name
                promo.percent = True if int(percent) == 0 else False
                promo.value = value
                promo.promo_date_status = False
                if promo_date_status == True:
                    promo.promo_date_status = True
                    promo.startdate = startdate
                    promo.enddate = enddate
                promo.apply_time_status = False
                if apply_time_status == True:
                    promo.apply_time_status = True
                    promo.starttime = starttime
                    promo.endtime = endtime
                for i in applied_day:
                    if i == 'sunday':
                        promo.minggu = True
                    elif i == 'monday':
                        promo.senin = True
                    elif i == 'tuesday':
                        promo.selasa = True
                    elif i == 'wednesday':
                        promo.rabu = True
                    elif i == 'thursday':
                        promo.kamis = True
                    elif i == 'friday':
                        promo.jumat = True
                    elif i == 'saturday':
                        promo.sabtu = True
                promo.owner_id = owner_id
                session.add(promo)
                session.commit()
                response_id = promo.id
                response['status'] = '00'
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            response['status'] = '50'
            response['message'] = 'Please fill all required fields'
        if response_id is not None:
            Hop_Promo_Outlet()._remove_all(promo_id=response_id, type_promo=2)
            for i in outlet_list:
                Hop_Promo_Outlet()._insert(outlet_id = i, promo_id=response_id, type_promo=2)
            response.update(Hop_Special_Promo()._basic_data(response_id, owner_id))
        return response

    def _list(self, owner_id):
        response = []
        session = Session()
        try:
            sp = session.query(Hop_Special_Promo).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in sp:
            response.append(Hop_Special_Promo()._basic_data(i.id, owner_id))
        return response

    def _listbyoutlet(self, _outletid):
        response = []
        session = Session()
        try:
            _special_promo = session.query(Hop_Special_Promo).filter_by(outlet_id = _outletid, status = True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _special_promo:
            response.append({
                'id' : i.id,
                'name' : i.name,
                'value' : str(i.value),
                'percent' : i.percent,
                'outlet_id' : i.outlet_id,
                'description' : i.description,
                'startdate' : str(i.startdate),
                'enddate' : str(i.enddate),
                'starttime' : str(i.starttime),
                'endtime' : str(i.endtime),
                'senin' : i.senin,
                'selasa' : i.selasa,
                'rabu' : i.rabu,
                'kamis' : i.kamis,
                'jumat' : i.jumat,
                'sabtu' : i.sabtu,
                'minggu' : i.minggu
            })
        return response

    def _basic_data(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _special_promo = session.query(Hop_Special_Promo).filter_by(id = _id, owner_id=owner_id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _special_promo is not None:
            response['id'] = _special_promo.id
            response['name'] =  _special_promo.name
            response['value'] =  str(_special_promo.value)
            response['percent'] =  _special_promo.percent
            response['description'] =  _special_promo.description
        return response

    def _remove(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _special_promo = session.query(Hop_Special_Promo).filter_by(id = _id, owner_id=owner_id, status = True).first()
            if _special_promo is not None:
                _special_promo.status = False
                session.add(_special_promo)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _remove_many(self, promo_list, owner_id):
        session = Session()
        try:
            for i in promo_list:
                _promo = session.query(Hop_Special_Promo).filter_by(id=i, owner_id=owner_id, status = True).first()
                if _promo is not None:
                    _promo.status = False
                    session.add(_promo)
                    session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _data(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _special_promo = session.query(Hop_Special_Promo).filter_by(id = _id, owner_id=owner_id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _special_promo is not None:
            response['id'] = _special_promo.id
            response['name'] =  _special_promo.name
            response['value'] = str(_special_promo.value)
            response['percent'] =  _special_promo.percent
            response['description'] =  _special_promo.description
            response['promo_date_status'] = _special_promo.promo_date_status
            response['startdate'] =  str(_special_promo.startdate)
            response['enddate'] =  str(_special_promo.enddate)
            response['apply_time_status'] = _special_promo.apply_time_status
            response['starttime'] =  str(_special_promo.starttime)
            response['endtime'] =  str(_special_promo.endtime)
            response['monday'] =  _special_promo.senin
            response['tuesday'] =  _special_promo.selasa
            response['wednesday'] =  _special_promo.rabu
            response['thursday'] =  _special_promo.kamis
            response['friday'] =  _special_promo.jumat
            response['saturday'] =  _special_promo.sabtu
            response['sunday'] =  _special_promo.minggu
            response['outlet_list'] = Hop_Promo_Outlet()._list_outlet(_special_promo.id, 2)
        return response

class Hop_Ap_Detail(Base):
    __tablename__ = 'ap_detail'

    id = Column(Integer,primary_key=True)
    owner_id = Column(Integer,ForeignKey('user.id'),default=None)
    name = Column(String(200))
    requirement_value = Column(Numeric(65,1))
    requirement_relation = Column(Integer)
    ap_requirement_id = Column(Integer,ForeignKey('ap_requirement.id'))
    reward_value = Column(Numeric(65,1))
    reward_relation = Column(Integer)
    ap_reward_id = Column(Integer,ForeignKey('ap_reward.id'))
    ap_type_id = Column(Integer,ForeignKey('ap_type.id'))
    multiple = Column(Boolean, default=False)
    promo_date_status = Column(Boolean, default=False)
    startdate = Column(DateTime, default=None)
    enddate = Column(DateTime, default=None)
    apply_time_status = Column(Boolean, default=False)
    starttime = Column(Time, default=None)
    endtime = Column(Time, default=None)
    senin = Column(Boolean,default=False)
    selasa = Column(Boolean,default=False)
    rabu = Column(Boolean,default=False)
    kamis = Column(Boolean,default=False)
    jumat = Column(Boolean,default=False)
    sabtu = Column(Boolean,default=False)
    minggu = Column(Boolean,default=False)
    activate = Column(DateTime,default=True)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)


    def _list(self, owner_id):
        response = []
        session = Session()
        try:
            sp = session.query(Hop_Ap_Detail).filter_by(owner_id=owner_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in sp:
            response.append(Hop_Ap_Detail()._basic_data(i.id, owner_id))
        return response

    def _basic_data(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _promo = session.query(Hop_Ap_Detail).filter_by(id = _id, owner_id=owner_id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _promo is not None:
            response['id'] = _promo.id
            response['name'] =  _promo.name
            response['promo_date'] =  '-'
            if _promo.promo_date_status == True:
                response['promo_date'] =  str(_promo.startdate) + ' to ' + str(_promo.enddate)
            response['applied_day'] = []
            if _promo.senin == True:
                response['applied_day'].append('Monday')
            if _promo.selasa == True:
                response['applied_day'].append('Tuesday')
            if _promo.rabu == True:
                response['applied_day'].append('Wednesday')
            if _promo.kamis == True:
                response['applied_day'].append('Thursday')
            if _promo.jumat == True:
                response['applied_day'].append('Friday')
            if _promo.sabtu == True:
                response['applied_day'].append('Saturday')
            if _promo.minggu == True:
                response['applied_day'].append('Sunday')
            response['applied_time'] =  '-'
            if _promo.apply_time_status == True:
                response['applied_time'] =  str(_promo.starttime) + ' to ' + str(_promo.endtime)
        return response

    def _remove(self, _id, owner_id):
        response = {}
        session = Session()
        try:
            _promo = session.query(Hop_Ap_Detail).filter_by(id = _id, owner_id=owner_id, status = True).first()
            if _promo is not None:
                _promo.status=False
                session.add(_promo)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _remove_many(self, promo_list, owner_id):
        response = {}
        session = Session()
        try:
            for i in promo_list:
                _promo = session.query(Hop_Ap_Detail).filter_by(id=i, owner_id=owner_id, status = True).first()
                if _promo is not None:
                    _promo.status = False
                    session.add(_promo)
                    session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _name(self, ap_type_id, ap_requirement_id, requirement_value,
        requirement_relation, ap_reward_id, reward_value, reward_relation, owner_id):
        response = Hop_Ap_Type()._data(ap_type_id)['description']
        _x = 'Rp ' + requirement_value
        if int(ap_requirement_id) == 1:
            _item = Hop_Product_Item()._basic_data(requirement_relation, owner_id)['name']
            _x = str(int(float(requirement_value))) + ' ' + _item
        elif int(ap_requirement_id) == 2:
            print(Hop_Product_Category()._basicdata(requirement_relation, owner_id))
            _category = Hop_Product_Category()._basicdata(requirement_relation, owner_id)['name']
            _x = str(int(float(requirement_value))) + ' ' + _category
        _y = 'Rp ' + reward_value
        if int(ap_reward_id) == 1:
            _item = Hop_Product_Item()._basic_data(reward_relation, owner_id)['name']
            _y = str(int(float(reward_value))) + ' ' + _item
        elif int(ap_reward_id) == 2:
            _category = Hop_Product_Category()._basicdata(reward_relation, owner_id)['name']
            _y = str(int(float(reward_value))) + ' ' + _category
        elif int(ap_reward_id) == 4:
            _y = str(reward_value) + '%'
        response = response.replace('_x', _x).replace('_y', _y)
        return response

    def _insert(self, ap_type_id, ap_requirement_id, requirement_value,
        requirement_relation, ap_reward_id, reward_value, reward_relation,
        multiple, promo_date_status, startdate, enddate, starttime, endtime,
        apply_time_status, applied_day, outlet_list, owner_id):
        response = {}
        response_id = None
        session = Session()
        try:
            if len(ap_type_id) > 0 and ap_requirement_id!= '' \
            and requirement_value!= '' and ap_reward_id!= '' \
            and reward_value!= '':
                promo = Hop_Ap_Detail()
                promo.name = Hop_Ap_Detail()._name(ap_type_id, ap_requirement_id, requirement_value,
                    requirement_relation, ap_reward_id, reward_value, reward_relation, owner_id)
                promo.ap_type_id = ap_type_id
                promo.ap_requirement_id = ap_requirement_id
                promo.requirement_value = float(requirement_value)
                promo.requirement_relation = requirement_relation if requirement_relation != 'None' else None
                promo.ap_reward_id = ap_reward_id
                promo.reward_value = float(reward_value)
                promo.reward_relation = reward_relation if reward_relation != 'None' else None
                promo.multiple = False
                if multiple == True:
                    promo.multiple = True
                promo.promo_date_status = False
                if promo_date_status == True:
                    promo.promo_date_status = True
                    promo.startdate = startdate
                    promo.enddate = enddate
                promo.apply_time_status = False
                if apply_time_status == True:
                    promo.apply_time_status = True
                    promo.starttime = starttime
                    promo.endtime = endtime
                for i in applied_day:
                    if i == 'sunday':
                        promo.minggu = True
                    elif i == 'monday':
                        promo.senin = True
                    elif i == 'tuesday':
                        promo.selasa = True
                    elif i == 'wednesday':
                        promo.rabu = True
                    elif i == 'thursday':
                        promo.kamis = True
                    elif i == 'friday':
                        promo.jumat = True
                    elif i == 'saturday':
                        promo.sabtu = True
                promo.owner_id = owner_id
                session.add(promo)
                session.commit()
                response_id = promo.id
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'Please fill all required fields'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if response_id is not None:
            Hop_Promo_Outlet()._remove_all(promo_id=response_id, type_promo=1)
            for i in outlet_list:
                Hop_Promo_Outlet()._insert(outlet_id = i, promo_id=response_id, type_promo=1)
            response.update(Hop_Ap_Detail()._basic_data(response_id, owner_id))
        return response

    def _update(self, promo_id, ap_type_id, ap_requirement_id, requirement_value,
        requirement_relation, ap_reward_id, reward_value, reward_relation,
        multiple, promo_date_status, startdate, enddate, starttime, endtime,
        apply_time_status, applied_day, outlet_list, owner_id):
        response = {}
        response_id = None
        session = Session()
        print(requirement_relation)
        try:
            if len(ap_type_id) > 0 and ap_requirement_id!= '' \
            and requirement_value!= '' and ap_reward_id!= '' \
            and reward_value!= '':
                promo = session.query(Hop_Ap_Detail).filter_by(id=promo_id, owner_id=owner_id, status=True).first()
                if promo is not None:
                    promo.name = Hop_Ap_Detail()._name(ap_type_id, ap_requirement_id, requirement_value,
                        requirement_relation, ap_reward_id, reward_value, reward_relation, owner_id)
                    promo.ap_type_id = ap_type_id
                    promo.ap_requirement_id = ap_requirement_id
                    promo.requirement_value = float(requirement_value)
                    promo.requirement_relation = requirement_relation if requirement_relation != 'None' else None
                    promo.ap_reward_id = ap_reward_id
                    promo.reward_value = float(reward_value)
                    promo.reward_relation = reward_relation if reward_relation != 'None' else None
                    promo.multiple = False
                    if multiple == True:
                        promo.multiple = True
                    promo.promo_date_status = False
                    if promo_date_status == True:
                        promo.promo_date_status = True
                        promo.startdate = startdate
                        promo.enddate = enddate
                    promo.apply_time_status = False
                    if apply_time_status == True:
                        promo.apply_time_status = True
                        promo.starttime = starttime
                        promo.endtime = endtime
                    for i in applied_day:
                        if i == 'sunday':
                            promo.minggu = True
                        elif i == 'monday':
                            promo.senin = True
                        elif i == 'tuesday':
                            promo.selasa = True
                        elif i == 'wednesday':
                            promo.rabu = True
                        elif i == 'thursday':
                            promo.kamis = True
                        elif i == 'friday':
                            promo.jumat = True
                        elif i == 'saturday':
                            promo.sabtu = True
                    session.add(promo)
                    session.commit()
                response_id = promo.id
                response['status'] = '00'
            else:
                response['status'] = '50'
                response['message'] = 'Please fill all required fields'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if response_id is not None:
            Hop_Promo_Outlet()._remove_all(promo_id=response_id, type_promo=1)
            for i in outlet_list:
                Hop_Promo_Outlet()._insert(outlet_id = i, promo_id=response_id, type_promo=1)
            response.update(Hop_Ap_Detail()._basic_data(response_id, owner_id))
        return response

    def _count(self, owner_id):
        response = 0
        session = Session()
        try:
            response = session.query(Hop_Ap_Detail).filter_by(owner_id=owner_id, status=True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _data(self, promo_id, owner_id):
        response = {}
        session = Session()
        try:
            _ap_detail = session.query(Hop_Ap_Detail).filter_by(id=promo_id, owner_id=owner_id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _ap_detail is not None:
            response['id'] = _ap_detail.id
            response['name'] = _ap_detail.name
            response['requirement_value'] = str(_ap_detail.requirement_value)
            response['requirement_relation'] = _ap_detail.requirement_relation
            response['requirement_id'] = _ap_detail.ap_requirement_id
            response['reward_value'] = str(_ap_detail.reward_value)
            response['reward_relation'] = _ap_detail.reward_relation
            response['reward_id'] = _ap_detail.ap_reward_id
            response['type'] = _ap_detail.ap_type_id
            response['multiple'] = _ap_detail.multiple
            response['promo_date_status'] = _ap_detail.promo_date_status
            response['startdate'] = str(_ap_detail.startdate)
            response['enddate'] = str(_ap_detail.enddate)
            response['apply_time_status'] = _ap_detail.apply_time_status
            response['starttime'] = str(_ap_detail.starttime)
            response['endtime'] = str(_ap_detail.endtime)
            response['monday'] = _ap_detail.senin
            response['tuesday'] = _ap_detail.selasa
            response['wednesday'] = _ap_detail.rabu
            response['thursday'] = _ap_detail.kamis
            response['friday'] = _ap_detail.jumat
            response['saturday'] = _ap_detail.sabtu
            response['sunday'] = _ap_detail.minggu
            response['outlet_list'] = Hop_Promo_Outlet()._list_outlet(_ap_detail.id, 1)
        return response

class Hop_Ap_Type(Base):
    __tablename__ = 'ap_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    description = Column(String(200))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _ap_type = session.query(Hop_Ap_Type).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _ap_type is not None:
            response['id'] = _ap_type.id
            response['name'] = _ap_type.name
            response['description'] = _ap_type.description
        return response

class Hop_Ap_Requirement(Base):
    __tablename__ = 'ap_requirement'

    id = Column(Integer,primary_key=True)
    type = Column(String(100))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _ap_requirement = session.query(Hop_Ap_Requirement).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _ap_requirement is not None:
            response['id'] = _ap_requirement.id
            response['type'] = _ap_requirement.type
        return response

class Hop_Ap_Reward(Base):
    __tablename__ = 'ap_reward'

    id = Column(Integer,primary_key=True)
    type = Column(String(100))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Promo_Outlet(Base):
    __tablename__ = 'promo_outlet'

    id = Column(Integer,primary_key=True)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    promo_id = Column(Integer, default=None)
    # 1. Auto Promo 2. Special Promo
    type_promo = Column(Integer, default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, outlet_id, promo_id, type_promo):
        session = Session()
        try:
            _exist_promo = session.query(Hop_Promo_Outlet).filter_by(outlet_id=outlet_id, promo_id=promo_id, type_promo=type_promo).first()
            if _exist_promo is None:
                promo = Hop_Promo_Outlet()
                promo.outlet_id = outlet_id
                promo.promo_id = promo_id
                promo.type_promo = type_promo
                session.add(promo)
            else:
                _exist_promo.status = True
                session.add(_exist_promo)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_all(self, promo_id, type_promo):
        session = Session()
        try:
            _promo = session.query(Hop_Promo_Outlet).filter_by(promo_id=promo_id, type_promo=type_promo).all()
            for i in _promo:
                i.status = False
                session.add(i)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def _list_outlet(self, promo_id, type_promo):
        response = []
        session = Session()
        try:
            _promo = session.query(Hop_Promo_Outlet).filter_by(promo_id=promo_id, type_promo=type_promo, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _promo:
            response.append(Hop_Outlet()._basic_data(i.outlet_id))
        return response

# CLASS FOR LOCATION

class Hop_Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    phonecode = Column(Integer)
    iso = Column(String(10))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self):
        response = []
        session = Session()
        try:
            _countries = session.query(Hop_Countries).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _countries:
            response.append({
                'id' : i.id,
                'name' : i.name,
                'phonecode' : i.phonecode,
                'iso' : i.iso,
                'added_time' : i.added_time
            })
        return response

    def _data(self, _id):
        response = {}
        session = Session()
        try:
            _countries = session.query(Hop_Countries).filter_by(id = _id).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _countries is not None:
            response['id'] = _countries.id
            response['name'] = _countries.name
            response['phonecode'] = _countries.phonecode
            response['iso'] = _countries.iso
        return response

class Hop_Provinces(Base):
    __tablename__ = 'provinces'

    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    code = Column(String(10))
    countries_id = Column(Integer,ForeignKey('countries.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer,primary_key=True)
    provinces_id = Column(Integer,ForeignKey('provinces.id'))
    latitude = Column(Numeric(10,8))
    longitude = Column(Numeric(11,8))
    name = Column(String(255))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

# CLASS FOR IMAGE

class Hop_Image_Service(Base):
    __tablename__ = 'image_service'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    added_time = Column(DateTime(), default=datetime.now())
    status = Column(Boolean, default=True)

class Hop_Image_Relation(Base):
    __tablename__ = 'image_relation'

    id = Column(Integer,primary_key=True)
    relation_id = Column(Integer)
    image_service_id = Column(Integer,ForeignKey('image_service.id'))
    relation_type_id = Column(Integer,ForeignKey('image_relation_type.id'))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Image_Relation_Type(Base):
    __tablename__ = 'image_relation_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)


# CLASS FOR USER LOG

class Hop_Login_Log(Base):
    __tablename__ = 'login_log'

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'),default=None)
    app_type_id = Column(Integer,ForeignKey('app_type.id'),default=None)
    user_agent = Column(Text,default=None)
    device_id = Column(Text,default=None)
    time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, _userid, _apptype):
        session = Session()
        try:
            _data = session.query(Hop_Login_Log).filter_by(user_id=_userid, app_type_id=_apptype, status=True).all()
            for i in _data:
                i.status = False
                session.add(i)
            session.commit()
            insert = Hop_Login_Log()
            insert.user_id = _userid
            insert.app_type_id = _apptype
            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _data(self, _user_id):
        response = None
        session = Session()
        try:
            _log = session.query(Hop_Login_Log).filter_by(user_id=_user_id, status=True).first()
            if _log is not None:
                response = _log.time
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_App_Type(Base):
    __tablename__ = 'app_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

# CLASS FOR USER BILLING

class Hop_Billing_Package_Type(Base):
    __tablename__ = 'billing_package_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, id):
        response = None
        session = Session()
        try:
            _type = session.query(Hop_Billing_Package_Type).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _type is not None:
            response = {}
            response['id'] = _type.id
            response['name'] = _type.name
        return response

class Hop_Billing_Package_Item(Base):
    __tablename__ = 'billing_package_item'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    type_id = Column(Integer,ForeignKey('billing_package_type.id'),default=None)
    value = Column(Integer,default=None)
    quantity = Column(Integer,default=None)
    description = Column(Text,default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, package_id):
        response = {}
        session = Session()
        try:
            _item = session.query(Hop_Billing_Package_Item).filter_by(id=package_id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _item is not None:
            response['id'] = _item.id
            response['name'] = _item.name
            response['type'] = Hop_Billing_Package_Type()._data(_item.type_id)
            response['value'] = _item.value
            response['quantity'] = _item.quantity
            response['total'] = _item.value * _item.quantity
        return response

    def _list(self, type_id):
        response = []
        session = Session()
        try:
            _item = session.query(Hop_Billing_Package_Item).filter_by(type_id=type_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _item:
            response.append({
                'id': i.id,
                'name': i.name,
                'type': Hop_Billing_Package_Type()._data(i.type_id),
                'value': i.value,
                'quantity': i.quantity,
                'total': int(i.value) * int(i.quantity),
                'description': i.description,
            })
        return response

class Hop_Billing_Package_Value(Base):
    __tablename__ = 'billing_package_value'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    item_id = Column(Integer,ForeignKey('billing_package_item.id'),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Billing_Outlet(Base):
    __tablename__ = 'billing_outlet'

    id = Column(Integer,primary_key=True)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    billing_package_id = Column(Integer,ForeignKey('billing_package_item.id'),default=None)
    expire = Column(Date,default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _checkbillingoutlet(self, _outletid):
        response = {}
        response['name'] = 'Free'
        response['expired'] = '-'
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Outlet).filter_by(outlet_id = _outletid).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _billing is not None:
            if _billing.expire >= datetime.now().date():
                response['name'] = 'Premium'
                response['expired'] = str(_billing.expire)
        return response

class Hop_Billing_Transaction(Base):
    __tablename__ = 'billing_transaction'

    id = Column(Integer,primary_key=True)
    billing_invoice_id = Column(Integer,ForeignKey('billing_invoice.id'),default=None)
    billing_package_id = Column(Integer,ForeignKey('billing_package_item.id'),default=None)
    outlet_id = Column(Integer,ForeignKey('outlet.id'),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, billing_invoice_id, billing_package_id, outlet_id):
        session = Session()
        try:
            _billing = Hop_Billing_Transaction()
            _billing.billing_invoice_id = billing_invoice_id
            _billing.billing_package_id = billing_package_id
            _billing.outlet_id = outlet_id
            session.add(_billing)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove(self, id, billing_invoice_id):
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Transaction).filter_by(id=id, billing_invoice_id=billing_invoice_id, status=True).first()
            if _billing is not None:
                _billing.status = False
                session.add(_billing)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _list(self, billing_invoice_id):
        response = []
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Transaction).filter_by(billing_invoice_id=billing_invoice_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _billing:
            response.append({
                'id': i.id,
                'outlet' : Hop_Outlet()._data(i.outlet_id),
                'package': Hop_Billing_Package_Item()._data(i.billing_package_id),
            })
        return response

    def _total(self, billing_invoice_id):
        response = 0
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Transaction).filter_by(billing_invoice_id=billing_invoice_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _billing:
            _package = Hop_Billing_Package_Item()._data(i.billing_package_id)
            response += _package['total']
        return response


class Hop_Billing_Invoice(Base):
    __tablename__ = 'billing_invoice'

    id = Column(Integer,primary_key=True)
    name = Column(String(200),default=None)
    description = Column(Text)
    user_id = Column(Integer,ForeignKey('user.id'),default=None)
    status_transaction_id = Column(Integer,ForeignKey('billing_status_transaction.id'),default=None)
    billing_payment_id = Column(Integer,ForeignKey('billing_payment.id'),default=None)
    subtotal = Column(Numeric(13,2),default=0)
    billing_promo_id = Column(Integer,ForeignKey('billing_promo.id'),default=None)
    billing_promo_value = Column(Numeric(13,2),default=0)
    total = Column(Numeric(13,2),default=0)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _basic_data(self, id):
        response = {}
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _billing is not None:
            response['id'] = _billing.id
            response['name'] = _billing.name
            response['description'] = _billing.description
            response['status_transaction_id'] = _billing.status_transaction_id
            response['billing_payment_id'] = _billing.billing_payment_id
        return response

    def _name(self, user_id, owner_id):
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status=True).order_by(desc(Hop_Billing_Invoice.id)).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        name = 'INV-'
        name_id = '0000000000001'
        if _billing is not None:
            _id = int(_billing.name.split('-')[2])
            name_id_len = len(str(int(_id) + 1))
            name_id = ''
            for i in range(13 - name_id_len):
                name_id += '0'
            name_id += str(int(_id) + 1)
        name += str(user_id) + '-' + name_id
        return name

    def _add_order_overview(self, user_id, package_id, outlet_list, owner_id):
        response = {}
        response['value'] = 0
        session = Session()
        try:
            _exist_billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
            if _exist_billing is not None:
                response['id'] = _exist_billing.id
            else:
                _billing = Hop_Billing_Invoice()
                _billing.name = Hop_Billing_Invoice()._name(user_id, owner_id)
                _billing.user_id = user_id
                _billing.status_transaction_id = 1
                session.add(_billing)
                session.commit()
                response['id'] = _billing.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in outlet_list:
            Hop_Billing_Transaction()._insert(response['id'], package_id, i)
        response['value'] = Hop_Billing_Invoice()._invoice_trx_count(user_id)
        return response

    def _cancel_transaction(self, user_id):
        session = Session()
        try:
            _exist_billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
            if _exist_billing is not None:
                _exist_billing.status_transaction_id = 4
                session.add(_exist_billing)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        session.commit()

    def _exist_order(self, user_id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _invoice = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _invoice is not None:
            response['id'] = _invoice.id
            response['name'] = _invoice.name
            response['list'] = Hop_Billing_Transaction()._list(_invoice.id)
            response['status'] = '00'
        return response

    def _data_ongoing(self, user_id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
            _invoice = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=2, status=True).filter(Hop_Billing_Invoice.added_time + timedelta(hours=2) > datetime.now()).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _invoice is not None:
            response['id'] = _invoice.id
            response['name'] = _invoice.name
            response['billing_payment'] = Hop_Billing_Payment()._data(_invoice.billing_payment_id)
            response['payment_tools'] = Hop_Billing_Payment_Tools()._list(_invoice.billing_payment_id)
            response['total'] = str(_invoice.total)
            response['user'] = Hop_User()._basic_data(_invoice.user_id)
            response['datetime'] = str(_invoice.added_time + timedelta(hours=2))
            response['status'] = '00'
        return response

    def _invoice_trx_count(self, user_id):
        response = 0
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
            if _billing is not None:
                response = session.query(Hop_Billing_Transaction).filter_by(billing_invoice_id=_billing.id, status=True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return int(response)

    def _order_trx_service(self, user_id):
        _list = []
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
            if _billing is not None:
                _trx = session.query(Hop_Billing_Transaction).filter_by(billing_invoice_id=_billing.id, status=True).filter(Hop_Billing_Transaction.billing_package_id.in_([1, 2, 3])).all()
                for i in _trx:
                    _list.append(i.outlet_id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return _list

    def _check_ongoing_payment(self, user_id):
        response = False
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=2, status=True).filter(Hop_Billing_Invoice.added_time + timedelta(hours=2) > datetime.now()).first()
            if _billing is not None:
                response = True
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

    def _proceed_payment(self, user_id, payment_id):
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
            if _billing is not None:
                _billing.status_transaction_id = 2
                _billing.billing_payment_id = payment_id
                _billing.subtotal = Hop_Billing_Transaction()._total(_billing.id)
                _billing.total = Hop_Billing_Transaction()._total(_billing.id)
                _billing.added_time = datetime.now()
                session.add(_billing)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remove_order(self, user_id, trx_list, owner_id):
        response = {}
        response['value'] = 0
        session = Session()
        try:
            _exist_billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id, status_transaction_id=1, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _exist_billing is not None:
            for i in trx_list:
                Hop_Billing_Transaction()._remove(i, _exist_billing.id)
        _trx_count = Hop_Billing_Invoice()._invoice_trx_count(user_id)
        if _trx_count == 0:
            Hop_Billing_Invoice()._cancel_transaction(user_id)
        response['value'] = _trx_count
        return response

    def _history_list(self, user_id):
        response = []
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Invoice).filter_by(user_id=user_id,status=True).filter(Hop_Billing_Invoice.status_transaction_id!=1).order_by(desc(Hop_Billing_Invoice.id)).all()
            for i in _billing:
                if i.status_transaction_id == 2 and i.added_time + timedelta(hours=2) < datetime.now():
                    i.status_transaction_id = 5
                    session.add(i)
                    session.commit()
                response.append({
                    'id': i.id,
                    'name': i.name,
                    'datetime': str(i.added_time),
                    'status': Hop_Billing_Status_Transaction()._data(i.status_transaction_id),
                    'payment': Hop_Billing_Payment()._data(i.billing_payment_id),
                    'total': str(i.total),
                })
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response

class Hop_Billing_Status_Transaction(Base):
    __tablename__ = 'billing_status_transaction'

    id = Column(Integer,primary_key=True)
    name = Column(String(200),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, id):
        response = {}
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Status_Transaction).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _billing is not None:
            response['id'] = _billing.id
            response['name'] = _billing.name
        return response

class Hop_Billing_Promo(Base):
    __tablename__ = 'billing_promo'

    id = Column(Integer,primary_key=True)
    name = Column(String(200),default=None)
    value = Column(Numeric(13,2),default=0)
    type = Column(Integer,default=0)
    code = Column(String(50),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

# CLASS FOR USER BILLING PAYMENT

class Hop_Billing_Payment_Type(Base):
    __tablename__ = 'billing_payment_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Billing_Payment(Base):
    __tablename__ = 'billing_payment'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    company_code = Column(String(36),default=None)
    apikey = Column(String(36),default=None)
    apisecret = Column(String(36),default=None)
    clientid = Column(String(36),default=None)
    clientsecret = Column(String(36),default=None)
    type_id = Column(Integer,ForeignKey('billing_payment_type.id'),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, id):
        response = {}
        session = Session()
        try:
            _payment = session.query(Hop_Billing_Payment).filter_by(id=id, status=True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _payment is not None:
            response['id'] = _payment.id
            response['name'] = _payment.name
            response['company_code'] = _payment.company_code
        return response

    def _list(self):
        response = []
        session = Session()
        try:
            _payment = session.query(Hop_Billing_Payment).filter(Hop_Billing_Payment.id!=1).filter_by(status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _payment:
            response.append({
                'id': i.id,
                'name': i.name,
            })
        return response

class Hop_Billing_Payment_Tools(Base):
    __tablename__ = 'billing_payment_tools'
    id = Column(Integer,primary_key=True)
    name = Column(String(255),default=None)
    payment_id = Column(Integer,ForeignKey('billing_payment.id'),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self, payment_id):
        response = []
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Payment_Tools).filter_by(payment_id=payment_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _billing:
            response.append({
                'id': i.id,
                'name': i.name,
                'list': Hop_Billing_Payment_Detail()._list(i.id)
            })
        return response

class Hop_Billing_Payment_Detail(Base):
    __tablename__ = 'billing_payment_detail'
    id = Column(Integer,primary_key=True)
    name = Column(String(512),default=None)
    tools_id = Column(Integer,ForeignKey('billing_payment_tools.id'),default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _list(self, tools_id):
        response = []
        session = Session()
        try:
            _billing = session.query(Hop_Billing_Payment_Detail).filter_by(tools_id=tools_id, status=True).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for i in _billing:
            response.append(i.name)
        return response

# Class for Sales and Partner

class Hop_Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer,primary_key=True)
    username = Column(String(16), default=None)
    name = Column(String(100), default=None)
    phone_number = Column(String(50),index=True, default=None)
    password_hash = Column(String(128), default=None)
    email = Column(String(100),index=True, default=None)
    role_id = Column(Integer,ForeignKey('sales_role.id'), default=None)
    address = Column(Text, default=None)
    gender_id = Column(String(15), default=None)
    birthdate = Column(DateTime, default=None)
    confirmed = Column(Boolean,default=True)
    ktp_number = Column(String(16), default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        response['status'] = '50'
        session = Session()
        try:
           _sales_id = session.query(Hop_Sales).filter_by(id=_id, status=True).first()
           _sales_username = session.query(Hop_Sales).filter_by(username=_id, status=True).first()
           _sales_phone = session.query(Hop_Sales).filter_by(phone_number=_id, status=True).first()
           _sales_email = session.query(Hop_Sales).filter_by(email=_id, status=True).first()
           if _sales_id is not None:
               response['id'] = _sales_id.id
               response['name'] = _sales_id.name
               response['status'] = '00'
           elif _sales_username is not None:
               response['id'] = _sales_username.id
               response['name'] = _sales_username.name
               response['status'] = '00'
           elif _sales_phone is not None:
               response['id'] = _sales_phone.id
               response['name'] = _sales_phone.name
               response['status'] = '00'
           elif _sales_email is not None:
               response['id'] = _sales_email.id
               response['name'] = _sales_email.name
               response['status'] = '00'
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return response


class Hop_Sales_Role(Base):
    __tablename__ = 'sales_role'

    id = Column(Integer,primary_key=True)
    name = Column(String(100), default=None)
    first_bonus = Column(DECIMAL(10,2), default=None)
    bonus = Column(DECIMAL(10,2), default=None)
    lifetime = Column(DateTime, default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _data(self, _id):
        response = {}
        session = Session_hop()
        try :
            _sales_role = session.query(Hop_Sales_Role).filter_by(id = _id, status = True).first()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        if _sales_role is not None:
            response['id'] = _sales_role.id
            response['name'] = _sales_role.name
        else:
            response = None
        return response

class Hop_Sales_Cash_Flow(Base):
    __tablename__ = 'sales_cash_flow'

    id = Column(Integer,primary_key=True)
    sales_id = Column(Integer,ForeignKey('sales.id'), default=None)
    amount = Column(DECIMAL(10,2), default=None)
    used = Column(Boolean, default=False)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Partner_Bank_Account(Base):
    __tablename__ = 'partner_bank_account'

    id = Column(Integer,primary_key=True)
    name = Column(String(100),primary_key=True)
    sales_id = Column(Integer,ForeignKey('sales.id'), default=None)
    partner_bank_id = Column(Integer,ForeignKey('partner_bank.id'), default=None)
    uid = Column(String(20), default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Partner_Bank(Base):
    __tablename__ = 'partner_bank'

    id = Column(Integer,primary_key=True)
    name = Column(String(100),primary_key=True)
    uid = Column(String(20), default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Partner_Promo(Base):
    __tablename__ = 'partner_promo'

    id = Column(Integer,primary_key=True)
    name = Column(String(100),primary_key=True)
    value = Column(DECIMAL(10,2), default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

class Hop_Log_Action(Base):
    __tablename__ = 'log_action'

    id = Column(Integer,primary_key=True)
    objectid = Column(String(100),default=None)
    id_transaction = Column(String(100),default=None)
    code_struk = Column(String(100),default=None)
    user_id = Column(Integer,ForeignKey('user.id'),default=None)
    time = Column(DateTime,default=None)
    type = Column(Integer,default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self,objectid, idtransac, codestruk, userid, time, type):
        session = Session_hop()
        try:
            insert = Hop_Log_Action()
            insert.objectid = objectid
            insert.id_transaction = idtransac
            insert.code_struk = codestruk
            insert.user_id = userid
            insert.time = time
            insert.type = type
            session.add(insert)
            session.commit()
            insert.id
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return insert

    def _countbyobjectid(self, _objectid):
        session = Session_hop()
        response = 0
        try:
            _logaction = session.query(Hop_Log_Action).filter_by(objectid = _objectid, status = True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return _logaction

class Hop_Log_Action_Detail(Base):
    __tablename__ = 'log_action_detail'

    id = Column(Integer,primary_key=True)
    log_action_id = Column(Integer,ForeignKey('log_action.id'),default=None)
    pid = Column(Integer,ForeignKey('product_item.id'),default=None)
    vid = Column(Integer,ForeignKey('variant_list.id'),default=None)
    price_id = Column(Integer,ForeignKey('price.id'),default=None)
    quantity = Column(Integer,default=None)
    type = Column(Integer,default=None)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)

    def _insert(self, logactionid, pid, vid, priceid, quantity, type):
        session = Session_hop()
        response = {}
        try:
            insert = Hop_Log_Action_Detail()
            insert.log_action_id = logactionid
            insert.pid = pid
            insert.vid = vid
            insert.price_id = priceid
            insert.quantity = quantity
            insert.type = type
            session.add(insert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return None

    def _countbylogactiondetail(self, _logactionid):
        session = Session_hop()
        response = {}
        try:
            _logactiondetail = session.query(Hop_Log_Action_Detail).filter_by(log_action_id = _logactionid, status = True).count()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return _logactiondetail

class Hop_Language(Base):
    __tablename__ = 'language'

    id = Column(Integer,primary_key=True)
    name = Column(String(50),default=1)
    added_time = Column(DateTime,default=datetime.now())
    status = Column(Boolean,default=True)


# REINIT FUNCTION
def reinit():
    drop_all()
    create_all()
