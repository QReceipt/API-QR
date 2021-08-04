# -*- coding: utf-8 -*-
from routes import app
from flask_sqlalchemy import SQLAlchemy
from config import DB_URL

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy() 
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)