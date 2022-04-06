from flask import Flask, request, jsonify, Response, json
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'hardsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/gudang_wahaji'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, username, password, created_at, updated_at):
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at


class Barang(db.Model):
    __tablename__ = "Barang"
    id = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(100), unique=True)
    nama_barang = db.Column(db.String(100))
    harga = db.Column(db.String(100))
    stok = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, kode_barang, nama_barang, harga, stok, created_at, updated_at):
        self.kode_barang = kode_barang
        self.nama_barang = nama_barang
        self.harga = harga
        self.stok = stok
        self.created_at = created_at
        self.updated_at = updated_at


class Transaksi(db.Model):
    __tablename__ = "Transaksi"
    id = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(100))
    id_user = db.Column(db.String(100))
    jumlah = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    # kode_barang = db.Column(
    #     db.String(100), db.ForeignKey('Barang.kode_barang'))
    # Barang = db.relationship(
    #     "Barang", backref=backref("Barang", uselist=False))
    # id_user = db.Column(db.String(100), db.ForeignKey('User.id'))
    # User = db.relationship(
    #     "User", backref=backref("User", uselist=False))

# Controller


class UserController(Resource):
    def get(self):
        result = db.engine.execute("select * from user")
        aData = [{"username": row[1], "password":row[2]} for row in result]
        data = {
            "message": "Get all user",
            "aData": aData
        }

        return data, 200, {'ContentType': 'application/json'}

    def post(self):
        username = request.json['username']
        password = request.json['password']

        error = None

        if username == "":
            error = 'Username is required.'
        elif password == "":
            error = 'Password is required.'

        if error:
            return {"result": False, "error": error}, 400, {'ContentType': 'application/json'}

        try:
            db.engine.execute(
                f"insert into user (username,password) values ('{username}','{password}')")
        except IntegrityError:
            error = f"User {username} is already registered."
            return {"result": False, "error": error}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 201, {'ContentType': 'application/json'}

    def put(self):
        userid = request.json['id']
        username = request.json['username']
        password = request.json['password']

        try:
            result = db.engine.execute(
                f"update user set username='{username}', password='{password}' where id={userid}")

        except IntegrityError:
            return {"result": False}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 200, {'ContentType': 'application/json'}

    def delete(self):
        userid = request.json['id']
        try:
            result = db.engine.execute(
                f"delete from user where id={userid}")
        except IntegrityError:
            return {"result": False}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 200, {'ContentType': 'application/json'}


class BarangController(Resource):
    def get(self):
        result = db.engine.execute(
            "select b.username,a.nama from barang a left join user b on a.id_user=b.id")
        aData = [{"username": row[0], "barang":row[1]} for row in result]
        data = {
            "message": "Get all user with barang",
            "aData": aData
        }

        return data, 200, {'ContentType': 'application/json'}

    def post(self):
        iduser = request.json['id_user']
        nama = request.json['nama_barang']

        try:
            result = db.engine.execute(
                f"insert into barang (id_user,nama) values ('{iduser}','{nama}')")
        except IntegrityError:
            return {"result": False}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 201, {'ContentType': 'application/json'}

    def put(self):
        userid = request.json['id']
        username = request.json['username']
        password = request.json['password']

        try:
            result = db.engine.execute(
                f"update user set username='{username}', password='{password}' where id={userid}")

        except IntegrityError:
            return {"result": False}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 200, {'ContentType': 'application/json'}

    def delete(self):
        userid = request.json['id']
        try:
            result = db.engine.execute(
                f"delete from user where id={userid}")
        except IntegrityError:
            return {"result": False}, 400, {'ContentType': 'application/json'}

        return {"result": True}, 200, {'ContentType': 'application/json'}

    def beli_barang(self):
        return "beli"


# Route
api.add_resource(UserController, '/user')
api.add_resource(BarangController, '/barang')


if __name__ == '__main__':
    app.run(debug=True)
