#follow.py
from pymongo.errors import ConnectionFailure
import sys
import main
single="+-----------------------------------------------+"




def printfollowings(db,user):
    print('+-------------You are now following-------------+')
    if user['following'] == []:
        print("No one\n")
    else:
        s = user['following'][0] + "   "
        if len(user['following']) == 1:
            print(s)
            print()
        else:

            for i in range(1, len(user['following'])):
                if len(s + user['following'][i] + "   ") <= 49:
                    s += user['following'][i] + "   "
                    if i == len(user['following']) - 1:
                        print(s)
                        print()
                else:
                    print(s)
                    s = user['following'][i] + "   "
                    if i == len(user['following']) - 1:
                        print(s)
                        print()


def follow(db, user):
    main.clear()
    while(True):
        try:
            user = db.member.find_one({'_id': user['_id']})
            print()
            print("+-----------------+".center(49))
            print("|     FOLLOW      |".center(49))
            print("+-----------------+".center(49))
            print()
            printfollowings(db,user)
            print('Enter id to follow')
            followid=input("Search id (Press 'q' to quit) : ")
            follow = db.member.find_one({'_id': followid})
            if followid=='q':
                return

            else: blocklist = follow['block']
            if follow == None:
                main.clear()
                print('There is no such user\n')

            elif user['_id'] in blocklist:
                main.clear()
                print(followid+" - You are blocked by this user.\n")
            elif followid == user['_id']:
                main.clear()
                print("You can't follow yourself :P\n")
            elif followid in user["following"]:
                main.clear()
                print("You are already following.\n")
            else:

                db.member.update({'_id':user['_id']},{'$push':{'following':followid}})
                db.member.update({'_id':followid},{'$push':{'follower':user['_id']}})
                main.clear()
                print("You are now following @"+followid+"\n")
        except Exception as e:
            main.clear()
            print("Can't follow... Try again.")
            sys.stderr.write("could not operate following %s\n" %e)


def unfollow(db, user):
    main.clear()
    while(True):
        try:
            print()
            print("+-----------------+".center(49))
            print("|    UNFOLLOW     |".center(49))
            print("+-----------------+".center(49))
            print()
            user = db.member.find_one({'_id': user['_id']})
            printfollowings(db,user)
            if user['following']!=[]:
                print('Enter id to unfollow')
                unfollowid = input("Search id (Press 'q' to quit): ")
                unfollow = db.member.find_one({'_id': unfollowid}, {"_id": 1, "name": 1})
                if unfollowid=='q':return
                elif unfollow == None:
                    main.clear()
                    print("There is no such user\n")
                elif unfollowid not in user["following"]:
                    main.clear()
                    print("You are not following @" + unfollowid+".\n")
                else:
                    db.member.update({'_id': user['_id']}, {'$pull': {'following': unfollowid}})
                    db.member.update({'_id': unfollowid}, {'$pull': {'follower': user['_id']}})
                    main.clear()
                    print("You have unfollowed @" + unfollowid+'\n')
            else:
                print("You can't unfollow anyone")
                return
        except Exception as e:
            main.clear()
            print("Can't unfollow! Try again.")
            #sys.stderr.write("could not operate following %s\n" %e)


