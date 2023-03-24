from spt_components.spt_home import SptHome
from spt_components.spt_course_details import SptCourseDetails
from spt_components.spt_load import SptLoad
from flet import *


def sptViews(page, home):
    return {
        '/': View(
            route='/',
            controls=[

                SptHome(page),
            ]
        ),
        '/details': View(
            route='/details',
            controls=[
                SptCourseDetails(home)
            ]
        ),
        '/load': View(
            route='/load',
            controls=[
                SptLoad(home)
            ]
        ),
    }
