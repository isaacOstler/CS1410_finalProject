from kivy.uix.boxlayout import BoxLayout
from user import User
from kivy.properties import StringProperty
from kivy.app import App
from kivy.core.window import Window

class NavBar(BoxLayout):
    username = StringProperty('')

    def updateUser(self, base_widget):
        user = App.get_running_app().signed_in_user
        self.username = user.username
        if not App.get_running_app().signed_in_user.is_admin:
            # disable non-admin buttons
            self.ids.form_editor.disabled = True
            self.ids.users.disabled = True
        else:
            # enable admin buttons
            self.ids.form_editor.disabled = False
            self.ids.users.disabled = False
        
        if App.get_running_app().root.current == 'home_screen':
            self.ids.home.state = 'down'

        if App.get_running_app().root.current == 'profile_screen':
            self.ids.profile.state = 'down'

        if App.get_running_app().root.current == 'form_editor_screen':
            self.ids.form_editor.state = 'down'

        return super().on_kv_post(base_widget)
    
    def goto_profile_screen(self):
        App.get_running_app().root.current = 'profile_screen'
        return

    def goto_form_editor_screen(self):
        user = App.get_running_app().signed_in_user
        if user.is_admin:
            App.get_running_app().root.current = 'form_editor_screen'

    def logout(self):
        App.get_running_app().signed_in_user = None
        self.username = ''
        Window.size = (500, 200)
        App.get_running_app().root.current = 'login_screen'
        return