from flask import Flask, render_template, flash
import flask_login
from flask_sqlalchemy import SQLAlchemy
from user import register, verify


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizzler.db'  # Creates a local SQLite file
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead warning

db = SQLAlchemy(app)

# Define a simple User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User {self.id} ({self.name})>"

with app.app_context():
    db.create_all()

    # try registering
    hashed=(register("test", "testpassword"))
    print(f'remove before use: Hash is {hashed}')
    # try logging in
    # read hashed value for user from db and store in hashed
    entered_password="testpassword"
    print("real password")
    logged=(verify(hashed, entered_password))
    if logged==True:
        print("logged in")
    else:
        print("not logged in")
    entered_password="falschespasswort"
    print("wrong password")
    logged=(verify(hashed, entered_password))
    if logged==True:
        print("logged in")
    else:
        print("not logged in")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


