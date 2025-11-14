from flask import Flask, request, session, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # In Produktion sicher speichern!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# 📦 Datenbankmodell
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

# 🧾 Registrierung
def register(name, password):
    if User.query.filter_by(name=name).first():
        return "Benutzername existiert bereits."
    password_hash = generate_password_hash(password)
    user = User(name=name, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return "Registrierung erfolgreich."

# 🔐 Verifizierung
def verify(name, password):
    user = User.query.filter_by(name=name).first()
    if user and check_password_hash(user.password_hash, password):
        session['user'] = user.name
        return True
    return False

# 🧼 Logout
def logout():
    session.pop('user', None)

# 🧪 Routen
@app.route('/')
def index():
    if 'user' in session:
        return f"✅ Eingeloggt als {session['user']} <br><a href='/logout'>Logout</a>"
    return "❌ Nicht eingeloggt. <a href='/login'>Login</a>"

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        message = register(name, password)
        return f"{message} <br><a href='/'>Zurück</a>"
    return '''
        <form method="post">
            Benutzername: <input name="name"><br>
            Passwort: <input name="password" type="password"><br>
            <input type="submit" value="Registrieren">
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if verify(name, password):
            return redirect(url_for('index'))
        return "Login fehlgeschlagen. <a href='/login'>Erneut versuchen</a>"
    return '''
        <form method="post">
            Benutzername: <input name="name"><br>
            Passwort: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout_route():
    logout()
    return redirect(url_for('index'))

# 🏁 Initialisierung
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)