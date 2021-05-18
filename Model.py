import datetime as dt
import pandas as pd
import numpy as np
from Shift import LinkedShift



class Model:
    def __init__(self):
        self._shifts = {}
        self.shifts_lst = []
        self._knapsacks = {}
        self.linked_shifts = []
        self.max_union_time = 1.
        self.default_fitness = 0

    def __repr__(self):
        return f'shifts : {self._shifts.__repr__()}\nknapsacks : {self._knapsacks.__repr__()}'

    # @property
    # def num_shift(self):
    #     return len(self._shifts)

    @property
    def num_knapsacks(self):
        return len(self._knapsacks)

    # def add_shift(self, shift):
    #     num = len(self._shifts)
    #     self._shifts[num] = shift

    def add_employee(self, knapsacks):
        num = len(self._knapsacks)
        self._knapsacks[num] = knapsacks
        self.default_fitness += knapsacks.threshold

    def add_shift(self, shift):
        self.shifts_lst.append(shift)

    @property
    def num_shift(self):
        return len(self.shifts_lst)

    def add_neighbor(self):
        stack = []
        for i in range(len(self.shifts_lst)):
            if i < len(self.shifts_lst)-1:
                if self.shifts_lst[i].date == self.shifts_lst[i+1].date:
                    # print(i, 'даты равны')
                    condition = self.shifts_lst[i] == self.shifts_lst[i+1]
                    if condition[0]:
                        #print(i,'объекты равны')
                        stack.append(self.shifts_lst[i])
                        #print('satck:', stack)
                        i += 1

                    else:
                        if len(stack) > 0:
                            for j in range(len(stack)):
                                if self.max_union_time >= \
                                        (dt.datetime.combine(self.shifts_lst[i+1].date,
                                                             self.shifts_lst[i+1].start_time) -
                                         dt.datetime.combine(stack[j].date,
                                                             stack[j].end_time)).seconds / 3600:
                                    linked_shift = LinkedShift(shift_name=stack[j].shift_name
                                                               , date=stack[j].date
                                                               , start_time=stack[j].start_time
                                                               , end_time=stack[j].end_time
                                                               , duration=stack[j].duration
                                                               , neighbor=self.shifts_lst[i+1]
                                                               )
                                    self.linked_shifts.append(linked_shift)
                                else:
                                    linked_shift = LinkedShift(shift_name=stack[j].shift_name
                                                               , date=stack[j].date
                                                               , start_time=stack[j].start_time
                                                               , end_time=stack[j].end_time
                                                               , duration=stack[j].duration
                                                               , neighbor=None
                                                               )
                                    self.linked_shifts.append(linked_shift)

                            stack = []

                            if self.max_union_time >= \
                                    (dt.datetime.combine(self.shifts_lst[i + 1].date, self.shifts_lst[i + 1].start_time) -
                                     dt.datetime.combine(self.shifts_lst[i].date, self.shifts_lst[i].end_time)).seconds/3600:
                                linked_shift = LinkedShift(shift_name = self.shifts_lst[i].shift_name
                                                           , date = self.shifts_lst[i].date
                                                           , start_time = self.shifts_lst[i].start_time
                                                           , end_time = self.shifts_lst[i].end_time
                                                           , duration =self.shifts_lst[i].duration
                                                           , neighbor=self.shifts_lst[i+1]
                                                           )
                                self.linked_shifts.append(linked_shift)
                            else:
                                linked_shift = LinkedShift(shift_name=self.shifts_lst[i].shift_name
                                                           , date=self.shifts_lst[i].date
                                                           , start_time=self.shifts_lst[i].start_time
                                                           , end_time=self.shifts_lst[i].end_time
                                                           , duration=self.shifts_lst[i].duration
                                                           , neighbor=None
                                                           )
                                self.linked_shifts.append(linked_shift)
                        else:
                            if self.max_union_time >= \
                                    (dt.datetime.combine(self.shifts_lst[i + 1].date, self.shifts_lst[i + 1].start_time) -
                                     dt.datetime.combine(self.shifts_lst[i].date, self.shifts_lst[i].end_time)).seconds/3600:
                                linked_shift = LinkedShift(shift_name = self.shifts_lst[i].shift_name
                                                           , date = self.shifts_lst[i].date
                                                           , start_time = self.shifts_lst[i].start_time
                                                           , end_time = self.shifts_lst[i].end_time
                                                           , duration =self.shifts_lst[i].duration
                                                           , neighbor=self.shifts_lst[i+1]
                                                           )
                                self.linked_shifts.append(linked_shift)
                            else:
                                linked_shift = LinkedShift(shift_name=self.shifts_lst[i].shift_name
                                                           , date=self.shifts_lst[i].date
                                                           , start_time=self.shifts_lst[i].start_time
                                                           , end_time=self.shifts_lst[i].end_time
                                                           , duration=self.shifts_lst[i].duration
                                                           , neighbor=None
                                                           )
                                self.linked_shifts.append(linked_shift)

                else:
                    linked_shift = LinkedShift(shift_name=self.shifts_lst[i].shift_name
                                               , date=self.shifts_lst[i].date
                                               , start_time=self.shifts_lst[i].start_time
                                               , end_time=self.shifts_lst[i].end_time
                                               , duration=self.shifts_lst[i].duration
                                               , neighbor= None
                                               )
                    self.linked_shifts.append(linked_shift)
            else:
                linked_shift = LinkedShift(shift_name=self.shifts_lst[i].shift_name
                                           , date=self.shifts_lst[i].date
                                           , start_time=self.shifts_lst[i].start_time
                                           , end_time=self.shifts_lst[i].end_time
                                           , duration=self.shifts_lst[i].duration
                                           , neighbor= None
                                           )
                self.linked_shifts.append(linked_shift)

    def _create_instance(self, allocation):
        instance = AllocationInstance()
        for i, value in enumerate(allocation):
            knapsack = self._knapsacks[value]
            shift = self.linked_shifts[i]
            instance.add_content(knapsack, shift)
        return instance

    def get_allocation_report(self, allocation):
        instance = self._create_instance(allocation)
        return str(instance)

    def result_to_df(self, allocation):
        instance = self._create_instance(allocation)
        content = instance._knapsacks_content
        result = pd.DataFrame()
        for emp in content:
            print('employee', emp.name)
            for shift in content[emp]:
                df = pd.DataFrame()

                for atr in shift.__dict__:
                    df['employee_name'] = emp.name
                    df['employee_time'] = emp.threshold
                    ser = pd.Series(getattr(shift, atr), name=atr)
                    df[atr] = ser
                result = result.append(df, ignore_index=True)
        return result

    def get_fitness(self, allocation):
        instance = self._create_instance(allocation)
        num_allocation_error = 0
        num_allocation_error += instance.get_false_employee_count(self.num_knapsacks)  # количество нераспределенных сотрудников по сменам
        num_allocation_error += instance.get_false_day_off()  # проверка соблюдения обязательных выходных дней для сотрудника

        if num_allocation_error > 0:
            return num_allocation_error * self.default_fitness
        else:
            return instance.get_knapsack_fitness()


class AllocationInstance:
    def __init__(self):
        self._knapsacks_content = {}
        self.min_day_off = 5
        self.min_day_off_together = 2

    def __str__(self):
        str = []
        for (knapsack, content) in self._knapsacks_content.items():
            str.append(f'{knapsack}, content={content}, volume={self.get_knapsack_volume(knapsack)}')
        return '\n'.join(str)

    def add_content(self, knapsack, shift):
        if not (knapsack in self._knapsacks_content):
            self._knapsacks_content[knapsack] = []  # список вместо множества
        content = self._knapsacks_content[knapsack]
        content.append(shift)

    def get_content(self, knapsack):
        knapsack.values()

    def get_knapsack_volume(self, knapsack):
        volume = 0
        content = self._knapsacks_content[knapsack]
        for shift in content:
            volume += shift.duration
        return volume

    def get_knapsack_fitness(self):
        return sum([abs(self.get_knapsack_volume(knapsack) - knapsack.threshold)
                    for knapsack in self._knapsacks_content.keys()])

    def get_week_from_date(self, date):
        # date = dt.datetime.strptime(str_date, '%Y-%m-%d').date()
        wk = date.isocalendar()[1]
        return wk

    def get_false_day_off(self):
        count_total_errors = 0
        for knapsack in self._knapsacks_content.values():
            shifts_dict = {}  # словарь со сменами, распределенными в соответствии с номером недели
            count_day_off_error = 0
            count_shifts_together = 0
            for el in knapsack:
                if self.get_week_from_date(el.date) in shifts_dict.keys():
                    shifts_dict[self.get_week_from_date(el.date)].append(el)
                else:
                    shifts_dict[self.get_week_from_date(el.date)] = [el]  # list вместо set
            for value in shifts_dict.values():  # value это множество смен для каждого сотрудника за неделю
                #date_set = set()
                date_dct = {}
                # tmp = []
                # Создаем словарь: ключ =  дата, значения = список смен за неделю
                for i in value:
                    if i.date in date_dct.keys():
                        date_dct[i.date].append(i)
                    else:
                        date_dct[i.date] = [i]
                    # tmp.append(i.date)
                # num_date_dct = {j: tmp.count(j) for j in tmp}

                for shft in date_dct.values():
                    count_shifts_together = 0
                    if len(shft) >1:
                        count_shifts_together = len(shft) -1
                        for i in shft:
                            if i.neighbor is not None:
                                for j in shft:
                                    condition = (i.neighbor == j)
                                    if condition[1] == True:
                                        count_shifts_together += -1


                    count_total_errors =+ count_shifts_together
                            # else:
                            #     count_shifts_together = 0
                # for elements in value:
                #     date_set.add(elements.date)
                # count_shifts_together += len(value) - len(date_set)  # число смен в день, распределенных на сотрудника
                if len(date_dct.keys()) > (7 - self.min_day_off):
                    count_day_off_error += 1
            count_total_errors += count_day_off_error

        return count_total_errors

    def get_false_employee_count(self, num_employees):
        count = num_employees - len(self._knapsacks_content.keys())
        return count
