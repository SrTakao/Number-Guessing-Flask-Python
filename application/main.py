from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import Usuario
from db import datab
from random import randint
import hashlib

app = Flask(__name__)
app.secret_key = 'rafacode'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
datab.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

@lm.user_loader
def user_loader(id):
    usuario = datab.session.query(Usuario).filter_by(id=id).first()
    return usuario

#=-=-=# criação das rotas

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']

        user = datab.session.query(Usuario).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return 'nome ou senha incorretos'
        
        login_user(user)
        
        return redirect(url_for('home'))



@app.route("/register", methods=['GET', 'POST']) # rota registrar
def registro():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']

        novo_usuario = Usuario(nome=nome, senha=hash(senha))
        datab.session.add(novo_usuario)
        datab.session.commit()

        login_user(novo_usuario)

        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    numSecret = randint(1,100)
    palpite = 0 
    resultado = ''
    if request.method == 'GET':
        return render_template('game.html')
    elif request.method == 'POST': 
        palpite = request.form['guess']
        if palpite == numSecret:
            resultado = 'Numero Correto! :D'
        else:
            resultado = f'Numero Errado! :( \nO resultado era:{numSecret}'
        
    return render_template('game.html', resposta = resultado)
        



#--# inicia o codigo pagina inicial
if __name__ == "__main__":
    with app.app_context():
        datab.create_all()
    app.run(debug=True)