from spt_components.spt_elements import *
from spt_lib.spt_ref import *
from spt_lib.spt_theme import *
import json
import time

control_map = return_spt_reference()


class SptHome(UserControl):
    def __init__(self, ui):
        self.ui = ui
        # self.page = Page
        # self.ui.bgcolor="#000000"
        # self.ui.update()
        super().__init__()
        global bar
        bar = 1

        self.getHome = self.Home()

        self.populateCourses()
        self.data = {}

    def getCourses(self):
        courseList = []
        activeCourses = loadActiveCourses()
        for courses in activeCourses:
            if courses['name'] == "":
                continue
            else:
                courseList.append(sptCard(courses['name'], courses['students'], courses['start'], courses['end'], self))
        return courseList

    def homeRef(self):
        add_to_spt_reference("SptHome", self)

    thisBottomSheet = sptBottomSheet()

    # thisFilePicker = sptFIlePicker()

    def createCsH(self):
        # self.page.go('/')
        self.thisBottomSheet.open = True

    homeList = []

    def Home(self):
        # self.thisBottomSheet.content.content.controls[2].append(self.thisFilePicker)
        home = Column(
            expand=True,
            scroll=ScrollMode.ALWAYS,
            controls=[
                Container(
                    # getHome.controls[0].content.controls[1].content.options.append(dropdown.Option(i))
                    border_radius=N.SPT_10,
                    padding=N.SPT_10,
                    bgcolor=C().SPT_DARK(),
                    border=border.all(N.SPT_2, C().SPT_BLACK()),
                    content=Row(
                        controls=[
                            sptFab(),
                            sptSearch(self.homeList),
                            Container(
                                bgcolor=C().SPT_MEDIUM_LIGHT(),
                                border_radius=N.SPT_5,
                                # expand=True,
                                content=Dropdown(
                                    bgcolor=C().SPT_MEDIUM_LIGHT(),
                                    content_padding=N.SPT_5,
                                    label="Theme",
                                    hint_text="Change Theme",
                                    height=N.SPT_50 - N.SPT_10,
                                    width=N.SPT_200,
                                    color=C().SPT_BLACK(),
                                    on_change=lambda e: self.changeTheme()
                                )),

                        ]
                    )
                ),
                Container(
                    # border=border.all(width=N.SPT_2, color=C.SPT_DARK),
                    border_radius=N.SPT_10,
                    # bgcolor=C().SPT_BLACK(),
                    # expand=1,
                    content=GridView(
                        scale=getScale.getScaleFactor(),
                        expand=1,
                        runs_count=N.SPT_2,
                        max_extent=N.SPT_400,
                        child_aspect_ratio=1.0,
                        spacing=N.SPT_5,
                        run_spacing=N.SPT_5,

                    )

                ),
                Row(
                    alignment=MainAxisAlignment.END,

                    controls=[

                        self.thisBottomSheet,
                    ]
                ),

            ]
        )

        return home

    def populateCourses(self):
        coursesInfo = self.getCourses()
        self.getHome.controls[1].content.controls.clear()
        for i in coursesInfo:
            self.getHome.controls[1].content.controls.append(i)
            self.homeList.append(i)

    def changeTheme(self):
        selctedTheme = self.getHome.controls[0].content.controls[2].content.value
        themeindex = getObjectIndexFromList(getThemeDB(), 'spt_themes', 'name', str(selctedTheme))
        with open(P.CONFIG_DIR + S.SPT_THEME) as tDB:
            newTheme = json.load(tDB)
            newTheme['sptTheme'] = themeindex
        saveTheme(newTheme)
        self.toggle()

    def toggle(self):
        self.ui.go('/load')
        time.sleep(0.13)
        self.ui.go('/')

    def build(self):
        themes = getThemeList()
        for i in themes:
            self.getHome.controls[0].content.controls[2].content.options.append(dropdown.Option(str(i)))
            pass
        self.getHome.controls[0].content.controls[2].content.value = C().SPT_CURRENT_THEME()

        # getHome.controls[0].content.controls[1].content.options.append(dropdown.Option(i))
        self.homeRef()

        # self.populateCourses()
        # self.ui.add(sptAppBar(1))
        return self.getHome
