# Womens-Safety-Protocol

Overview

The Women's Safety Protocol is a real-time emergency alert system designed to enhance women's safety. This Flask-based web application enables users to trigger an emergency alert, sending a distress message with location details to predefined contacts via WhatsApp. The system includes passcode verification to prevent false alerts and ensures repeated alerts if the situation persists.

Features

One-Click Emergency Activation: Instantly triggers emergency mode via the web interface.

Passcode Protection: Prevents unauthorized deactivation of alerts.

Automated WhatsApp Alerts: Sends emergency messages with live location details to multiple contacts.

Smart Location Selection: Randomly selects a predefined location within 200 meters to maintain privacy.

Sound Alerts: Plays an emergency alarm to alert people nearby.

Repeated Alerts: Continues sending messages every 20 seconds until deactivated.

Technologies Used

Flask: Backend framework for handling routes and application logic.

PyWhatKit: Automates WhatsApp messaging.

Threading: Manages timed alerts and repeating messages.

Pygame: Triggers emergency sound alerts.

HTML, CSS: Builds an interactive and visually appealing web interface.

Installation and Setup

Prerequisites

Ensure you have the following installed:

Python (>=3.7)

pip (Python package manager)

Google Chrome (for WhatsApp Web automation)

Steps

Clone the Repository:

git clone https://github.com/Abhinav-sbhat/womens-safety-protocol.git
cd womens-safety-protocol

Install Required Packages:

pip install flask pywhatkit pygame geopy

Run the Application:

python app.py

Access the Web Interface:
Open your browser and go to http://127.0.0.1:5000/.

How It Works

The user clicks the Activate Emergency button.

The system prompts the user to set a passcode.

The user must re-enter the passcode to confirm safety.

If the user fails to enter the correct passcode within 10 seconds, the system:

Plays an emergency sound.

Sends a WhatsApp alert with location details.

Continues sending messages every 20 seconds until deactivated.

The alert stops only when the correct passcode is entered.

File Structure

├── templates/
│   ├── index1.html  # Home page
│   ├── set_passcode.html  # Passcode setup page
│   ├── index3.html  # Passcode re-entry page
│   ├── passcode.html  # Success page after correct passcode entry
│   ├── alert.html  # Alert page after incorrect passcode entry
├── static/
│   ├── styles.css  # Custom styles for the web interface
├── app.py  # Main Flask application
├── README.md  # Project documentation
