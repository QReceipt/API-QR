# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from .serializer import Serializer

db = SQLAlchemy()



class Menu(db.Model):
    __tablename__ = 'Menu'

    id = db.Column(db.Integer, primary_key=True)
    receipt = db.Column(db.ForeignKey('Receipt.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    menuName = db.Column(db.String(1024), nullable=False)
    quentity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(512), nullable=False)

    Receipt = db.relationship('Receipt', primaryjoin='Menu.receipt == Receipt.id', backref='menus')



class Origin(db.Model):
    __tablename__ = 'Origin'

    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(2048))


class QRimage(db.Model):
    __tablename__ = 'QRimage'

    id = db.Column(db.Integer, primary_key=True)
    receipt = db.Column(db.ForeignKey('Receipt.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    QRpath = db.Column(db.String(512))

    Receipt = db.relationship('Receipt', primaryjoin='QRimage.receipt == Receipt.id', backref='q_rimages')

    def __init__(self, receipt, QRpath) -> None:
        self.receipt = receipt
        self.QRpath = QRpath

    def __repr__(self) -> str:
        return '<QRimage %r>' % (self.QRpath)

class Receipt(db.Model):
    __tablename__ = 'Receipt'

    id = db.Column(db.Integer, primary_key=True)
    receiptID = db.Column(db.String(512), nullable=False)
    seller = db.Column(db.ForeignKey('User.id', onupdate='CASCADE'), index=True)
    destinationAddr1 = db.Column(db.String(1024))
    destinationAddr2 = db.Column(db.String(1024))
    destinationPhoneNum = db.Column(db.String(512))
    shopRequest = db.Column(db.String(2048))
    deliveryRequests = db.Column(db.String(2048))
    origin = db.Column(db.ForeignKey('Origin.id', onupdate='CASCADE'), index=True)
    orderDate = db.Column(db.DateTime)

    Origin = db.relationship('Origin', primaryjoin='Receipt.origin == Origin.id', backref='receipts')
    User = db.relationship('User', primaryjoin='Receipt.seller == User.id', backref='receipts')

    def __repr__(self) -> str:
        return '<Receipt %r %r>' % (self.orderDate, self.destinationPhoneNum)


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(512))
    addr1 = db.Column(db.String(1024))
    addr2 = db.Column(db.String(1024))
    phoneNumber = db.Column(db.String(512))
    userCategory = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % (self.name)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d