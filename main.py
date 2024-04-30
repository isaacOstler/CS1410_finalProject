from kivy.app import App
from kivy.lang import Builder
from user import User
from name import Name

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")

def main():
    MainApp().run()
    while True:
        # try to login
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            user = User.sign_in(username, password)
            print(f"Welcome {user.name.first}!")
            break
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()