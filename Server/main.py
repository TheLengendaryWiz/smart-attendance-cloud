import dataRetreival.drv
import flask
from datetime import datetime
import json
import register

app=flask.Flask(__name__, static_folder='templates/static') 

timeThreshold = 60
filePath = r"data.json"


RetTypes = {"name": dataRetreival.drv.name, "usn": dataRetreival.drv.usn, "date": dataRetreival.drv.date}

@app.route("/q", methods=["POST"])
def retQuery():
    global RetTypes
    payload = flask.request.form
  
    type = payload["q"]
    args = payload["args"]
    print("from main" + RetTypes[type](args))
    return RetTypes[type](args)

@app.route("/dashboard")
def dash():
    return flask.render_template("index.html")

def checkTime(t1, t2):
    global timeThreshold
    t1 = datetime(int(t1[0]), int(t1[1]), int(t1[2]), int(t1[3]), int(t1[4]), int(t1[5]))
    print(t1.strftime("%Y:%m:%d:%H:%M:%S"))
    print(t2.strftime("%Y:%m:%d:%H:%M:%S"))
    diff = (t2 - t1).total_seconds()
    print(f"difference is {diff}")
    if diff <= timeThreshold:
        return True
    else:
        return False

def updateEntry(usn):
    global filePath
    with open(filePath, "r") as fil:
        data = fil.read()

    data = json.loads(data)
    #NOTE : ON REPLIT SERVER THIS DEFAULTS TO UTC
    now = datetime.now()
    if usn in data.keys():
        currUser = data[usn]
    else:
        print(usn, "is not in the database")
        print("User Not Registered")
        return
    current_time = now.strftime("%Y:%m:%d:%H:%M:%S")
    if currUser["inSchool"]:
        lastTimeEntry = currUser["entries"][len(currUser["entries"]) - 1]["start"].split(":")
        print(lastTimeEntry)
        if not checkTime(lastTimeEntry, now):
            currUser["entries"][len(currUser["entries"]) - 1]["end"] = current_time
            currUser["inSchool"] = False

        else:
            print("cool down needed")
            return
    else:
        try:
            lastTimeEntry = currUser["entries"][len(currUser["entries"]) - 1]["end"].split(":")
        except Exception as e:
            print(e)
            currUser["entries"].append({"start": current_time})
            currUser["inSchool"] = True
            with open(filePath, "w") as fil1:
                data = json.dumps(data)
                fil1.write(data)
            return

        if not checkTime(lastTimeEntry, now):
            print("cool down not needed")
            currUser["entries"].append({"start": current_time})
            currUser["inSchool"] = True

        else:
            print("cool down needed")
            return

    with open(filePath, "w") as fil1:
        data = json.dumps(data)
        fil1.write(data)

@app.route('/' , methods=['GET','POST'])
def update():
    if flask.request.method == 'POST':
        usn = flask.request.form['usn']
        updateEntry(usn)
        print("post") 
        return "Done"
    if flask.request.method=='GET':
        print("get")
        return 'GET'

@app.route('/register' , methods=['GET','POST'])
def registerEndpoint():
    if flask.request.method=='GET':
        return 'GEt'
    if flask.request.method=='POST':
        nameusnuid=flask.request.json['data']
        nameusnuidarray=nameusnuid.split(';')
        register.register(nameusnuidarray[0],nameusnuidarray[1],nameusnuidarray[2],nameusnuid[3],nameusnuid[4])
        return "Done"

app.run(host='0.0.0.0', port=8080)