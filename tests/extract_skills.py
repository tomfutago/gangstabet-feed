import re
#s = "{\"1\":5,\"4\":33}"
s = "{\"1\":32,\"2\":33,\"3\":32,\"4\":33,\"5\":35}"

s = s.replace('{', '').replace('}', '').replace('"', '')
print(s)

type = "Gangster"
if type == "Gangster":
    skills = ["racketeering", "shooting", "gambling", "intelligence", "strategy"]
elif type == "Detective":
    skills = ["logic", "critical thinking", "incorruptible", "attention to detail", "intelligence"]

for n in range(5):
    s = s.replace(str(n+1) + ":", skills[n] + ": ")

print(s)
x = "\n".join(str(v) for v in s.split(","))
print(x)


#x = "\n".join(str(v) for v in s.split(","))
#print(x)

#x = "\n".join(": ".join((k,v)) for (k,v) in s.items())
#print(x)


"""
#racketeering
#shooting
#gambling
#intelligence
#strategy

skill_inc = {}

found1 = re.search('"1":(.+?)[,}]', s)
if found1:
    skill_inc["logic"] = found1.group(1)

found2 = re.search('"2":(.+?)[,}]', s)
if found2:
    skill_inc["critical thinking"] = found2.group(1)

found3 = re.search('"3":(.+?)[,}]', s)
if found3:
    skill_inc["incorruptible"] = found3.group(1)

found4 = re.search('"4":(.+?)[,}]', s)
if found4:
    skill_inc["attention to detail"] = found4.group(1)

found5 = re.search('"5":(.+?)}', s)
if found5:
    skill_inc["intelligence"] = found5.group(1)

print(skill_inc)

x = "\n".join(": ".join((k,v)) for (k,v) in skill_inc.items())
print(x)
"""
