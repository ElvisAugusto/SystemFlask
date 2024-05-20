import os

SECRET_KEY = 'sua-chave-secreta'
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db/banco.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
