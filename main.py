from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from loginScreen import LoginScreen
from user import User
from name import Name

class HomeScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file("main.kv")
        Builder.load_file("login_screen.kv")
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(HomeScreen(name='home_screen'))
        return sm

def main():
    Config.set('graphics', 'resizable', False)
    Window.size = (500, 200)
    MainApp().run()

if __name__ == "__main__":
    main()