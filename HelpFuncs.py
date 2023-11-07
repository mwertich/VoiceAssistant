from typing import List
from datetime import datetime
import calendar


def sortDays(lst: List[str]):
    """sortiert Wochentage relativ nach Dringlichkeit"""
    days = dict(zip(calendar.day_name, range(7)))
    today = datetime.today().weekday()

    for i in range(len(lst)):
        if lst[i] != "not specified":
            lst[i] = days[lst[i].capitalize()] - today
        else:
            lst.pop(i)

    lst = sorted(lst)
    for i in range(len(lst) - 1):
        if int(lst[i]) < 0:
            lst.append(lst[0])
            lst.remove(lst[0])

    return [calendar.day_name[int(e) + today] for e in lst]


def roundFloat(x: float):
    if x - int(x) == 0:
        num = list(str(int(x)))
        for i in range(len(num) - 3, 0, -3):
            num.insert(i, ",")
        num = "".join(num)
        return num
    else:
        return f"roughly {round(x, 2)}"
