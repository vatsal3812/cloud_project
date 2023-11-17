from flask import Flask,render_template,request 
import redis
import time
from datetime import datetime
import logging

timeV = []
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
hash_set_name = "applied"
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    curTime = datetime.now()
    for a,b in timeV:
        if a<=curTime<=b:
            return render_template("index.html")
    return "You are out of time, please wait for the next slot!"

def parseTime():
    times = redis_client.get('validtime').split(" ")
    logging.warning(times)
    for timeRange in times:
        a,b = timeRange.split("-")
        ah, am = a.split(":")
        bh,bm = b.split(":")
        cur = datetime.now()
        a = datetime(2023,1,1,int(ah),int(am),0)
        b = datetime(2023,cur.month,cur.day,int(bh),int(bm),0)
        timeV.append((a,b))

@app.route('/book',methods=["GET","POST"])
def login():
    curTime2 = datetime.now()
    flag = 0
    for a,b in timeV:
        #print(a,b)
        if a<=curTime2<=b:
            flag = 1
    if not flag : 
        return "You are out of time, please wait for the next slot!"
    content = request.args.get("id")
    if content is None:
        resp = request.form.get('content')
        if(resp is None):
            return "No key found!"
        content = request.form['content']
    isPresent = redis_client.hget(hash_set_name, content)
    if isPresent is not None:
            return render_template('applied.html')
    member_score = redis_client.zscore("tester", content)
    if member_score is not None:
        return render_template('booked.html')
    else:
        curTime = time.time()
        redis_client.hset(hash_set_name, content, 1)
        redis_client.zadd("tester", {content: curTime})
        return "PASS APPLIED!"

if __name__ == "new":
    redis_client.set("validtime","00:00-23:59")
    parseTime()
    #redis_client.connection_pool.disconnect()