from kivy.uix.screenmanager import Screen
from user import User
from kivy.properties import StringProperty
from kivy.app import App
from navBar import NavBar
from guiFormListItem import GUI_FormTemplateListItem

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