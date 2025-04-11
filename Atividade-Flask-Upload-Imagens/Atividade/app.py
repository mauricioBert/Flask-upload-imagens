from flask import Flask, render_template
import pymysql.cursors
from controllers import routes
from models.database import db
import os
import pymysql

app = Flask(__name__, template_folder='views')
routes.init_app(app)
dir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'folders'
app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = F'mysql+pymysql://root:@localhost/{DB_NAME}'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTEN_LENGTH'] = 16 * 1024 * 1024
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir,'models/studants.sqlite3')

if __name__ == '__main__':
    connetion = pymysql.connect(host='localhost',user='root',passwd='',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connetion.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"O banco de dados está criado!")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
         connetion.close()
    
    db.init_app(app=app)

    with app.test_request_context():
        db.create_all()
    app.run(host='localhost', port=4000, debug=True)
