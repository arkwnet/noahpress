import NoahCommon
import NoahProject

import cv2
import tkinter
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
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
        self.master.canvas.place(w = self.project.pixel_zoom(self.project.get_width_px()), h = self.project.pixel_zoom(self.project.get_height_px()))
        return

    def draw(self, data):
        inw = self.project.get_width_px()
        inh = self.project.get_height_px()
        exw = self.project.pixel_zoom(inw)
        exh = self.project.pixel_zoom(inh)
        image_bgr_in = 255 * np.ones((inh, inw, 3), np.uint8)
        image_bgr_ex = 255 * np.ones((exh, exw, 3), np.uint8)
        cv2.rectangle(image_bgr_in, (100, 100), (800, 600), (255, 0, 0), thickness = -1)
        image_bgr_resize = cv2.resize(image_bgr_in, (exw, exh), interpolation = cv2.INTER_AREA)
        image_bgr_ex[:, :] = image_bgr_resize
        image_rgb = cv2.cvtColor(image_bgr_ex, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.master.canvas.create_image(0, 0, image = self.image_tk, anchor = "nw")
        return

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
        self.master.canvas = tkinter.Canvas(self.master.frame_main, borderwidth = 1, relief = "solid")
        self.master.canvas.place(x = 10, h = 10)
        self.master.canvas.bind("<Button-1>", self.mouse_down)
        self.master.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.filename = ""
        self.is_edit = False
        self.image_tk = None
        self.project = NoahProject.Project()

        self.update()
        self.draw(self.project.data)
