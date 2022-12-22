import json
from urllib.request import urlopen

f = open('JSON/department.json')

data = json.load(f)
  
for subject in data:
    for dept in subject.items():
        link = "http://luthers-list.herokuapp.com/api/dept/" + dept[1] + "/?format=json"
        e = urlopen(link)
        myfile = e.read()
        myfile = myfile.decode('utf-8')
        with open("JSON/" + dept[1] + ".json", 'w') as f:
            f.write(myfile)