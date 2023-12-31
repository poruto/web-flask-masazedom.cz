import json
from json import JSONDecodeError
from datetime import datetime

class Reservation:
    def __init__(self, name, surname, year, email, phone, date, time, massage_type, notes, timestamp, id, place, active):
        self.name = name
        self.surname = surname
        self.year = year
        self.email = email
        self.phone = phone
        self.date = date
        self.date_object = datetime.strptime(date, '%Y-%m-%d').date()
        self.time = time
        self.massage_type = massage_type
        self.notes = notes
        self.active = active
        self.timestamp = timestamp
        self.id = id
        self.place = place
    
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
            "notes": self.notes,
            "timestamp": self.timestamp,
            "id": self.id,
            "place": self.place,
            "active": self.active
            }
    
    def get_id(self):
        return self.id
    

class ReservationManager:
    def __init__(self):
        self.reservations = []
        self.counter = 0
        self.load()
    
    #  Set max counter
    def set_max_counter(self):
        self.counter = 0

        for r in self.reservations:
            if r.id > self.counter:
                self.counter = r.id
    
    def get_new_id(self):
        self.counter += 1
        return self.counter
    
    #  Check if time and date is not reserved
    def is_available(self, date, time):
        for r in self.reservations:
            if r.date == date and r.time == time and r.active == "1":
                return False
        
        return True
    
    #  Create reservation to the system
    def create_reservation(self, name, surname, year, email, phone, date, time, massage_type, notes, place):
        timestamp = str(datetime.now())
        r = Reservation(name, surname, year, email, phone, date, time, massage_type, notes, timestamp, self.get_new_id(), place, "1")
        self.reservations.append(r)

        # Save data
        self.save()
    
    def get_reservation_by_id(self, id):
        for r in self.reservations:
            if str(r.get_id()) == id:
                return r

        return None
    
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
                                    data[rData]["phone"], data[rData]["date"], data[rData]["time"], data[rData]["type"], data[rData]["notes"], data[rData]["timestamp"], data[rData]["id"], data[rData]["place"], data[rData]["active"])
                    self.reservations.append(r)
                
                self.set_max_counter()

        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass

        
