import datetime as dt


# creating a class which objects would be our records of spendings
class Record:
    def __init__(self, amount, comment, date=None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date is None:
            # if date is not determined, just using current date
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


# creating a class that will calculate our spendings and remaining cash
class Calculator:
    USD_RATE = 73.79  # yes, it is august 2021 USD course
    EURO_RATE = 86.62

    def __init__(self, limit, interval) -> None:
        self.limit = limit
        self.interval = interval
        self.records = []

    # function, that takes objects of Record class
    def add_record(self, obj: Record):
        # appending our spendings to an array within the class
        self.records.append(obj)

    # function that calculate amount of money spent
    def get_stats(self):
        if self.interval == 'День':
            day_sum = 0
            for i in self.records:
                if i.date == dt.date.today():
                    day_sum += i.amount
            return day_sum
        elif self.interval == 'Неделя':
            week_sum = 0
            now = dt.date.today()
            week_interval = now - dt.timedelta(days=6)
            for i in self.records:
                if week_interval <= i.date <= now:
                    week_sum += i.amount
            return week_sum
        elif self.interval == 'Месяц':
            months_sum = 0
            for i in self.records:
                if i.date.month == dt.date.today().month:
                    months_dict_dur = {
                        1: 31,
                        2: 28,
                        3: 31,
                        4: 30,
                        5: 31,
                        6: 30,
                        7: 31,
                        8: 31,
                        9: 30,
                        10: 31,
                        11: 30,
                        12: 31
                    }
                    month_duration = months_dict_dur[dt.date.today().month]
                    if 1 <= i.date.day <= month_duration:
                        months_sum += i.amount
            return months_sum
        else:
            print('Неизвестный формат интервала')

    # function that calculate remaining cash for selected period
    def get_cash_remained(self, currency):
        cash_remained = self.limit - self.get_stats()
        currencies = {
            'rub': ['руб.', 1],
            'usd': ['USD', Calculator.USD_RATE],
            'eur': ['Euro', Calculator.EURO_RATE]
        }
        months_dict_names = {
                1: 'январь',
                2: 'февраль',
                3: 'марь',
                4: 'апрель',
                5: 'май',
                6: 'июнь',
                7: 'июль',
                8: 'август',
                9: 'сентябрь',
                10: 'октябрь',
                11: 'ноябрь',
                12: 'декабрь'
        }
        interval_returned = {
            'День': 'день',
            'Неделя': 'неделю',
            'Месяц': months_dict_names[dt.date.today().month]
        }
        interval_name = interval_returned[self.interval]
        if currency not in currencies:
            print('Неизвестная валюта')
        else:
            cash_converted = cash_remained / currencies[currency][1]
            currency_name = currencies[currency][0]
        if cash_remained > 0:
            print(f'На {interval_name} осталось '
                  f'{cash_converted:.2f} {currency_name}')
        elif cash_remained == 0:
            print('Денег нет, зовут Олег')
        elif cash_remained < 0:
            cash_converted_abs = abs(cash_converted)
            print(f'Финансы поют романсы: твой долг - '
                  f'{cash_converted_abs:.2f} {currency_name}')


# creating object of Calculator class with attributes of
# our month and amount of money for this particular month
august = Calculator(20000, 'Месяц')
# creating records of our spendings without date
# which are using Calculator class inner function
# that takes objects of Record class
august.add_record(Record(amount=100, comment='сухарики с чесноком'))
august.add_record(Record(amount=350, comment='пиво'))
august.add_record(Record(amount=650, comment='инвестиции в другую злую воду'))
# creating records of our spendings with determinate date
august.add_record(Record(amount=1000, comment='бар с друзьяшками',
                         date='13.08.2021'))
# checking record with wrong month
august.add_record(Record(amount=80, comment='магазин (за едой)',
                         date='13.09.2021'))
august.add_record(Record(amount=800, comment='магазин (за едой)',
                         date='1.08.2021'))  # checking first
august.add_record(Record(amount=1200, comment='магазин (за едой)',
                         date='31.08.2021'))  # and last days of month
# checking how much money remains
print(august.get_cash_remained('rub'))
