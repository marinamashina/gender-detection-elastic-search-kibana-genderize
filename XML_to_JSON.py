#-*- coding: utf-8 -*-
import xml.etree.cElementTree as cElementTree
import time
import re
import string
import json
import uuid


def add_element(dict,key,value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)


def remove_punctuation (text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)


if __name__ == '__main__':
    start_time = time.time()

    with open('JsonGenderize v2 0.json') as json_genderize_dict:
        dictUniqueNames = json.load(json_genderize_dict)

    with open('datos_formato_elastic.json', 'a') as file:

        context = cElementTree.iterparse('dblp_utf8.xml', events=("start", "end"))
        context = iter(context)
        event, root = context.__next__()

        for event, elem in context:
            temp_dict = {}
            full_dict = {}
            if event == "end":
                if elem.tag in ['article']:
                    article_type = elem.tag
                    authorsList = []

                    for inner_elem in iter(elem):
                        if inner_elem.tag == 'title':
                            if inner_elem.text is not None:
                                title = inner_elem.text
                                title_id = abs(hash(title))
                        elif inner_elem.tag == 'year':
                            if inner_elem.text is not None:
                                year = int(inner_elem.text)
                        if inner_elem.tag == 'author':
                            authorsList.append(inner_elem.text)
                    print("authorsList", authorsList)

                    #print (authorsList) #OK no mover
                    authors = []
                    #print("authorList length: ", len(authorsList))
                    #print("dict Unique names", len(dictUniqueNames))

                    for aut in authorsList:

                        authorInfo = {}
                        author = aut
                        author_id = abs(hash(author))
                        authorInfo['author_id'] = author_id
                        authorInfo['author'] = author
                        authorName = remove_punctuation(author)
                        names = authorName.split(' ')
                        name = names[0]
                        #print("name ", name)
                        if len(name) >= 2:
                            if name in dictUniqueNames:
                                try:
                                    authorInfo['name'] = name
                                    authorInfo['gender'] = dictUniqueNames[name]['gender']
                                    authorInfo['probability'] = int(dictUniqueNames[name]['probability'] * 100)
                                    authorInfo['count'] = dictUniqueNames[name]['count']
                                except:
                                    authorInfo['name'] = name
                                    authorInfo['gender'] = 'Unknown'
                                    authorInfo['probability'] = 0
                                    authorInfo['count'] = 0
                        else:
                            authorInfo['name'] = name
                            authorInfo['gender'] = 'Unknown'
                            authorInfo['probability'] = 0
                            authorInfo['count'] = 0
                        authors.append(authorInfo)
                        #print("authorInfo ", authorInfo)
                        #print("authors ", authors)


                    #print("authors ", authors)

                    for auth in authors:
                    # for a authorInfo:
                        try:
                            temp_dict['IDtitle'] = title_id
                            temp_dict['title'] = title
                            temp_dict['year'] = year
                            temp_dict['author_id'] = auth['author_id']
                            temp_dict['author_full_name']= auth['author']
                            temp_dict['author_first_name'] = auth['name']
                            temp_dict['gender'] = auth['gender']
                            temp_dict['probability'] = auth['probability']
                            temp_dict['count'] = auth['count']

                            full_dict['_index'] = 'practice'
                            full_dict['_type'] = article_type
                            id = uuid.uuid1()  # creo un identificador unico para cada registro por author/titulo
                            full_dict['_id'] = id.hex
                            full_dict['_source'] = temp_dict
                        #add_element(temp_dict, 'authors', authorInfo)
                        except:
                            print("Do nothing")
                        print("full_dict", full_dict)
                        json.dump(full_dict, file, indent=2)
        root.clear()  # when done parsing a section clear the tree to safe memory
    json_genderize_dict.close()# Cierro el archivo: diccionario de nombres únicos y generificación
    file.close()# Cierro el fichero con el json completo para ES

    print("time elapsed: {:.2f}s".format(time.time() - start_time))
