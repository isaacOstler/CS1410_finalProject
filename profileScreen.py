from kivy.uix.screenmanager import Screen
from user import User
from kivy.app import App
from navBar import NavBar
from name import Name
from kivy.properties import StringProperty, BooleanProperty

class ProfileScreen(Screen):
    nameOfUser = StringProperty('')
    username = StringProperty('')
    rank = StringProperty('')
    is_admin = BooleanProperty(False)
    message = StringProperty('')

    def on_pre_enter(self, *args):
        self.ids.navbar.updateUser(self)
        user = App.get_running_app().signed_in_user
        self.nameOfUser = f'{user.name.last}, {user.name.first}, {user.name.middle}'
        self.username = user.username
        self.rank = user.rank
        self.is_admin = user.is_admin

        return super().on_pre_enter(*args)
    
    def cancel_profile(self):
        user = App.get_running_app().signed_in_user
        self.ids.name.text = f'{user.name.last}, {user.name.first}, {user.name.middle}'
        self.ids.username.text = user.username
        self.ids.rank.text = user.rank
        self.ids.admin.active = user.is_admin
        self.message = ''
    
    def save_profile(self):
        user = App.get_running_app().signed_in_user
        newName = user.name
        try:
            #if the text has one comma
            if self.ids.name.text.count(',') == 1:
                last, first = self.ids.name.text.split(',')
                newName = Name(last=last.strip(), first=first.strip())
            #if the text has two commas
            elif self.ids.name.text.count(',') == 2:
                last, first, middle = self.ids.name.text.split(',')
                newName = Name(last=last.strip(), first=first.strip(), middle=middle.strip())
            else:
                raise IndexError('Name must have one or two commas')
        except IndexError as e:
            self.message = 'Names must be in the format "Last, First" or "Last, First, Middle"'
            return
        
        if self.ids.password.text != self.ids.verify.text:
            self.message = 'Passwords do not match'
            return

        if len(self.ids.password.text) > 0:
            user.set_password(self.ids.password.text)

        self.message = ''
        user.name = newName
        user.username = self.ids.username.text
        user.rank = self.ids.rank.text
        user.is_admin = self.ids.admin.active
        user.save()
        self.ids.navbar.updateUser(self)
        self.manager.current = 'home_screen'
        self.ids.password.text = ''
        self.ids.verify.text = ''