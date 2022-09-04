import json
import openpyxl
import random


def name(name):
    with open("data.json", "r") as f:
        cont = f.read()
        cont = json.loads(cont)
        final = []
        for i in cont.keys():
            if cont[i]["name"].lower() == name.lower():
                new = cont[i]
                new["usn"] = i
                final.append(new)

    return final


def usn(usn):
    with open("data.json", "r") as f:
        cont = f.read()
        print(cont)
        cont = json.loads(cont)
    try:
        print("from drv" + json.dumps(cont[usn]))
        return json.dumps(cont[usn])
    except Exception as e:
        return "Usn Not Found"


def clas(classec):
    clas = classec.split(" ")[0]
    sec = classec.split(" ")[1]
    with open("data.json", "r") as f:
        cont = f.read()

        cont = json.loads(cont)
        final = []
        for i in cont.keys():

            if str(cont[i]["clas"]) == str(clas) and str(cont[i]["section"]).lower() == sec.lower():
                new = cont[i]
                new["usn"] = i
                final.append(new)
    print(final)
    return final


def gExClass(classec, date):
    students = clas(classec)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = classec
    ws["B1"] = "Attendance"
    ws["C1"] = "Entry Time"
    ws["D1"] = "Exit Time"
    for i in students:
        print("hello")
        entry = []
        for j in i["entries"]:
            if date in j["start"]:
                entry = [j["start"], j["end"]]
        if len(entry) > 0:
            attendance = "present"
        else:
            attendance = "absent"
        print([f"Name: {i['name']} Usn: {i['usn']}", attendance, entry[0], entry[1]])
        ws.append([f"Name: {i['name']} Usn: {i['usn']}", attendance, entry[0], entry[1]])

    return wb
