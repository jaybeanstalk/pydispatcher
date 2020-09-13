import frontmatter
import os
import nationstates
import configparser
import re
from guietta import Gui, _
config = configparser.ConfigParser()
# config_file should be the path to an ini file holding the configuration for all of your nations, by default is in the same repository
config_file = 'config.ini'
cats = {
"factbook": "1",
"bulletin": "3",
"account": "5",
"meta": "8",
}
subcats = {
    "factbook" : {"overview": "100","history": "101","geography": "102","politics": "104","legislation": "105","religion": "106","economy": "108","international": "109","trivia": "110","miscellaneous": "111"},
    "bulletin" : {
        "policy": "305",
        "news": "315",
        "opinion": "325",
        "campaign": "385",},
    "account": {
        "trade": "515",
        "sport": "525",
        "drama": "535",
        "diplomacy": "545",
        "science": "555",
        "other": "595",
        },
    "meta": {
        "gameplay": "835",
        "reference": "845"
        },
}
#def setup(guiset, *args):


def post(gui, *args):
    nation = gui.nation
    config.read(config_file)
    password = config[nation]['password']
    path = config[nation]["path"]
    useragent = config[nation]["useragent"]
    api = nationstates.Nationstates("Glaciosia-Dispatcher run by " + useragent)
    nation = api.nation(nation, password)

    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                post = frontmatter.load(entry.path)
                category = post['category']
                subcategory = post['subcategory']
                category_number = cats[category]
                subcategory_number = subcats[category][subcategory]
                titletext = post['title']
                content = post.content
                print(category, subcategory, category_number, subcategory_number, titletext, content)
                if 'id' in post.metadata:
                    dispatch_id = post["id"]
                    r = nation.command('dispatch',
                                    dispatch='edit', mode='prepare',
                                    dispatchid=dispatch_id,
                                    title=titletext,
                                    text=content,
                                    category=category_number,
                                    subcategory=subcategory_number)

                    print(r)
                    token = r['success']

                    nation.command('dispatch',
                                    token=token,
                                    dispatch='edit', mode='execute',
                                    dispatchid=dispatch_id,
                                    title=titletext,
                                    text=content,
                                    category=category_number,
                                    subcategory=subcategory_number)
                else:
                    r = nation.command('dispatch',
                                dispatch='add', mode='prepare',
                                title=titletext,
                                text=content,
                                category=category_number,
                                subcategory=subcategory_number)

                    print(r)
                    token = r['success']

                    r = nation.command('dispatch',
                                    token=token,
                                    dispatch='add', mode='execute',
                                    title=titletext,
                                    text=content,
                                    category=category_number,
                                    subcategory=subcategory_number)
                    id = r['success'];
                    digits = re.compile(r'[0-9]+')
                    id = digits.findall(id)
                    print(id[0])
                    post['id'] = id[0]
                    frontmatter.dump(post, entry.path)

gui = Gui( [ 'Enter Nation' , '__nation__' ],
           [ 'Post & Edit Dispatches:' , ['Go'] ] )

gui.events([       _        ,     _     ,],
           [       _        ,   post    ])
gui.run()