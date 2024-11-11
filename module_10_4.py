import threading
from random import randint
import time
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for g in guests:
            guest_place = False
            for t in self.tables:
                if t.guest is None:
                    t.guest = g
                    g.start()
                    print(f'{g.name} сел(-а) за стол номер {t.number}')
                    guest_place = True
                    break
            if guest_place is False:
                self.queue.put(g)
                print(f'{g.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(t.guest for t in self.tables):
            for t in self.tables:
                if t.guest and not t.guest.is_alive():
                    print(f'{t.guest.name} покушал(-а) и ушел(ушла)')
                    print(f'Стол номер {t.number} свободен')
                    t.guest = None
                if not self.queue.empty() and t.guest is None:
                    new_guest = self.queue.get()
                    t.guest = new_guest
                    print(f'{t.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {t.number}')
                    t.guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]

print(list(guests))

# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
