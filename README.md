# dispatcherns
A python application to automate the posting of dispatches. Use entails two things:
* a configuration .ini file, in the same directory as this program, with each nation you want to dispatch to as the [section_heading] and the nations password, the path to a directory of dispatch files and a useragent which will be appended to the application's.
'''INI  
    [testlandia]
    password = hunter9
    path = /users/folder/nations/testlandia
    useragent = User Agent Example
'''
* a directory, pointed to by the configuration you set up, which contains the dispatches you want posted.  
* files, with arbitrary names, with a YAML block of metadata at the beginning. This should start and end with a line with three dashes "---" and should have title, category, subcategory and (if applicable) the id of the dispatch you want to edit. If there is no id field, the program will post the dispatch and add the id field for you.

With those things set up, the program can be launched, the path to the config file provided, and the name of the nation you want to use inputted. the program will then go through the directory and read each file, editing it if it has been posted already and posting it if not.

This tool uses pynationstates, configparser, guietta and python-frontmatter

Thanks to the kind folks in the NS coders discord server for their help.
