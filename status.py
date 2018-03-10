import main
import user as us

def status(n,db,user):
    if n=='1':
        moname(db,user)
    elif n=='2':
        update(db,user)
    elif n=='3':
        showfollow(db,user)
    elif n=='4':
        showfollower(db,user)
    elif n=='5':
        myblock(db,user)

def moname(db,user):
    user = db.member.find_one({'_id': user['_id']})
    newname=input('Enter your new name : ')
    if input('Are U Sure? (Yes:y/No:n) : ')=='y':
        db.member.update({'_id':user['_id']},{'$set':{'name':newname}})

        main.clear()
        print('Successfully modified.')
        us.printstatus(db, user)



def update(db,user):
    user = db.member.find_one({'_id': user['_id']})
    print('Your profile : ',end='')
    try:
        pro=user['profile']
        print(pro)
    except:
        print('None')
    up=input('Enter your new profile : ')
    rusure = input('Are U Sure? (Yes:y/No:n) :')
    if rusure=='n':return
    else:
        db.member.update({'_id':user['_id']},{'$set':{'profile':up}})
        main.clear()
        print('Successfully modifed!')
        us.printstatus(db, user)

def showfollow(db,user):
    user = db.member.find_one({'_id': user['_id']})
    followings=user['following']
    main.clear()
    print('+-------------You are now following-------------+')
    if followings==[]:
        print('No one')
    for f in followings:
        tain=db.member.find_one({'_id':f},{'_id':1,'name':1})
        print(tain['name']+'(@'+tain['_id']+')')
    print('+'+'-'*47+'+')
    while(True):
        #print('-'*49)
        print('1) Follow more')
        print('2) Unfollow')
        print("3) Explore the other's page")
        print('q) Exit')
        print('-'*49)
        a=input('Enter:')
        if a=='1':
            import follow
            follow.follow(db,user)
        elif a=='2':
            import follow
            follow.unfollow(db,user)
        elif a=='3':
            other=input('Enter id to explore (enter q to quit) : ')
            if other=='q':
                return
            exploreothers(db,user,other)
        else:
            return

def exploreothers(db,user,other):
    import post
    user = db.member.find_one({'_id': other})
    post.wall(db,user)

def showfollower(db,user):
    user = db.member.find_one({'_id': user['_id']})
    followings=user['follower']
    main.clear()
    print('+-------------You are followed by---------------+')
    if followings==[]:
        print('No one')
    for f in followings:
        tain=db.member.find_one({'_id':f},{'_id':1,'name':1})
        print(tain['name']+'(@'+tain['_id']+')')
    print('+'+'-'*47+'+')
    while(True):
        #print('-'*49)
        print('1) Block')
        print('2) Unblock')
        print("3) Explore the other's page")
        print('q) Exit')
        print('-'*49)
        a=input('Enter:')
        if a=='1':
            blockid = input('Enter an id to block  : ')
            try:
                f=db.member.find_one({'_id':blockid})
                if user['_id'] == blockid:
                    raise Exception
                try:
                    if user['follower'] != []:
                        db.member.update({'_id': user['_id']}, {'$pull': {'follower': blockid}})
                        db.member.update({'_id': blockid}, {'$pull': {'following': user['_id']}})
                except:
                    pass
                finally:
                    db.member.update({'_id': user['_id']}, {'$push': {'block': blockid}})
                    print("You have blocked @" + blockid + '\n')
            except:print("You can't block.\n")
        elif a=='2':
            try:
                b=user['block']
                if b==[]:raise Exception
                id=input("Enter id to delete from the block list : ")
                db.member.update({'_id': user['_id']}, {'$pull': {'block': id}})
                print('Successfully unblocked\n')
            except:
                print("You can't unblock.\n")
        elif a=='3':
            other=input('Enter id to explore : ')
            return
        else:
            return


def myblock(db,user):
    while(True):
        user = db.member.find_one({'_id': user['_id']})
        main.clear()
        print('+----------------My block list------------------+')
        try:
            blocks = user['block']
            if blocks == []:
                print('No one')
            for f in blocks:
                tain = db.member.find_one({'_id': f}, {'_id': 1, 'name': 1})
                print(tain['name'] + '(@' + tain['_id'] + ')')
        except:
            print('No one')
        print('+' + '-' * 47 + '+')
        print('1) Delete ')
        print('2) Add ')
        print('q) Exit')
        print('-'*49)
        a=input('Enter:')
        if a=='1':
            try:
                b=user['block']
                if b==[]:raise Exception
                id=input("Enter id to delete from the block list : ")
                db.member.update({'_id': user['_id']}, {'$pull': {'block': id}})
                print('Successfully unblocked\n')
            except:
                print("You can't unblock.\n")
        elif a=='2':
            showfollower(db,user)
        else:
            return



