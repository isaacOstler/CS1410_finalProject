from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.app import App
from user import User
from kivy.uix.label import Label
from navBar import NavBar
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from name import Name

class UsersScreen(Screen):
    def on_pre_enter(self, *args):
        App.get_running_app().viewing_form_from = 'users_screen'
        users = User.get_all_users()
        self.ids.navbar.updateUser(self)
        self.ids.user_list.clear_widgets()
        for user in users:
            #get index of user
            index = users.index(user)
            self.ids.user_list.add_widget(GUI_UserRow(index % 2 == 0, user))
        return super().on_pre_enter(*args)

    def add_user(self):
        App.get_running_app().profile_edit_user = User(Name("New","User",""), "FF/EMT", "new_user", "password")
        App.get_running_app().root.current = 'profile_screen'
        return

class GUI_UserRow(BoxLayout):
    username = StringProperty('')
    rank = StringProperty('')
    role = StringProperty('')
    real_name = StringProperty('')
    background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, show_background, user, **kwargs):
        super().__init__(**kwargs)
        self.username = user.username
        self.rank = user.rank
        self.role = 'Admin' if user.is_admin else 'User'
        self.real_name = f'{user.name.last}, {user.name.first}, {user.name.middle}'
        self.confirmDelete = False
        if show_background:
            self.background_color = [0.1, 0.1, 0.1, 1]
        else:
            self.background_color = [0,0,0,0]
        self.user = user

    def edit_user(self):
        App.get_running_app().profile_edit_user = self.user
        App.get_running_app().root.current = 'profile_screen'
        return

    def delete_user(self):
        if self.confirmDelete:
            if self.user.id == App.get_running_app().signed_in_user.id:
                self.confirmDelete = False
                self.ids.delete_button.text = 'Delete'
                self.ids.delete_button.background_color = [1, 0, 0, 1]
                layout = GridLayout(cols = 1, padding = 10) 

                popupLabel = Label(text = "You cannot delete the user you are logged in as") 
                closeButton = Button(text = "Okay") 

                layout.add_widget(popupLabel) 
                layout.add_widget(closeButton)        

                # Instantiate the modal popup and display 
                popup = Popup(title ='Cannot Delete Yourself', 
                                content = layout, 
                                size_hint =(None, None), size =(700, 300))   
                popup.open()    

                # Attach close button press with popup.dismiss action 
                closeButton.bind(on_press = popup.dismiss) 
                return
            self.parent.remove_widget(self)
            User.delete_user(self.user.id)
        else:
            self.confirmDelete = True
            self.ids.delete_button.text = 'Confirm?'
            self.ids.delete_button.background_color = [1, .5, .5, 1]