from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import App
from navBar import NavBar
from form import FormTemplate, Frequency, Form
from apparatus import Apparatus
from kivy.uix.boxlayout import BoxLayout

class ViewFormScreen(Screen):
    title = StringProperty('')
    subtitle = StringProperty('')
    apparatus = StringProperty('')
    message = StringProperty('')

    def on_pre_enter(self, *args):
        # get formManager from app
        try:
            formManager = App.get_running_app().formManager
            self.form = formManager.get_form_by_id(App.get_running_app().viewing_form_id)
            self.title = self.form.name
            human_readable_date = self.form.dateAssigned.strftime("%m/%d/%Y")
            self.subtitle = f"{human_readable_date} - Locked" if self.form.completed else human_readable_date
            if self.form.completed:
                self.message = "This form has been submitted and is locked."
            else:
                self.message = ""
            self.apparatus = self.form.apparatus.name
            self.ids.navbar.updateUser(self)

            self.ids.form_fields.clear_widgets()
            for question in self.form.questions:
                self.ids.form_fields.add_widget(Text_FormField(self.form.completed, question))

            return super().on_pre_enter(*args)
        except Exception as e:
            print(e)
            App.get_running_app().root.current = 'home_screen'

    def save_and_close(self):
        formManager = App.get_running_app().formManager
        formManager.save_form_to_file_system()
        App.get_running_app().root.current = 'home_screen'

    def complete(self):
        self.form.completed = True
        formManager = App.get_running_app().formManager
        formManager.save_form_to_file_system()
        App.get_running_app().root.current = 'home_screen'

class Text_FormField(BoxLayout):
    label = StringProperty('')
    value = StringProperty('')
    disabled = BooleanProperty(False)  

    def __init__(self, disabled, question, **kwargs):
        super(Text_FormField, self).__init__(**kwargs)
        self.question = question
        self.label = question.label
        self.value = question.value
        self.disabled = disabled

    def update_value(self, value):
        self.question.value = value