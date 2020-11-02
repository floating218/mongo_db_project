import pymongo
import post
import os
import main

def hashtag(db,user):
    a=""
    while(True):
        main.clear()
        print()
        print("+-----------------+".center(49))
        print("| Search hash tag |".center(49))
        print("+-----------------+".center(49))
        print()
        print("OR  : word1 word2".center(49))
        print("AND : word1&word2".center(49))
        print("\n+-----------------------------------------------+\n")
        from bson.son import SON
        if a=="":
            tag=input("Search hash tag (enter 'q' to quit) : ")
        else:
            print(a)
        if tag=='q':
            return
        if tag[0]!='#':
            tag='#'+tag
        for i in range(len(tag)):
            if tag[i]==" ":
                if tag[i+1]!='#':
                    tag=tag[:i+1]+"#"+tag[i+1:]
        if "&" in tag:
            tag=tag.split("&")
            tag=list(map(lambda x: "\""+x+"\"",tag))
            tag=" ".join(tag)
        db.posts.drop_indexes()
        db.posts.create_index([('content',pymongo.TEXT)])
        c=db.posts.aggregate([
            {'$match':{'$text':{'$search':tag}}},
            {'$sort': SON([('rawtime', -1)])}
        ])
        post.printpost(db,c)
        print("\n+-----------------------------------------------+\n")
        a="Search hash tag (enter 'q' to quit) : "
        tag = input(a)
        a=a+tag
        if tag=='q':return



a="""      
 -------------------------------------
| 1 LOG IN  |  2 SIGN UP  |  3  EXIT  | 
 -------------------------------------
 
 -----------
| 2 LOG OUT | 
 -----------

 -----------
| 3  EXIT   | 
 -----------

""".center(50)

