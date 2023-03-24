from spt_lib.spt_theme import *
import json
class SptStrings:
    SPT_APP_NAME = "Student Progress Tracker"
    GRADES = "grades"
    ATTENDANCE = "attendance"
    STUDENTS = "students"
    INFO = "info"
    GRADES_DATABASE = "grades.json"
    ATTENDANCE_DATABASE = "attendance.json"
    STUDENTS_DATABASE = "students.json"
    INFO_DATABASE = "info.json"
    BACKUP_DATABASE = "spt_backUp_list.json"
    COURSE_DATABASE = "spt_courses.json"
    DEFAULT_IMAGE = "spt1.png"
    DEFAULT_QR = "sptQR.png"
    TEMP_VALUES = "tmp_vals.json"
    SPT_THEME = "theme.json"



class SptColors():
    def __init__(self):
        self.spt_theme=loadTheme()
        self.index = self.spt_theme
        self.themes=getTheme()
    def SPT_BLACK(self):
        return "#000000"
    def SPT_DARK(self):
        return self.themes[self.index]["1"]
    def SPT_MEDIUM_DARK(self):
        return self.themes[self.index]["2"]
    def SPT_MEDIUM_LIGHT(self):
        return self.themes[self.index]["3"]
    def SPT_LIGHT(self):
        return self.themes[self.index]["4"]
    def SPT_CURRENT_THEME(self):
        return self.themes[self.index]["name"]


class SptPath:
    COURSE_DIR = "data/courses/"
    DATA_DIR = "data/"
    BACKUP_DIR = "data/backup/"
    TEMPLATES_DIR = "data/data_templates/"
    EXPORTED_DATABASES_DIR = "data/exportedDatabases/"
    EXPORTED_TMP = "data/exportedTmp/"
    ASSETS_DIR = "assets/"
    IMAGES_DIR = "assets/img/"
    TEMP_DIR = "config/tmp/"
    CONFIG_DIR = "config/"
    IMAGES = "images/"


class SptNumbers:
    SPT_1 = 1
    SPT_2 = 2
    SPT_3 = 3
    SPT_4 = 4
    SPT_5 = 5
    SPT_9 = 9
    SPT_10 = 10
    SPT_12 = 12
    SPT_14 = 14
    SPT_20 = 20
    SPT_30 = 30
    SPT_40 = 40
    SPT_50 = 50
    SPT_100 = 100
    SPT_150 = 150
    SPT_180 = 180
    SPT_190 = 190
    SPT_200 = 200
    SPT_250 = 250
    SPT_300 = 300
    SPT_350 = 350
    SPT_400 = 400
    SPT_450 = 450
    SPT_500 = 500
    SPT_550 = 550
    SPT_600 = 600
    SPT_650 = 650
    SPT_700 = 700
    SPT_750 = 750
    SPT_800 = 800
    SPT_850 = 850
    SPT_900 = 900
    SPT_950 = 950
    SPT_1000 = 1000
    SPT_1050 = 1050
    SPT_1100 = 1100
    SPT_1150 = 1150
    SPT_1200 = 1200
    SPT_1250 = 1250
    SPT_1300 = 1300
    SPT_1350 = 1350
    SPT_1400 = 1400
    SPT_1450 = 1450
    SPT_1500 = 1500
    SPT_1550 = 1550
    SPT_1600 = 1600
    SPT_1650 = 1650
    SPT_1700 = 1700
    SPT_1750 = 1750
    SPT_1800 = 1800
    SPT_1850 = 1850
    SPT_1900 = 1900
    SPT_1950 = 1950
    SPT_2000 = 2000

    zoom_factor = 1.0

    @classmethod
    def apply_zoom(cls):
        for name, value in vars(cls).items():
            if name.startswith('SPT_'):
                setattr(cls, name, int(value * cls.zoom_factor))

    @classmethod
    def set_zoom_factor(cls, factor):
        cls.zoom_factor = factor
        cls.apply_zoom()

    @classmethod
    def load_last_zoom_factor(cls):
        try:
            with open(SptPath.TEMP_DIR+SptStrings.TEMP_VALUES, 'r') as f:
                data = json.load(f)
                factor = data.get('zoom', 1.0)
                cls.set_zoom_factor(factor)
        except (FileNotFoundError, json.JSONDecodeError):

            pass

    @classmethod
    def save_last_zoom_factor(cls):
        with open(SptPath.TEMP_DIR+SptStrings.TEMP_VALUES, 'r') as zoom:
            data = json.load(zoom)
            data['zoom']=cls.zoom_factor
        with open(SptPath.TEMP_DIR+SptStrings.TEMP_VALUES, 'w') as f:
            json.dump(data, f)

