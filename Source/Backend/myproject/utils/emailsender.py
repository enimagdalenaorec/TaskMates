import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, content):
    sender_email="taskmatesfer@gmail.com"
    sender_password='sjjgdmjhwnpaobsx'#lose
    #sender_password=os.getenv("APP_PASSWORD") kako triba bit

    # Postavke SMTP servera za Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Kreiranje MIME poruke
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Dodavanje sadržaja u e-mail
    message.attach(MIMEText(content, "plain"))  # Plain text verzija

    try:
        # Povezivanje na SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Pokretanje TLS enkripcije
            server.login(sender_email, sender_password)  # Prijava na Gmail račun
            server.sendmail(sender_email, to_email, message.as_string())  # Slanje e-maila
    except Exception as e:
        print(f"Dogodila se pogreška prilikom slanja pošte korisniku {to_email}: {e}")

