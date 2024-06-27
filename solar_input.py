# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
import tkinter
from tkinter.filedialog import *
from solar_model import *

class InOut_system:
    def read_space_objects_data_from_file(self, input_filename):
        """Cчитывает данные о космических объектах из файла, создаёт сами объекты
        и вызывает создание их графических образов

        Параметры:

        **input_filename** — имя входного файла
        """
        objects = []
        with open(input_filename) as input_file:
            for line in input_file:
                if len(line.strip()) == 0 or line[0] == '#':
                    continue  # пустые строки и строки-комментарии пропускаем
                object_type = line.split()[0].lower()
                if object_type == "star":
                    star = Star()
                    self.parse_star_parameters(line, star)
                    objects.append(star)
                else:
                    print("Unknown space object")

                if object_type == "planet":
                    planet = Planet()
                    self.parse_planet_parameters(line, planet)
                    objects.append(planet)
                else:
                    print("Unknown space object")

        return objects

    @staticmethod
    def parse_star_parameters(line, star):
        """Считывает данные о звезде из строки.
        Входная строка должна иметь слеюущий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
        Пример строки:
        Star 10 red 1000 1 2 3 4

        Параметры:

        **line** — строка с описание звезды.
        **star** — объект звезды.
        """
        words = line.split()
        star.R = float(words[1])
        star.color = words[2]
        star.m = float(words[3])
        star.x, star.y = float(words[4]), float(words[5])
        star.Vx, star.Vy = float(words[6]), float(words[7])

    @staticmethod
    def parse_planet_parameters(line, planet):
        """Считывает данные о планете из строки.
        Предполагается такая строка:
        Входная строка должна иметь слеюущий формат:
        Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
        Пример строки:
        Planet 10 red 1000 1 2 3 4

        Параметры:

        **line** — строка с описание планеты.
        **planet** — объект планеты.
        """

        words = line.split()
        planet.R = float(words[1])
        planet.color = words[2]
        planet.m = float(words[3])
        planet.x, planet.y = float(words[4]), float(words[5])
        planet.Vx, planet.Vy = float(words[6]), float(words[7])

    @staticmethod
    def write_space_objects_data_to_file(output_filename, space_objects):
        """Сохраняет данные о космических объектах в файл.
        Строки должны иметь следующий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
        Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Параметры:

        **output_filename** — имя входного файла
        **space_objects** — список объектов планет и звёзд
        """
        with open(output_filename, 'w') as out_file:
            for obj in space_objects:
                if obj.type == "star":
                    out_file.write("Star %f %s %f %f %f %f %f \n" % (obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy))
                    print(out_file, "Star %f %s %f %f %f %f %f \n" % (obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy))
                if obj.type == "planet":
                    out_file.write("Planet %f %s %f %f %f %f %f \n" % (obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy))
                    print(out_file, "Planet %f %s %f %f %f %f %f \n" % (obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy))

    @staticmethod
    def open_file_dialog(solar_system, gui):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список space_objects
        """

        solar_system.perform_execution = False
        for obj in solar_system.space_objects:
            gui.space.delete(obj.image)  # удаление старых изображений планет
        in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
        solar_system.space_objects = inout_system.read_space_objects_data_from_file(in_filename)
        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in solar_system.space_objects])
        gui.calculate_scale_factor(max_distance)

        for obj in solar_system.space_objects:
            if obj.type == 'star':
                gui.create_star_image(gui.space, obj)
            elif obj.type == 'planet':
                gui.create_planet_image(gui.space, obj)
            else:
                raise AssertionError()

    def save_file_dialog(self, solar_system):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в список space_objects
        """
        out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
        self.write_space_objects_data_to_file(out_filename, solar_system.space_objects)

inout_system = InOut_system()

if __name__ == "__main__":
    print("This module is not for direct call!")
