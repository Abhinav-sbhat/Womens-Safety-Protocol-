from flask import Flask, render_template, request, redirect, url_for
import threading
import pywhatkit as kit
import pygame
import time
import random

app = Flask(__name__)

user_passcode = None  
TIMEOUT = 10
emergency_active = False
danger_detected = False
alert_sent = False
timer = None
repeating_alert_timer = None 
message_loop_active = False  

PHONE_NUMBERS = ["+918431011609", "+918618266736"]

USER_LOCATIONS = [
    (12.878874661455884, 77.54463602878046),
    (12.880200, 77.544758),
    (12.879553, 77.545104),
    (12.880389, 77.543966)
]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/activate', methods=['POST'])
def activate():
    global emergency_active, alert_sent
    emergency_active = True
    alert_sent = False
    return redirect(url_for('set_passcode'))

@app.route('/set_passcode', methods=['GET', 'POST'])
def set_passcode():
    global user_passcode
    if request.method == 'POST':
        user_passcode = request.form['new_passcode']
        return redirect(url_for('reenter_passcode')) 
    return render_template('set_passcode.html')

@app.route('/reenter_passcode')
def reenter_passcode():
    global timer, alert_sent, message_loop_active
    if timer is None and not alert_sent:
        timer = threading.Timer(TIMEOUT, timeout_handler)
        timer.start()
    message_loop_active = True  
    return render_template('index3.html')

@app.route('/verify_reenter_passcode', methods=['POST'])
def verify_reenter_passcode():
    global danger_detected, timer, alert_sent, repeating_alert_timer, message_loop_active
    passcode = request.form['passcode']
    
    if passcode == user_passcode:
        danger_detected = False
        emergency_active = False
        message_loop_active = False  
        if timer is not None:
            timer.cancel()
            timer = None
        if repeating_alert_timer is not None:
            repeating_alert_timer.cancel() 
            repeating_alert_timer = None
        return render_template('passcode.html')
    else:
        if not alert_sent:
            danger_detected = True
            alert_sent = True
            if timer is not None:
                timer.cancel()
                timer = None
            play_emergency_sound()  
            return redirect(url_for('send_alert'))
        else:
            return render_template('alert.html')

def play_emergency_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(r'C:\Users\Abhinav S  Bhat\OneDrive\Desktop\5th sem Mini Project\activate message.mp3')
    pygame.mixer.music.play()

def timeout_handler():
    global alert_sent
    if not alert_sent:
        play_emergency_sound()  
        send_alert()

@app.route('/send_alert')
def send_alert():
    global danger_detected, alert_sent, repeating_alert_timer, message_loop_active
    danger_detected = True
    alert_sent = True

    selected_location = random.choice(USER_LOCATIONS)
    location_link = f"https://www.google.com/maps/search/?api=1&query={selected_location[0]},{selected_location[1]}"
    
    message = (
        f"⚠️ *Emergency Alert*\n\n"
        f"I am currently in a dangerous situation and urgently need assistance.\n\n"
        f"📍 *Location*: {location_link}\n\n"
        f"Please respond immediately or alert the authorities.\n"
        f"Thank you for your support.\n\n"
    )

    try:
        send_whatsapp_message_sequence(PHONE_NUMBERS, message)
        
        if emergency_active and message_loop_active:
            repeating_alert_timer = threading.Timer(20, send_alert)
            repeating_alert_timer.start()

        return render_template('alert.html')
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"

def send_whatsapp_message_sequence(phone_numbers, message, retries=3):
   
    initial_wait_time = 15  
    print(f"Waiting {initial_wait_time} seconds for WhatsApp Web to load...")
    time.sleep(initial_wait_time) 
    
    for i, number in enumerate(phone_numbers):
        print(f"Preparing to send message to {number}...")
        for attempt in range(retries):
            try:
                kit.sendwhatmsg_instantly(number, message, wait_time=10)
                print(f"Help Message successfully sent to {number}")
                
               
                print("Waiting 10 seconds before processing the next contact...")
                time.sleep(10)  
                break  
            except kit.core.exceptions.CallTimeException:
                
                print(f"Retry {attempt + 1}/{retries} for {number} due to load time issue.")
                time.sleep(5) 
            except Exception as e:
                print(f"Error sending message to {number}: {e}")
                break
    
    print("All messages processed.")

if __name__ == "__main__":
    app.run(debug=True)
