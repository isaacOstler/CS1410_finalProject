from name import Name
import csv

''' A class that keeps track of a user.  Also has static methods for getting and saving users from a database'''
class User:
    def __init__(self, name: Name, rank, username, id: str, isAdmin: bool = False):
        if(not isinstance(name, Name)):
            raise TypeError("name must be a Name object")
        self.name = name
        self.rank = rank
        self.username = username
        self.isAdmin = isAdmin
        self.id = str(id)

    def __str__(self):
        return f"User #{self.id}: {str(self.name)}, ({self.rank})"
    
    @staticmethod
    def _read_csv():
        ''' Reads the csv file users.csv and returns a list of users'''
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            users = []
            for row in reader:
                name = Name(row[0], row[1], row[2])
                users.append(User(name, row[3], row[4], row[5], bool(row[6])))
            return users

    @staticmethod
    def get_user_by_id(id: str):
        ''' Gets a user by their id from the csv file users.csv'''
        users = User._read_csv()
        for user in users:
            if str(user.id) == str(id):
                return user
        return None

    @staticmethod
    def save_user(user):
        ''' Saves a user to the csv file users.csv'''
        users = User._read_csv()
        # first check if the user is already in the list
        for i in range(len(users)):
            if users[i].id == user.id:
                users[i] = user
                break
        else:
            users.append(user)
        with open("users.csv", "w") as file:
            writer = csv.writer(file)
            for user in users:
                writer.writerow([user.name.first, user.name.last, user.name.middle, user.rank, user.username, user.id, user.isAdmin])

    @staticmethod
    def delete_user(id: str):
        ''' Deletes a user from the csv file users.csv'''
        users = User._read_csv()
        userFound = False
        for i in range(len(users)):
            if users[i].id == id:
                users.pop(i)
                userFound = True
                break
        if(not userFound):
            raise ValueError("User not found")
        with open("users.csv", "w") as file:
            writer = csv.writer(file)
            for user in users:
                writer.writerow([user.name.first, user.name.last, user.name.middle, user.rank, user.username, user.id, user.isAdmin])