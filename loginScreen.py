from kivy.uix.screenmanager import Screen
from user import User
from kivy.clock import Clock
from kivy.core.window import Window

class LoginScreen(Screen):
    def sign_in(self, username:str = "", password:str = ""):
        # bcrypt by it's nature takes a little bit to hash the password,
        # so we should let the user know it's going to take a second and that
        # the button click was registered.  We can do this by scheduling the
        # sign_in_process function to run at the start of the next frame, and
        # disabling the button and changing the text to "Logging in..." on this frame.
        def sign_in_process(dt):
            login_success = False
            try:
                #try to log in
                user = User.sign_in(username, password)
                #success
                self.ids.message.text = f"Welcome {user.name.first}!"
                #change to the next screen
                login_success = True
            except ValueError as e:
                #login failed
                self.ids.message.text = str(e)
            # these need to be outside the try catch block, otherwise if there's an error
            # any point after a successful login the catch block will still execute, even
            # if the error was not related to the login process
            if login_success:
                Window.size = (800, 800)
                self.manager.current = "home_screen"
            else:
                #restore functionality to the login button
                self.ids.login_button.disabled = False
                self.ids.login_button.text = "Login"
        
        # Disable login button and set text while logging in
        self.ids.login_button.disabled = True
        self.ids.login_button.text = "Logging in..."
        # Schedule the sign_in_process function to run at the start of the next frame
        Clock.schedule_once(sign_in_process, 0)