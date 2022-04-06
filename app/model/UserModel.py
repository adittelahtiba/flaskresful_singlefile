class UserController(Resource):
    def get(self):
        result = db.engine.execute("select * from user")
        aData = [{"username": row[1], "password":row[2]} for row in result]
        data = {
            "message": "Get all user",
            "aData": aData
        }

        return data, 200

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
