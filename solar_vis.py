# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *

from solar_model import *

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""


class GUI:
    def __init__(self):

        self.start_button = None

        self.space = None

        self.header_font = "Arial-16"
        """Шрифт в заголовке"""

        self.window_width = 800
        """Ширина окна"""

        self.window_height = 800
        """Высота окна"""

        self.scale_factor = None
        """Масштабирование экранных координат по отношению к физическим.
        Тип: float
        Мера: количество пикселей на один метр."""

        self.displayed_time = None
        """Отображаемое на экране время.
        Тип: переменная tkinter"""

        self.load_file_button = None
        self.save_file_button = None
        self.time_label = None

    def calculate_scale_factor(self, max_distance):
        """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
        self.scale_factor = 0.4*min(self.window_height, self.window_width)/max_distance
        print('Scale factor:', self.scale_factor)


    def scale_x(self, x):
        """Возвращает экранную **x** координату по **x** координате модели.
        Принимает вещественное число, возвращает целое число.
        В случае выхода **x** координаты за пределы экрана возвращает
        координату, лежащую за пределами холста.

        Параметры:

        **x** — x-координата модели.
        """

        return int(x*self.scale_factor) + self.window_width//2


    def scale_y(self, y):
        """Возвращает экранную **y** координату по **y** координате модели.
        Принимает вещественное число, возвращает целое число.
        В случае выхода **y** координаты за пределы экрана возвращает
        координату, лежащую за пределами холста.
        Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

        Параметры:

        **y** — y-координата модели.
        """

        return int(y*self.scale_factor) + self.window_height//2


    def create_star_image(self, space, star):
        """Создаёт отображаемый объект звезды.

        Параметры:

        **space** — холст для рисования.
        **star** — объект звезды.
        """

        x = self.scale_x(star.x)
        y = self.scale_y(star.y)
        r = star.R
        star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


    def create_planet_image(self, space, planet):
        """Создаёт отображаемый объект планеты.

        Параметры:

        **space** — холст для рисования.
        **planet** — объект планеты.
        """

        x = self.scale_x(planet.x)
        y = self.scale_y(planet.y)
        r = planet.R
        planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)


    def update_system_name(self, space, system_name):
        """Создаёт на холсте текст с названием системы небесных тел.
        Если текст уже был, обновляет его содержание.

        Параметры:

        **space** — холст для рисования.
        **system_name** — название системы тел.
        """
        space.create_text(30, 80, tag="header", text=system_name, font=self.header_font)


    def update_object_position(self, space, body):
        """Перемещает отображаемый объект на холсте.

        Параметры:

        **space** — холст для рисования.
        **body** — тело, которое нужно переместить.
        """
        x = self.scale_x(body.x)
        y = self.scale_y(body.y)
        r = body.R
        if x + r < 0 or x - r > self.window_width or y + r < 0 or y - r > self.window_height:
            space.coords(body.image, self.window_width + r, self.window_height + r,
                         self.window_width + 2*r, self.window_height + 2*r)  # положить за пределы окна
        space.coords(body.image, x - r, y - r, x + r, y + r)

    @staticmethod
    def main(solar_system, inout_system, gui):
        """Главная функция главного модуля.
        Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
        """

        print('Modelling started!')

        root = tkinter.Tk()

        # космическое пространство отображается на холсте типа Canvas
        gui.space = tkinter.Canvas(root, width=gui.window_width, height=gui.window_height, bg="black")
        gui.space.pack(side=tkinter.TOP)
        # нижняя панель с кнопками
        frame = tkinter.Frame(root)
        frame.pack(side=tkinter.BOTTOM)

        gui.start_button = tkinter.Button(frame, text="Start", command=solar_system.start_execution, width=6)
        gui.start_button.pack(side=tkinter.LEFT)

        solar_system.time_step = tkinter.DoubleVar()
        solar_system.time_step.set(1)
        solar_system.time_step_entry = tkinter.Entry(frame, textvariable=solar_system.time_step)
        solar_system.time_step_entry.pack(side=tkinter.LEFT)

        solar_system.time_speed = tkinter.DoubleVar()
        scale = tkinter.Scale(frame, variable=solar_system.time_speed, orient=tkinter.HORIZONTAL)
        scale.pack(side=tkinter.LEFT)

        gui.load_file_button = tkinter.Button(frame, text="Open file...", command=lambda: inout_system.open_file_dialog(solar_system, gui))
        gui.load_file_button.pack(side=tkinter.LEFT)
        gui.save_file_button = tkinter.Button(frame, text="Save to file...", command=lambda: inout_system.save_file_dialog(solar_system))
        gui.save_file_button.pack(side=tkinter.LEFT)

        gui.displayed_time = tkinter.StringVar()
        gui.displayed_time.set(str(solar_system.physical_time) + " seconds gone")
        gui.time_label = tkinter.Label(frame, textvariable=gui.displayed_time, width=30)
        gui.time_label.pack(side=tkinter.RIGHT)

        root.mainloop()
        print('Modelling finished!')


gui = GUI()


if __name__ == "__main__":
    print("This module is not for direct call!")
