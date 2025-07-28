from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    #protect the password_hash property
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed')
    
    #hash the password
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    #verify a user's password
    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()