from spt_lib.spt_course_operations import *
from spt_lib.spt_data import loadTemp
import statistics
import openai
import platform


def getOS():
    return platform.system()


def getGradeAverage(course, _type, name):
    gradeList = getStudentGrdaes(course, _type, name)
    average = 0
    try:
        average = statistics.mean(gradeList[2])
    except Exception as e:
        print(e)
    return average


def getAnalysis(apiKey, data):
    openai.api_key = apiKey
    messages = [
        {"role": "system", "content": "You are a shrewd and friendly data analyst."}
    ]
    instruction = '''Interpret and discuss the following data:\n
    '''
    messages.append({"role": "user", "content": instruction + data})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    return reply


class ZoomFactor:
    zoomFactor = 1.0
    zoomFactor2 = 1.0

    @classmethod
    def setScaleFactor(cls, x):
        data = loadTemp(S.TEMP_VALUES)
        data['zoom'] = x
        saveSptData(P.TEMP_DIR + S.TEMP_VALUES, data)
        cls.zoomFactor = x

    @classmethod
    def setScaleFactor2(cls, x):
        data = loadTemp(S.TEMP_VALUES)
        data['zoom'] = x
        saveSptData(P.TEMP_DIR + S.TEMP_VALUES, data)
        cls.zoomFactor2 = x

    @classmethod
    def getScaleFactor(cls):
        return cls.zoomFactor

    @classmethod
    def getScaleFactor2(cls):
        return cls.zoomFactor2
