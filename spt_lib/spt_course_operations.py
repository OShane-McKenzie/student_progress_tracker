import json
from spt_lib.spt_constants import SptPath as P
from spt_lib.spt_constants import SptStrings as S
import random
import string


# Object data to check, list key, key within sub-object, value of key within sub-object
def getObjectIndexFromList(data, _key, _targetKey, _target):
    current_events = data[_key]
    _index = -1

    for i, event in enumerate(current_events):
        if event[_targetKey] == _target:
            _index = i
            break
    if _index > -1:
        return _index
    else:
        return -1


def checkIfExists(_course, item, _db):
    try:
        with open(P.COURSE_DIR + _course + _db) as DB:
            __DB = json.load(DB)
        if item in __DB:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def checkIfExists2(item, _db):
    try:
        if item in _db:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def loadDatabases(_course):
    '''
    :return: a list of databases [attendance_db, grades_db, info_db, students_db]
    '''
    try:
        with open(P.COURSE_DIR + _course + '/' + S.INFO_DATABASE) as info:
            info_db = json.load(info)

        with open(P.COURSE_DIR + _course + '/' + S.ATTENDANCE_DATABASE) as attendance:
            attendance_db = json.load(attendance)

        with open(P.COURSE_DIR + _course + '/' + S.GRADES_DATABASE) as grades:
            grades_db = json.load(grades)

        with open(P.COURSE_DIR + _course + '/' + S.STUDENTS_DATABASE) as students:
            students_db = json.load(students)

        return [attendance_db, grades_db, info_db, students_db]
    except Exception as e:
        print(e)


def loadActiveCourses():
    try:
        with open(P.DATA_DIR + S.COURSE_DATABASE) as active:
            getActive = json.load(active)
        return getActive['current']
    except Exception as e:
        print(e)


def getCourseImage(course):
    try:
        with open(P.COURSE_DIR + course + "/" + S.INFO_DATABASE) as image:
            getImage = json.load(image)
            i = getImage['image']
        if i != "":
            return i
        else:
            return S.DEFAULT_IMAGE
    except Exception as e:
        print(e)


def setCourseImage(course, _image: str):
    try:
        with open(P.COURSE_DIR + course + "/" + S.INFO_DATABASE) as image:
            getImage = json.load(image)
            getImage['image'] = _image
        with open(P.COURSE_DIR + course + "/" + S.INFO_DATABASE, 'w') as newImage:
            json.dump(getImage, newImage, indent=2, sort_keys=True)
    except Exception as e:
        print(e)


def generate_random_student_id():
    prefix = 'spt_'

    length = 10

    characters = string.ascii_lowercase + string.digits

    random_id = ''.join(random.choices(characters, k=length))

    student_id = prefix + random_id
    return student_id


def saveSptData(_file, data):
    with open(_file, 'w') as sptData:
        json.dump(data, sptData, indent=2, sort_keys=True)


def addStudent(course, firstName="", lastName="", ageRange="",
               completedCourses=None, ongoingCourses=None, regulationNumber=0,
               rank="", email="", mobile="", division="", station=""):
    if ongoingCourses == None:
        ongoingCourses = []

    if completedCourses == None:
        completedCourses = []

    getStudentDB = loadDatabases(course)[3]
    id = generate_random_student_id()

    x = -1
    for i in getStudentDB['students']:
        x = x + 1
        if 'id' in i:
            if i['id'] not in getStudentDB['student_count']:
                getStudentDB['student_count'][i['id']] = x

    while True:
        if id not in getStudentDB['student_count']:
            getStudentDB['student_count'][id] = x + 1
            break
        else:
            id = generate_random_student_id()

    # print(getStudentDB)

    studentObject = {}

    studentObject["id"] = id
    studentObject["firstName"] = firstName
    studentObject["lastName"] = lastName
    studentObject["ageRange"] = ageRange
    studentObject["completedCourses"] = completedCourses
    studentObject["ongoingCourses"] = ongoingCourses
    studentObject["regulationNumber"] = regulationNumber
    studentObject["rank"] = rank
    studentObject["email"] = email
    studentObject["mobile"] = mobile
    studentObject["division"] = division
    studentObject["station"] = station

    getStudentDB['students'].append(studentObject)

    saveSptData(P.COURSE_DIR + course + '/' + S.STUDENTS_DATABASE, getStudentDB)


def createModules(course, module):
    getModuleDB = loadDatabases(course)[1]
    x = -1
    for i in getModuleDB['modules']:
        x = x + 1
        if 'name' in i:
            if i['name'] not in getModuleDB['modules_count']:
                getModuleDB['modules_count'][i['name']] = x
            if i['name'] == module:
                return 1
    print('here')
    getModuleDB['modules_count'][module] = x + 1
    newMod = {'name': module}
    getModuleDB['modules'].append(newMod)
    saveSptData(P.COURSE_DIR + course + '/' + S.GRADES_DATABASE, getModuleDB)
    return 0


def addStudentsToModule(course, module, studentID, grade=0):
    getModuleDB = loadDatabases(course)[1]
    if module not in getModuleDB['modules_count']:
        return 1
    else:
        index = int(getModuleDB['modules_count'][module])
        if getModuleDB['modules'][index]['name'] == module:
            getModuleDB['modules'][index][studentID] = grade
            saveSptData(P.COURSE_DIR + course + '/' + S.GRADES_DATABASE, getModuleDB)
            return 0
        else:
            return 2


def addStudentFinalGrades(course, studentID: str, theory=0, practical=0):
    getGradeDB = loadDatabases(course)[1]

    getGradeDB['majorAssessments'][0][studentID] = theory

    getGradeDB['majorAssessments'][1][studentID] = practical

    saveSptData(P.COURSE_DIR + course + '/' + S.GRADES_DATABASE, getGradeDB)


def deleteStudentsFromModule(course, module, studentID):
    getModuleDB = loadDatabases(course)[1]

    if module not in getModuleDB['modules_count']:
        return 1
    else:
        index = int(getModuleDB['modules_count'][module])
        if getModuleDB['modules'][index]['name'] == module:
            del getModuleDB['modules'][index][studentID]

            '''
            if studentID in getModuleDB['majorAssessments'][0]:
                del getModuleDB['majorAssessments'][0][studentID]

            if studentID in getModuleDB['majorAssessments'][1]:
                del getModuleDB['majorAssessments'][1][studentID]
            '''

            saveSptData(P.COURSE_DIR + course + '/' + S.GRADES_DATABASE, getModuleDB)
            return 0
        else:
            return 2


def loopStudents(course, value):
    '''
    :param course: This is the name of the course.
    :param value: The data value to return: 1 = student ID, 2 = Student ID, Student First Name and Last Name.
    :return: A list of student data; either a list of names or student ID.
    '''
    getStudents = loadDatabases(course)[3]
    studentList = []
    for i in getStudents['student_count']:

        index = getStudents['student_count'][i]

        if value == 2:
            studentList.append(
                getStudents['students'][index]['id'] + ' ' + getStudents['students'][index]['firstName'] + ' ' +
                getStudents['students'][index]['lastName'])
        elif value == 1:
            studentList.append(getStudents['students'][index]['id'])

    return studentList


def getStudentGrdaes(course, _type: int, name):
    '''
    :param course: This is the name of the course.
    :param _type: The type of the grade to return such as a major assessment grade (1) or a mdule grade(0)
    :param name: The name of the module or major assessment
    :return: A list of three lists [[],[],[]]. The list at the first index (0) has the name value, second index (1) has the
    name of the students and the third index (2) has the student grades. Student names and grades will correspond.
    '''
    start = 0
    index = -1
    grade = [[], [], []]
    # final={"theory":[[],[]],"practical":[[],[]]}
    db = loadDatabases(course)
    try:
        if _type == 0:
            db = loadDatabases(course)[1]['modules']
        elif _type == 1:
            db = loadDatabases(course)[1]['majorAssessments']
        else:
            return 1
    except Exception as e:
        print(e)

    # print(db)

    for i in db:
        index = index + 1

    while index >= 0:
        thisName = ''
        for i in db[index]:

            if str(i) == 'name':
                if db[index][i] != str(name):
                    continue
                else:
                    thisName = db[index][i]

            if str(i) != 'name' and thisName == str(name):
                grade[1].append(i)
                grade[2].append(db[index][i])
                pass
            elif str(i) == 'name':
                grade[0].append(db[index][i])
        index = index - 1

    return grade


def getStudetByID(course, studentID):
    students = loadDatabases(course)[3]

    if studentID in students['student_count']:
        index = students['student_count'][studentID]

        return students['students'][index]
    else:
        return {
            "ageRange": "",
            "completedCourses": [],
            "division": "",
            "email": "",
            "firstName": "",
            "id": "",
            "lastName": "",
            "mobile": "",
            "ongoingCourses": [],
            "rank": "",
            "regulationNumber": 0,
            "station": ""
        }
