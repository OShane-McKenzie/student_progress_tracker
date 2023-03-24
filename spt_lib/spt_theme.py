import json

CONFIG_DIR = "config/"


def loadTheme(db="theme.json"):
    try:
        with open(CONFIG_DIR + db) as tmp:
            getTemp = json.load(tmp)
        return getTemp['sptTheme']
    except Exception as e:
        print(e)


def saveTheme(data, db="theme.json"):
    try:
        with open(CONFIG_DIR + db, 'w') as tmp:
            json.dump(data, tmp, indent=2, sort_keys=True)
    except Exception as e:
        print(e)


def getTheme(db="theme.json"):
    try:
        with open(CONFIG_DIR + db) as tmp:
            getTemp = json.load(tmp)
        return getTemp['spt_themes']
    except Exception as e:
        print(e)


def getThemeDB(db="theme.json"):
    try:
        with open(CONFIG_DIR + db) as tmp:
            getTemp = json.load(tmp)
        return getTemp
    except Exception as e:
        print(e)
    pass


def getThemeList(db="theme.json"):
    try:
        with open(CONFIG_DIR + db) as tmp:
            themeList = []
            getTemp = json.load(tmp)
            for i in getTemp['spt_themes']:
                themeList.append(i['name'])
        return themeList
    except Exception as e:
        print(e)
