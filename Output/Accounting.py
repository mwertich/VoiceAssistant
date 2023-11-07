from _datetime import datetime
from typing import List
from gkeepapi import Keep
import re

date_format = "%d.%m.%Y"


class Item:
    price: float
    name: str
    date: str
    category: str

    def __init__(self, price: float, name, date, category=None):
        self.price = price
        self.name = name.lower()
        self.date = date
        self.category = category.lower() if category else None

    def __repr__(self):
        if self.category:
            return f"( {self.price}€ | {self.name} | {self.category} | {self.date} )"
        else:
            return f"( {self.price}€ | {self.name} | {self.date} )"

    def __str__(self):
        return self.__repr__()


class Data:
    starting_balance: float
    balance: float
    balance_delta: float
    _items: List[Item]
    _empty: bool

    def __init__(self):
        self.starting_balance = 0
        self.balance = 0
        self.balance_delta = 0
        self._items = []
        self._empty = True

    def add_item(self, item: Item):
        self._items.append(item)
        self._empty = False

    def get_item(self, i: int):
        return self._items[i]

    def get_items(self):
        return self._items

    def is_empty(self):
        return self._empty

    def round(self):
        self.balance_delta = round(self.balance_delta, 2)
        self.balance = round(self.balance, 2)
        self.starting_balance = round(self.starting_balance, 2)


class Accounting:
    assistant: object
    input: str
    output: str
    data: Data
    keep: Keep
    note: object

    def __init__(self, assistant, input: str, output: str):
        self.assistant = assistant
        self.input = input
        self.output = output
        self.data = Data()
        self.keep = Keep()
        self._get_note()
        self._transform_note()

    def _get_note(self):
        _ = self.keep.login('jdjunior20@gmail.com', 'password', sync=True)
        self.note = self.keep.get("1OCI5DGva1MRDZJg-ty35szW9wi8U2E1FS6Y0Kw4pD2ZcqLeO1v9NRDtDFOJ5vxk")

    def _transform_note(self):
        tmp = self.note.text.split("\n")
        self.data.starting_balance = float(tmp[0].split(" ")[-1].replace(".", "").replace(",", "."))
        self.data.balance = self.data.starting_balance
        cur_day = tmp[0].split(" ")[1]
        for e in tmp[1:]:
            # check if row has new cur_day
            try:
                res = bool(datetime.strptime(e, date_format))
            except ValueError:
                res = False
            if res:
                cur_day = datetime.strptime(e, date_format).strftime(date_format)
            elif e and e[0] in ["-", "+"]:
                item = e.split(" ")
                # add item to listr
                if item[-1] == "":
                    item.remove("")
                # convert to standard notation
                item[0] = item[0].replace(",", ".")
                if item[-1][0] == "(" and item[-1][-1] == ")":
                    self.data.add_item(Item(float(item[0]), " ".join(item[1:-1]), cur_day, item[-1][1:-1]))
                else:
                    self.data.add_item(Item(float(item[0]), " ".join(item[1:]), cur_day))
                # update balancer
                self.data.balance += self.data.get_item(-1).price
        self.data.balance_delta = self.data.balance - self.data.starting_balance
        self.data.round()

    def _sort(self):
        if self.data.is_empty():
            return self.data
        else:
            self.data.get_items().sort(key=lambda e: e.price)
            print(f"sorted after price")

    def _mono_filter(self, key: str, column: str):
        new_data = Data()
        new_data.starting_balance = self.data.starting_balance
        new_data.balance = self.data.starting_balance
        key = key.lower()
        for e in self.data.get_items():
            if column == "price" and e.price == float(key):
                new_data.add_item(e)
            elif column == "name" and e.name.__contains__(key):
                new_data.add_item(e)
            elif column == "date" and e.date == datetime.strptime(key, date_format).strftime(date_format):
                new_data.add_item(e)
            elif column == "category" and e.category == key:
                new_data.add_item(e)
            elif column == "delta":
                if key == "+" and "-" != str(e.price)[0]:
                    new_data.add_item(e)
                elif key == str(e.price)[0]:
                    new_data.add_item(e)

        for e in new_data.get_items():
            new_data.balance += e.price
        new_data.balance_delta = new_data.balance - new_data.starting_balance
        new_data.round()
        print(f"filtered in {column} for {key}")
        self.data = new_data

    def add(self):
        delta = "-" if "expense" in self.input else "+"
        input = self.input.replace("add expense", "").replace("add income", "")
        price = float(re.findall("[+-]?\d+\.\d+", input)[0])
        name = input.split(str(price))[0].lstrip()
        if delta == "-":
            price *= -1
        category = input.split(" ")[-1]
        date = datetime.now().strftime(date_format)
        tmp = date
        for word in input.split(" "):
            try:
                datetime.strptime(word, date_format)
            except ValueError:
                continue
            date = datetime.strptime(word, date_format).strftime(date_format)
            break
        if date == tmp:
            self.note.text = self.note.text + f"\n{delta}{abs(price)} {name} ({category})"
        else:
            self.note.text = self.note.text + f"\n{delta}{abs(price)} {name} ({category}) [{date}]"
        if not self.assistant.debugMode:
            self.data.add_item(Item(price, name, date, category))
            self.keep.sync()
        return self.output.format(name)

    def balance(self):
        return self.output.format(self.data.starting_balance, self.data.balance_delta, self.data.balance)

    def list(self):
        if "sorted" in self.input:
            self._sort()
        if "filtered" in self.input:
            input = self.input.split(" ")
            i = input.index("filtered")
            self._mono_filter(input[i + 2], input[i + 1])
        if self.data.is_empty():
            return self.output.split("|")[1]
        else:
            table = ""
            for e in self.data.get_items():
                table += "\n" + str(e)
            table += f"\ndelta: {self.data.balance_delta}"
            return self.output.split("|")[0].format(table)
