import smtplib, ssl
import re  

GMAIL_SERVER = "smtp.gmail.com"

class EmailClient:
    def __init__(self, serverip, email, password, port=465):
        self.serverip = serverip
        self.port = port
        self.email = email
        self.password = password

        # Create a secure SSL context
        context = ssl.create_default_context()

        self.server = smtplib.SMTP_SSL(serverip, port, context=context)
        self.server.login(email, password)
    
    def send_email(self, receiver_email, message, subject):
        msg = 'Subject: {}\n\n'.format(subject)
        msg += message
        self.server.sendmail(self.email, receiver_email, msg.encode())
    
    def send_email_self(self, message, subject):
        self.send_email(self.email, message, subject)
    
    def quit(self):
        self.server.quit()

#  ***************************** TOOLS ***************************** 
def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False  

#  ***************************** TESTS ***************************** 
def __run_tests():
    # Testing E-mail
    client = EmailClient(GMAIL_SERVER, "masazedomukm@gmail.com", "kmrartrbwgkczosm")
    client.send_email_self("Tohle je automatický testovací email", "Test Mail")
    client.quit()

if __name__ == "__main__":
    __run_tests()

