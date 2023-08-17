import os
import pickle
import time
import getpass
import random
from PIL import Image 
import shutil
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

def Menu():
    while True:
        os.system('cls')
        print("\nHello,")
        print("==============================")
        print("This programm was made to help")
        print("You with learning")
        print("==============================")
        print("(0) Log in")
        print("(1) Create a new account")
        print("(2) Exit")
        choice = CheckInput()
        match choice:
            case 0:
                person = LogIn()
            case 1:
                person = NewAccountData()
            case 2:
                exit()
        if person == None:
            break
        StartingOptions(person)
        
def StartingOptions(person):
    while True:
        os.system('cls')
        print("========Choose========")
        print("(0) Create a new set")
        print("(1) Show all my sets")
        print("(2) Log out")
        print("(3) Show my profile")
        print("(4) Delete my profile")
        choice = CheckInput()
        match choice:
            case 0:
                person.CreateMySet()
            case 1:
                ShowAllMySets(person)
            case 2:
                break
            case 3:
                person.ShowProfileData()
            case 4:
                if not person.DeleteAccount():
                    break
               
def LogIn():
    os.system('cls')
    while True:
        list_of_users_out = []
        user = 0
        while True:
            try:
                if os.path.isfile("users_data.pkl"):
                    with open('users_data.pkl', 'rb') as users_data:
                        list_of_users_out = pickle.load(users_data)
                break
            except:
                user = None
                break
        if user == None:
            return user
        print("Enter your username:")
        username = input()
        os.system('cls')
        print("Enter your password:")
        password = getpass.getpass()
        for user in list_of_users_out:
            if username == user.username and password == user.password:
                os.system('cls')
                print("Welcome", user.name)
                time.sleep(2)
                return user
        os.system('cls')
        print("There is no such account")
        user = None 
        time.sleep(3)
        return user
def CheckInput():
    while True:
        try:
            choice = int(input())
            break
        except:
            print("Wrong input. Try again.")
    return choice
def NewAccountData():
    while True:
        os.system('cls')
        print("Enter your name:")
        name = input()
        os.system('cls')
        print("Enter your surname:")
        surname = input()
        os.system('cls')
        username = CheckUsername()
        if username == None:
            person = None
            break
        os.system('cls')
        email = CheckEmail()
        if email == None:
            person = None
            break
        os.system('cls')
        print("Enter your password:")
        password = IsPasswordStrong()
        person = User(name, surname, username, email, password)
        person.AddUserData()
        with open('users_data.pkl', 'wb') as users_data:
            pickle.dump(person.list_of_users, users_data)
        os.system('cls')
        print("Welcome", person.name)
        print("You've created an account")
        time.sleep(2)
        return person
def CheckUsername():
    print("Enter your username:")
    username = input()
    list_of_users_out = []
    list_of_usernames = []
    try:
        if os.path.isfile("users_data.pkl"):
            with open('users_data.pkl', 'rb') as users_data:
                list_of_users_out = pickle.load(users_data)
    except:
        pass
    for user in list_of_users_out:
        list_of_usernames.append(user.username)
    while username in list_of_usernames:
        print("This username is not available")
        print("(0) Choose a different username:")
        print("(1) Log into this account")
        choice = CheckInput()
        match choice:
            case 0:
                username = input()
            case 1:
                username = None
                return username
    return username        
def CheckEmail():
    print("Enter your email:")
    email = input()
    list_of_users_out = []
    list_of_emails = []
    try:
        if os.path.isfile("users_data.pkl"):
            with open('users_data.pkl', 'rb') as users_data:
                list_of_users_out = pickle.load(users_data)
    except:
        pass
    for user in list_of_users_out:
        list_of_emails.append(user.email)
    while email in list_of_emails:
        print("This e-mail has already an account")
        print("(0) Log into this account")
        print("(1) Choose a different e-mail")
        choice = CheckInput()
        match choice:
            case 0:
                email = None
                return None
            case 1:
                email = input()
    return email
def IsPasswordStrong():
    password = getpass.getpass()
    while len(password) < 8:
        print("Your password is too short. Try again: ")
        password = getpass.getpass()
    #check for ascii 
    print("Enter your password again:")
    passwordCheck = getpass.getpass()
    while password != passwordCheck:
        os.system('cls')
        print("\nPasswords aren't the same -- try again")
        print("\nEnter your password: ")
        password = getpass.getpass()
        print("\nEnter your password once again: ")
        passwordCheck = getpass.getpass()
    return password

class User:
    def __init__(self, name, surname, username, email, password):
        self.list_of_users = []
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.password = password
    def AddUserData(self):
        self.LoadPickle()
        self.list_of_users.append(self)
    def LoadPickle(self):
        try:
            if os.path.isfile("users_data.pkl"):
                with open('users_data.pkl', 'rb') as users_data:
                    self.list_of_users = pickle.load(users_data)
        except:
            pass
    def UpdatePickle(self):
        with open('users_data.pkl', 'wb') as users_data:
            pickle.dump(self.list_of_users, users_data)
    def DeleteAccount(self):
        while True:
            os.system('cls')
            print("========Choose=========")
            print("(0) Delete your account")
            print("(1) Return")
            choice = CheckInput()
            match choice:
                case 0:
                    listOfAllSets_out = []
                    print("\nTo delete your account enter your password:")
                    password = getpass.getpass()
                    self.LoadPickle()
                    for user in self.list_of_users:
                        if user.username == self.username and password == self.password:
                            self.list_of_users.remove(user)
                            try:
                                if os.path.isfile("sets_data.pkl"):
                                    with open('sets_data.pkl', 'rb') as sets_data:
                                        listOfAllSets_out = pickle.load(sets_data)
                            except:
                                pass
                            for set in listOfAllSets_out:
                                if set.owner.username == self.username:
                                    listOfAllSets_out.remove(set)
                            with open('sets_data.pkl', 'wb') as sets_data:
                                pickle.dump(listOfAllSets_out, sets_data)
                            self.UpdatePickle()
                            return False
                        while password != self.password:
                            os.system('cls')
                            print("Your password is incorrect. Try again:")
                            password = getpass.getpass()
                case 1:
                    break
    def ChangePassword(self):
        while True:
            os.system('cls')
            print("Enter your current password:")
            password =  getpass.getpass()
            while password != self.password:
                os.system('cls')
                print("(0) Return")
                print("Your current password is incorrect. Try again:")
                password = getpass.getpass()
                if password == "0":
                    break
            if password == "0":
                    break 
            os.system('cls')   
            print("Enter your new password:")
            newPassword = IsPasswordStrong()        
            self.LoadPickle()
            for user in self.list_of_users:
                if user.username == self.username and password == self.password:
                    user.password = newPassword
                    self.password = newPassword
                    self.UpdatePickle()
                    break
            break                      
    def ShowProfileData(self):
        while True:
            os.system('cls')
            print("This is your profile:")
            print("========================")
            print("Name:", self.name)
            print("Surname:", self.surname)
            print("Username:", self.username)
            print("E-mail:", self.email)
            print("========================")
            print("(0) Change your password")
            print("(1) Return")
            choice = CheckInput()
            match choice:
                case 0:
                    self.ChangePassword()
                case 1 :
                    break
    def CreateMySet(self):
        while True:
            os.system('cls')
            print("(0) Create new set")
            print("(1) Return")
            choice = CheckInput()
            match choice:
                case 0:
                    os.system('cls')
                    print("Enter name of your new set:")
                    setname = input()
                    dir = os.getcwd()
                    path = dir + '//' + setname
                    while os.path.exists(path) is True:
                        os.system('cls')
                        print("This name is in use. Try again:")
                        setname = input()
                        path = dir + '//' + setname
                    newSet = Sets(setname, self)
                    os.system('cls')
                    print("Will you use picters:")
                    print("(0) Yes")
                    print("(1) No")           
                    choice = CheckInput()
                    newSet.AddWords(setname, choice)
                    newSet.ShowNewSet()
                case 1:
                    break

class Sets:
    def __init__(self, name, owner):
        self.listOfAllSets = []
        self.listOfWords = []
        self.progressOfAll = []
        self.Images = []
        self.owner = owner
        self.name = name
    def LoadPickle(self):
        try:
            if os.path.isfile("sets_data.pkl"):
                with open('sets_data.pkl', 'rb') as sets_data:
                    self.listOfAllSets = pickle.load(sets_data)
        except:
            pass
    def UploadData(self):
        with open('sets_data.pkl', 'wb') as sets_data:
            self.listOfAllSets.append(self)
            pickle.dump(self.listOfAllSets, sets_data)
    def AddWords(self, setname, choice):
        word = 1
        while True:
            if word == "0":
                break
            self.LoadPickle()
            match choice:
                case 0:
                    while True:
                        os.system('cls')
                        parent_dir = os.getcwd()
                        directory = self.name
                        path = os.path.join(parent_dir, directory)
                        os.mkdir(path)
                        print("Check the directory where you saved this programm")
                        print("Add all pictures to your new folder", self.name)
                        print("When you are ready enter anything")
                        input()
                        break
                    while True:
                        os.system('cls')
                        print("=====Choose=================================")
                        print("(0) Save your set")
                        print("(1) Add a picture and a word with definition")
                        print("(2) Add just a word with definition")
                        print("============================================")
                        choice = CheckInput()
                        match choice:
                            case 0:
                                os.system('cls')
                                print("Saving a new set")
                                self.UploadData()
                                word = "0"
                            case 1:
                                print("(4) Return")
                                print("==========")
                                print("Add a word:")
                                word = input() 
                                print("Add a definition:")
                                definition = input()
                                print("Add a picture by entering its name (*.jpg for example -- they have to be unique!!):")
                                image = input()
                                dir = os.getcwd()
                                path = dir +'\\'+ setname + '\\'+image
                                path = os.path.join(dir,)
                                if image == "4" or word == "4" or definition == "4":
                                    break
                                while not os.path.exists(path):
                                    print("This image is not available. Try again:")
                                    image = input()
                                    if image == "4":
                                        break
                                self.listOfWords.append(Words(word, definition, image))
                            case 2:
                                print("(4) Return")
                                print("==========")
                                print("Add a word:")
                                word = input() 
                                print("Add a definition:")
                                definition = input()
                                if image == "4" or word == "4" or definition == "4":
                                    break
                                image = None
                                self.listOfWords.append(Words(word, definition, image))
                        if word == "0":
                            break
                case 1:
                    os.system('cls')
                    print("(0) Save your set")
                    print("=================")
                    print("Add a word:")
                    word = input() 
                    if word == "0":
                        os.system('cls')
                        print("Saving a new set")
                        self.UploadData()
                        break                             
                    print("Add a definition:")
                    definition = input()
                    self.listOfWords.append(Words(word, definition, None))
        
    def ShowNewSet(self):
        os.system('cls')
        print(self.name)
        print("======================")
        for words in self.listOfWords:
            print(words.word, "-", words.definition, "-", words.image)
        print("======================")
        time.sleep(2)
        ShowAllMySets(self.owner)


def ShowAllMySets(person):
        while True:
            os.system('cls')
            listOfAllSets_out = []
            MySets = []
            id = 0
            try:
                if os.path.isfile("sets_data.pkl"):
                    with open('sets_data.pkl', 'rb') as sets_data:
                        listOfAllSets_out = pickle.load(sets_data)
            except:
                print("You own 0 sets")
                print("=====Choose=====")
                print("(0) Return")
                print("(1) Create a set")
                choice = CheckInput()
                match choice:
                    case 0:
                        break
                    case 1:
                        person.CreateMySet()
            for set in listOfAllSets_out:
                if set.owner.username == person.username:
                    MySets.append(set)
            id = 0
            for set in MySets:
                print(id, "-", set.name)
                id=id+1 
            if len(MySets) == 0:
                print("You own 0 sets")
                print("=====Choose=====")
                print("(0) Return")
                print("(1) Create a set")
                choice = CheckInput()
                match choice:
                    case 0:
                        break
                    case 1:
                        person.CreateMySet()
                        break
            print("=====Choose=====")
            print("(0) Return")  
            print("(1) Learn a set")
            print("(2) Edit a set")
            print("(3) Delete a set")
            print("(4) Flash cards")
            choice = CheckInput()
            match choice:
                case 0:
                    break
                case 1:
                    while True:
                        print("Enter a number of a set you would like to learn:")
                        nr = CheckInput()
                        os.system('cls')
                        print(MySets[nr].name)
                        print("================")
                        id = 0
                        dir = os.getcwd()
                        path = dir +"\\"+MySets[nr].name 
                        for wordToLearn in MySets[nr].listOfWords:
                            if os.path.exists(path):
                                print(id, "-", wordToLearn.word, "-", wordToLearn.definition, "-", wordToLearn.image)
                            else:
                                print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
                            id = id + 1
                        print("======Choose======")
                        print("(0) Start learning")
                        print("(1) Return")
                        choice = CheckInput()
                        match choice:
                            case 0:
                                if not Learning(MySets[nr]):
                                    break
                            case 1:
                                break
                case 2:
                    while True:
                        os.system('cls')
                        id = 0
                        for set in MySets:
                            print(id, "-", set.name)
                            id=id+1  
                        print("=====Choose=====")
                        print("(0) Edit a set")
                        print("(1) Return")
                        choice = CheckInput()
                        match choice:
                            case 0:
                                while True:
                                    print("Enter a number of a set you would like to edit")
                                    nr = CheckInput()
                                    os.system('cls')
                                    id = 0
                                    print(MySets[nr].name)
                                    print("================")
                                    dir = os.getcwd()
                                    path = dir +"\\"+MySets[nr].name 
                                    for wordToLearn in MySets[nr].listOfWords:
                                        if os.path.exists(path):
                                            print(id, "-", wordToLearn.word, "-", wordToLearn.definition, "-", wordToLearn.image)
                                        else:
                                            print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
                                        id = id + 1
                                    print("=====Choose=====")
                                    print("(0) Edit")
                                    print("(1) Return")
                                    choice = CheckInput()
                                    match choice:
                                        case 0:
                                            if not OperatingOnSet(MySets[nr], person, listOfAllSets_out):
                                                break
                                        case 1:
                                            break
                            case 1:
                                break
                case 3:
                    DeleteSet(MySets, listOfAllSets_out)
                case 4:
                    while True:
                        print("Enter a number of a set you would like to learn:")
                        nr = CheckInput()
                        os.system('cls')
                        print(MySets[nr].name)
                        print("================")
                        id = 0
                        dir = os.getcwd()
                        path = dir +"\\"+MySets[nr].name 
                        for wordToLearn in MySets[nr].listOfWords:
                            if os.path.exists(path):
                                print(id, "-", wordToLearn.word, "-", wordToLearn.definition, "-", wordToLearn.image)
                            else:
                                print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
                            id = id + 1
                        print("======Choose======")
                        print("(0) Start learning flash cards")
                        print("(1) Return")
                        choice = CheckInput()
                        match choice:
                            case 0:
                                if not FlashCards(MySets[nr]):
                                    break
                            case 1:
                                break
def DeleteSet(MySets, listOfAllSets):
    while True:
        os.system('cls')
        id = 0
        for set in MySets:
            print(id, "-", set.name)
            id=id+1  
        print("=====Choose=====")
        print("(0) Delete a set")
        print("(1) Return")
        choice = CheckInput()
        match choice:
            case 0:
                while True:
                    print("Enter a number of a set you would like to delete:")
                    nr = CheckInput()
                    os.system('cls')
                    print(MySets[nr].name)
                    print("===============")
                    id = 0
                    for wordToLearn in MySets[nr].listOfWords:
                        print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
                        id = id + 1
                    print("=====Choose=====")
                    print("(0) Continue")
                    print("(1) Return")   
                    choice = CheckInput()
                    match choice:
                        case 0:
                            parent_dir = os.getcwd()
                            path = parent_dir+"\\"+MySets[nr].name
                            if os.path.exists(path):
                                shutil.rmtree(path)
                            listOfAllSets.remove(MySets[nr])
                            with open('sets_data.pkl', 'wb') as sets_data:
                                pickle.dump(listOfAllSets, sets_data)
                            return
                        case 1:
                            break
            case 1:
                break
def EditWord(MySet, listOfAllSets, person):
    while True:
        os.system('cls')
        for set in listOfAllSets:
            if set.name == MySet.name and set.owner.username == person.username and MySet.listOfWords == set.listOfWords:
                listOfAllSets.remove(set)
                break
        id = 0
        print(MySet.name)
        print("=============================")
        for wordToLearn in MySet.listOfWords:
            id = id + 1
            print(id, "-", wordToLearn.word, "-", wordToLearn.definition)  
        print("===Choose a word to edit===")
        print("(0) Return")
        nr = CheckInput()
        if nr == 0:
            listOfAllSets.append(MySet)
            with open('sets_data.pkl', 'wb') as sets_data:
                pickle.dump(listOfAllSets, sets_data)
            break
        else:
            print("=====Choose=====")
            print("(0) Return")
            print("(1) Continue")
            choice = CheckInput()
            match choice:
                case 0:
                    break
                case 1:
                    while True:
                        os.system('cls')
                        print(MySet.listOfWords[nr-1].word, "-", MySet.listOfWords[nr-1].definition)
                        print("=====Choose=====")
                        print("(0) Return")
                        print("(1) Edit a word")
                        print("(2) Edit a definition")
                        choice = CheckInput()
                        match choice:
                            case 0:
                                break
                            case 1:
                                while True:
                                    os.system('cls')
                                    print(MySet.listOfWords[nr-1].word)
                                    print("=====Enter a word======")
                                    print("(0) Return")
                                    word = input()
                                    if word == "0":
                                        break
                                    else:
                                        MySet.listOfWords[nr-1].word = word
                                        break
                            case 2:
                                while True:
                                    os.system('cls')
                                    print(MySet.listOfWords[nr-1].definition)
                                    print("=====Enter a definition=======")
                                    print("(0) Return")
                                    definition = input()
                                    if definition == "0":
                                        break
                                    else:
                                        MySet.listOfWords[nr-1].definition = definition
                                        break
            listOfAllSets.append(MySet)
            with open('sets_data.pkl', 'wb') as sets_data:
                pickle.dump(listOfAllSets, sets_data)
def AddWord(MySet, listOfAllSets, person):
    while True:
        os.system('cls')
        id = 0
        print(MySet.name)
        print("=============================")
        for wordToLearn in MySet.listOfWords:
            id = id + 1
            print(id, "-", wordToLearn.word, "-", wordToLearn.definition)  
        print("===Choose===")
        print("(0) Return")
        print("(1) Add a new word")
        choice = CheckInput()
        match choice:
            case 0:
                break
            case 1:
                os.system('cls')
                id = 0
                print(MySet.name)
                print("=============================")
                for wordToLearn in MySet.listOfWords:
                    id = id + 1
                    print(id, "-", wordToLearn.word, "-", wordToLearn.definition) 
                print("=============================")
                print("(0) Return")
                print("Add a word:")
                word = input()
                if word == "0":
                    break
                print("Add a definition:")
                definition = input()
                if definition == "0":
                    break 
                MySet.listOfWords.append(Words(word, definition, None))
                for set in listOfAllSets:
                    if set.name == MySet.name and set.owner.username == person.username and MySet.listOfWords == set.listOfWords:
                        listOfAllSets.remove(set)
                listOfAllSets.append(MySet)
                with open('sets_data.pkl', 'wb') as sets_data:
                    pickle.dump(listOfAllSets, sets_data)
def DeleteWord(MySet, listOfAllSets, person):
    id = 0
    print(MySet.name)
    print("=============================")
    for wordToLearn in MySet.listOfWords:
        print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
        id = id + 1
    print("===Choose a word to delete===")
    nr = CheckInput()
    for set in listOfAllSets:
        if set.name == MySet.name and set.owner.username == person.username and MySet.listOfWords == set.listOfWords:
            listOfAllSets.remove(set)
            break
    MySet.listOfWords.remove(MySet.listOfWords[nr])
    listOfAllSets.append(MySet)
    with open('sets_data.pkl', 'wb') as sets_data:
        pickle.dump(listOfAllSets, sets_data)
def OperatingOnSet(MySet, person, listOfAllSets):
    while True:
        os.system('cls')
        id = 0
        print(MySet.name)
        print("================")
        for wordToLearn in MySet.listOfWords:
            print(id, "-", wordToLearn.word, "-", wordToLearn.definition)
            id = id + 1
        print("=====Choose=====")
        print("(0) Delete a word")
        print("(1) Edit a word")
        print("(2) Add a word")
        print("(3) Return")
        choice = CheckInput()
        os.system('cls')
        match choice:
            case 0:
                DeleteWord(MySet, listOfAllSets, person)
            case 1:
                EditWord(MySet, listOfAllSets, person)
            case 2:
                AddWord(MySet, listOfAllSets, person)
            case 3:
                return False

def Learning(MySet):
    while True:
        listToLearn = MySet.listOfWords
        length = len(listToLearn)
        while len(listToLearn) != 0:
            length = len(listToLearn)
            id = random.randint(0,length-1)
            os.system('cls')
            print(listToLearn[id].definition)
            if listToLearn[id].image != None:
                dir = os.getcwd()
                path = dir + "\\"+MySet.name + "\\" + listToLearn[id].image
                img = Image.open(path)
                img.show()
            answer = input()
            if answer == listToLearn[id].word:
                prGreen("\tcorrect")
                listToLearn.remove(listToLearn[id])
                time.sleep(1)
            else:
                prRed("\tincorrect")
                print("The correct answer is:", listToLearn[id].word, "Is it correct? (0)Yes (1)No")
                choice = CheckInput()
                match choice:
                    case 0:
                        if listToLearn[id].image != None:
                            img = Image.close(path)
                        listToLearn.remove(listToLearn[id])
                    case 1:
                        while answer != listToLearn[id].word:
                            print("Type it now:")
                            answer = input()
        os.system('cls')
        print("\nYou finished your learning")
        print("(0) Return")
        choice = CheckInput()
        match choice:
            case 0:
                return False
def FlashCards(MySet):
    listToLearn = MySet.listOfWords
    while True:
        length = len(listToLearn)
        print("To show an answer type in any key and/or click enter")
        time.sleep(2)
        os.system('cls')
        while len(listToLearn) != 0:
            length = len(listToLearn)
            id = random.randint(0,length-1)
            os.system('cls')
            print(listToLearn[id].definition)
            if listToLearn[id].image != None:
                dir = os.getcwd()
                path = dir + "\\"+MySet.name + "\\" + listToLearn[id].image
                img = Image.open(path)
                img.show()
            input()
            print(listToLearn[id].word)
            prGreen("(0) I knew it")
            prRed("(1) Learn again")
            answer = CheckInput()
            if answer == 0:
                listToLearn.remove(listToLearn[id])
            elif answer == 1:
                pass
        os.system('cls')
        print("\nYou finished your falsh cards")
        print("(0) Return")
        choice = CheckInput()
        match choice:
            case 0:
                return False
class Words:
    def __init__(self, word, definition, image):
        self.word = word
        self.definition = definition
        self.image = image

while True:
    Menu()