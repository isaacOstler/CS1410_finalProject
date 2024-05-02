from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from user import User
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
from navBar import NavBar

class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        App.get_running_app().viewing_form_from = 'home_screen'
        # get formManager from app
        formManager = App.get_running_app().formManager
        formManager.generate_forms()
        self.ids.navbar.updateUser(self)
        self._draw_forms()
        return super().on_pre_enter(*args)
    
    def _draw_forms(self):
        formManager = App.get_running_app().formManager
        self.ids.forms_list.clear_widgets()
        forms = list(filter(lambda form: form.completed == False, formManager.get_forms()))
        for form in forms:
            self.ids.forms_list.add_widget(GUI_FormListItem(form))
        if len(forms) == 0:
            new_label = Label(text="All Forms Completed", size_hint_y=None, height=40)
            new_form_button = Button(
                text="Design a New Form Template",
                size_hint_y=None,
                size_hint_x=None,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                height=60,
                width=450
            )
            new_form_button.bind(on_release=self.switch_to_form_editor)
            new_boxLayout = BoxLayout(orientation='vertical')
            new_boxLayout.add_widget(new_label)
            new_boxLayout.add_widget(new_form_button)
            new_boxLayout.size_hint_y = None
            new_boxLayout.height = 300
            new_stackLayout = StackLayout(orientation='lr-tb')
            new_stackLayout.add_widget(new_boxLayout)
            self.ids.forms_list.add_widget(new_stackLayout)
    
    def switch_to_form_editor(self, instance):
        # Change the current screen to the form editor screen
        App.get_running_app().root.current = 'form_editor_screen'

class GUI_FormListItem(BoxLayout):
    form_name = StringProperty('')
    form_apparatus = StringProperty('')
    form_status = StringProperty('')
    form_status_color = ObjectProperty((1, 0, 0, 1))
    form_date = StringProperty('')

    def __init__(self, form, **kwargs):
        super(GUI_FormListItem, self).__init__(**kwargs)
        self.form = form
        self.form_name = form.name
        self.form_apparatus = form.apparatus.name
        self.form_date = form.dateAssigned.strftime("%m/%d/%Y")
        self.form_status = "Complete" if form.completed else "Incomplete"
        self.form_status_color = (0, 1, 0, 1) if form.completed else (1, 0, 0, 1)

    def view_form(self):
        App.get_running_app().viewing_form_id = self.form.form_id
        App.get_running_app().root.current = 'view_form_screen'