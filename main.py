from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition
from loginScreen import LoginScreen
from homeScreen import HomeScreen
from profileScreen import ProfileScreen
from navBar import NavBar
from kivy.properties import StringProperty
from user import User
from name import Name

class MainApp(App):
    user = StringProperty('')
    
    def build(self):
        #App.get_running_app().signed_in_user = User.get_user_by_id("b78da9da-e885-4ccf-8718-3372577fde4c")
        App.get_running_app().signed_in_user = User.get_user_by_id("920c33e2-bd0b-4837-a3fa-7079884ad513")
        Builder.load_file("nav_bar.kv")
        Builder.load_file("profile_screen.kv")
        Builder.load_file("home_screen.kv")
        Builder.load_file("login_screen.kv")
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition(duration=0.18))
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(ProfileScreen(name='profile_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        return sm

def main():
    Config.set('graphics', 'resizable', False)
    Window.size = (800, 800)
    #Window.size = (500, 200)
    MainApp().run()

if __name__ == "__main__":
    main()