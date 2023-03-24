import shutil
import zipfile
from datetime import datetime
from spt_lib.spt_course_operations import *
import qrcode
import os


def saveData(data, db, course):
    # creating vars for backup folder and file
    curr_date_time = datetime.now()
    folder_name = curr_date_time.strftime("%d_%m_%Y_%H_%M_%S_%f")
    backupDir = P.BACKUP_DIR + folder_name

    def save():
        # loading the existing data..
        print('loading the existing data..')
        backup_data_path = backupDir + course
        try:
            os.makedirs(backup_data_path)
            with open(P.COURSE_DIR + course + "/" + db) as _name:
                existing_data = json.load(_name)
        except Exception as _e:
            print(_e)

        with open(P.BACKUP_DIR + S.BACKUP_DATABASE) as backup:
            try:
                # creating a backup list
                print('creating a backup list')
                thisBackup = json.load(backup)
                if course + "_" + db not in thisBackup["history"]:
                    thisBackup["history"][course + "_" + db] = []
                thisBackup['history'][course + "_" + db].append(folder_name)
                # backing up data in dedicated folder
                print('backing up data in dedicated folder')
                with open(backup_data_path + "/" + db, 'w') as fp:
                    json.dump(existing_data, fp, indent=2, sort_keys=True)
                    try:
                        # overwriting old data with new
                        with open(P.COURSE_DIR + course + "/" + db, 'w') as new_data:
                            json.dump(data, new_data, indent=2, sort_keys=True)
                            print('done')
                    except Exception as _e:
                        print(_e)
            except Exception as _e:
                print(_e)
        # writing out the backup list
        print('writing out the backup list')
        with open(P.BACKUP_DIR + S.BACKUP_DATABASE, 'w') as backup_now:
            try:
                json.dump(thisBackup, backup_now, indent=2, sort_keys=True)
                print('done')
            except Exception as _e:
                print(_e)

    # calling functions
    if os.path.exists(backupDir):
        try:
            save()
            return 0
        except Exception as e:
            print(e)
            return 1
    else:
        try:
            os.mkdir(backupDir)
            save()
            return 0
        except Exception as e:
            print(e)
            return 1


def compress_folder_to_zip(folder_path, zip_file_path):
    parent_folder = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    # remember the original working directory
    working_dir = os.getcwd()
    os.chdir(parent_folder)
    # Compress the directory
    try:
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
            for root, dirs, files in os.walk(folder_name):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_f.write(file_path)

                    zip_f.write(file_path, arcname=os.path.join(folder_name, file_path.replace(folder_name + '/', '')))
        # change back to working directory
        os.chdir(working_dir)
    except Exception as e:
        print(e)


def exportDataBase():
    curr_date_time = datetime.now()
    source = P.COURSE_DIR
    thisDate = curr_date_time.strftime("%d_%m_%Y_%H_%M_%S")
    destination = P.EXPORTED_TMP + thisDate
    try:
        os.makedirs(destination)
    except Exception as e:
        print(e)

    def copy_contents():
        try:
            for child in os.listdir(source):
                child_path = os.path.join(source, child)
                if not os.path.exists(destination + "/" + os.path.basename(child_path)) and os.path.isdir(child_path):
                    os.mkdir(destination + "/" + os.path.basename(child_path))
                if os.path.isdir(child_path):
                    for files in os.listdir(child_path):
                        # thisFile = os.path.basename(child_path)+"/"+files
                        print(f"File: {child_path + files}")
                        shutil.copy2(child_path + "/" + files, destination + "/" + os.path.basename(child_path))
        except Exception as _e:
            print(_e)

    copy_contents()


def sendDataBase(zipName):
    try:
        shutil.copy2(P.EXPORTED_TMP + zipName, P.EXPORTED_DATABASES_DIR)
        shutil.rmtree(P.EXPORTED_TMP)
    except Exception as e:
        print(e)


def importDataBase(archive):
    zip_file = archive
    source_dir = os.path.basename(archive).split('.')[0] + '/'
    destination_folder = P.COURSE_DIR

    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
    except Exception as e:
        print(e)

    for item in os.listdir(destination_folder + source_dir):
        # print(destination_folder+item)
        if os.path.isdir(destination_folder + source_dir):

            if not os.path.exists(destination_folder + item):
                try:
                    os.makedirs(destination_folder + item)
                except Exception as e:
                    print(e)
                with open(destination_folder + source_dir + item + '/' + S.INFO_DATABASE) as info:
                    getInfo = json.load(info)
                    date_string = getInfo['end']
                    date_format = "%d_%m_%Y_%H_%M"
                    parsed_date = datetime.strptime(date_string, date_format)
                    curr_date_time = datetime.now()
                    if parsed_date > curr_date_time:
                        with open(P.DATA_DIR + S.COURSE_DATABASE) as _coursesInfo:
                            getCourseInfo = json.load(_coursesInfo)
                            getCourseInfo['current'].append(getInfo)
                        with open(P.DATA_DIR + S.COURSE_DATABASE, 'w') as _coursesInfoSave:
                            json.dump(getCourseInfo, _coursesInfoSave, indent=2, sort_keys=True)
                    else:
                        with open(P.DATA_DIR + S.COURSE_DATABASE) as _coursesInfo:
                            getCourseInfo = json.load(_coursesInfo)
                            getCourseInfo['history'].append(getInfo)
                        try:
                            with open(P.DATA_DIR + S.COURSE_DATABASE, 'w') as _coursesInfoSave:
                                json.dump(getCourseInfo, _coursesInfoSave, indent=2, sort_keys=True)
                        except Exception as e:
                            print(e)
                for dataFile in os.listdir(destination_folder + source_dir + item):
                    try:
                        shutil.copy2(destination_folder + source_dir + item + '/' + dataFile, destination_folder + item)
                    except Exception as e:
                        print(e)
            else:
                with open(destination_folder + item + '/' + S.INFO_DATABASE) as info:
                    # print(destination_folder + item + '/' + S.INFO_DATABASE)
                    getInfo = json.load(info)
                    date_string = getInfo['updated']
                    date_format = "%d_%m_%Y_%H_%M"
                    parsed_date = datetime.strptime(date_string, date_format)
                    with open(destination_folder + source_dir + item + '/' + S.INFO_DATABASE) as srcInfo:
                        src = json.load(srcInfo)
                        d = src['updated']
                        getUpdated = datetime.strptime(d, date_format)

                    if parsed_date < getUpdated:
                        print(parsed_date)
                        print(getUpdated)
                        with open(P.DATA_DIR + S.COURSE_DATABASE) as _coursesInfo:
                            getCourseInfo = json.load(_coursesInfo)
                            # getCourseInfo['current'].append(getInfo)

                            index = getObjectIndexFromList(getCourseInfo, 'current', 'name', 'make')
                            if index > -1:
                                print(index)
                                getCourseInfo['current'][index] = src
                        try:
                            with open(P.DATA_DIR + S.COURSE_DATABASE, 'w') as _coursesInfoSave:
                                json.dump(getCourseInfo, _coursesInfoSave, indent=2, sort_keys=True)
                            shutil.rmtree(destination_folder + item)
                            os.makedirs(destination_folder + item)
                        except Exception as e:
                            print(e)
                        for dataFile in os.listdir(destination_folder + source_dir + item):
                            try:
                                shutil.copy2(destination_folder + source_dir + item + '/' + dataFile,
                                             destination_folder + item)
                            except Exception as e:
                                print(e)

    try:
        shutil.rmtree(P.COURSE_DIR + source_dir)
    except Exception as e:
        print(e)


def createCourse(_name, _start, _end, _students):
    courseName = _name
    # createCourseOK = True
    if os.path.exists(P.COURSE_DIR + courseName) or courseName == "new":
        createCourseOK = False
    else:
        createCourseOK = True
    try:
        if createCourseOK:
            os.mkdir(P.COURSE_DIR + courseName)
            os.mkdir(P.COURSE_DIR + courseName + '/' + P.IMAGES)
            for files in os.listdir(P.TEMPLATES_DIR):
                shutil.copy2(P.TEMPLATES_DIR + files, P.COURSE_DIR + courseName)
            with open(P.COURSE_DIR + courseName + '/' + S.INFO_DATABASE) as _new:
                newCourseInfo = json.load(_new)
                newCourseInfo['name'] = courseName
                newCourseInfo['start'] = _start
                newCourseInfo['end'] = _end
                newCourseInfo['students'] = _students
                newCourseInfo['updated'] = _start
                newCourseInfo['image'] = ""
            with open(P.DATA_DIR + S.COURSE_DATABASE) as _coursesInfo:
                getCourseInfo = json.load(_coursesInfo)
                getCourseInfo['current'].append(newCourseInfo)

            x = loadTemp(S.TEMP_VALUES)
            x['thisCourse'] = courseName
            saveTemp(S.TEMP_VALUES, x)

            with open(P.COURSE_DIR + courseName + '/' + S.INFO_DATABASE, 'w') as _save:
                json.dump(newCourseInfo, _save, indent=2, sort_keys=True)

            with open(P.DATA_DIR + S.COURSE_DATABASE, 'w') as _coursesInfoSave:
                json.dump(getCourseInfo, _coursesInfoSave, indent=2, sort_keys=True)
            return 0
        else:
            print("Course Already Exists")
    except Exception as e:
        print(e)
        return 1


def deleteCourse(_course: str, db):
    try:
        shutil.rmtree(P.COURSE_DIR + _course)

        with open(P.DATA_DIR + S.COURSE_DATABASE) as courseInfo:
            getCourseInfo = json.load(courseInfo)

        index = getObjectIndexFromList(getCourseInfo, db, 'name', _course)
        del getCourseInfo[db][index]

        with open(P.DATA_DIR + S.COURSE_DATABASE, 'w') as updateCurseInfo:
            json.dump(getCourseInfo, updateCurseInfo, indent=2, sort_keys=True)

        x = loadTemp(S.TEMP_VALUES)
        x['thisCourse'] = 'new'
        saveTemp(S.TEMP_VALUES, x)
    except Exception as e:
        print(e)


def loadTemp(db):
    try:
        with open(P.TEMP_DIR + db) as tmp:
            getTemp = json.load(tmp)
        return getTemp
    except Exception as e:
        print(e)


def saveTemp(db, data):
    try:
        with open(P.TEMP_DIR + db, 'w') as tmp:
            json.dump(data, tmp, indent=2, sort_keys=True)
    except Exception as e:
        print(e)


def getStudentQR(course, module, studentID):
    imagePath = P.COURSE_DIR + course + '/' + P.IMAGES + module + '/' + studentID + '.png'

    if not os.path.exists(imagePath):
        return P.IMAGES_DIR + S.DEFAULT_QR
    else:
        print(imagePath)
        return imagePath
        pass


def setStudentQR(course, module, studentID, data):
    imagePath = P.COURSE_DIR + course + '/' + P.IMAGES + module + '/' + studentID + '.png'
    modulePath = P.COURSE_DIR + course + '/' + P.IMAGES + module + '/'
    if not os.path.exists(modulePath):
        try:
            os.makedirs(modulePath)
        except Exception as e:
            print(e)

    # if os.path.exists(imagePath):
    #    print("file found")
    #    os.remove(imagePath)

    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(imagePath)
