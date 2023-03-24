import flet as ft
from spt_lib.spt_data import *
from spt_lib.spt_course_calculations import *
from spt_lib.spt_constants import SptNumbers as N
from spt_lib.spt_constants import SptStrings as S
from spt_lib.spt_ref import *
from spt_lib.spt_views import *
from spt_lib.spt_course_calculations import ZoomFactor as getScale

control_map = return_spt_reference()


def setPlatformScaling():
    OS = getOS()
    if OS.lower() == 'linux':
        getScale.setScaleFactor2(1.0)
        N.load_last_zoom_factor()
    else:
        getScale.setScaleFactor2(0.6)
        N.load_last_zoom_factor()


def courseCreate(_name, _startDate, _endDate, _numOfStudents):
    createCourse(_name, _startDate, _endDate, _numOfStudents)


def databaseImport(_path):
    importDataBase(_path)


def startDatabaseExport():
    curr_date_time = datetime.now()
    thisDate = curr_date_time.strftime("%d_%m_%Y_%H_%M_%S")
    exportDataBase()
    compress_folder_to_zip("data/exportedTmp/" + thisDate, thisDate + ".zip")
    sendDataBase(thisDate + ".zip")


def main(ui: Page):
    setPlatformScaling()
    ui.title = S.SPT_APP_NAME
    ui.window_min_width = N.SPT_1850
    ui.window_min_height = N.SPT_1000
    ui.window_maximized = True
    home = SptHome(ui)

    def route_change(route):
        ui.views.clear()
        ui.views.append(
            sptViews(ui, home)[ui.route]
        )

    ui.on_route_change = route_change
    ui.go('/')


if __name__ == "__main__":
    # WEB_BROWSER and WindowsOS scaling issues
    # retrieving student qr images in browser and on windows
    ft.app(target=main, assets_dir=P.ASSETS_DIR)
