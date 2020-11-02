# user.py
import post
import follow
import hashtag
import os
import main

single="+-----------------------------------------------+"
double="================================================="

class userinstance:

    def __init__(self,db,userid):
        self._id=userid
        self.document=db.member.find_one({'_id':self._id})

    def update(self):
        self.document=db.member.find_one({'_id':self._id})
        return self.document

    def mystatus(self):
        user=self.update()
        print("\n" + single)
        user = db.member.find_one({'_id': user['_id']})
        print('\n' + 'My Status'.center(49))
        print('ID : ' + user['_id'])
        print('Name : ' + user['name'])
        try:
            print('Profile : ' + user['profile'])
        except:
            print('Profile : None')
        print('Followers : ' + str(len(user['follower'])))
        print('Followings : ' + str(len(user['following'])))
        print("\n" + single)

def signup(db):
    print("\n"+double)
    a = """      
                  +-----------+
                  | 2 SIGN UP | 
                  +-----------+
                    """



    print("\n"+a)
    print("\n1. ID must be at least 2 characters")
    print("2. Password must be at least 4 characters")
    print("3. If you want to quit the sign-up menu, ")
    print("   enter 'q' as ID or password")
    print("\n"+double)
    while (True):
        userid=input("ID : ")
        if userid=='q':
            return
        elif len(userid)<2:
            print("Invaid ID... try again\n")
            continue
        username=input("name : ")
        pw=input("password : ")
        if pw == 'q': return
        ensure=input("password once more: ")
        while pw!=ensure or len(pw)<4 :
            print("\nInvalid password... try again")
            pw=input("password : ")
            if pw=='q':return
            ensure=input("password once more: ")
        break
    try:
        while (True):
            rusure=input('Are U Sure? (Yes:y/No:n/Quit:q) :')
            if rusure=='y':break #while문을 나가서 signin메뉴로 이어지게
            elif rusure=='n':signup(db) #signup메뉴를 다시 불러들임
            elif rusure=='q':return #signup 함수를 종료하고 메인메뉴로 돌아감
        db.member.insert({'_id':userid,'name':username,'password':pw,'pnumber':0,\
                         'follower':[],'following':[],'block':[],'mylikes':[]})
    except:
        main.clear()
        print('ID already taken. Please input new ID')
        signup(db)
    main.clear()
    print('Successfully signed up!')
    signin(db) #로그인 성공시 signin 메뉴로 바로 이어진다
    '''
    1. Get his/her information.
    2. Check if his/her password equals confirm password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''

def signin(db):
    while(True):
        a = """      
                  +-----------+
                  | 1 SIGN IN | 
                  +-----------+
                """
        print(a)
        print(double)
        print("(Press q to quit)")
        userid=input("                  ID : ")
        if userid=='q':return
        pw=input("                  password : ")
        if pw=='q':return
        user=db.member.find_one({'_id':userid,'password':pw})
        if user!=None:break
        else:
            main.clear()
            print("Log-in failed! Try again")
    print("Successfully logged in!")
    main.clear()
    userpage(db,user)
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''

def userpage(db, user,addstring=""):
    menu_num = -1
    while(menu_num != '0'):
        main.clear()
        user = db.member.find_one({'_id': user['_id']})
        if addstring=="":pass
        else:print(addstring)
        print("\n" + double)
        welcomeyou="Welcome %s"%user['name']
        print("\n"+welcomeyou.center(49))
        print("Select User Menu".center(49))
        print()
        print("+------------+------------------+-------------+")
        print("| 1 Status   | 2   Newsfeed     | 3  My wall  |")
        print("+------------+------------------+-------------+")
        print("| 4 Explore  | 5    Follow      | 6 Unfollow  |")
        print("+------------+------------------+-------------+")
        print("| 7  Hash#   | 8 Delete account | 9  My likes |")
        print("+------------+------------------+-------------+")
        print("| q LOG OUT  |")
        print("+------------+")
        print()
        print("\n" + double)
        menu_num = input("Enter : ")
        switcher = {
            'q' : log_out,
            '1' : mystatus,
            '2' : post.newsfeed,
            '3' : post.postInterface,
            '5' : follow.follow,
            '6' : follow.unfollow,
            '8' : delacc,
            '7' : hashtag.hashtag,
            '9' : post.showlikes,
            '4' : explore
        }
        selected_func = switcher.get(menu_num, print_wrong)
        a=selected_func(db,user)
        if  a:return

def delacc(db,user):
    if input("Do you really want to delete your account?? (Yes:y, Quit:q) : ")=='y':
        if input("Are U sure? (Yes:y) : ")=='y':
            user = db.member.find_one({'_id': user['_id']})
            db.member.remove({'_id':user['_id']})
            db.member.update({'following':user['_id']},{'$pull':{'following':user['_id']}})
            db.member.update({'follower': user['_id']}, {'$pull': {'follower': user['_id']}})
            db.member.update({'block': user['_id']}, {'$pull': {'block': user['_id']}})
            print("You have deleted your account")
            return True
    return False

def printstatus(db,user):
    print("\n" + single)
    user = db.member.find_one({'_id': user['_id']})
    print('\n' + 'My Status'.center(49))
    print('ID : ' + user['_id'])
    print('Name : ' + user['name'])
    try:
        print('Profile : ' + user['profile'])
    except:
        print('Profile : None')
    print('Followers : ' + str(len(user['follower'])))
    print('Followings : ' + str(len(user['following'])))
    print("\n" + single)

def mystatus(db, user):
    while(True):
        main.clear()
        user = db.member.find_one({'_id': user['_id']})
        printstatus(db,user)
        modify=input('Want more options? (Yes:y/No:q) :')
        if modify=='y':statusmenu(db,user)
        else:break

def statusmenu(db,user):
    import status
    while(True):
        user = db.member.find_one({'_id': user['_id']})
        print('-'*49)
        print('1) Modify my name')
        print('2) Update my profile')
        print('3) Show my followings')
        print('4) Show my followers')
        print('5) Config my block list')
        print('q) Back to my status')
        print('-' * 49)
        n=input('Enter:')
        if n=='q':return
        status.status(n,db,user)

def explore(db,user):
    msg=""
    while(True):
        main.clear()
        try:
            print(msg)
            print()
            print("+-----------------+".center(49))
            print("|     EXPLORE     |".center(49))
            print("+-----------------+".center(49))
            print()
            print(single)
            print("You can explore the other user's wall!")
            otherid=input("Enter the id (q:quit) : ")
            if otherid=='q':return
            import post
            me=db.member.find_one({'_id':user['_id']})
            other= db.member.find_one({'_id': otherid})
            post.other_wall(db,me,other)
            inp=input("Want to explore more? (Yes:y,Quit:q) : ")
            msg=""
            if inp=='y':pass
            else:return
        except:
            msg=("Can't find.. try again.")

def print_wrong(db,user):
    print('wrong menu number.')
    return

def log_out(db,user):
    print("Successfully logged out")
    return True
