from flet import Page

global spt_reference
spt_reference = {}

spt_reference['ui'] = Page

global spt_page
spt_page = []

global bar
bar = 0

global spt_course
spt_course = {}


def setCourse(key, value):
    global spt_course
    try:
        spt_course[key] = value
    except KeyError as e:
        print(e)
    finally:
        pass


def add_to_spt_reference(key, value):
    global spt_reference
    try:
        spt_reference[key] = value
    except KeyError as e:
        print(e)
    finally:
        pass


def getCourse():
    global spt_course
    return spt_course


def return_spt_reference():
    global spt_reference
    return spt_reference


def get_spt_bar():
    global bar
    return bar


def return_spt_page():
    global spt_page
    return spt_page
