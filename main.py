# main.py
from pymongo import MongoClient
import user
single="+-----------------------------------------------+"
double="================================================="
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def mainpage(db): #mainpage(db)
    choice = -1
    while(choice != '0'):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + double)
        print('\n'+'Welcome!'.center(49))
        print('Select Main Menu'.center(49))
        a = """      
                  +-----------+
                  | 1 SIGN IN | 
                  +-----------+

                  +-----------+
                  | 2 SIGN UP | 
                  +-----------+

                  +-----------+
                  | q  EXIT   | 
                  +-----------+

        """
        print(a)
        print(double)
        choice = input("Enter: ")
        clear()
        if choice=="1":
            user.signin(db)
        elif choice=="2":
            user.signup(db)
        elif choice == "q":
            print("BYE-!")
            return

if __name__ == "__main__":

    client=MongoClient()
    db=client.project
    mainpage(db)
    client.close()
    '''
    call mainpage()
    '''
