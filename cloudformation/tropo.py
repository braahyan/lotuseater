from os import listdir
from os.path import isfile, join

TEMPLATE_FILE_NOEX = "06-continuousIntegration"
TEMPLATE_FILE = TEMPLATE_FILE_NOEX + ".tmpl"
onlyfiles = [f for f in listdir(".") if
             isfile(join(".", f)) and f.find(".yml") >= 0]
allstuff = [{"name": f, "cfg": isfile(f.replace(".yml",".cfg"))} for f in onlyfiles]
print(onlyfiles)

import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(stacks=allstuff)  # this is where to put args to the template renderer

with open('./06-continuousIntegration.yml', 'w') as f:
    f.write(outputText)
