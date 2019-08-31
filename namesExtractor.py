#!/usr/bin/env python
import xml.etree.cElementTree as cElementTree
import time
import re, string

def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

def remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

if __name__ == '__main__':
    names=[]
    start_time = time.time()
    context = cElementTree.iterparse('dblp_utf8.xml', events=("start", "end"))
    context = iter(context)
    event, root = context.__next__() # get the root element of the XML doc

    f = open("UniqueNames.txt", "a")

    for event, elem in context:
        if event == "end":
            if elem.tag in ['article']: # i want to write out all <bucket> entries
                for inner_elem in iter(elem):
                    if inner_elem.tag =='author':
                        authorName= inner_elem.text
                        authorName= remove_punctuation(authorName)
                        n = authorName.split(' ')

                        if len(n[0]) >= 2:
                            if n[0] not in names:
                                name = n[0]
                                names.append(name)
                                f.write(name+"\n")
                                print(name)
            root.clear()  # when done parsing a section clear the tree to safe memory
    print (names.__len__())
    f.close()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


