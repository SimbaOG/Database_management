import time
import hashlib
import random
# import sqlite3  ---> Next Implementation?
# salt = os.urandom('32')


class UserData:

    @staticmethod
    def validate_actual_name(*names :str) -> bool:
        """
        :params: `name(s)` is the string of which we check if the `str` consists alphabets or not.
        even if 1 string is alphanumeric or numeric, false will be returned
        :return: `bool`
        """
        name_error = 0
        for name in names:
            # return True if name.isalpha() else False
            if not name.isalpha():
                name_error += 1
        if name_error > 0:
            return False
        else:
            return True

    @staticmethod
    def validate_uname(username :str) -> bool:
        """
        :params: username is a `str` with which we check if same `str` exists in the file or not
        """
        with open("userdata.txt", 'r') as datafile:
            global registering
            user_data = datafile.readlines()
            for id in user_data:
                yeah = id.split('\t')
                if username == yeah[0].strip('\n'):
                    if registering:
                        print("Username already exists! Try again!")
                    print()
                    return False
            else:
                print("Username does not exist!")
                return True

    @staticmethod
    def validate_mail(email: str) -> bool or str:
        """
        :params: email is a `str` with which we check if the `str` provided is an actual e-mail address or not
        """
        global email_char
        if email_char in email:
            e_length = len(email)
            if e_length > 4 and (email[e_length - 4:].casefold() == '.com' or email[e_length - 3:].casefold() == '.in'):
                with open("userdata.txt", 'r') as datafile:
                    data_user = datafile.readlines()
                    # data_user_clean = []  # redundant method, not storing.
                    for id in data_user:
                        # print(f"ID: {id}")  # TODO: Debugging
                        # print(type(id)) # Type -> str
                        yeah = id.split('\t')
                        # print(yeah)
                        if email == yeah[1].strip('\n'):
                            print("Email already exists! Try again!") # TODO: Dedbugging
                            print()
                            return False
                    else:
                        print("Email does not exist!")  # TODO: Debugging
                        return True
            else:
                print("Not a valid e-mail address!")
        else:
            # raise ValueError("Not a valid email address!")
            print("Not a valid email address! Please make sure to use '@' while entering an e-mail address")
            # show_menu
        
    @staticmethod
    def validate_data(username, email, password1, password2, firstname, lastname):
        global validated_data
        # if validated_data == False:
        if len(password1) >= 8:
            if password1 == password2:
                if UserData.validate_mail(email):
                    if UserData.validate_uname(username):
                        if UserData.validate_actual_name(firstname, lastname):
                            validated_data = True
                            UserData.storing_data_to_file(username, email, password1, password2, firstname, lastname)
                        else:
                            print("Invalid First/Last Name!")
                        # else:
                        #     print("The username you entered already exists!") # Redundant/no use
            else:
                print("Passwords do not match!")
            # else:
                # print("Data already verified!")
        else:
            print("Password should be atleast 8 or more characters")

    @staticmethod
    def hash_password(pwd, username):
        start = time.time()
        global salt
        key = hashlib.pbkdf2_hmac('sha256',
        pwd.encode('utf-8'),
        bytes(salt),
        100000,
        dklen=128)
        # with open(f"c:/Users/User/MyProject/user_hashes/{username}.txt", "w") as user_pass:
        #      print(key, file=user_pass)
        end = time.time()
        print(f"HASHING TOOK >>>>>>>>>>> {end-start}")
        return key

    @staticmethod
    def storing_data_to_file(username, email, password1, password2, firstname, lastname):
        start = time.time()
        if validated_data:
            global store_count
            global salt
            with open("userdata.txt", 'a+') as datafile:
                print(f"{username}\t{email}\t{UserData.hash_password(password1, username)}\t{UserData.hash_password(password2, username)}\t{firstname}\t{lastname}\t{salt}",
                file=datafile)
                print("Data saved!") # TODO: debugging
                store_count += 1
                # validated_data = False
                end = time.time()
                print(f"STORING TOOK >>>>>>>>>>> {end-start}")

    def __init__(self, username, email, password1, password2, firstname, lastname):
        self.username = username
        self.email = email
        self.password1 = password1
        self.password2 = password2
        self.firstname = firstname
        self.lastname = lastname 
        UserData.validate_data(username, email, password1, password2, firstname, lastname)


class UserLogin:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        UserData.validate_uname(username)
        if not UserData.validate_uname(username):
            UserLogin.validate_password(username, password)

    @staticmethod
    def validate_password(username, pwd):
        global salt
        with open(f"userdata.txt", 'r') as user_hash:
            user_data = user_hash.readlines()
            for fields in user_data:
                # print(fields) # str type, remove the entry field though ^_^
                yeah = fields.split('\t')
                if username == yeah[0]:
                    old_key = yeah[2]
                    old_salt = yeah[6].strip('\n')
                    break
            old_s_int = int(old_salt)
            crr_salt = bytes(old_s_int)
            new_key = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), crr_salt, 100000, dklen=128)
            if old_key == str(new_key):
                show_menu()
            else:
                print("Invalid Credentials!")
                print("Try Again!")
                time.sleep(3)
                show_menu_2()

def register_user():
    un = input("Username: ")
    em = input("Email: ")
    p1 = input("Password: ")
    p2 = input("Please re-enter your password: ")
    fn = input("Your first name: ")
    ln = input("Your last name: ")
    UserData.validate_data(un, em, p1, p2, fn, ln)

def start_script():
    initiate = ""
    while initiate != 'n':
            initiate = input("Start adding data to the database? (y for yes, n for no) ")
            if initiate == 'n':
                return_to_main()
                break
            elif initiate == 'y':
                un = input("Username: ")
                em = input("Email: ")
                p1 = input("Password: ")
                p2 = input("Please re-enter your password: ")
                fn = input("Your first name: ")
                ln = input("Your last name: ")
                UserData.validate_data(un, em, p1, p2, fn, ln)
            else:
                print("Invalid Input!")
                initiate = input("> ")
            time.sleep(3)
            initiate = input("Would you like to add more data to database? (y for yes, n for no) ")
            if initiate == 'n':
                return_to_main()
    else:
        if store_count > 0:
            print("Data added successfully!")


def format_data(field1, field2, field3, field4, master_length=20):
    global start_view
    print("_" * 109)
    cent_uname = "Username".center(master_length)
    cent_email = "E-Mail".center(master_length)
    cent_fname = "First Name".center(master_length)
    cent_lname = "Last Name".center(master_length)
    print(f"|   {cent_uname}   |   {cent_email}   |   {cent_fname}   |   {cent_lname}   |")
    print("_" * 109)

    for i in range(0, len(field1)):
        if len(field1[i]) < master_length:
            centered_uname = field1[i].center(master_length)
        else:
            centered_uname = "MAX_LENGTH".center(master_length)

        if len(field2[i]) < master_length:
            centered_email = field2[i].center(master_length)
        else:
            centered_email = "MAX_LENGTH".center(master_length)

        if len(field3[i]) < master_length:
            centered_fname = field3[i].center(master_length)
        else:
            centered_fname = "MAX_LENGTH".center(master_length)

        if len(field4[i]) < master_length:
            centered_lname = field4[i].center(master_length)
        else:
            centered_lname = "MAX_LENGTH".center(master_length)

        print(f"|   {centered_uname}   |   {centered_email}   |   {centered_fname}   |   {centered_lname}   |")
        print("-" * 109)
    print(f"Total Entries: {len(field1)}")
    end_view = time.time()
    print(f"VIEWING TOOK >>>>>>>>> {end_view - start_view}")
    return_to_main(12)


def return_to_main(times=9):
    print()
    for i in range(times, -1, -1):
        if i > 9:
            time.sleep(1)
            print(f"Returning to main menu in... {i}", end='\r')
        if i < 10:
            
            time.sleep(1)
            print(f"Returning to main menu in... 0{i}", end='\r')
    show_menu()


def view_data():
    global start_view
    start_view = time.time()
    usernames = []
    emails = []
    firstnames = []
    lastnames = []
    with open("userdata.txt", 'r') as user_data:
        user_list = user_data.readlines()
        # print(user_list)

        for fields in user_list:
            # print(fields) # str type, remove the entry field though ^_^
            yeah = fields.split('\t')
            usernames.append(yeah[0].strip('\n'))
            emails.append(yeah[1].strip('\n'))
            firstnames.append(yeah[4].strip('\n'))
            lastnames.append(yeah[5].strip('\n'))
        print()
        print("Displaying User Data....")
        format_data(usernames, emails, firstnames, lastnames)
        # return_to_main()
        # TODO: PRINTING THE MENU!!!!!!!!!!!


def delete_users_by_name():
    user_to_delete = input("Please input the username you have to delete: ")
    line_number: int
    positive = False
    with open("userdata.txt", 'r') as user_data:
        data_list = user_data.readlines()
        for number, data in enumerate(data_list):
            word_fix = data.split('\t')
            # print(word_fix)
            if user_to_delete in word_fix[0].strip('\n'):
                # print("woohoo")
                line_number = number
                positive = True
                break
        # print(line_number)
    if positive:
        with open("userdata.txt", 'w') as user_data:
            del data_list[line_number]
            for lines in data_list:
                user_data.write(lines)
            print(f"{user_to_delete}'s entry deleted!")
        return_to_main()
    else:
        print(f"No records found for: {user_to_delete} in USERNAME")
        return_to_main()
                

def delete_users_by_mail():
    user_to_delete = input("Please input the email you have to delete: ")
    line_number: int
    positive = False
    with open("userdata.txt", 'r') as user_data:
        data_list = user_data.readlines()
        for number, data in enumerate(data_list):
            word_fix = data.split('\t')
            # print(word_fix)
            if user_to_delete in word_fix[1].strip('\n'):
                # print("woohoo")
                line_number = number
                positive = True
                break
        # print(line_number)
    if positive:
        with open("userdata.txt", 'w') as user_data:
            del data_list[line_number]
            for lines in data_list:
                user_data.write(lines)
    else:
        print(f"No records found for: {user_to_delete} in E-MAILS")
        return_to_main()
        

def delete_users_menu():
    print("Delete Users from Database: ")
    print("Delete By:")
    for i in range(0, len(search_method_count)):
        print(f"{search_method_count[i]}:\t {search_method[i]}")
    print("0:\t Go back to main menu")
    user_inp = input("> ")
    delete_switch(user_inp)

def user_search():
    user_to_find = input("Please enter the username you have to find: ")
    positive = False
    suggest_user = []
    suggestions = False
    with open("userdata.txt", 'r') as user_data:
        data_list = user_data.readlines()
        for number, data in enumerate(data_list):
            word_fix = data.split('\t')
            # print(word_fix)
            if user_to_find == word_fix[0].strip('\n'):
                # print("woohoo")
                line_number = number
                positive = True
            if user_to_find.casefold() in word_fix[0].strip('\n').casefold():
                suggest_user.append(word_fix[0].strip('\n'))
                suggestions = True
    if positive:
        print(f"{user_to_find} found at ---> line no. {line_number + 1}")
        return_to_main()
    else:
        # print(f"{user_to_find} not found!")
        print(f"{user_to_find}  NOT FOUND!")
        if suggestions and len(user_to_find) > 3:
            print(f"Are you looking for {random.choice(suggest_user)}?")
        return_to_main()


def login_page():
    print("Please enter your credenials: ")
    u_name = input("Username: ")
    passwd = input("Password: ")
    print("Please wait... Verifying your details...")
    UserLogin(u_name, passwd)


if __name__ == '__main__':
    start_view = 0
    salt = random.randint(1, 100000)
    print(f"SALT >>>>>>>>>>>>>>> {salt}")
    registering = False
    validated_data = False
    email_char = "@"
    store_count = 0
    options = ["Add an entry", "View the data", "Remove an entry", "Search a user"]
    options_count = [str(i) for i in range(1, len(options) + 1)]
    search_method = ["Username", "E-mail"]
    search_method_count = [str(i) for i in range(1, len(search_method) + 1)]
    main_options = ["Login", "Register"]
    main_options_count = [str(i) for i in range(1, len(main_options) + 1)]
    # print(f"SEARCH METHODS: {search_method_count}") #TODO: DEBUG
    # # Initializing the number of options
    # for i in range(1, len(options) + 1):
    #     options_count.append(str(i))
    # print(options_count)

    def delete_switch(arg):
        if arg != '0':
            if arg not in search_method_count:
                print("Invalid Option!")
                print()
                time.sleep(2)
                delete_users_menu()
            else:
                options = {
                    '1': "delete_users_by_name()",
                    '2': "delete_users_by_mail()",
                }
                eval(options.get(arg, "Invalid Option!"))
        else:
            time.sleep(3)
            show_menu()

    # ******************
    def switcher(argument):
        if argument != '0':
            if argument not in options_count:
                print("Invalid Option!")
                print()
                time.sleep(2)
                show_menu()
            else:
                selections = {
                    '1': "start_script()",
                    '2': "view_data()",                  
                    '3': "delete_users_menu()",
                    '4': "user_search()"
                }
                eval(selections.get(argument, "Invalid Option!"))
        else:
            print("Thank you!")
    # *****************************************************************************************************

    def main_switcher(arg):
        if arg != '0':
            if arg not in main_options_count:
                print("Invalid Option!")
                print()
                time.sleep(2)
                show_menu_2()
            else:
                selections = {
                    '1': "login_page()",
                    '2': "register_user()"
                }
                eval(selections.get(arg, "Invalid Option!"))
        else:
            print("Thank you!")
        

    # ***** SHowing the menu******************


    def show_menu():
        print("Welcome to our Database Management System! What would you like to do?\r")
        for i in range(0, len(options)):
            print(f"{options_count[i]}: \t{options[i]}")
        print("0: \tTo Quit")
        u_input = input("> ")
        # print(u_input)
        # print(type(u_input))
        # function_to_call = selctions[u_input]
        switcher(u_input)
        # start_script()
        # user1 = UserData("a", "c@", "c", "c", "e", "f")
        # # user1.validate_mail("b@") #  TODO:Debbugging
        # # user1.validate_data("a", "a", "c@")
        # # user1.storing_data_to_file("a", "b", "c", "d", "e", "f")
    
    # show_menu()
    def show_menu_2():
        print("Please choose an option: ")
        for i in range(0, len(main_options)):
            print(f"{main_options_count[i]}: \t{main_options[i]}")
        print("0: \tTo Quit")
        user_inp = input("> ")
        main_switcher(user_inp)

    show_menu_2()