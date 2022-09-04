import json

def register(name,usn,uid,clas, section):
  with open(r"data.json", "r") as f:
      content = json.loads(f.read())
  
  content[usn] = {"name": name, "uid": uid, "clas":clas, "section": section, "entries": [], "inSchool": False}
  
  newContent = json.dumps(content)
  
  with open(r"data.json", "w") as f:
      f.write(newContent)
