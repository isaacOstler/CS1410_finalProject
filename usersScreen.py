from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from navBar import NavBar

class UsersScreen(Screen):
    def on_pre_enter(self, *args):
        App.get_running_app().viewing_form_from = 'users_screen'
        # get formManager from app
        self.ids.navbar.updateUser(self)
        return super().on_pre_enter(*args)