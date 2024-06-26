## CS1410 Final Project
Final project for CS1410, Spring 2024

## Installation
To install this project, simply clone the repository and run the following command:
`python3 -m pip install -r requirements.txt`

## Usage
To use this project, run the following command:
`python3 main.py`
Please note, the default screen sizes might not work well on every monitor size.  The GUI should be responsive to resize however, so upon starting the program you may need to resize some of the windows for everything to fit on the screen.

## Guide
This project is a form-checkoff management system.  This is used to meet industry required check-offs at the beginning of a shift.  The system allows administrators to create forms, set the requirements for each form, and the frequency of how often a form must be completed.  The system also allows employees to log on and complete said forms.  After a form is submitted it will be locked and available for future review.  Administrators can create new users, and assign a password.  Each user has their own log-on, and when forms are submitted it will be tied to the user who filled it out.

## First Time Login
When you clone this repo, a default admin user is already setup.  The username is `test_user` and the password is `password`.  Feel free to create your own user and password in the user tab.

## Features
- Fully Customizable Forms
- Automatic Form Creation Based on Date/Time
- User Management
- Passwords hashed and salted using bcrypt
- Record Management

## UML diagram
![final_project_UML](https://github.com/isaacOstler/CS1410_finalProject/assets/30113240/e3460f7d-2235-47e0-83f8-df877d706a82)
