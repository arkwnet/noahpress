import NoahClass
import NoahCommon
import NoahComponent
import NoahProject

import cv2
import pickle
import tkinter
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog, messagebox

class Application(tkinter.Frame):
    def exit(self):
        if self.is_edit == True:
            rsp = messagebox.askyesno("", NoahCommon.MESSAGE_IS_EDIT)
        if self.is_edit == False or (self.is_edit == True and rsp == True):
            self.master.quit()
        return

    def set_title(self):
        title = ""
        if self.filename == "":
            title = "無題 - " + NoahCommon.PRODUCT_NAME
        else:
            title = self.filename + " - " + NoahCommon.PRODUCT_NAME
        self.master.title(title)
        return

    def file_new(self):
        if self.is_edit == True:
            rsp = messagebox.askyesno("", NoahCommon.MESSAGE_IS_EDIT)
        if self.is_edit == False or (self.is_edit == True and rsp == True):
            self.project = NoahProject.Project()
            self.filename = ""
            self.is_edit = False
            self.is_draw = True
            self.set_title()
        return

    def file_open(self):
        if self.is_edit == True:
            rsp = messagebox.askyesno("", NoahCommon.MESSAGE_IS_EDIT)
        if self.is_edit == False or (self.is_edit == True and rsp == True):
            fn = filedialog.askopenfilename(filetypes = [("NoahPress プロジェクト", "*.npp")])
            if fn != "":
                with open(fn, mode = "rb") as f:
                    self.filename = fn
                    self.is_edit = False
                    self.is_draw = True
                    self.set_title()
                    self.project = pickle.load(f)
        return

    def file_save(self):
        if self.filename != "":
            self.file_save_process()
        else:
            self.file_save_as()
        return

    def file_save_as(self):
        fn = filedialog.asksaveasfilename(filetypes = [("NoahPress プロジェクト", "*.npp")])
        if fn != "":
            if fn.find(".npp") == -1:
                fn = fn + ".npp"
            self.filename = fn
            self.set_title()
            self.file_save_process()
        return

    def file_save_process(self):
        with open(self.filename, mode = "wb") as f:
            pickle.dump(self.project, f)
        self.is_edit = False
        return

    def file_export_png(self):
        fn = filedialog.asksaveasfilename(filetypes = [("PNG 画像ファイル", "*.png")])
        if fn != "":
            if fn.find(".png") == -1:
                fn = fn + ".png"
            cv2.imwrite(fn, self.draw())
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
        self.is_draw = True
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
            self.is_edit = True
            self.is_draw = True
        return

    def scroll_horizontal(self, *args):
        if args[0] == "moveto":
            self.position_horizontal = float(args[1])
        elif args[0] == "scroll":
            self.position_horizontal += int(args[1]) * 0.01
        self.position_horizontal = max(0, min(1, self.position_horizontal))
        self.master.scroll_horizontal.set(self.position_horizontal, self.position_horizontal)
        self.master.canvas.place_configure(x = -1.0 * self.project.pixel_zoom(self.project.get_width_px()) * self.position_horizontal)
        return

    def scroll_vertical(self, *args):
        if args[0] == "moveto":
            self.position_vertical = float(args[1])
        elif args[0] == "scroll":
            self.position_vertical += int(args[1]) * 0.01
        self.position_vertical = max(0, min(1, self.position_vertical))
        self.master.scroll_vertical.set(self.position_vertical, self.position_vertical)
        self.master.canvas.place_configure(y = -1.0 * self.project.pixel_zoom(self.project.get_height_px()) * self.position_vertical)
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

    def draw(self):
        image_bgr_in = 255 * np.ones((self.project.get_height_px(), self.project.get_width_px(), 3), np.uint8)
        for i in range(len(self.project.data)):
            x = self.project.mm_to_px(self.project.data[i].x)
            y = self.project.mm_to_px(self.project.data[i].y)
            if self.project.data[i].mode == NoahComponent.COMPONENT_RECTANGLE:
                cv2.rectangle(image_bgr_in, (x, y), (x + self.project.mm_to_px(self.project.data[i].w), y + self.project.mm_to_px(self.project.data[i].h)), self.project.data[i].fill, thickness = -1)
            elif self.project.data[i].mode == NoahComponent.COMPONENT_TEXT:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\" + self.project.data[i].obj.font, self.project.data[i].obj.size)
                img = Image.fromarray(image_bgr_in)
                draw = ImageDraw.Draw(img)
                tx = x
                ty = y
                for char in self.project.data[i].obj.body:
                    draw.text((tx, ty), char, font = font, fill = self.project.data[i].fill)
                    tx = tx + self.project.data[i].obj.size
                    if tx > x + self.project.mm_to_px(self.project.data[i].w):
                        tx = x
                        ty = ty + self.project.data[i].obj.lh
                    if ty > y + self.project.mm_to_px(self.project.data[i].h):
                        break
                image_bgr_in = np.array(img)
        return image_bgr_in

    def loop(self):
        if self.is_draw == True:
            exw = self.project.pixel_zoom(self.project.get_width_px())
            exh = self.project.pixel_zoom(self.project.get_height_px())
            image_bgr_ex = 255 * np.ones((exh, exw, 3), np.uint8)
            image_bgr_resize = cv2.resize(self.draw(), (exw, exh), interpolation = cv2.INTER_NEAREST)
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
            self.is_draw = False
        self.after(int(1000 / 10), self.loop)

    def __init__(self, master = None):
        super().__init__(master)
        self.master.geometry(str(NoahCommon.MAIN_WINDOW_WIDTH) + "x" + str(NoahCommon.MAIN_WINDOW_HEIGHT))
        self.master.resizable(0, 0)
        self.master.bind("<Motion>", self.mouse_move)
        self.master.protocol("WM_DELETE_WINDOW", self.exit)

        self.master.frame_tool = tkinter.Frame(self.master, bg = NoahCommon.COLOR_WHITE)
        self.master.frame_tool.place(x = 0, y = 0, w = 40, h = NoahCommon.MAIN_WINDOW_HEIGHT)

        self.master.frame_main = tkinter.Frame(self.master)
        self.master.frame_main.place(x = 40, y = 0, w = NoahCommon.MAIN_WINDOW_WIDTH - 40, h = NoahCommon.MAIN_WINDOW_HEIGHT)
        self.master.canvas = tkinter.Canvas(self.master.frame_main, borderwidth = 1, relief = "solid")
        self.master.canvas.place(x = 0, y = 0)
        self.master.canvas.bind("<Button-1>", self.mouse_down)
        self.master.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.master.scroll_horizontal = tkinter.Scrollbar(self.master.frame_main, orient = "horizontal")
        self.master.scroll_horizontal.config(command = self.scroll_horizontal)
        self.master.scroll_horizontal.place(x = 0, y = NoahCommon.MAIN_WINDOW_HEIGHT - NoahCommon.SCROLL_SIZE, w = NoahCommon.MAIN_WINDOW_WIDTH - NoahCommon.SCROLL_SIZE - 40, h = NoahCommon.SCROLL_SIZE)
        self.position_horizontal = 0.0
        self.master.scroll_horizontal.set(self.position_horizontal, self.position_horizontal)
        self.master.scroll_vertical = tkinter.Scrollbar(self.master.frame_main, orient = "vertical")
        self.master.scroll_vertical.config(command = self.scroll_vertical)
        self.master.scroll_vertical.place(x = NoahCommon.MAIN_WINDOW_WIDTH - NoahCommon.SCROLL_SIZE - 40, y = 0, w = NoahCommon.SCROLL_SIZE, h = NoahCommon.MAIN_WINDOW_HEIGHT - NoahCommon.SCROLL_SIZE)
        self.position_vertical = 0.0
        self.master.scroll_vertical.set(self.position_vertical, self.position_vertical)

        self.master.menu = tkinter.Menu(self.master)
        self.master.config(menu = self.master.menu)
        self.master.menu_file = tkinter.Menu(self.master, tearoff = 0)
        self.master.menu.add_cascade(label = "ファイル", menu = self.master.menu_file)
        self.master.menu_file.add_command(label = "新規作成", command = self.file_new)
        self.master.menu_file.add_command(label = "開く", command = self.file_open)
        self.master.menu_file.add_command(label = "上書き保存", command = self.file_save)
        self.master.menu_file.add_command(label = "名前を付けて保存", command = self.file_save_as)
        self.master.menu_file.add_command(label = "PNG画像出力", command = self.file_export_png)
        self.master.menu_file.add_separator()
        self.master.menu_file.add_command(label = "閉じる", command = self.exit)

        self.filename = ""
        self.is_edit = False
        self.is_draw = True
        self.image_tk = None
        self.project = NoahProject.Project()
        self.mouse = NoahClass.Mouse(False, 0, 0, None)

        self.set_title()
        self.project.data.append(NoahComponent.Box(NoahComponent.COMPONENT_RECTANGLE, 10, 10, 60, 40, (255, 0, 0), None))
        self.project.data.append(NoahComponent.Box(NoahComponent.COMPONENT_TEXT, 20, 20, 200, 100, (0, 255, 0), NoahComponent.Text("MINIX/ミニックスは、1987年にオランダ・アムステルダム自由大学の教授であるアンドリュー・タネンバウムが教育目的で開発したUNIX系の軽量オペレーティングシステムで、マイクロカーネル方式を採用し構造が単純で理解しやすいことを特徴とし、後にLinux誕生にも影響を与えた。", "msgothic.ttc", 220, 240)))
        self.update()
        self.loop()
