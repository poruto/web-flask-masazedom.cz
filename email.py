import smtplib, ssl

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
    
    def send_email(self, receiver_email, message):
        self.server.sendmail(self.email, receiver_email, message)
    
    def send_email_self(self, message):
        self.send_email(self, self.email, message)
    
    def quit(self):
        self.server.quit()

def __run_tests():
    # Testing E-mail
    client = EmailClient(GMAIL_SERVER, "masazedomukm@gmail.com", "Soudkynebarbara123")
    client.send_email_self("Tohle je automatický testovací email")
    client.quit()

if __name__ == "__main__":
    __run_tests()

