from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizzler.db'  # Creates a local SQLite file
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead warning

db = SQLAlchemy(app)

# --- Datenbankmodelle --- 

# User-Modell: Erweitert um UserMixin und Quiz-Beziehung
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # KORREKTUR: Dies ist das Haupt-Login-Feld
    username = db.Column(db.String(80), unique=True, nullable=False) 
    
    # NEU: E-Mail für die Registrierung hinzugefügt
    email = db.Column(db.String(120), unique=True, nullable=True) 
    
    password = db.Column(db.String(256), unique=False, nullable=False)
    
    # User -> Quiz (1:n) Beziehung
    quizzes = db.relationship('Quiz', backref='creator', lazy='dynamic')
    
    def __repr__(self):
        # KORREKTUR: Nutzt jetzt das korrekte Feld 'username'
        return f"<User {self.id} ({self.username})>"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)

    # Beziehung: Quiz gehört zu einem User (Fremdschlüssel)(n:1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Quiz -> Question (1:n) Beziehung
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    
    # KORREKTUR: __repr__ ist sauber definiert
    def __repr__(self):
        return f"<Quiz {self.title}>"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    
    # Frage gehört zu einem Quiz
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    # Question -> Answer (1:n)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    
    # KORREKTUR: __repr__ ist sauber definiert
    def __repr__(self):
        return f'<Question {self.id}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    
    # Antwort gehört zu einer Frage
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    def __repr__(self):
        return f'<Answer {self.id} (Correct: {self.is_correct})>'
    
# --- Ende der Datenbankmodelle ---

@app.route("/")
def index():
    return render_template("index.html")

# --- Start der Anwendung ---
if __name__ == "__main__":
    with app.app_context():
        # Stellt sicher, dass die Datenbank und alle Tabellen existieren
        db.create_all() 

    # Startet die Flask-Anwendung im Debug-Modus
    app.run(debug=True)
# --- Ende der Anwendung ---



