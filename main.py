from flask import *
from flask_session import Session
from email_tools import *
from reservations import *


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

def get_my_client_email():
    return EmailClient(GMAIL_SERVER, config.settings["email"], config.settings["password"])

@app.route('/rezervace/check')
@app.route('/rezervace/check/<date>/<time>')
def is_reservation_available(date=None, time=None):
    if date != None and time != None:
        if rm.is_available(date, time):
            return "y"
        else:
            return "n"
    else:
        return "n"

@app.route('/rezervace_create/', methods=(['POST']))
def rezervace_create():
    created = 1

    name = request.form["reservation_name"]
    surname = request.form["reservation_surname"]
    year = request.form["reservation_year"]
    email = request.form["reservation_email"]
    phone = request.form["reservation_phone"]
    date = request.form["reservation_date"]
    massage_type = request.form["reservation_type"]
    notes = request.form["reservation_notes"]

    time = ""

    if "reservation_time" in request.form:
        time = request.form["reservation_time"]

    print("Name", name)
    print("Surname", surname)
    print("Year", year)
    print("Email", email)
    print("Phone", phone)
    print("Date", date)
    print("Time", time)

    errmsg = ""

    if len(name) == 0:
        errmsg += "Nevyplnili jste Jméno. "

    if len(surname) == 0:
        errmsg += "Nevyplnili jste Příjmení. "

    if len(year) == 0:
        errmsg += "Nevyplnili jste Rok narození. "
    
    if len(email) == 0:
        errmsg += "Nevyplnili jste Email. "
    elif not validate_email(email):
        errmsg += "Email je nesprávně zadaný! "

    if len(phone) < 9 or len(phone) > 15:
        errmsg += "Nevyplnili jste Telefon. "
    
    if len(date) == 0:
        errmsg += "Nevyplnili jste Datum. "
    
    if len(time) == 0:
        errmsg += "Nevyplnili jste Čas. "

    if not rm.is_available(date, time):
        errmsg += "Vámi zvolený termín není dostupný! "
    
    if len(errmsg) > 0:
        created = 0

    # If everything valid, try to send email
    if created == 1:
        rm.create_reservation(str(name), str(surname), str(year), str(email), str(phone), str(date), str(time), str(massage_type))

        #  Send notification to own email
        create_email = ("Založena rezervace v systému\nJméno: %s "
                        "\nPříjmení: %s"
                        "\nRok narození: %s"
                        "\nEmail: %s"
                        "\nTelefon: %s"
                        "\nDatum: %s"
                        "\nČas: %s"
                        "\nTyp masáže: %s"
                        "\nPoznámky: %s") % (
            name, surname, year, email, phone, date, time, massage_type, notes
        )

        client = get_my_client_email()
        client.send_email_self(create_email, "Založení rezervace %s %s %s" % (name, surname, date))

        # Send notification to customer's email
        client.send_email(email, "Tohle je testovací potvrzení rezervace!", "Masáže domů - Potvrzení rezervace")

        #  Stop connection to the mail server
        client.quit()


    return render_template("rezervace_create.html",
                           nav_page="reservation",
                           created=created,
                           errmsg=errmsg)

@app.route('/kontakt')
def kontakt():
    return render_template("kontakt.html",
                           nav_page="kontakt")

@app.route('/admin')
def admin():
    return render_template("admin.html")



if __name__ == '__main__':
    rm = ReservationManager()
    app.run(host=HOST, port=PORT, debug=True)