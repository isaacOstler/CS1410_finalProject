from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from navBar import NavBar
from homeScreen import GUI_FormListItem

class RecordsScreen(Screen):
    def on_pre_enter(self, *args):
        App.get_running_app().viewing_form_from = 'records_screen'
        # get formManager from app
        self.ids.navbar.updateUser(self)
        self._draw_forms()
        return super().on_pre_enter(*args)
    
    def _draw_forms(self):
        formManager = App.get_running_app().formManager
        self.ids.forms_list.clear_widgets()
        forms = list(filter(lambda form: form.completed == True, formManager.get_forms()))
        for form in forms:
            self.ids.forms_list.add_widget(GUI_FormListItem(form))
        if len(forms) == 0:
            new_label = Label(text="No Records Submitted", size_hint_y=None, height=40)
            self.ids.forms_list.add_widget(new_label)