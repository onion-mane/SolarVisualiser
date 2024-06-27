# coding: utf-8
# license: GPLv3

from solar_vis import *
class Solar_system:

    def __init__(self):
        self.gravitational_constant = 6.67408E-11
        """Гравитационная постоянная Ньютона G"""

        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""

        self.physical_time = 0
        """Физическое время от начала расчёта.
        Тип: float"""



        self.time_step = None
        """Шаг по времени при моделировании.
        Тип: float"""

        self.time_speed = None

        self.time_step = None
        self.time_step_entry = None
        self.space_objects = []
        """Список космических объектов."""

    @staticmethod
    def calculate_force(body, space_objects):
        """Вычисляет силу, действующую на тело.

        Параметры:

        **body** — тело, для которого нужно вычислить дейстующую силу.
        **space_objects** — список объектов, которые воздействуют на тело.
        """

        body.Fx = body.Fy = 0
        for obj in space_objects:
            if body == obj:
                continue  # тело не действует гравитационной силой на само себя!
            r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
            Fxy = (6.7 * (10 ** -11) * body.m * obj.m) / r ** 2
            Fvec = [-(body.x - obj.x)*Fxy/r, -(body.y - obj.y)*Fxy/r]
            body.Fx += Fvec[0]
            body.Fy += Fvec[1]


    def move_space_object(body, dt):
        """Перемещает тело в соответствии с действующей на него силой.

        Параметры:

        **body** — тело, которое нужно переместить.
        """

        ax = body.Fx/body.m
        body.Vx += ax*dt  #
        body.x += body.Vx*dt

        ay = body.Fy/body.m
        body.Vy += ay*dt
        body.y += body.Vy*dt

    @classmethod
    def recalculate_space_objects_positions(self, space_objects, dt):
        """Пересчитывает координаты объектов.

        Параметры:

        **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
        **dt** — шаг по времени
        """

        for body in space_objects:
            self.calculate_force(body, space_objects)
        for body in space_objects:
            self.move_space_object(body, dt)

    def execution(self):
        """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
        а также обновляя их положение на экране.
        Цикличность выполнения зависит от значения глобальной переменной perform_execution.
        При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
        """

        self.recalculate_space_objects_positions(self.space_objects, self.time_step.get())
        for body in self.space_objects:
            gui.update_object_position(gui.space, body)
        self.physical_time += self.time_step.get()
        gui.displayed_time.set("%.1f" % self.physical_time + " seconds gone")

        if self.perform_execution:
            gui.space.after(101 - int(self.time_speed.get()), self.execution)

    def start_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution.
        """
        self.perform_execution = True
        gui.start_button['text'] = "Pause"
        gui.start_button['command'] = self.stop_execution

        self.execution()
        print('Started execution...')

    def stop_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Останавливает циклическое исполнение функции execution.
        """

        self.perform_execution = False
        gui.start_button['text'] = "Start"
        gui.start_button['command'] = self.start_execution
        print('Paused execution.')



solar_system = Solar_system()

if __name__ == "__main__":
    print("This module is not for direct call!")
