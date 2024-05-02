from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty, BooleanProperty, ListProperty
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
                self.message = f"This form has been submitted and is locked.  Submitted by: {User.get_user_by_id(self.form.completed_by).username}"
            else:
                self.message = ""
            self.apparatus = self.form.apparatus.name
            self.ids.navbar.updateUser(self)
            self.ids.scroll.scroll_y = 1

            if self.form.completed:
                self.ids.complete_button.disabled = True
                self.ids.complete_button.text = "Completed"
            else:
                self.ids.complete_button.disabled = False
                self.ids.complete_button.text = "Complete"

            self.ids.form_fields.clear_widgets()
            for question in self.form.questions:
                # get index of question
                index = self.form.questions.index(question)
                match question.type:
                    case "Good / Bad":
                        self.ids.form_fields.add_widget(GoodBad_FormField(index % 2 == 0, self.form.completed, question))
                    case _:
                        self.ids.form_fields.add_widget(Text_FormField(index % 2 == 0, self.form.completed, question))

            return super().on_pre_enter(*args)
        except Exception as e:
            print(e)
            App.get_running_app().root.current = 'home_screen'

    def save_and_close(self):
        formManager = App.get_running_app().formManager
        formManager.save_form_to_file_system()
        App.get_running_app().root.current = App.get_running_app().viewing_form_from

    def complete(self):
        self.form.completed = True
        self.form.completed_by = App.get_running_app().signed_in_user.id
        formManager = App.get_running_app().formManager
        formManager.save_form_to_file_system()
        App.get_running_app().root.current = 'home_screen'

class Text_FormField(BoxLayout):
    label = StringProperty('')
    value = StringProperty('')
    disabled = BooleanProperty(False)
    background_color = ListProperty([1, 1, 1, 0.05])

    def __init__(self, show_background, disabled, question, **kwargs):
        super(Text_FormField, self).__init__(**kwargs)
        self.question = question
        self.label = question.label
        self.value = question.value
        self.disabled = disabled
        self.background_color = [1,1,1,0.05] if show_background else [1,1,1,0]

    def update_value(self, value):
        self.question.value = value

class GoodBad_FormField(BoxLayout):
    label = StringProperty('')
    value = StringProperty('')
    disabled = BooleanProperty(False)
    prompt = StringProperty('Select')
    prompt2 = StringProperty('Or')
    background_color = ListProperty([1, 1, 1, 0.05])

    def __init__(self, show_background, disabled, question, **kwargs):
        super(GoodBad_FormField, self).__init__(**kwargs)
        self.question = question
        self.label = question.label
        self.value = question.value
        self.disabled = disabled
        self.background_color = [1,1,1,0.05] if show_background else [1,1,1,0]
        self.update_button_color()

    def update_button_color(self):
        self.ids.good_button.background_color = [0, 1, 0, 1] if self.value == "Good" else [0.5, 0.5, 0.5, 1]
        self.ids.bad_button.background_color = [1, 0, 0, 1] if self.value == "Bad" else [0.5, 0.5, 0.5, 1]
        if self.value != "":
            self.prompt = ""
            self.prompt2 = ""
        else:
            self.prompt = "Select "
            self.prompt2 = "Or"

    def update_value(self, value):
        if not self.disabled:
            self.value = value
            self.question.value = value
            self.update_button_color()