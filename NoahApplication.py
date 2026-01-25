import NoahCommon
import NoahProject
import tkinter
from tkinter import messagebox

class Application(tkinter.Frame):
    def exit(self):
        if self.is_edit == True:
            rsp = messagebox.askyesno("", "編集中の内容は破棄されます。よろしいですか?")
        if self.is_edit == False or (self.is_edit == True and rsp == True):
            self.master.quit()
        return

    def mouse_down(self, event):
        return

    def mouse_up(self, event):
        return

    def mouse_move(self, event):
        return

    def update(self):
        dw = int(self.project.w * self.project.dpi / NoahCommon.ONE_INCH_MM * (self.project.zoom / 100))
        dh = int(self.project.h * self.project.dpi / NoahCommon.ONE_INCH_MM * (self.project.zoom / 100))
        self.master.canvas.place(w = dw, h = dh)

    def __init__(self, master = None):
        super().__init__(master)
        self.master.geometry(str(NoahCommon.MAIN_WINDOW_WIDTH) + "x" + str(NoahCommon.MAIN_WINDOW_HEIGHT))
        self.master.title("無題 - " + NoahCommon.PRODUCT_NAME)
        self.master.resizable(0, 0)
        self.master.bind("<Motion>", self.mouse_move)
        self.master.protocol("WM_DELETE_WINDOW", self.exit)

        self.master.frame_tool = tkinter.Frame(self.master, bg = NoahCommon.COLOR_WHITE)
        self.master.frame_tool.place(x = 0, y = 0, w = 40, h = NoahCommon.MAIN_WINDOW_HEIGHT)

        self.master.frame_main = tkinter.Frame(self.master)
        self.master.frame_main.place(x = 40, y = 0, w = NoahCommon.MAIN_WINDOW_WIDTH - 40, h = NoahCommon.MAIN_WINDOW_HEIGHT)
        self.master.canvas = tkinter.Canvas(self.master.frame_main, borderwidth = 1, relief = "solid", bg = NoahCommon.COLOR_WHITE)
        self.master.canvas.place(x = 10, h = 10)
        self.master.canvas.bind("<Button-1>", self.mouse_down)
        self.master.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.filename = ""
        self.is_edit = False
        self.image_bgr = None
        self.project = NoahProject.Project()

        self.update()
