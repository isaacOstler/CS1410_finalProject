from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty
from kivy.app import App
from navBar import NavBar
from form import FormTemplate, Frequency
from apparatus import Apparatus
from kivy.uix.boxlayout import BoxLayout

class FormEditorScreen(Screen):
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
        forms = formManager.get_form_templates()
        for form in forms:
            self.ids.forms_list.add_widget(GUI_FormTemplateListItem(form))

    def add_form(self):
        formManager = App.get_running_app().formManager
        newForm = FormTemplate(
            "New Form",
            Apparatus("New Apparatus"),
            Frequency.WEEKLY,
            []
        )
        formManager.add_form_template(newForm)
        App.get_running_app().editing_form_template_id = newForm.template_id
        App.get_running_app().root.current = 'edit_form_template_screen'

class GUI_FormTemplateListItem(BoxLayout):
    form_name = StringProperty('')
    form_frequency = StringProperty('')
    form_apparatus = StringProperty('')

    def __init__(self, formTemplate: FormTemplate, **kwargs):
        super(GUI_FormTemplateListItem, self).__init__(**kwargs)
        self.form_name = formTemplate.name
        self.template_id = formTemplate.template_id
        self.form_frequency = Frequency(formTemplate.frequency).name
        self.form_apparatus = formTemplate.apparatus.name
        self.confirm_delete = False

    def edit_form(self):
        App.get_running_app().editing_form_template_id = self.template_id
        App.get_running_app().root.current = 'edit_form_template_screen'

    def delete_form(self):
        if self.confirm_delete:
            try:
                App.get_running_app().formManager.delete_form_template(self.template_id)
                self.parent.remove_widget(self)
            except Exception as e:
                print(e)
        self.confirm_delete = True
        self.ids.delete_button.text = "Confirm"
        self.ids.delete_button.background_color = (1, .6, .6, 1)
        pass