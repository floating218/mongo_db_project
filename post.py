import time
import main
import user
import pymongo
import os
single="+-----------------------------------------------+"
double="================================================="

def newsfeed(db,user):
    while(True):
        me = db.member.find_one({'_id': user['_id']})
        main.clear()
        print('The Newsfeed'.center(49))
        followings=user['following']+[user['_id']]
        db.posts.create_index('uid')
        cursor=db.posts.find({'uid':{'$in':followings}}).sort('rawtime',pymongo.DESCENDING)
        printpost(db,cursor)
        print('\n'+single)
        print("1 좋아요 2 좋아요 취소")
        print("3 댓글 보기 4 댓글 달기")
        inp=input("Enter (Quit:q) : ")
        if inp=='q':return
        elif inp=='1':
            cursor = db.posts.find({'uid': {'$in': followings}}).sort('rawtime', pymongo.DESCENDING)
            likey(db,me,cursor)
        elif inp=='2':
            cursor = db.posts.find({'uid': {'$in': followings}}).sort('rawtime', pymongo.DESCENDING)
            dislikey(db, me, cursor)
        elif inp=='3':
            cursor = db.posts.find({'uid': {'$in': followings}}).sort('rawtime', pymongo.DESCENDING)
            comment(db, me, cursor)
        else:
            input("잘못누르셨습니다. 엔터를 눌러주세요")


def wall(db,user):
    main.clear()
    print()
    print(('The Wall of '+user['name']).center(49))
    user = db.member.find_one({'_id': user['_id']})
    db.posts.create_index('uid')
    cursor=db.posts.find({'uid':user['_id']}).sort('rawtime',pymongo.DESCENDING)
    printpost(db,cursor)
    print('\n'+single)

    #########


    #########

    return db.posts.find({'uid':user['_id']}).sort('rawtime',pymongo.DESCENDING)

def other_wall(db,me,other):
    try:
        while(True):
            me = db.member.find_one({'_id': me['_id']})
            other=db.member.find_one({'_id':other['_id']})
            main.clear()
            print()
            print(('The Wall of ' + other['name']).center(49))
            db.posts.create_index('uid')
            cursor = db.posts.find({'uid': other['_id']}).sort('rawtime', pymongo.DESCENDING) ################
            cursor=list(cursor)
            printpost(db, cursor)
            print('\n' + single)
            cursor= list(cursor)
            print("1 좋아요 2 좋아요 취소 3 댓글 보기")
            inp=input("Enter (q to quit) : ")
            if inp=='q':return
            elif inp=='1':
                likey(db,me,cursor)
            elif inp=='2':
                dislikey(db, me,cursor)
            elif inp=='3':
                comment(db,me,cursor)
            else:
                input('Wrong number...Enter to proceed')
    except:
        print("다른 담벼락 메뉴에서 문제가 생겼습니다. 다시 해주세요 ㅠ")

def printpost(db,cursor):
    try:
        c=list(cursor)
        if c==[]:raise Exception
        p=0
        for apost in c:
            username=db.member.find_one({'_id':apost['uid']})['name']
            print("\n"+single)
            print('\nUser : ' + username+'(@'+apost['uid']+')')
            print('post# : ' + str(p))
            p+=1
            print(apost['content'])
            lc=("LIKE : "+str(apost['like'])+"  "+"Comments : "+str(len(apost['comments'])))
            print(lc.rjust(49))
            print(apost['time'].rjust(49))
    except:
        print("\n"+single)
        print("\nNo post to show.".center(49))

def postInterface(db, user):
    menu_num = -1
    while (menu_num != '0'):
        user = db.member.find_one({'_id': user['_id']})
        cursor=wall(db,user)
        print("\n"+double)
        welcomeyou = "Welcome %s" % user['name']
        print("\n" + welcomeyou.center(49))
        print("Select Post Menu".center(49))


        ####

        print("1 좋아요 2 좋아요 취소 3 댓글 보기")


        ####

        print("4 포스트 작성")
        nopost=(list(db.posts.find({'uid':user['_id']})))
        if nopost!=[]:
            print("5 포스트 삭제")
        print("q user menu로 돌아가기")
        print("\n"+double)

        inp = input("Enter : ")
        if inp == 'q':
            return
        if inp=='5' and nopost==[]:
            input("잘못 입력하였습니다. 엔터를 누르면 돌아갑니다.")

        elif inp == '1':
            likey(db, user, cursor)
        elif inp == '2':
            dislikey(db, user, cursor)
        elif inp == '3':
            comment(db, user, cursor)
        elif inp=='4':insertPost(db,user,cursor)
        elif inp=='5':deletePost(db,user,cursor)
        else:
            input('Wrong number...Enter to proceed')



def insertPost(db,user,cursor):
    print("q:문서입력 취소 /end:문서입력 끝내기")
    print("Write : ")
    newline=""
    totalline=[]
    while(newline!='q' and newline!='/end'):
        newline=input()
        if newline=='q':
            totalline=[]
        elif newline=='/end':
            pass
        else:
            totalline.append(newline)
    if newline=='q':
        return
    totalline='\n'.join(totalline)

    mytime=time.ctime()
    rawtime=time.time()
    post_number=list(db.member.find({'_id':user['_id']}))[0]['pnumber']
    db.posts.insert({'uid':user['_id'],'pid':post_number,'content':totalline,'time':mytime,'rawtime':rawtime,'like':0,'comments':[]})
    db.member.update({'_id':user['_id']},{'$inc':{'pnumber':1}})

def deletePost(db,user,cursor):
    try:
        print("Please enter post numbers you'd like to delete (ex: 4,1,0)")
        print("Enter 'q' to exit this menu")
        print()
        post_numbers=input("Enter post numbers: ")
        post_numbers=list(map(int,post_numbers.split(",")))
        post_numbers=sorted(post_numbers)
        count=0
        for apost in cursor:
            if count in post_numbers:
                unique_id=apost['_id']
                db.posts.remove({'_id':unique_id})
            count+=1
    except:
        if post_numbers=='q':
            return
        else:
            print('Wrong post numbers... Try again\n')
            deletePost(db,user)

def likey(db,me,cursor):
    try:
        me = db.member.find_one({'_id': me['_id']})
        print("Enter post numbers you LIKE (quit:q)")
        post_numbers=int(input("Enter : "))
        count=0
        for apost in cursor:
            if count == post_numbers:
                unique_id=apost['_id']
                if unique_id in me['mylikes']:
                    print("이미 좋아요를 눌러서 더 누를 수 없어요!")
                    input("Press enter to proceed")
                else:
                    db.member.update({'_id':me['_id']},{'$addToSet':{'mylikes':unique_id}})
                    db.posts.update({'_id':unique_id},{'$inc':{'like':1}})
            count+=1

    except:
        if post_numbers=='q':
            return
        else:
            print('Wrong post numbers... Try again\n')
            input("Press enter to preceed")

def dislikey(db,me,cursor):
    try:
        me = db.member.find_one({'_id': me['_id']})
        print("Enter post numbers you DISLIKE (quit:q)")
        post_numbers=int(input("Enter : "))
        count=0

        for apost in cursor:
            if count == post_numbers:
                unique_id=apost['_id']
                if unique_id not in db.member.find_one({'_id':me['_id']})['mylikes']:
                    print("좋아요를 누르지 않아서 취소할 수 없습니다.")
                    input("Press enter to preceed")
                db.posts.update({'_id':unique_id},{'$inc':{'like':-1}})
                db.member.update({'_id': me['_id']}, {'$pull': {'mylikes': unique_id}})
            count+=1
    except:
        if post_numbers=='q':
            print()
            return
        else:
            print('Wrong post numbers... Try again\n')
            input("Press enter to preceed")

def comment(db,me,cursor):
    try:

        cursor=list(cursor)
        #print(cursor)
        me = db.member.find_one({'_id': me['_id']})

        pnum = int(input("Enter post number : "))

        main.clear()
        if pnum == 'q': return
        apost=cursor[pnum]
        unique_id = apost['_id']

        while(True):
            apost=db.posts.find_one({'_id':unique_id})
            username = db.member.find_one({'_id': apost['uid']})['name']
            print("\n" + single)
            print('\nUser : ' + username + '(@' + apost['uid'] + ')')
            print(apost['content'])
            lc = ("LIKE : " + str(apost['like']) + "  " + "Comments : " + str(len(apost['comments'])))
            print(lc.rjust(49))
            print(apost['time'].rjust(49))
            print("\n" )
            print("+댓글+".center(49))
            foundcomments = apost['comments']
            count=0
            for c in foundcomments:
                print('@' + str(c['uid']) + "("+str(count)+") : " + str(c['text']))
                count+=1
            print()
            print(single)
            your_comment = input("댓글(-번호 입력시 삭제됩니다) : ")

            if your_comment[0]=='-':
                try:
                    delnum=int(your_comment[1:])
                    count=0
                    for c in foundcomments:
                        if count==delnum:
                            delcom=c
                        count+=1
                    commentlist=foundcomments
                    #print(commentlist)
                    #print(delcom)
                    commentlist.remove(delcom)
                    #print(commentlist)
                    db.posts.update({'_id':unique_id},{'$set':{'comments':commentlist}})


                    main.clear()
                    continue
                except:
                    main.clear()
                    continue

            if your_comment == 'q'or your_comment=="":
                print()
                return
            else:
                db.posts.update({'_id': unique_id}, {'$push': {'comments': {'uid': me['_id'], 'text': your_comment}}})
            main.clear()
    except :
        input('Wrong ...press enter to try again')


def showlikes(db,me):
    try:
        while(True):
            me = db.member.find_one({'_id': me['_id']})
            main.clear()
            print()
            print("내가 좋아요 누른 글들".center(49))
            print()

            db.posts.create_index('rawtime')

            mylikelist=me['mylikes']

            #print(mylikelist)

            cursor=db.posts.find({'_id':{'$in':mylikelist}}).sort('rawtime',pymongo.DESCENDING)
            cursor=list(cursor)

            #print(cursor)

            printpost(db, cursor)
            print('\n' + single)

            if cursor==[]:
                input("엔터를 누르면 돌아갑니다.")
                return

            print("1 좋아요 2 좋아요 취소 3 댓글 보기")
            inp=input("Enter (q to quit) : ")
            if inp=='q':return
            elif inp=='1':
                likey(db,me,cursor)
            elif inp=='2':
                dislikey(db, me,cursor)
            elif inp=='3':
                comment(db,me,cursor)
            else:
                input('Wrong number...Enter to proceed')
    except:
        input("좋아요 열람 메뉴에서 문제가 생겼습니다. 엔터를 누르면 돌아갑니다")












