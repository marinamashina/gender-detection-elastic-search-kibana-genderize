#!/usr/bin/env python
# To call http://genderize.io API
# 1000 name per day limit. Check header info for current count. See docs.
# This wrapper written by John Oberlin | github.com/oberljn

import requests as r
import json
import sys
import traceback

# Names file
with open("UniqueNames.txt") as names_file:
    text = names_file.read()
raw_names = text.split("\n")
names_file.close()

names = []
for line in raw_names:
    if line not in names:
        names.append(line)
        print(line)

print("Names to run: " + str(len(names)))

# Split names list into groups of 10 in an array: [ [a,b,..j], [a,b,..j], [a] ]
name_groups = []
sub = []
limit = 9

for n in names:
    ndx = names.index(n)

    if ndx == limit:
        sub.append(n)
        name_groups.append(sub)
        sub = []
        limit += 10

    else:
        sub.append(n)

        if ndx == len(names) - 1:
            name_groups.append(sub)

# #Check array output
# for g in name_groups:
#  print(str(len(g)) + ": " + str(g),)

# Build query URLs
# If names list not dedupes, will causing index error

urls = []

for g in name_groups:
    url = "https://api.genderize.io/?apikey=48dcd4d1b9f521dff79bc96dd20b5bb8&"

    for n in g:
        ndx = g.index(n)

        if ndx < 10:
            query = "name[%s]=%s&" % (ndx, n.replace(" ", "%20"))
            url += query

        else:
            break

    #url += "country_id=us"
    urls.append(url)

# Check URL output
# for u in urls:
#  print(u)

# Call API and append to results list
results = []
fullDict = {}

for u in urls:
    try:
        got = r.get(u).json()
        #got = json.loads(got.text)
        #print (got.text)

        for g in got:
            results.append(g)
    except Exception:
        print(r.status_codes)
print(results)

# break # for testing
with open('JsonGenderize.json', "w") as json_file:
    for res in results:
        content = {}
        full_content = {}
        try:
            content['gender'] = res['gender']
            content['probability'] = res['probability']
            content['count'] = res['count']
        except KeyError:
            print("KeyError")
        full_content[res["name"]] = content
        json_file.write('{}\n'.format(json.dumps(full_content)))

#Guardamos el resultado de genderize en un fichero json


json_file.close()

# #Genera fichero csv separado por tabuladores
# # Print as tab-separated text
#
# f = open("csvGenderize.txt", "a")
# f.write("name;gender;probability;count"+"\n")
# for res in results:
#     try:
#         line=res["name"] + ";" + res["gender"] + ";" + str(res["probability"])+ ";" +str(res["count"])+"\n"
#         f.write(line)
#         print(line)
#     except:
#         line = res["name"] + ";" + "Unknown" + ";" + "0" + ";" + "0" + "\n"
#         f.write(line)
#         print(line)
# f.close()