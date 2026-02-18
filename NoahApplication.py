import NoahClass
import NoahCommon
import NoahComponent
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
        hit = False
        mx = event.x
        my = event.y
        for i in range(len(self.project.data) - 1, -1, -1):
            bx = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].x))
            by = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].y))
            bw = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].w))
            bh = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].h))
            if hit == False and mx >= bx and mx <= bx + bw and my >= by and my <= by + bh:
                self.project.data[i].select = 1
                self.mouse = NoahClass.Mouse(True, mx - bx, my - by, i)
                hit = True
            else:
                self.project.data[i].select = 0
        self.draw(self.project.data)
        return

    def mouse_up(self, event):
        self.mouse.status = False
        return

    def mouse_move(self, event):
        if self.mouse.status == True:
            if self.project.unit == "px":
                self.project.data[self.mouse.i].x = int((event.x - self.mouse.x) * (100 / self.project.zoom))
                self.project.data[self.mouse.i].y = int((event.y - self.mouse.y) * (100 / self.project.zoom))
            elif self.project.unit == "mm":
                self.project.data[self.mouse.i].x = int(self.project.px_to_mm(event.x - self.mouse.x) * (100 / self.project.zoom))
                self.project.data[self.mouse.i].y = int(self.project.px_to_mm(event.y - self.mouse.y) * (100 / self.project.zoom))
            self.draw(self.project.data)
        return

    def update(self):
        self.master.canvas.place(w = self.project.pixel_zoom(self.project.get_width_px()), h = self.project.pixel_zoom(self.project.get_height_px()))
        return

    def draw_dashed_line(self, img, start, end, dash = 2, gap = 3, fill = "black", width = 1):
        x1, y1 = start
        x2, y2 = end
        total = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dx = (x2 - x1) / total
        dy = (y2 - y1) / total
        step = dash + gap
        for i in range(0, int(total), step):
            sx = x1 + dx * i
            sy = y1 + dy * i
            ex = x1 + dx * min(i + dash, total)
            ey = y1 + dy * min(i + dash, total)
            img.line((sx, sy, ex, ey), fill = fill, width = width)
        return

    def draw(self, data):
        inw = self.project.get_width_px()
        inh = self.project.get_height_px()
        exw = self.project.pixel_zoom(inw)
        exh = self.project.pixel_zoom(inh)
        image_bgr_in = 255 * np.ones((inh, inw, 3), np.uint8)
        image_bgr_ex = 255 * np.ones((exh, exw, 3), np.uint8)
        for i in range(len(self.project.data)):
            x = self.project.mm_to_px(self.project.data[i].x)
            y = self.project.mm_to_px(self.project.data[i].y)
            cv2.rectangle(image_bgr_in, (x, y), (x + self.project.mm_to_px(self.project.data[i].w), y + self.project.mm_to_px(self.project.data[i].h)), self.project.data[i].fill, thickness = -1)
        image_bgr_resize = cv2.resize(image_bgr_in, (exw, exh), interpolation = cv2.INTER_AREA)
        image_bgr_ex[:, :] = image_bgr_resize
        image_rgb = cv2.cvtColor(image_bgr_ex, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_draw = ImageDraw.Draw(image_pil)
        for i in range(len(self.project.data)):
            x = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].x))
            y = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].y))
            w = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].w))
            h = self.project.pixel_zoom(self.project.mm_to_px(self.project.data[i].h))
            if self.project.data[i].select == True:
                image_draw.line((x, y, x + w, y), fill = "black", width = 1)
                image_draw.line((x, y, x, y + h), fill = "black", width = 1)
                image_draw.line((x, y + h, x + w, y + h), fill = "black", width = 1)
                image_draw.line((x + w, y, x + w, y + h), fill = "black", width = 1)
            else:
                self.draw_dashed_line(image_draw, (x, y), (x + w, y))
                self.draw_dashed_line(image_draw, (x, y), (x, y + h))
                self.draw_dashed_line(image_draw, (x, y + h), (x + w, y + h))
                self.draw_dashed_line(image_draw, (x + w, y), (x + w, y + h))
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
        self.mouse = NoahClass.Mouse(False, 0, 0, None)

        self.project.data.append(NoahComponent.Box(NoahComponent.COMPONENT_RECTANGLE, 10, 10, 60, 40, (255, 0, 0)))
        self.project.data.append(NoahComponent.Box(NoahComponent.COMPONENT_RECTANGLE, 30, 30, 50, 50, (0, 255, 0)))
        self.update()
        self.draw(self.project.data)
