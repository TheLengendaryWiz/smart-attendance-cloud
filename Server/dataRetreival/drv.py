import json
import openpyxl
    

def name(name):
    pass


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
        

def date(date):
    pass