import json
from json import JSONDecodeError

class Reservation:
    def __init__(self, name, surname, year, email, phone, date, time, massage_type, active):
        self.name = name
        self.surname = surname
        self.year = year
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.massage_type = massage_type
        self.active = active
    
    def get_data(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "year": self.year,
            "email": self.email,
            "phone": self.phone,
            "date": self.date,
            "time": self.time,
            "type": self.massage_type,
            "active": self.active
            }
    
    def get_id(self):
        return str(hash("%s%s%s" % (self.date, self.time, self.email)))
    

class ReservationManager:
    def __init__(self):
        self.reservations = []
        self.load()
    
    #  Check if time and date is not reserved
    def is_available(self, date, time):
        for r in self.reservations:
            if r.date == date and r.time == time and r.active == "1":
                return False
        
        return True
    
    #  Create reservation to the system
    def create_reservation(self, name, surname, year, email, phone, date, time, massage_type):
        r = Reservation(name, surname, year, email, phone, date, time, massage_type, "1")
        self.reservations.append(r)

        # Save data
        self.save()
    
    #  Save reservations
    def save(self):
        data = {}

        for r in self.reservations:
            data[r.get_id()] = r.get_data()
        
        with open('data.json', 'w', encoding="UTF-8") as file:
            json.dump(data, file)
    
    #  Load reservations from file
    def load(self):
        try:
            with open("data.json") as file:
                data = json.load(file)

                for rData in data:
                    r = Reservation(data[rData]["name"], data[rData]["surname"], data[rData]["year"], data[rData]["email"],
                                    data[rData]["phone"], data[rData]["date"], data[rData]["time"], data[rData]["type"], data[rData]["active"])
                    self.reservations.append(r)

        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass

        
