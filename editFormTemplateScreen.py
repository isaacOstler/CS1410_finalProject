from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty
from kivy.app import App
from navBar import NavBar

class EditFormTemplateScreen(Screen):
    def on_pre_enter(self, *args):
        # get formManager from app
        formManager = App.get_running_app().formManager
        self.ids.navbar.updateUser(self)
        return super().on_pre_enter(*args)