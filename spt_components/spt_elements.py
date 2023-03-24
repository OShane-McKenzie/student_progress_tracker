from flet import *
from spt_lib.spt_data import *
from spt_lib.spt_constants import SptNumbers as N
from spt_lib.spt_constants import SptColors as C
from spt_lib.spt_course_calculations import getAnalysis
from spt_lib.spt_course_calculations import ZoomFactor as getScale
from spt_lib.spt_data import setStudentQR
import re
from spt_lib.spt_ref import *
from spt_lib.spt_course_operations import *
from datetime import datetime
import time


def sptBottomSheet():
    def bs_dismissed(e):

        close_bs(e)
        thisBottomSheet.update()

    def show_bs(e):
        thisBottomSheet.open = True
        thisBottomSheet.update()

    def is_integer(e):
        thisBottomSheet.update()
        end = [
            thisBottomSheet.content.content.controls[0].controls[1].value,
            thisBottomSheet.content.content.controls[1].controls[0].value,
            thisBottomSheet.content.content.controls[1].controls[1].value,
            thisBottomSheet.content.content.controls[1].controls[2].value,
            thisBottomSheet.content.content.controls[2].controls[0].value,
            thisBottomSheet.content.content.controls[2].controls[1].value,
        ]
        sendErr = [
            thisBottomSheet.content.content.controls[0].controls[1],
            thisBottomSheet.content.content.controls[1].controls[0],
            thisBottomSheet.content.content.controls[1].controls[1],
            thisBottomSheet.content.content.controls[1].controls[2],
            thisBottomSheet.content.content.controls[2].controls[0],
            thisBottomSheet.content.content.controls[2].controls[1],
        ]
        x = -1
        for i in end:
            x = x + 1
            if i != "":
                _type = bool(re.match(r"^\d+$", str(i)))

                if _type is False:
                    sendErr[x].error_text = "Must be a valid number"
                    thisBottomSheet.update()
                    pass
                else:
                    sendErr[x].error_text = None
                    thisBottomSheet.update()
            else:
                sendErr[x].error_text = None
                thisBottomSheet.update()

    def close_bs(e):
        def getInt(y):
            return bool(re.match(r"^\d+$", str(y)))

        try:
            thisBottomSheet.open = False
            curr_date_time = datetime.now()
            start = curr_date_time.strftime("%d_%m_%Y_%H_%M")
            name = thisBottomSheet.content.content.controls[0].controls[0].value
            students = thisBottomSheet.content.content.controls[0].controls[1].value

            end1 = thisBottomSheet.content.content.controls[1].controls[0].value
            end2 = thisBottomSheet.content.content.controls[1].controls[1].value
            end3 = thisBottomSheet.content.content.controls[1].controls[2].value

            end4 = thisBottomSheet.content.content.controls[2].controls[0].value
            end5 = thisBottomSheet.content.content.controls[2].controls[1].value

            if (getInt(end1) is True and getInt(end2) is True and getInt(end3) is True and getInt(end4) is
                    True and getInt(end5) is True):
                end = str(end1) + "_" + str(end2) + "_" + str(end3) + "_" + str(end4) + "_" + str(end5)
                thisBottomSheet.content.content.controls[0].controls[0].value = ""
                thisBottomSheet.content.content.controls[0].controls[1].value = ""
                thisBottomSheet.content.content.controls[1].controls[0].value = ""
                thisBottomSheet.content.content.controls[1].controls[1].value = ""
                thisBottomSheet.content.content.controls[1].controls[2].value = ""
                thisBottomSheet.content.content.controls[2].controls[0].value = ""
                thisBottomSheet.content.content.controls[2].controls[1].value = ""
                thisBottomSheet.update()
            else:
                thisBottomSheet.content.content.controls[0].controls[0].value = ""
                thisBottomSheet.content.content.controls[0].controls[1].value = ""
                thisBottomSheet.content.content.controls[1].controls[0].value = ""
                thisBottomSheet.content.content.controls[1].controls[1].value = ""
                thisBottomSheet.content.content.controls[1].controls[2].value = ""
                thisBottomSheet.content.content.controls[2].controls[0].value = ""
                thisBottomSheet.content.content.controls[2].controls[1].value = ""
                end = None
                thisBottomSheet.update()

            if name != "" and end is not None and students != "":
                thisBottomSheet.content.content.controls[2].controls[1].text = "Create Course"
                thisBottomSheet.update()
                global spt_reference
                createCourse(str(name), str(start), str(end), int(students))
                spt_reference["SptHome"].populateCourses()
                spt_reference["SptHome"].update()
                thisBottomSheet.open = False
                thisBottomSheet.update()

            thisBottomSheet.update()
        except Exception as e:
            thisBottomSheet.open = False
            print(e)

    thisBottomSheet = BottomSheet(
        # content.content.controls[2].append()
        content=Container(
            scale=getScale.getScaleFactor(),
            content=Column(
                scale=getScale.getScaleFactor(),
                controls=[
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[
                            TextField(label="Course Name", color=C().SPT_DARK(), border_color=C().SPT_DARK(),
                                      scale=getScale.getScaleFactor()),
                            TextField(label="Number of students", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                        ]
                    ),
                    Row(
                        controls=[
                            TextField(label="End Day", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                            TextField(label="End Month", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                            TextField(label="End Year", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                        ]
                    ),
                    Row(
                        controls=[
                            TextField(label="End Hour", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                            TextField(label="End Minute", on_change=is_integer, color=C().SPT_DARK(),
                                      border_color=C().SPT_DARK(), scale=getScale.getScaleFactor()),
                        ]
                    ),
                    ElevatedButton("Save and Close", on_click=close_bs, color=C().SPT_LIGHT(), bgcolor=C().SPT_DARK(),
                                   scale=getScale.getScaleFactor()),
                ],
                tight=True,
            ),
            padding=N.SPT_10,
        ),

        open=False,
        on_dismiss=bs_dismissed,
    )
    return thisBottomSheet


# noinspection PyTypeChecker
def sptCard(courseName, students, startDate, endDate, ui):
    thisImage = getCourseImage(courseName)

    def hoverAnim(e):
        if e.data == "true":
            thisCard.content.border = border.all(N.SPT_3, C().SPT_DARK())
            thisCard.update()

            for __ in range(20):
                thisCard.elevation += N.SPT_2
                thisCard.update()

        else:
            thisCard.content.border = border.all(N.SPT_1, C().SPT_MEDIUM_DARK())
            thisCard.update()

            for __ in range(20):
                thisCard.elevation -= N.SPT_2
                thisCard.update()

    thisCard = Card(

        elevation=1,
        width=N.SPT_400,
        height=N.SPT_300,
        visible=True,
        scale=getScale.getScaleFactor(),
        # i.content.content.controls[1].value
        content=Container(
            scale=getScale.getScaleFactor(),
            animate=animation.Animation(N.SPT_600, curve="ease"),
            border_radius=N.SPT_10,
            padding=N.SPT_10,
            width=N.SPT_400,
            height=N.SPT_300,
            bgcolor=C().SPT_MEDIUM_LIGHT(),
            border=border.all(N.SPT_1, C().SPT_MEDIUM_DARK()),
            on_hover=lambda e: hoverAnim(e),
            on_click=lambda e: loadDetails(e),
            content=Column(
                scale=getScale.getScaleFactor(),
                spacing=N.SPT_2,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Image(
                        scale=getScale.getScaleFactor(),
                        src=f"{P.IMAGES_DIR + str(thisImage)}",
                        width=N.SPT_300,
                        height=N.SPT_200,
                        border_radius=border_radius.all(N.SPT_10),
                        fit=ImageFit.CONTAIN,
                    ),
                    Text(f"Title: {courseName}", size=N.SPT_14, color=C().SPT_BLACK(),
                         scale=getScale.getScaleFactor()),
                    Text(f"Students: {students}", size=N.SPT_14 + N.SPT_2, color=C().SPT_BLACK(),
                         scale=getScale.getScaleFactor()),
                    Text(f"Started: {startDate}", size=N.SPT_14 + N.SPT_2, color=C().SPT_BLACK(),
                         scale=getScale.getScaleFactor()),
                    Text(f"End: {endDate}", size=N.SPT_14, color=C().SPT_BLACK(),
                         scale=getScale.getScaleFactor()),
                ]
            )
        ),
    )

    # thisCard.content.content.controls[1].value
    def loadDetails(e):
        setCourse('thisCourse', courseName)
        passCourse = loadTemp(S.TEMP_VALUES)
        passCourse['thisCourse'] = courseName
        saveTemp(S.TEMP_VALUES, passCourse)
        ui.data['thisCourse'] = courseName
        ui.update()
        ui.ui.go('/details')

    return thisCard


def sptFab():
    def createCs(e):
        global spt_reference
        spt_reference["SptHome"].thisBottomSheet.open = True
        spt_reference["SptHome"].update()

        # spt_reference["SptHome"].thisBottomSheet.open = True

        pass

    thisFab = FloatingActionButton(
        on_click=createCs,
        scale=getScale.getScaleFactor(),
        content=Row(
            scale=getScale.getScaleFactor(),
            controls=[Icon(icons.ADD), Text("Create", color=C().SPT_BLACK(), size=N.SPT_12)], alignment='center',
            spacing=N.SPT_5
        ),
        bgcolor=C().SPT_MEDIUM_LIGHT(),
        shape=RoundedRectangleBorder(radius=N.SPT_5),
        width=N.SPT_100,
        mini=True
    )
    return thisFab


class sptAppBar(UserControl):
    def __init__(self, bar):
        super().__init__()
        self.bar = bar

        def createCs(e):
            global spt_reference
            spt_reference["SptHome"].thisBottomSheet.open = True
            spt_reference["SptHome"].update()

        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            self.thisAppBar.update()

        self.thisAppBar = AppBar(
            leading=Icon(icons.VILLA),
            leading_width=N.SPT_40,
            title=Text(S.SPT_APP_NAME, color=C().SPT_LIGHT(), size=N.SPT_12),
            center_title=False,
            bgcolor=C().SPT_DARK(),

            actions=[

                IconButton(icons.FILTER_3),
                Text("  ", width=N.SPT_10, size=N.SPT_12),
                FloatingActionButton(
                    on_click=lambda e: createCs(e),

                    content=Row(
                        [Icon(icons.ADD), Text("Create", color=C().SPT_LIGHT())], alignment='center', spacing=N.SPT_5,

                    ),
                    bgcolor=C().SPT_DARK(),
                    shape=RoundedRectangleBorder(radius=5),
                    width=N.SPT_100 - N.SPT_10,
                    mini=True,

                ),
                Text("  ", width=N.SPT_10, size=N.SPT_12),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Item 1", ),
                        PopupMenuItem(),  # divider
                        PopupMenuItem(
                            text="Checked item", checked=False, on_click=check_item_clicked
                        ),
                    ]
                )
            ],
        )
        self.thisAppBar2 = AppBar(
            leading=Icon(icons.VILLA),
            leading_width=N.SPT_40,
            title=Text(S.SPT_APP_NAME, color=C().SPT_LIGHT(), size=N.SPT_12),
            center_title=False,
            bgcolor=C().SPT_DARK(),

            actions=[

                IconButton(icons.FILTER_3),
                Text("  ", width=N.SPT_10, size=N.SPT_12),
                Text("  ", width=N.SPT_10, size=N.SPT_12),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Item 1", ),
                    ]
                )
            ],
        )

    def build(self):
        if self.bar == 1:
            return self.thisAppBar
        else:
            return self.thisAppBar2


def sptDataTable():
    thisDataTable = Container(
        width=N.SPT_950,
        height=N.SPT_600,
        scale=getScale.getScaleFactor(),
        content=DataTable(
            scale=getScale.getScaleFactor(),
            visible=True,

            expand=True,
            column_spacing=N.SPT_5,
            bgcolor=C().SPT_LIGHT(),
            width=N.SPT_800,
            height=N.SPT_600,
            border=border.all(N.SPT_1, C().SPT_DARK()),
            border_radius=N.SPT_10,
            columns=[
                DataColumn(Text("First Name", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Last Name", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Division", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Station", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Module Grade", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Course Theory Grade", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(Text("Course Practical Grade", weight=FontWeight.BOLD, expand=True, size=N.SPT_12,
                                scale=getScale.getScaleFactor2())),
                DataColumn(
                    Text("Edit", weight=FontWeight.BOLD, expand=True, size=N.SPT_12, scale=getScale.getScaleFactor2()))
            ],

            rows=[

            ],
        )
    )
    return thisDataTable


def sptSearch(_filter):
    searchContainer = Container(
        scale=getScale.getScaleFactor(),
        bgcolor=C().SPT_MEDIUM_LIGHT(),
        width=N.SPT_200 + N.SPT_100,
        height=N.SPT_50 - N.SPT_9,
        border_radius=N.SPT_10 - N.SPT_2,
        alignment=alignment.bottom_center,
        content=TextField(
            # border=InputBorder.UNDERLINE,
            height=N.SPT_50,
            filled=False,
            label="Search",
            on_change=lambda e: sptFilter(e),
            scale=getScale.getScaleFactor()

        )
    )

    def sptFilter(x):

        for i in _filter:
            def l(y):
                return str(i.content.content.controls[y].value).lower()

            s = str(searchContainer.content.value).lower()
            if str(searchContainer.content.value) != "" and str(searchContainer.content.value) is not None:
                if s not in l(1) and s not in l(2) and s not in l(3) and s not in l(4):
                    i.visible = False
                    spt_reference["SptHome"].update()
                else:
                    i.visible = True
                    spt_reference["SptHome"].update()
            else:
                i.visible = True
                spt_reference["SptHome"].update()

    return searchContainer


def sptFilePicker():
    course = loadTemp(S.TEMP_VALUES)['thisCourse']

    # CREATE FUNCTION OPEN FILE
    def dialog_picker(e: FilePickerResultEvent):
        print(course)
        for x in e.files:
            shutil.copy2(x.path, P.IMAGES_DIR + x.name)
        setCourseImage(course, x.name)

        spt_reference["SptCourseDetails"].ui.ui.go('/load')
        time.sleep(0.13)
        spt_reference["SptCourseDetails"].ui.ui.go('/details')

    Mypick = FilePicker(on_result=dialog_picker)
    return Mypick


def sptDialog(course: str, page):
    def del_dlg(e):
        page.ui.go('/')
        deleteCourse(course, 'current')
        spt_reference["SptHome"].update()
        page.ui.go('/load')
        time.sleep(0.13)
        page.ui.go('/')

    def close_dlg(e):
        spt_dialog.open = False
        spt_dialog.update()
        page.ui.update()

    spt_dialog = AlertDialog(
        modal=True,
        title=Text(course, size=N.SPT_12),
        content=Text("Do you really want to delete this course?", size=N.SPT_12),
        actions=[
            TextButton("Yes", on_click=lambda e: del_dlg(e)),
            TextButton("No", on_click=lambda e: close_dlg(e)),
        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: close_dlg(e),
    )
    return spt_dialog


def sptDialog2(course: str, page):
    def no_err(e):
        spt_dialog.content.controls[2].error_text = None
        spt_dialog.update()

    def cre_dlg(e):
        module = str(spt_dialog.content.controls[2].value)

        if module != "" and module is not None:
            createModules(course, module)
            spt_reference["SptHome"].update()
            page.ui.go('/load')
            time.sleep(0.13)
            page.ui.go('/details')
        else:
            spt_dialog.content.controls[2].error_text = "No name provided."
            spt_dialog.update()

    def close_dlg(e):
        spt_dialog.open = False
        spt_dialog.update()
        page.ui.update()

    spt_dialog = AlertDialog(
        modal=True,
        title=Text(course, size=N.SPT_12),
        content=Column(
            height=N.SPT_100,
            controls=[
                Text("Type the name of the module you wish to create.", size=N.SPT_12),
                Divider(),
                TextField(height=N.SPT_50, label="Module", on_change=lambda e: no_err(e))
            ]
        ),
        actions=[
            TextButton("Create", on_click=lambda e: cre_dlg(e), scale=getScale.getScaleFactor2()),
            TextButton("Cancel", on_click=lambda e: close_dlg(e), scale=getScale.getScaleFactor2()),
        ],
        actions_alignment=MainAxisAlignment.CENTER,
        on_dismiss=lambda e: close_dlg(e),
    )
    return spt_dialog


def sptBottomSheet2():
    def close_bs(e):
        x = 0
        y = 1
        z = 2
        a = 0
        b = 1
        for i in thisBottomSheet.content.content.controls:
            if b > 4:
                break
            i.controls[x].value = ""
            a = a + 1
            i.controls[y].value = ""
            a = a + 1
            i.controls[z].value = ""
            a = a + 1
            b = b + 1
            pass
        thisBottomSheet.open = False
        thisBottomSheet.update()

    controlDict = {}
    novalControlDict = {}

    def setStudent(e):
        # thisBottomSheet.content.controls[0].controls[0].value
        x = 0
        y = 1
        z = 2
        a = 0
        b = 1
        key = 'key'

        for i in thisBottomSheet.content.content.controls:
            if b > 4:
                break
            controlDict[key + str(a)] = str(i.controls[x].value)
            novalControlDict[key + str(a)] = i.controls[x]
            a = a + 1
            controlDict[key + str(a)] = str(i.controls[y].value)
            novalControlDict[key + str(a)] = i.controls[y]
            a = a + 1
            controlDict[key + str(a)] = str(i.controls[z].value)
            novalControlDict[key + str(a)] = i.controls[z]
            a = a + 1
            b = b + 1
            pass
        if controlDict['key0'] != "" and controlDict['key0'] is not None and controlDict['key1'] != "" and controlDict[
            'key1'] is not None and controlDict['key5'] != "" and controlDict['key5'] is not None:
            addStudent(loadTemp(S.TEMP_VALUES)['thisCourse'],
                       firstName=controlDict['key0'], lastName=controlDict['key1'], ageRange=controlDict['key2'],
                       completedCourses=controlDict['key3'].split(','), ongoingCourses=controlDict['key4'].split(','),
                       regulationNumber=int(controlDict['key5']), rank=controlDict['key6'], email=controlDict['key7'],
                       mobile=controlDict['key8'], division=controlDict['key9'], station=controlDict['key10'])
            close_bs(0)
        else:
            if controlDict['key0'] == "" or controlDict['key0'] is None:
                novalControlDict['key0'].error_text = "Must complete"
                thisBottomSheet.update()
                pass
            if controlDict['key1'] == "" or controlDict['key1'] is None:
                novalControlDict['key1'].error_text = "Must complete"
                thisBottomSheet.update()
                pass
            if controlDict['key5'] == "" or controlDict['key5'] is None:
                novalControlDict['key5'].error_text = "Must be a valid number"
                thisBottomSheet.update()
                pass
            # close_bs(0)

    def clearError(e):
        novalControlDict['key0'].error_text = None
        novalControlDict['key1'].error_text = None
        thisBottomSheet.update()

    def isInt(e):

        if thisBottomSheet.content.content.controls[1].controls[2].value != "":
            _type = bool(re.match(r"^\d+$", str(thisBottomSheet.content.content.controls[1].controls[2].value)))

            if not _type:
                thisBottomSheet.content.content.controls[1].controls[2].error_text = "Must be a valid number"
                thisBottomSheet.update()
                pass
            else:
                thisBottomSheet.content.content.controls[1].controls[2].error_text = None
                thisBottomSheet.update()
        else:
            thisBottomSheet.content.content.controls[1].controls[2].error_text = None
            thisBottomSheet.update()

    thisBottomSheet = BottomSheet(
        content=Container(
            scale=getScale.getScaleFactor(),
            padding=N.SPT_10,
            border_radius=N.SPT_10 + N.SPT_2,
            content=Column(
                tight=True,
                controls=[
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[
                            TextField(label="First Name", border=InputBorder.UNDERLINE,
                                      on_change=lambda e: clearError(e)),
                            TextField(label="Last Name", border=InputBorder.UNDERLINE,
                                      on_change=lambda e: clearError(e)),
                            TextField(label="Age Range", hint_text="eg. 18-24", border=InputBorder.UNDERLINE)
                        ]
                    ),
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[
                            TextField(label="Completed Courses", border=InputBorder.UNDERLINE,
                                      hint_text="separate courses with comma: course 1,course 2,course3"),
                            TextField(label="Ongoing Courses", border=InputBorder.UNDERLINE,
                                      hint_text="separate courses with comma: course 1,course 2,course3"),
                            TextField(label="Regulation Number", border=InputBorder.UNDERLINE,
                                      on_change=lambda e: isInt(e))
                        ]
                    ),
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[
                            TextField(label="Rank", border=InputBorder.UNDERLINE),
                            TextField(label="Email", border=InputBorder.UNDERLINE),
                            TextField(label="Mobile", border=InputBorder.UNDERLINE)
                        ]
                    ),
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[

                            TextField(label="Division", border=InputBorder.UNDERLINE),
                            TextField(label="Station", border=InputBorder.UNDERLINE),
                            TextField(label=" ", border_color=colors.TRANSPARENT, read_only=True)
                        ]
                    ),
                    Row(
                        scale=getScale.getScaleFactor(),
                        controls=[
                            FilledButton("Save and close", on_click=lambda e: setStudent(e)),
                            FilledButton("Close without saving", on_click=lambda e: close_bs(e)),
                        ]
                    )
                ]
            )
        )
    )
    return thisBottomSheet


def sptChart(course, spt_y_series: list, spt_x_series: list, spt_bar_labels: list, name, spt_bar_colours: list = None):
    if spt_bar_colours is None:
        spt_bar_colours = []
        if len(spt_bar_labels) == len(spt_x_series):
            def switchCol(c):
                if c % 2 == 0:
                    barCol = C().SPT_MEDIUM_LIGHT()
                else:
                    barCol = C().SPT_MEDIUM_DARK()
                return barCol

            c = 2
            for i in spt_x_series:
                spt_bar_colours.append(switchCol(c))
                c = c + 1

    else:
        allSizeEqual = True
        allData = [spt_y_series, spt_x_series, spt_bar_labels, spt_bar_colours]
        firstDataSize = allData[0]
        for i in allData:
            if len(i) != firstDataSize:
                allSizeEqual = False
                break
        if not allSizeEqual:
            return 1

    def y_series_text(y):
        Y = "      " + str(y)
        return Y

    def get_x_Ratios():
        largestX = 0
        try:
            largestX = max(spt_x_series)
        except Exception as e:
            print(e)

        ratios = []
        for i in spt_x_series:
            if int(largestX) > 0:
                thisRatio = int(i) / int(largestX)
            else:
                thisRatio = 0
            ratios.append(thisRatio)
        return ratios

    def getBar():
        sptBar = Column(
            height=N.SPT_350,
            scale=getScale.getScaleFactor(),
            controls=[
                Text("     80%", size=N.SPT_12),
                Container(
                    border=border.all(N.SPT_1, C().SPT_DARK()),
                    width=N.SPT_50 + N.SPT_20,

                    content=Column(

                        alignment=MainAxisAlignment.END
                    )
                )
            ]
        )
        return sptBar

    thisChart = Column(
        scale=getScale.getScaleFactor(),
        height=N.SPT_400,
        spacing=N.SPT_2,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        controls=[
            Row(
                scale=getScale.getScaleFactor(),
                vertical_alignment=CrossAxisAlignment.END
            ),
            Row(
                scale=getScale.getScaleFactor(),
                controls=[
                    Container(
                        scale=getScale.getScaleFactor(),
                        border_radius=N.SPT_10,
                        bgcolor=C().SPT_LIGHT(),
                        # border=border.all(N.SPT_1, C().SPT_DARK()),
                        content=Text(size=N.SPT_12, scale=getScale.getScaleFactor()
                                     )
                    ),
                ]
            )
        ]
    )
    ratios = get_x_Ratios()
    index = len(spt_x_series) - 1
    counter = 0
    for i in spt_y_series:

        if counter > index:
            break
        else:
            firstInitial = getStudetByID(course, spt_bar_labels[counter])['firstName'][0]
            lastName = getStudetByID(course, spt_bar_labels[counter])['lastName']
            y_label = spt_y_series[counter]
            x_bar_height = ratios[counter] * N.SPT_300
            thisbar = getBar()

            thisbar.controls[1].bgcolor = spt_bar_colours[counter]
            if x_bar_height > 0:
                thisbar.controls[0].value = y_series_text(y_label)
                thisbar.controls[1].height = x_bar_height
                thisbar.controls[1].content.controls.append(
                    Text(firstInitial + ". " + lastName + "\n", no_wrap=True, size=N.SPT_12))
            else:
                thisbar.controls[1].height = x_bar_height
                thisbar.controls[0].value = y_series_text(y_label) + "\n" + firstInitial + ". " + lastName

            thisChart.controls[0].controls.append(thisbar)

            # thisChart.controls[0].controls.append(Text("     "))
            thisChart.controls[1].controls[0].content.value = name
            counter = counter + 1

    return thisChart


def sptBadge(title, body):
    thisBadge = Container(
        scale=getScale.getScaleFactor(),
        border=border.all(N.SPT_1, C().SPT_DARK()),
        border_radius=N.SPT_10,
        bgcolor=C().SPT_LIGHT(),

        content=Column(
            scale=getScale.getScaleFactor(),
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text(title, style=TextThemeStyle.TITLE_LARGE, size=N.SPT_30 + N.SPT_2),
                Divider(),
                Text(body, style=TextThemeStyle.BODY_LARGE, size=N.SPT_30 + N.SPT_4, selectable=True)
            ]
        )
    )
    return thisBadge
    pass


def sptDialog3(course, module, studentID, data, text_field, image):
    tf = text_field
    im = image

    def no_err(e):
        spt_dialog.content.controls[2].error_text = None
        spt_dialog.update()

    def cre_dlg(e):
        api_key = str(spt_dialog.content.controls[2].value)

        if api_key != "" and api_key != None:
            print(course)

            tf.value = "Generating analysis, please wait...."
            tf.update()
            close_dlg(0)
            analysis = getAnalysis(api_key, data)
            tf.value = ""
            tf.update()
            tf.value = analysis
            tf.update()
            setStudentQR(course, module, studentID, analysis)
            thisImage = getStudentQR(course, module, studentID)
            im.src = f"{thisImage}"
            im.update()
        else:
            spt_dialog.content.controls[2].error_text = "No api_key provided."
            spt_dialog.update()

    def close_dlg(e):
        spt_dialog.open = False
        spt_dialog.update()

    spt_dialog = AlertDialog(
        modal=True,
        title=Text(course),
        content=Column(
            spacing=N.SPT_2,
            height=N.SPT_100,
            controls=[
                Text("Enter your api_key.", size=N.SPT_12),
                Divider(),
                TextField(label="API_KEY", on_change=lambda e: no_err(e), password=True, can_reveal_password=True,
                          height=N.SPT_100, autofocus=True)
            ]
        ),
        actions=[
            TextButton("Generate", on_click=lambda e: cre_dlg(e), scale=getScale.getScaleFactor2()),
            TextButton("Cancel", on_click=lambda e: close_dlg(e), scale=getScale.getScaleFactor2()),
        ],
        actions_alignment=MainAxisAlignment.CENTER,
        on_dismiss=lambda e: close_dlg(e),
    )
    return spt_dialog


def sptDialog4(course, module, studentID):
    def close_dlg(e):
        spt_dialog.open = False
        spt_dialog.update()

    spt_dialog = AlertDialog(
        modal=True,

        title=Text(course),
        content=Column(
            width=N.SPT_800,
            height=N.SPT_800,
            controls=[
                Image(
                    width=N.SPT_800,
                    height=N.SPT_800,
                    border_radius=border_radius.all(N.SPT_10),
                    fit=ImageFit.CONTAIN,
                )
            ]
        ),
        actions=[
            TextButton("Close", on_click=lambda e: close_dlg(e), scale=getScale.getScaleFactor2()),
        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: close_dlg(e),
    )
    spt_dialog.content.controls[0].src = f"{getStudentQR(course, module, studentID)}"
    return spt_dialog
