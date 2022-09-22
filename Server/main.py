import dataRetreival.drv
import flask
from datetime import datetime,timedelta
import json
import register
from openpyxl.writer.excel import save_virtual_workbook

app = flask.Flask(__name__, static_folder='templates/static')

timeThreshold = 60
filePath = r"data.json"

RetTypes = {"name": dataRetreival.drv.name, "usn": dataRetreival.drv.usn, "class": dataRetreival.drv.clas}

@app.route('/download')
def download():
    return flask.render_template("download.html")

#/d?classec=12%20E3&date=2022:08:13 (sample)
@app.route("/d", methods=["GET"])
def retExcel():
    try:
        classec = flask.request.args.get("classec")
        date = flask.request.args.get("date")
        workbook = dataRetreival.drv.gExClass(classec, date)

        return flask.Response(
            save_virtual_workbook(workbook),
            headers={
                'Content-Disposition': f'attachment; filename={classec}:{date}.xlsx',
                'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
        )
    except Exception as e:
        print(e.with_traceback())
        return "An Unexpected Error occured. Please check your input data"


@app.route("/q", methods=["POST"])
def retQuery():
    global RetTypes
    payload = flask.request.form

    type = payload["q"]
    args = payload["args"]

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
    # NOTE : ON REPLIT SERVER THIS DEFAULTS TO UTC
    now = datetime.now()
    if str(now.astimezone().tzinfo)=='UTC':
      now = now + timedelta(hours=5,minutes=30)
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
            prevEntry = datetime(int(lastTimeEntry[0]),int(lastTimeEntry[1]),int(lastTimeEntry[2]))
            current_time_array = current_time.split(':')
            currEntry = datetime(int(current_time_array[0]),int(current_time_array[1]),int(current_time_array[2]))
            if int((currEntry-prevEntry).days )== 0:
                currUser["entries"][len(currUser["entries"]) - 1]["end"] = current_time
                currUser["inSchool"] = False
            else:
                currUser["entries"][len(currUser["entries"]) - 1]["end"] = None
                currUser["entries"].append({"start": current_time})
                currUser["inSchool"] = True

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
            #TODO : Once we convert the entire thing to use IST instead of UTC , we also need to ensure that if entry time is logged in the AFTERNOON , entry must be set to null and exit as current time
            print("cool down not needed")
            currUser["entries"].append({"start": current_time})
            currUser["inSchool"] = True

        else:
            print("cool down needed")
            return

    with open(filePath, "w") as fil1:
        data = json.dumps(data)
        fil1.write(data)


@app.route('/', methods=['GET', 'POST'])
def update():
    if flask.request.method == 'POST':
        usn = flask.request.form['usn']
        updateEntry(usn)
        print("post")
        return "Done"
    if flask.request.method == 'GET':
        print("get")
        return 'GET'


@app.route('/register', methods=['GET', 'POST'])
def registerEndpoint():
    if flask.request.method == 'GET':
        return 'GEt'
    if flask.request.method == 'POST':
        nameusnuid = flask.request.json['data']
        nameusnuidarray = nameusnuid.split(';')
        register.register(nameusnuidarray[0], nameusnuidarray[1], nameusnuidarray[2], nameusnuidarray[3], nameusnuidarray[4])
        return "Done"


app.run(host='0.0.0.0', port=8080)
