import os


class Route:
    _count = 0

    def __init__(self, a, b, x, y, s, f):
        self.count = Route._count
        Route._count += 1
        self.start_x = a
        self.start_y = b
        self.finish_x = x
        self.finish_y = y
        self.min_start = s  # the earliest start
        self.max_finish = f  # latest finish
        self.length = abs(x-a) + abs(y-b)
        self.done = False

    def make_done(self):
        self.done = True

    def set_to_zero():
        Route._count = 0

    set_to_zero = staticmethod(set_to_zero)


class Car:
    global current_time

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = None
        self.routes_list = []
        self.av_time = 0

    def add_route(self, _route, _min_time):
        self.av_time += _route.length + _min_time
        self.x = _route.finish_x
        self.y = _route.finish_y
        self.routes_list.append(_route)

    def available(self):
        _f = False
        if current_time == self.av_time:
            _f = True
        return _f

    def closest_route(self):
        global current_time, routes_list
        _min_time = float('+inf')
        _min_route = None
        for _route in routes_list:
            if not _route.done:
                _time = abs(_route.start_x - self.x) + abs(_route.start_y - self.y)
                if _time + current_time < _route.min_start:
                    _time += _route.min_start - (_time + current_time)
                if _time + current_time <= _route.max_finish:
                    if _min_route is None or _time - _min_time < _route.length - _min_route.length:
                        _min_time = _time
                        _min_route = _route
        return _min_route, _min_time


def input_inf(filename):
    """
    функція введення
    :param filename: назва файлу
    :return: карта(масив з 0), словник автомобілів (№ автомобіля: позиція(0, 0)),
             маршрутний список кортежів (координати початку, координати кінця(кортежи), початковий час, кінцевий час,
             бонус (ціле число)
             к-ть кроків (ціле число)
    """
    _routes_list = []
    with open(filename, 'r') as file:
        line = file.readline().split()
        car_count = int(line[2])
        _car_list = []
        for i in range(car_count):
            _car_list.append(Car(0, 0))
        _total_time = int(line[5])
        for line in file:
            line = line.split()
            a = int(line[0])
            b = int(line[1])
            x = int(line[2])
            y = int(line[3])
            s = int(line[4])
            f = int(line[5])
            _routes_list.append(Route(a, b, x, y, s, f))

    return _car_list, _routes_list, _total_time


def output_inf(filename):
    global car_list
    _File = open(filename, 'w')
    _output = ''
    for _car in car_list:
        _route_numbers = []
        for r in _car.routes_list:
            _route_numbers.append(str(r.count))
        _output += str(len(_car.routes_list)) + ' ' + " ".join(_route_numbers) + '\n'
    _File.write(_output)
    _File.close()


if __name__ == "__main__":

    input_names = []
    root_in = 'in_d/'  # input folder (must exist)
    root_out = 'out_d/'  # output folder (must exist)
    for root, dirs, files in os.walk(root_in):
        input_names.extend(files)

    for file_name in input_names:
        car_list, routes_list, total_time = input_inf(root_in + file_name)

        for current_time in range(total_time):
            for car in car_list:
                if car.available():
                    route, min_time = car.closest_route()
                    if route is not None:
                        route.done = True
                        car.add_route(route, min_time)
        file_name = file_name.split('.')[0] + '.out'

        output_inf(root_out + file_name)
