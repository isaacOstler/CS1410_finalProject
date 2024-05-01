from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from user import User
from kivy.app import App
from navBar import NavBar
from form import Frequency
from formQuestion import FormQuestion

class EditFormTemplateScreen(Screen):
    def on_pre_enter(self, *args):
        # get formManager from app
        formManager = App.get_running_app().formManager
        # get the form template we're editing
        self.form_template_id = App.get_running_app().editing_form_template_id
        try:
            form_template = formManager.get_form_template_by_id(self.form_template_id)
            self.ids.form_name_textInput.text = form_template.name
            self.ids.apparatus_textInput.text = form_template.apparatus.name
            self.frequency = form_template.frequency
            self.set_button_color()
            
            self.ids.form_fields.clear_widgets()
            for question in form_template.questions:
                formField = FormField(question)
                self.ids.form_fields.add_widget(formField)
        except Exception as e:
            print(e)
            # if we can't find the form template, go back to the form editor screen
            self.manager.current = 'form_editor_screen'

        self.ids.navbar.updateUser(self)
        return super().on_pre_enter(*args)
    
    def save_changes(self):
        formManager = App.get_running_app().formManager
        form_template = formManager.get_form_template_by_id(self.form_template_id)
        form_template.name = self.ids.form_name_textInput.text
        form_template.frequency = self.frequency
        form_template.apparatus.name = self.ids.apparatus_textInput.text
        formManager.write_form_template(form_template)
        self.manager.current = 'form_editor_screen'

    def setFrequency(self,frequency):
        self.frequency = Frequency[frequency]
        self.set_button_color()

    def set_button_color(self):
        white_color = (1, 1, 1, 1)
        blue_color = (0, 0.5, 1, 1)
        self.ids.daily_button.background_color = blue_color if self.frequency == Frequency.DAILY else white_color
        self.ids.weekly_button.background_color = blue_color if self.frequency == Frequency.WEEKLY else white_color
        self.ids.monthly_button.background_color = blue_color if self.frequency == Frequency.MONTHLY else white_color
        self.ids.yearly_button.background_color = blue_color if self.frequency == Frequency.YEARLY else white_color

    def add_field(self):
        formManager = App.get_running_app().formManager
        form_template = formManager.get_form_template_by_id(self.form_template_id)
        newQuestion = FormQuestion("New Field", "text", "Default Value")
        form_template.questions.append(newQuestion)
        formField = FormField(newQuestion)
        self.ids.form_fields.add_widget(formField)

class FormField(BoxLayout):
    def __init__(self, question: FormQuestion, **kwargs):
        super().__init__(**kwargs)
        self.form_template_id = App.get_running_app().editing_form_template_id
        self.question = question
        self.ids.field_name_textInput.text = question.label
        self.ids.field_type_spinner.text = question.type

    def remove_field(self):
        App.get_running_app().formManager.get_form_template_by_id(self.form_template_id).questions.remove(self.question)
        self.parent.remove_widget(self)

    def update_field_name(self):
        self.question.label = self.ids.field_name_textInput.text

    def update_field_type(self):
        self.question.type = self.ids.field_type_spinner.text