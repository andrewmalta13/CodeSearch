# Author: Andrew Malta 2017
# Code to extract variable, function, and class names from 
# the source files in the AAN repos.

import jedi
import os
import sys
import json
from collections import defaultdict

# return the name of the parent of the defintion passed in
# If it doesn't have a parent, return the empty string.
def parent(definition):
    try:
        return definition.parent().name
    except Exception:
        return ""

# return the docstring of the corresponding
# line, but catches some weird exceptions.
def docstring(definition):
    try:
        return definition.docstring()
    except Exception:
        return ""


# for a given string of python source code
# return a list of tuples of the form
# (variable type, variable name, docstring, parent name)
# for each definition in the source code.
def get_docstrings_tups(source):
    objs = []
    try:
        defs = jedi.names(source, all_scopes = True)
    except Exception:
        return []
    for definition in defs:
        if definition.type in ["function", "class", "statement"]:
            objs.append({
                "type": definition.type,
                "name": definition.name,
                "docstring": docstring(definition),
                "line": definition.line,
                "parent": parent(definition)
            })
    return objs


n = 0
skip = set([11476])
# begin = 11476
# end = 15000
if __name__ == "__main__":
    path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/AAN/source/")
    tokendict = defaultdict(list)

    for root, dirs, files in os.walk(path):
        for item in files:
            if n in skip:
                n += 1
                continue
            if item.endswith(".py"):
                with open(path + item, "r") as f:
                    source = f.read()
                    for d in get_docstrings_tups(source):
                        tokendict[path + item].append(d)
                print "Finished reading tokens in {}".format(path + item)
            n += 1
            # if n == end:
            #     break
    path_str = "~/Dropbox/classes/Fall 2017/project/data/AAN/source_features.json"
    output_path = path = os.path.expanduser(path_str)
    with open(output_path, "w") as f:
        f.write(json.dumps(tokendict))
    # with open("/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/source/Newmu-dcgan_code-ee12b2d_train_cond_dcgan.py", "r") as f:
    #     source = f.read()
    #     for d in get_docstrings_tups(jedi, source):
    #         tokendict["/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/source/Newmu-dcgan_code-ee12b2d_train_cond_dcgan.py"].append(d)
    # print "finished one"
    # import jedi as newjedi
    # with open("/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/source/Newmu-dcgan_code-ee12b2d_train_uncond_dcgan.py", "r") as f:
    #     source = f.read()
    #     for d in get_docstrings_tups(newjedi, source):
    #         tokendict["/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/source/Newmu-dcgan_code-ee12b2d_train_uncond_dcgan.py"].append(d)
    # print "finished two"
    
