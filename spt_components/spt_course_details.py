from spt_components.spt_elements import *
from spt_lib.spt_ref import *
from spt_lib.spt_course_calculations import getGradeAverage
from spt_lib.spt_course_calculations import ZoomFactor as getScale

control_map = return_spt_reference()


class SptCourseDetails(UserControl):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.getDetails = self.mainRow()
        self.homeRef()
        self.spt_table_data = self.tableData()
        self.currentTableRow = self.getCurrentTableRow()
        self.currentStudentID = self.getCurrentStudentID()
        self.currentModuleName = self.getCurrentModuleName()

    def homeRef(self):
        add_to_spt_reference("SptCourseDetails", self)

    def getCurrentModuleName(self):
        return 'new'

    def tableData(self):
        return {}

    def getCurrentTableRow(self):
        return None

    def getCurrentStudentID(self):
        return None

    def getUI(self):
        return self.ui

    def getTheCurrentCourse(self):
        global spt_course
        current_course = loadTemp(S.TEMP_VALUES)
        if 'thisCourse' in current_course:
            thisCourse = current_course['thisCourse']
        else:
            thisCourse = 'new'
        thesecourses = loadDatabases(thisCourse)
        return thesecourses

    def mainRow(self):
        spt_table = sptDataTable()

        studentReport = False
        courseReport = ""

        def setZoom():
            thisZoomFactor = float(thisView.controls[0].controls[12].value)

            getScale.setScaleFactor2(thisZoomFactor)
            N.load_last_zoom_factor()
            print(loadTemp(S.TEMP_VALUES)['zoom'])
            thisView.update()
            pass

        def getChart():
            thisView.controls[3].controls[0].content.controls[0].controls.clear()
            thisView.controls[3].controls[0].content.controls[1].controls.clear()
            thisView.update()
            if str(thisView.controls[0].controls[2].value) == "" or str(thisView.controls[0].controls[2].value) == None:
                return 1
            else:
                average = getGradeAverage(loadTemp(S.TEMP_VALUES)['thisCourse'], 0,
                                          str(thisView.controls[0].controls[2].value))
                average2 = getGradeAverage(loadTemp(S.TEMP_VALUES)['thisCourse'], 1, 'practical')
                average3 = getGradeAverage(loadTemp(S.TEMP_VALUES)['thisCourse'], 1, 'theory')

                data = getStudentGrdaes(loadTemp(S.TEMP_VALUES)['thisCourse'], 0,
                                        str(thisView.controls[0].controls[2].value))
                data2 = getStudentGrdaes(loadTemp(S.TEMP_VALUES)['thisCourse'], 1, 'practical')
                data3 = getStudentGrdaes(loadTemp(S.TEMP_VALUES)['thisCourse'], 1, 'theory')

            thisChart = sptChart(loadTemp(S.TEMP_VALUES)['thisCourse'], data[2], data[2], data[1], 'Module Grades')
            thisBadge = sptBadge('Module Average', average)

            thisChart2 = sptChart(loadTemp(S.TEMP_VALUES)['thisCourse'], data3[2], data3[2], data3[1],
                                  'Course Theory Grades')
            thisBadge2 = sptBadge('Course Theory Average', average3)

            thisChart3 = sptChart(loadTemp(S.TEMP_VALUES)['thisCourse'], data2[2], data2[2], data2[1],
                                  'Course Practical Grades')
            thisBadge3 = sptBadge('Course Practical Average', average2)

            thisView.controls[3].controls[0].content.controls[0].controls.append(
                Row(width=N.SPT_1000, alignment=MainAxisAlignment.SPACE_BETWEEN, controls=[thisChart, thisBadge]))

            thisView.controls[3].controls[0].content.controls[0].controls.append(
                Row(width=N.SPT_1000, alignment=MainAxisAlignment.SPACE_BETWEEN, controls=[thisChart2, thisBadge2]))

            thisView.controls[3].controls[0].content.controls[0].controls.append(
                Row(width=N.SPT_1000, alignment=MainAxisAlignment.SPACE_BETWEEN, controls=[thisChart3, thisBadge3]))

            thisView.update()

        def analysisAndDetails(data, type):
            if type == 0:
                buttonData = json.loads(data)
                studentID = buttonData['tooltip']
            else:
                studentID = data

            thisModule = str(thisView.controls[0].controls[2].value)
            thisCourse = loadTemp(S.TEMP_VALUES)['thisCourse']

            thisStudent = getStudetByID(thisCourse, studentID)

            index = loadDatabases(thisCourse)[1]['modules_count'][thisModule]

            studentModuleGrade = loadDatabases(thisCourse)[1]['modules'][index][studentID]

            inCourseTheory = checkIfExists2(studentID, loadDatabases(thisCourse)[1]['majorAssessments'][0])
            inCoursePractical = checkIfExists2(studentID, loadDatabases(thisCourse)[1]['majorAssessments'][1])

            studentQR = getStudentQR(thisCourse, thisModule, studentID)

            if not inCourseTheory:
                studentTheoryGrade = 0
            else:
                studentTheoryGrade = loadDatabases(thisCourse)[1]['majorAssessments'][0][studentID]

            if not inCoursePractical:
                studentPracticalGrade = 0
            else:
                studentPracticalGrade = loadDatabases(thisCourse)[1]['majorAssessments'][1][studentID]

            studentDetails = thisView.controls[2].controls[3].content.controls[0].controls
            analysis = thisView.controls[2].controls[3].content.controls[2].controls

            text_field = thisView.controls[2].controls[3].content.controls[2].controls[0]
            dialogHome = thisView.controls[2].controls[3].content.controls[3].controls

            studentDetails[0].content.src = f"{studentQR}"
            studentDetails[1].controls[0].controls[1].value = thisStudent['id']
            studentDetails[1].controls[1].controls[1].value = thisStudent['firstName']
            studentDetails[1].controls[2].controls[1].value = thisStudent['lastName']

            studentDetails[2].controls[0].controls[1].value = thisStudent['email']
            studentDetails[2].controls[1].controls[1].value = thisStudent['division']
            studentDetails[2].controls[2].controls[1].value = thisStudent['station']

            studentDetails[3].controls[0].controls[1].value = studentModuleGrade
            studentDetails[3].controls[1].controls[1].value = studentTheoryGrade
            studentDetails[3].controls[2].controls[1].value = studentPracticalGrade

            average = str(getGradeAverage(thisCourse, 0, thisModule))
            average2 = str(getGradeAverage(thisCourse, 1, 'practical'))
            average3 = str(getGradeAverage(thisCourse, 1, 'theory'))

            data0 = 'This Course: ' + thisCourse + ' This Module: ' + thisModule + "\n"
            data1 = 'ID: ' + thisStudent['id'] + " First Name: " + thisStudent['firstName'] + " Last Name: " + \
                    thisStudent['lastName'] + "\n"
            data2 = 'Rank: ' + thisStudent['rank'] + ' Division: ' + thisStudent['division'] + ' Station: ' + \
                    thisStudent['station'] + "\n"
            data3 = 'Student Module Grade: ' + str(studentModuleGrade) + ' Student Course Theory Grade: ' + str(
                studentTheoryGrade) + ' Student Course Practical Grade: ' + str(studentPracticalGrade) + "\n"
            data4 = 'Average Combined Grade for this Module: ' + average + ' Average Combined Theory Grade for this Course: ' + average2 + ' Average Combined Practical Grade for this Course: ' + average3 + "\n"

            thisStudentReport = data0 + data1 + data2 + data3 + data4

            analysisDialog = sptDialog3(thisCourse, thisModule, studentID, thisStudentReport, text_field,
                                        studentDetails[0].content)
            imageDialog = sptDialog4(thisCourse, thisModule, studentID)
            dialogHome.clear()
            dialogHome.append(analysisDialog)
            dialogHome.append(imageDialog)

            thisView.update()

        def generateReport():
            try:
                thisView.controls[2].controls[3].content.controls[3].controls[0].open = True
                thisView.update()
            except Exception as e:
                print(e)

        def showQR():
            try:
                thisView.controls[2].controls[3].content.controls[3].controls[1].open = True
                thisView.update()
            except Exception as e:
                print(e)

        def populateTable(val):
            spt_table.content.rows.append(val)
            spt_table.visible = True
            spt_table.update()

        def getCourseImage():
            if self.getTheCurrentCourse()[2]['image'] != "":
                return str(self.getTheCurrentCourse()[2]['image'])
            else:
                return S.DEFAULT_IMAGE

        def getStudentOfModule(e):
            spt_table.content.rows.clear()
            spt_table.update()
            # [attendance_db, grades_db, info_db, students_db]
            db1 = self.getTheCurrentCourse()[1]['modules']
            db2 = self.getTheCurrentCourse()[3]['students']
            db3 = self.getTheCurrentCourse()[1]['majorAssessments']
            pg = 0
            tg = 0
            currentModule = {}
            for i in db1:
                if i['name'] != str(thisView.controls[0].controls[2].value):
                    continue
                else:
                    currentModule = i
                    self.currentModuleName = i['name']
                    break

            def sendSelf(e):

                if "object at " in str(e.control):
                    buttonData = str(e.control.tooltip)
                    type = 1
                else:
                    type = 0
                    buttonData = str(e.control).split('textbutton ')[1].replace("'", '"')

                analysisAndDetails(buttonData, type)

            for x in db2:
                if x['id'] in currentModule:
                    newRow = DataRow(cells=[])
                    newRow.cells.append(DataCell(
                        TextButton(x['firstName'],
                                   expand=True,
                                   tooltip=str(x['id']), on_click=lambda e: sendSelf(e),
                                   scale=getScale.getScaleFactor2()
                                   )
                    ))

                    if x['id'] not in db3[0]:
                        tg = 0
                    else:
                        tg = db3[0][x['id']]

                    if x['id'] not in db3[1]:
                        pg = 0
                    else:
                        pg = db3[1][x['id']]

                    newRow.cells.append(DataCell(
                        TextButton(x['lastName'], expand=True, tooltip=str(x['id']), on_click=lambda e: sendSelf(e),
                                   scale=getScale.getScaleFactor2())))
                    newRow.cells.append(
                        DataCell(Text(x['division'], expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2())))
                    newRow.cells.append(
                        DataCell(Text(x['station'], expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2())))
                    newRow.cells.append(DataCell(
                        Text(currentModule[x['id']], expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2())))
                    newRow.cells.append(
                        DataCell(Text(tg, expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2())))
                    newRow.cells.append(
                        DataCell(Text(pg, expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2())))
                    newRow.cells.append(DataCell(IconButton(icon=icons.EDIT, tooltip=str(x['id']),
                                                            icon_color=C().SPT_MEDIUM_DARK(),
                                                            on_click=lambda e: sptEdit(e),
                                                            scale=getScale.getScaleFactor2())))

                    self.spt_table_data[str(x['id'])] = newRow

                    populateTable(newRow)
            getChart()
            thisView.update()

        def isInt(y):
            return bool(re.match(r"^\d+$", str(y)))

        def sptEdit(id):

            if 'object at ' not in str(id.control):
                cont = str(id.control).split('iconbutton ')[1].replace("'", '"')
                contentDict = json.loads(cont)
                key = contentDict['tooltip']
            else:
                key = str(id.control.tooltip)

            self.currentStudentID = key
            thisView.controls[2].controls[1].content.content.controls[0].controls.clear()
            thisView.controls[2].controls[1].open = True
            thisView.controls[2].controls[1].content.content.controls[0].controls.append(Row(controls=[
                TextField(value=str(self.spt_table_data[key].cells[0].content.text)
                          , border=InputBorder.UNDERLINE, label='First Name:'),
                TextField(value=str(self.spt_table_data[key].cells[1].content.text)
                          , border=InputBorder.UNDERLINE, label='Last Name:')
            ]))

            thisView.controls[2].controls[1].content.content.controls[0].controls.append(Row(controls=[
                TextField(value=str(self.spt_table_data[key].cells[2].content.value)
                          , border=InputBorder.UNDERLINE, label='Division:'),
                TextField(value=str(self.spt_table_data[key].cells[3].content.value)
                          , border=InputBorder.UNDERLINE, label='Station:')
            ]))

            thisView.controls[2].controls[1].content.content.controls[0].controls.append(Row(controls=[
                TextField(value=str(self.spt_table_data[key].cells[4].content.value)
                          , border=InputBorder.UNDERLINE, label='Module Grade:'),
                TextField(value=str(self.spt_table_data[key].cells[5].content.value)
                          , border=InputBorder.UNDERLINE, label='Course Theory Grade:')
            ]))

            thisView.controls[2].controls[1].content.content.controls[0].controls.append(Row(controls=[
                TextField(value=str(self.spt_table_data[key].cells[6].content.value)
                          , border=InputBorder.UNDERLINE, label='Course Practical Grade:')
            ]))

            self.currentTableRow = self.spt_table_data[key]
            thisView.controls[2].controls[1].update()
            thisView.controls[2].controls[1].open = True

        def updateRec(e):
            getInt1 = isInt(thisView.controls[2].controls[1].content.content.controls[0].controls[2].controls[1].value)
            getInt2 = isInt(thisView.controls[2].controls[1].content.content.controls[0].controls[3].controls[0].value)
            getInt3 = isInt(thisView.controls[2].controls[1].content.content.controls[0].controls[2].controls[0].value)
            if getInt1 is True:
                theoryGrade = int(
                    thisView.controls[2].controls[1].content.content.controls[0].controls[2].controls[1].value)
            else:
                theoryGrade = '0'

            if getInt2 is True:
                practicalGrade = int(
                    thisView.controls[2].controls[1].content.content.controls[0].controls[3].controls[0].value)
            else:
                practicalGrade = '0'

            if getInt3 is True:
                moduleGrade = int(
                    thisView.controls[2].controls[1].content.content.controls[0].controls[2].controls[0].value)
            else:
                moduleGrade = '0'
            thisView.controls[2].controls[1].open = False
            # fn
            self.currentTableRow.cells[0].content.text = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[0].controls[0].value
            # ln
            self.currentTableRow.cells[1].content.text = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[0].controls[1].value
            # div
            self.currentTableRow.cells[2].content.value = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[1].controls[0].value
            # st
            self.currentTableRow.cells[3].content.value = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[1].controls[1].value
            # mgr
            self.currentTableRow.cells[4].content.value = moduleGrade
            # tgr
            self.currentTableRow.cells[5].content.value = theoryGrade
            # pgr
            self.currentTableRow.cells[6].content.value = practicalGrade
            thisView.controls[2].controls[1].update()

            # [attendance_db, grades_db, info_db, students_db]

            selectedModule = str(thisView.controls[0].controls[2].value)

            moduleIndex = getObjectIndexFromList(self.getTheCurrentCourse()[1], 'modules', 'name', selectedModule)
            studentIndex = getObjectIndexFromList(self.getTheCurrentCourse()[3], 'students', 'id',
                                                  self.currentStudentID)

            addStudentFinalGrades(loadTemp(S.TEMP_VALUES)['thisCourse'], self.currentStudentID, theory=theoryGrade,
                                  practical=practicalGrade)

            db1 = self.getTheCurrentCourse()[1]
            db2 = self.getTheCurrentCourse()[3]
            db1['modules'][moduleIndex][self.currentStudentID] = int(moduleGrade)
            db2['students'][studentIndex]['firstName'] = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[0].controls[0].value
            db2['students'][studentIndex]['lastName'] = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[0].controls[1].value
            db2['students'][studentIndex]['division'] = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[1].controls[0].value
            db2['students'][studentIndex]['station'] = \
                thisView.controls[2].controls[1].content.content.controls[0].controls[1].controls[1].value

            print(int(moduleGrade))

            saveData(db1, S.GRADES_DATABASE, loadTemp(S.TEMP_VALUES)['thisCourse'])
            saveData(db2, S.STUDENTS_DATABASE, loadTemp(S.TEMP_VALUES)['thisCourse'])
            getChart()
            thisView.update()

        def closeBs(e):
            thisView.controls[2].controls[1].open = False
            thisView.controls[2].controls[1].update()

        def deleteStudent(e):
            deleteStudentsFromModule(loadTemp(S.TEMP_VALUES)['thisCourse'], self.currentModuleName,
                                     self.currentStudentID)
            closeBs(0)
            getStudentOfModule(0)

        def updateImg():
            thisView.update()
            global spt_course
            thisView.controls[0].controls[0].content.src = f"{P.IMAGES_DIR + getCourseImage()}"

        thisFilePicker = sptFilePicker()

        def _setCourseImage():
            thisFilePicker.pick_files(
                allow_multiple=False,
                file_type=FilePickerFileType.IMAGE
            )

        bottomSheet2 = sptBottomSheet2()
        thisDialog = sptDialog(loadTemp(S.TEMP_VALUES)['thisCourse'], self.ui)
        thisDialog2 = sptDialog2(loadTemp(S.TEMP_VALUES)['thisCourse'], self.ui)

        def launchDialog():
            thisDialog.open = True
            thisView.update()

        def launchDialog2():
            thisDialog2.open = True
            thisView.update()

        def open_bs2(e):
            bottomSheet2.open = True
            bottomSheet2.update()

        def getStudent(e):
            thisCourse = loadTemp(S.TEMP_VALUES)['thisCourse']
            thisModule = self.currentModuleName

            try:
                index = loadDatabases(thisCourse)[1]['modules_count'][thisModule]
                studentID = thisView.controls[0].controls[7].content.controls[0].controls[0].value.split(' ')[0]

                inModule = checkIfExists2(studentID, loadDatabases(thisCourse)[1]['modules'][index])

                if not inModule:
                    print(studentID)
                    addStudentsToModule(thisCourse, thisModule, studentID)
                    getStudentOfModule(0)
            except Exception as e:
                print(e)

        thisView = Row(
            # scale=getScale.getScaleFactor(),
            spacing=N.SPT_50,
            scroll=ScrollMode.ALWAYS,
            alignment=MainAxisAlignment.START,
            vertical_alignment=CrossAxisAlignment.START,
            expand=True,
            controls=[

                Column(
                    # scale=getScale.getScaleFactor(),
                    alignment=MainAxisAlignment.START,
                    controls=[
                        Container(
                            scale=getScale.getScaleFactor2(),
                            on_click=lambda e: _setCourseImage(),
                            border_radius=N.SPT_10,
                            padding=N.SPT_10,
                            width=N.SPT_200,
                            bgcolor=None,
                            content=Image(
                                scale=getScale.getScaleFactor(),
                                width=N.SPT_200,
                                height=N.SPT_100,
                                border_radius=border_radius.all(10),
                                fit=ImageFit.CONTAIN,
                                src=f"{P.IMAGES_DIR + getCourseImage()}"
                            )
                        ),

                        TextField(
                            scale=getScale.getScaleFactor(),
                            multiline=True,
                            width=N.SPT_250,
                            height=N.SPT_100 + N.SPT_40,
                            read_only=True,
                            text_size=N.SPT_10 + N.SPT_2,
                            text_style=TextStyle(weight=FontWeight.BOLD)
                        ),
                        Dropdown(
                            scale=getScale.getScaleFactor(),
                            content_padding=N.SPT_5,
                            label="Course Modules",
                            hint_text="Choose a module",
                            height=N.SPT_50 - N.SPT_10,
                            width=N.SPT_250,
                            on_change=lambda e: getStudentOfModule(e),
                            text_size=N.SPT_12,

                        ),
                        FilledTonalButton(
                            height=N.SPT_30,
                            text="Create module",
                            on_click=lambda e: launchDialog2()
                        ),
                        FilledTonalButton(
                            height=N.SPT_30,
                            text="Add students to Course",
                            on_click=lambda e: open_bs2(e)
                        ),
                        FilledTonalButton(
                            height=N.SPT_30,
                            text="Delete Course",
                            on_click=lambda e: launchDialog()
                        ),
                        thisDialog,
                        Container(
                            scale=getScale.getScaleFactor(),
                            content=Column(
                                scale=getScale.getScaleFactor(),
                                controls=[
                                    Row(
                                        scale=getScale.getScaleFactor(),
                                        controls=[
                                            Dropdown(
                                                scale=getScale.getScaleFactor(),
                                                width=N.SPT_300 - N.SPT_20,
                                                height=N.SPT_50+N.SPT_10,

                                                label='Students',
                                                text_size=N.SPT_12
                                            ),
                                            FilledTonalButton(text="Add to module", on_click=lambda e: getStudent(e), height=N.SPT_30,)
                                        ]
                                    )

                                ]
                            )
                        ),
                        thisDialog2,
                        Divider(),
                        FilledTonalButton(
                            text="Home",
                            on_click=lambda e: self.ui.ui.go('/'),
                            height=N.SPT_30
                        ),
                        thisFilePicker,
                        # Slider(min=0, max=2, divisions=20, label="Zoom x {value}",
                        #       scale=loadTemp(S.TEMP_VALUES)['zoom'], value=loadTemp(S.TEMP_VALUES)['zoom'],
                        #       on_change=lambda e: setZoom())
                    ]
                ),
                Divider(),
                Column(
                    scale=getScale.getScaleFactor(),
                    width=N.SPT_950,
                    height=N.SPT_1700,
                    scroll=ScrollMode.ALWAYS,
                    # expand=True,
                    spacing=N.SPT_50,
                    controls=[

                        spt_table,

                        BottomSheet(
                            content=Container(
                                scale=getScale.getScaleFactor(),
                                padding=N.SPT_10,
                                border_radius=N.SPT_10 + N.SPT_2,
                                content=Column(
                                    scale=getScale.getScaleFactor(),
                                    tight=True,
                                    controls=[
                                        Column(
                                            scale=getScale.getScaleFactor(),
                                            tight=True
                                        ),
                                        Divider(),
                                        Row(
                                            scale=getScale.getScaleFactor(),
                                            controls=[
                                                FilledButton("Save and close", on_click=lambda e: updateRec(e)),
                                                FilledButton("Close without saving", on_click=lambda e: closeBs(e)),
                                                FilledButton("Remove Student From module",
                                                             on_click=lambda e: deleteStudent(e)),
                                            ]
                                        )
                                    ]
                                )
                            )
                        ),
                        bottomSheet2,
                        Container(
                            scale=getScale.getScaleFactor(),
                            bgcolor=C().SPT_LIGHT(),
                            width=N.SPT_950,
                            height=N.SPT_600,
                            padding=N.SPT_10,
                            border=border.all(N.SPT_1, C().SPT_DARK()),
                            border_radius=N.SPT_10,
                            content=Column(

                                controls=[
                                    Row(
                                        scale=getScale.getScaleFactor(),
                                        spacing=N.SPT_10,
                                        controls=[
                                            Container(
                                                scale=getScale.getScaleFactor(),
                                                width=N.SPT_200,
                                                height=N.SPT_200,
                                                on_click=lambda e: showQR(),
                                                content=Image(
                                                    scale=getScale.getScaleFactor(),
                                                    width=N.SPT_200,
                                                    height=N.SPT_200,
                                                    border_radius=border_radius.all(N.SPT_10),
                                                    fit=ImageFit.CONTAIN,
                                                    src=f"{P.IMAGES_DIR + S.DEFAULT_QR}"
                                                )),
                                            Column(
                                                scale=getScale.getScaleFactor(),
                                                spacing=N.SPT_1,
                                                controls=[
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('ID:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="", width=N.SPT_180,
                                                                            text_size=N.SPT_12, height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('First Name:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="", width=N.SPT_180,
                                                                            text_size=N.SPT_12, height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Last Name:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="", width=N.SPT_180,
                                                                            text_size=N.SPT_12, height=N.SPT_30)]
                                                    )
                                                ]
                                            ),
                                            Column(
                                                scale=getScale.getScaleFactor(),
                                                spacing=N.SPT_1,
                                                controls=[
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Email:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="",
                                                                            width=N.SPT_180, text_size=N.SPT_12,
                                                                            height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Division:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="", width=N.SPT_180,
                                                                            text_size=N.SPT_12, height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Station:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT,
                                                                            value="", width=N.SPT_180,
                                                                            text_size=N.SPT_12, height=N.SPT_30)]
                                                    )
                                                ]
                                            ),
                                            Column(
                                                scale=getScale.getScaleFactor(),
                                                spacing=N.SPT_1,
                                                controls=[
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Module Grade:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT, value="",
                                                                            width=N.SPT_180, text_size=N.SPT_12,
                                                                            height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Course Theory Grade:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT, value="",
                                                                            width=N.SPT_180, text_size=N.SPT_12,
                                                                            height=N.SPT_30)]
                                                    ),
                                                    Row(
                                                        scale=getScale.getScaleFactor(),
                                                        controls=[Text('Course Practical Grade:', size=N.SPT_12),
                                                                  TextField(read_only=True,
                                                                            border_color=colors.TRANSPARENT, value="",
                                                                            width=N.SPT_180, text_size=N.SPT_12,
                                                                            height=N.SPT_30)]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    Row(
                                        controls=[
                                            Text("Analysis:", size=N.SPT_30 + N.SPT_2, style=TextThemeStyle.TITLE_LARGE,
                                                 scale=getScale.getScaleFactor2(), )
                                        ]
                                    ),
                                    Row(
                                        controls=[
                                            TextField(multiline=True, max_lines=8, scale=getScale.getScaleFactor2()),
                                            TextButton("Generate analysis", on_click=lambda e: generateReport(),
                                                       scale=getScale.getScaleFactor2()),

                                        ]
                                    ),
                                    Row(
                                        scale=getScale.getScaleFactor(),
                                        controls=[

                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                ),
                Column(
                    scroll=ScrollMode.ALWAYS,

                    controls=[
                        Container(
                            width=N.SPT_1100,

                            content=Row(
                                width=N.SPT_1100,
                                scroll=ScrollMode.ALWAYS,
                                spacing=N.SPT_50,
                                vertical_alignment=CrossAxisAlignment.END,
                                controls=[
                                    Column(

                                        scroll=ScrollMode.ALWAYS,
                                        spacing=N.SPT_12,
                                        controls=[
                                        ]
                                    ),
                                    Column(
                                        spacing=N.SPT_400,
                                        controls=[
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )

            ]
        )

        def getObjects(_source, _key):
            displayInfo = f"Title: {self.getTheCurrentCourse()[2]['name']}\nStart Date: {self.getTheCurrentCourse()[2]['start']}\nEnd Date: {self.getTheCurrentCourse()[2]['end']}\nStudenst: {self.getTheCurrentCourse()[2]['students']}"
            thisView.controls[0].controls[1].value = displayInfo
            for i in _source:
                thisView.controls[0].controls[2].options.append(dropdown.Option(i[_key]))

            studentDropDown = thisView.controls[0].controls[7].content.controls[0].controls[0]
            loadStudents = loopStudents(loadTemp(S.TEMP_VALUES)['thisCourse'], 2)

            for i in loadStudents:
                studentDropDown.options.append(dropdown.Option(i))

        getObjects(self.getTheCurrentCourse()[1]["modules"], 'name')
        return thisView

    def build(self):
        return self.getDetails
