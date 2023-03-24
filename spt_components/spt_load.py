from flet import *
from spt_lib.spt_ref import *

control_map = return_spt_reference()

class SptLoad(UserControl):
    def __init__(self, ui):
        self.ui = ui
        super().__init__()
        self.startLoad = self.spt_Load()
        self.homeRef()

    def homeRef(self):
        add_to_spt_reference("SptCourseDetails", self)
    
    def spt_Load(self):
        
        sptLoad=Column(
            expand=True,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                IconButton(icon=icons.ARROW_BACK_IOS_NEW,
                on_click=lambda e:self.back(e)
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text("Loading..")
                    ]
                )
            ]
        )
        return sptLoad
        
    def back(self,e):
        self.ui.ui.go('/')
    
    def build(self):
        return self.startLoad