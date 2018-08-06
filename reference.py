
"""
Author : Chandra sekhar Polavarapu

"""
#Importing required libraries
import random  # https://docs.python.org/3.6/library/random.html
import sqlite3  # https://docs.python.org/3.6/library/sqlite3.html
import string  # https://docs.python.org/3.6/library/string.html
import re
import urllib.request, json
from sqlite3 import Error
from termcolor import colored,cprint #To print colored output in terminal

#Function That generates a password based on given length and the complexity
def generate_password(length: int, complexity: int) -> str:
    """Generate a random password with given length and complexity

    Complexity levels:
        Complexity == 1: return a password with only lowercase chars
        Complexity ==  2: Previous level plus at least 1 digit
        Complexity ==  3: Previous levels plus at least 1 uppercase char
        Complexity ==  4: Previous levels plus at least 1 punctuation char

    :param length: number of characters
    :param complexity: complexity level
    :returns: generated password
    """
    password = "" #initializing the password variable

    # validating the input variables
    if complexity <1 or complexity >4 or length <= 0:
        print("Invalid input...Please check your input numbers")
        return None
    elif complexity ==1 :
        print("Original Complexity at password genereation function is 1")
        s = string.ascii_lowercase
        password = password.join(random.sample(s,length)) #Random functio nthat generates a tandom string
        return password
    elif complexity ==2 :
        print("Original Complexity at password genereation function is 2")
        s = string.ascii_lowercase + string.digits
        password = password.join(random.sample(s,length))
        return password
    elif complexity == 3:
        print("Original Complexity at password genereation function is 3")
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase
        password = password.join(random.sample(s, length))
        return password
    elif complexity == 4:
        print("Original Complexity at password genereation function is 4")
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation
        password = password.join(random.sample(s, length))
        return password
    else:
        print("Invalid entry")
    pass

#Function that checks the password complexity level
#input: Password string
def check_password_level(password: str) -> int:
    """Return the password complexity level for a given password

    Complexity levels:
        Return complexity 1: If password has only lowercase chars
        Return complexity 2: Previous level condition and at least 1 digit
        Return complexity 3: Previous levels condition and at least 1 uppercase char
        Return complexity 4: Previous levels condition and at least 1 punctuation

    Complexity level exceptions (override previous results):
        Return complexity 2: password has length >= 8 chars and only lowercase chars
        Return complexity 3: password has length >= 8 chars and only lowercase and digits

    :param password: password
    :returns: complexity level
    """
    passwordLevel = 0
    regex = re.compile('[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]''')

    if(regex.search(password) is not None):
        return 4
    elif (any(i.isupper() for i in password)):
        return 3
    elif(any(i.isdigit() for i in password)):
        if (len(password) >= 8):  # checking overriding conditions
            print(colored('Complexity of the password has been overrided...!!!', 'blue', attrs=['reverse', 'blink']))
            return 3  # returning the changed result
        else:
            return 2

    elif (password.islower()):
        if(len(password)>=8): #checking overriding conditions
            print(colored('Complexity of the password has been overrided...!!!', 'blue', attrs=['reverse', 'blink']))
            return 2 #returning the changed result
        else:
            return 1
    return 0

    pass

#Function that creates a connection to the Sqlite database then calls the following functions like creating table and inserting data into it.
#Input: Path to the database
def create_user(db_path: str) -> None:  # you may want to use: http://docs.python-requests.org/en/master/
    """Retrieve a random user from https://randomuser.me/api/
    and persist the user (full name and email) into the given SQLite db

    :param db_path: path of the SQLite db file (to do: sqlite3.connect(db_path))
    :return: None
    """
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)

    # calling the function that retrieves a random user from the given api
    details = pull_user_from_api()

    #generating a random password with random number of digits betwen 6-12 and a random comlexity level between 1-4
    passcode = generate_password(random.randint(6, 12), random.randint(1, 4))

    #Printing random passwords complexity(This will not be stored in database.)
    print("\n ---------------------------------------- \n")
    print('Random Password is: ', passcode)
    complexity = check_password_level(passcode)
    print('Random password end complexity level is: ',complexity)

    #Calling the create new table function which creates a new table if not already exists
    create_table(conn)

    #inserting Full name and email to the table
    insertData(details[0],details[1],passcode, conn)
    print("row inserted")

    #Commiting all the data to make sure its stored on database permanantly.
    conn.commit()
    # closing the connection after committing the data.
    conn.close()

#Function that gets a random user from the given API
def pull_user_from_api():

    #url to fetch the random user
    uri = "https://randomuser.me/api/"
    with urllib.request.urlopen(uri) as url:
        data = json.loads(url.read().decode()) #it contains whole data in dictionary
        #locating first name, lasname and email in JSON and assigning them to varibles to return
        full_name = data['results'][0]['name']['first'] +" "+ data['results'][0]['name']['last']
        email = data['results'][0]['email']
        return full_name,email

#Function that creates a new table in database
def create_table(conn):

    nexusedge_table = """CREATE TABLE IF NOT EXISTS nexusDataBase(userName text NOT NULL, emailId text, password text);"""
    try:

        if conn is not None:
            c= conn.cursor()
            c.execute(nexusedge_table)
    except Error as e:
        print(e)
    pass

#function that inserts values to the database
def insertData(name,email,password,conn):
    insertUser = "INSERT INTO nexusDataBase(userName,emailId,password)  values (?,?,?);"
    cur = conn.cursor()
    cur.execute(insertUser, (name, email, password))
    conn.commit()
    #c.execute("""SELECT * FROM nexusDataBase""")
    # print(c.fetchall())  # priting values in database
    pass

#Main Script
def main():
    print("******************************************** \n Testing Basic functions and achieving first 5 functionalities in the challenge \n ********************************************")
    password = generate_password(5,1)
    print("the password is: ", password)
    if(password is not None):
        passwordLevel = check_password_level(password)
        print("Check password function says the password level is : ", passwordLevel)

    #create_user("Nexus_Edge_Interview_Database.sqlite")
    print("\n *********************************************** \n Point 6 in the challenge being executed from here \n***********************************************\n")
    #Implementing point 6 : randomly pickup a user from the API, generate a random password for it and save all the details in database

    for i in range(1,11): #10 users
        create_user("nexusDataBase.sqlite") #calling the function
        pass


if __name__ == "__main__":
    main()