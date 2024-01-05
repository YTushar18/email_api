from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app) 

@app.route("/", methods=["GET"])
def index():
    return "hello world"


def validate_and_sanitize(data):

    required_fields = ['name', 'email', 'subject', 'message']
    
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing or empty value for {field}")
    
    validate_email(data['email'])
        
def validate_email(email):
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        raise ValueError("Invalid email address")



@app.route("/send", methods=["POST"])
def send():
    try:
        print(request.json)
        data = request.json
        validate_and_sanitize(data)
        email_name = request.json['name']
        email_address = request.json['email']
        email_subject = request.json['subject']
        email_message = request.json['message']

        sender_email = 'senders email address'
        sender_password = 'gmail app key'
        receiver_email = 'recievers eail address'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = email_subject
        email_message = email_name + f" ({email_address}) sent you an email with the message: " + email_message
        message.attach(MIMEText(email_message, 'plain'))

    
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)}), 400, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(port='5000', debug=True)