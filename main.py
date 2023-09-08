from flask import *
from flask_session import Session


# Settings
HOST = "0.0.0.0"
PORT = 80

# Init
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'Vk\xda\x97)4\xe51_\xec\x86\x94'
Session(app)

# Other flask imports
from inject_global_vars import *


@app.route('/')
def index():
    return render_template("main.html",
                           nav_page="home")

@app.route('/cenik')
def cenik():
    return render_template("cenik.html",
                           nav_page="cenik")

@app.route('/rezervace')
def rezervace():
    return render_template("rezervace.html",
                           nav_page="reservation")

@app.route('/kontakt')
def kontakt():
    return render_template("kontakt.html",
                           nav_page="kontakt")

@app.route('/admin')
def admin():
    return render_template("admin.html")



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)