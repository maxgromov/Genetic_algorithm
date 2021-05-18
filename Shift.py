import datetime as dt

class Shift:
    def __init__(self, shift_name,  date, start_time, end_time, duration):
        self.shift_name = shift_name

        if type(date) is str:
            self.date = dt.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.date = date
        self.duration = duration

        if type(start_time) is str:
            self.start_time = dt.datetime.strptime(start_time, '%H:%M:%S').time()
        else:
            self.start_time = start_time

        if type(end_time) is str:
            self.end_time = dt.datetime.strptime(end_time, '%H:%M:%S').time()
        else:
            self.end_time = end_time
        # self.start_time = dt.datetime.strptime(start_time, '%H:%M:%S').time()
        # self.end_time = dt.datetime.strptime(end_time, '%H:%M:%S').time()

    def __eq__(self, other):
        if isinstance(other, Shift):
            return [(self.date == other.date
                    and self.start_time == other.start_time
                    and self.end_time == other.end_time),
                    (self.shift_name == other.shift_name
                    and self.date == other.date
                    and self.start_time == other.start_time
                    and self.end_time == other.end_time)]
        return NotImplemented

    def __repr__(self):
        return f'shift_name = {self.shift_name}, date = {self.date}, satrt_time = {self.start_time}, end_time = {self.end_time} ,duration = {self.duration}'


class LinkedShift(Shift):
    def __init__(self, shift_name, date, start_time, end_time, duration, neighbor):
        super(LinkedShift, self).__init__(shift_name, date, start_time, end_time, duration)
        self.neighbor = neighbor

    def __repr__(self):
        return f'shift_name = {self.shift_name}, date = {self.date}, satrt_time = {self.start_time}, end_time = {self.end_time} ,duration = {self.duration}, neighbor = {self.neighbor}'







