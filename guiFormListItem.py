from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from form import FormTemplate, Frequency
from kivy.app import App

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
        self.ids.delete_button.background_color = (1, 0, 0, 1)
        pass