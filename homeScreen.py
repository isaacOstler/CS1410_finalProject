from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty
from kivy.app import App
from navBar import NavBar

class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.navbar.updateUser(self)
        return super().on_pre_enter(*args)