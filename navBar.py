from kivy.uix.boxlayout import BoxLayout
from user import User
from kivy.properties import StringProperty
from kivy.app import App

class NavBar(BoxLayout):
    username = StringProperty('')
    
    def __init__(self, **kwargs):
        super(NavBar, self).__init__(**kwargs)
        self.username = App.get_running_app().username