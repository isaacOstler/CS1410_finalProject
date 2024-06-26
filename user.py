from name import Name
import csv
import uuid
import bcrypt
import portalocker

''' A class that keeps track of a user.  Also has static methods for getting and saving users from a database.  If id is not specified a default GUID will be generated.  Passwords will be hashed using bcrypt.'''
class User:
    CONST_USER_FILE = 'users.csv'
    def __init__(self, name: Name, rank, username, password, is_admin: bool = False, id: str = "", hash_password: bool = True):
        if(not isinstance(name, Name)):
            raise TypeError("name must be a Name object")
        self.name = name
        self.rank = rank
        self.username = username
        if(id == ""):
            self.id = str(uuid.uuid4())
        else:
            self.id = str(id)
        if(not hash_password):
            self._hashed_password = password
        else:
            self._hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.is_admin = is_admin

    def __str__(self):
        return f"User #{self.id}: {str(self.name)}, ({self.rank})"
    
    # just a little helper function to save the user
    def save(self, callback = None):
        '''Saves the user to the database, equivalent to User.save_user(user)'''
        return User.save_user(self, callback)
    
    def set_password(self, password):
        '''Sets the password for the user'''
        self._hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod 
    def sign_in(username, password):
        '''Returns a user object if the username and password match a user in the database'''
        # find the user by username
        users = User.get_all_users()
        for user in users:
            if user.username == username:
                # check the password
                if bcrypt.checkpw(
                    password.encode('utf-8'), 
                    user._hashed_password.encode('utf-8')
                ):
                    return user
                else:
                    raise ValueError("Password Incorrect")
        raise ValueError("User not found")

    @staticmethod
    def get_all_users():
        ''' Reads the csv file users.csv and returns a list of users'''
        with open(User.CONST_USER_FILE, "r") as file:
            reader = csv.reader(file)
            users = []
            for row in reader:
                name = Name(row[0], row[1], row[2])
                rank = row[3]
                username = row[4]
                password = row[5]
                id = row[6]
                is_admin = row[7] == "True"
                users.append(User(name, rank, username, password, is_admin, id, hash_password=False))
            #close the file
            file.close()
            return users

    @staticmethod
    def get_user_by_id(id: str):
        ''' Gets a user by their id from the csv file users.csv'''
        users = User.get_all_users()
        for user in users:
            if str(user.id) == str(id):
                return user
        return None

    @staticmethod
    def save_user(user, callback = None):
        ''' Saves a user to the csv file users.csv'''
        users = User.get_all_users()
        # first check if the user is already in the list
        for i in range(len(users)):
            if users[i].id == user.id:
                users[i] = user
                break
        else:
            users.append(user)
        
        with open(User.CONST_USER_FILE, "w") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                writer = csv.writer(file)
                for user in users:
                    writer.writerow([user.name.first, user.name.last, user.name.middle, user.rank, user.username, user._hashed_password, user.id, user.is_admin])
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)
        if callback:
            callback()

    @staticmethod
    def delete_user(id: str,callback = None):
        ''' Deletes a user from the csv file users.csv'''
        users = User.get_all_users()
        userFound = False
        for i in range(len(users)):
            if users[i].id == id:
                users.pop(i)
                userFound = True
                break
        if(not userFound):
            raise ValueError("User not found")
        with open(User.CONST_USER_FILE, "w") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                writer = csv.writer(file)
                for user in users:
                    writer.writerow([user.name.first, user.name.last, user.name.middle, user.rank, user.username, user._hashed_password, user.id, user.is_admin])
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)
        if callback:
            callback()