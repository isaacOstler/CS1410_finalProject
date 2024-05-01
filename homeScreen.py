from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from user import User
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
from navBar import NavBar

class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        # get formManager from app
        formManager = App.get_running_app().formManager
        formManager.generate_forms()
        self.ids.navbar.updateUser(self)
        self._draw_forms()
        return super().on_pre_enter(*args)
    
    def _draw_forms(self):
        formManager = App.get_running_app().formManager
        self.ids.forms_list.clear_widgets()
        forms = formManager.get_forms()
        for form in forms:
            self.ids.forms_list.add_widget(GUI_FormListItem(form))

class GUI_FormListItem(BoxLayout):
    form_name = StringProperty('')
    form_apparatus = StringProperty('')
    form_status = StringProperty('')
    form_status_color = ObjectProperty((1, 0, 0, 1))

    def __init__(self, form, **kwargs):
        super(GUI_FormListItem, self).__init__(**kwargs)
        self.form = form
        self.form_name = form.name
        self.form_apparatus = form.apparatus.name
        self.form_status = "Complete" if form.completed else "Incomplete"
        self.form_status_color = (0, 1, 0, 1) if form.completed else (1, 0, 0, 1)

    def view_form(self):
        App.get_running_app().viewing_form_id = self.form.form_id
        App.get_running_app().root.current = 'view_form_screen'