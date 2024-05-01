from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition
from loginScreen import LoginScreen
from homeScreen import HomeScreen
from profileScreen import ProfileScreen
from formEditorScreen import FormEditorScreen
from editFormTemplateScreen import EditFormTemplateScreen
from navBar import NavBar
from kivy.properties import StringProperty
from user import User
from name import Name
from form import FormTemplate, Form, Frequency
from formQuestion import FormQuestion
from formManager import FormManager
from apparatus import Apparatus

class MainApp(App):
    user = StringProperty('')
    
    def build(self):
        #App.get_running_app().signed_in_user = User.get_user_by_id("b78da9da-e885-4ccf-8718-3372577fde4c")
        App.get_running_app().signed_in_user = User.get_user_by_id("920c33e2-bd0b-4837-a3fa-7079884ad513")
        App.get_running_app().formManager = FormManager()

        Builder.load_file("gui_form_template_list_item.kv")
        Builder.load_file("nav_bar.kv")
        Builder.load_file("edit_form_template_screen.kv")
        Builder.load_file("profile_screen.kv")
        Builder.load_file("form_editor_screen.kv")
        Builder.load_file("home_screen.kv")
        Builder.load_file("login_screen.kv")
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition(duration=0.18))
        sm.add_widget(FormEditorScreen(name='form_editor_screen'))
        sm.add_widget(EditFormTemplateScreen(name='edit_form_template_screen'))
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(ProfileScreen(name='profile_screen'))
        return sm

def main():
    # formManager.add_form_template(FormTemplate(
    #     "MA261 Weekly",
    #     Apparatus("MA261"),
    #     Frequency.WEEKLY,
    #     [
    #         FormQuestion("Ventilator", "boolean", 1),
    #     ]
    # ))
    # formManager.add_form_template(FormTemplate(
    #     "MA261 Monthly",
    #     Apparatus("MA261"),
    #     Frequency.MONTHLY,
    #     [
    #         FormQuestion("Suspension", "boolean", 1),
    #     ]
    # ))
    # formManager.add_form_template(FormTemplate(
    #     "MA261 Yearly",
    #     Apparatus("MA261"),
    #     Frequency.MONTHLY,
    #     [
    #         FormQuestion("State Inspection", "boolean", 1),
    #     ]
    # ))

    Config.set('graphics', 'resizable', False)
    Window.size = (800, 800)
    #Window.size = (500, 200)
    MainApp().run()

if __name__ == "__main__":
    main()