import smtplib
import ssl
import csv
import os
import random
import time
from email.message import EmailMessage

# config
EMAIL_ADDRESS = "add_email_here"
EMAIL_PASSWORD = "add_password_here"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

CODE_EXPIRY = 300  # 5 minutes
USER_FILE = "users.csv"
active_codes = {} 

# opens csv and gets users
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    email, username = row
                    users[username.lower()] = email.lower()
    return users

# adds user to csv
def save_user(username, email):
    with open(USER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email.lower(), username.lower()])

# sends email using smtp
def send_email(to_address, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def generate_code():
    return str(random.randint(100000, 999999))

def register():
    username = input("Enter your name: ").strip().lower()
    email = input("Enter your email: ").strip().lower()

    users = load_users()
    if username in users:
        print("Username already registered.")
        return

    save_user(username, email)
    print(f"Registered {username} with email {email}.")

def login():
    username = input("Enter your username: ").strip().lower()
    users = load_users()
    if username not in users:
        print("Username not registered.")
        return

    email = users[username]
    code = generate_code()
    active_codes[username] = {"email": email, "code": code, "timestamp": time.time()}

    try:
        send_email(
            to_address=email,
            subject="Your Login Code",
            body=f"Your login code is: {code}\nIt expires in 5 minutes."
        )
        print(f"Code sent to {email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        return

    # Prompt immediately for code
    code_input = input("Enter the code sent to your email: ").strip()
    record = active_codes.get(username)

    if not record:
        print("No code stored. Try again.")
        return

    if time.time() - record["timestamp"] > CODE_EXPIRY:
        print("Code expired.")
        del active_codes[username]
        return

    if record["code"] != code_input:
        print("Incorrect code.")
        return

    print(f"Logged in as {username}!")
    exit(0)

def main():
    print("\nEmail Authenticator")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()