# -*- coding: utf-8 -*-

import sys
from pymongo import MongoClient
    
def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    global all_con
    for a in db.contests.find():
        if all_con.get(a["user_id"]) is None:
            temp=[a["user_id"],a["challenge_id"],a["score"],a["submit_time"],0]
            all_con[a["user_id"]]=temp
        else:
            temp=all_con.get(a["user_id"])
            temp[2]=temp[2]+a["score"]
            temp[3]=temp[3]+a["submit_time"]
    all_user=[]
    for value in all_con.values():
        all_user.append(value)
    all_user1=sorted(all_user,key=lambda a:(a[2],-a[3]),reverse=True)
    for t in all_user1:
        t[4]=all_user1.index(t)+1
    for tt in all_user1:
        all_con.get(tt[0])[4]=tt[4]
    need=all_con.get(user_id)
    if not need:
        print("Parameter Error")
        sys.exit()
    rank=need[4]
    score=need[2]
    submit_time=need[3]
    return rank, score, submit_time

if __name__ == "__main__":
    all_con={}
    user_id=0
    if len(sys.argv)!=2:
        print("Parameter Error")
        sys.exit()
    else:
        if not sys.argv[1].isdigit():
            print("Parameter Error")
            sys.exit()
        user_id=int(sys.argv[1])
    userdata = get_rank(user_id)
    print(userdata)
