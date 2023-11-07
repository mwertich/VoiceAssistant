from HelpFuncs import sortDays


class Task:
    assistant: object
    input: str
    output: str

    def __init__(self, assistant, input: str, output: str):
        self.assistant = assistant
        self.input = input
        self.output = output

    def list(self):
        rows = self.assistant.databank.getTable("tasks")
        selected = []

        if not rows:
            return self.output.split("|")[1]
        elif all(rows[i][2] == 1 for i in range(len(rows))):
            return self.output.split("|")[2]
        else:
            for i in range(len(rows)):
                if rows[i][2] == 0:
                    selected.append(i)
            if len(selected) > 1:
                return self.output.format(rows[selected[0]][0], rows[0], [1]) + \
                       "".join([f" and {rows[selected[i]][0]} until {rows[selected[i]][2]}" for i in selected])
            else:
                return self.output.split("|")[0].format(rows[selected[0]][0], rows[selected[0]][1])

    def done(self):
        dbCursor = self.assistant.databank.getDbConn().cursor()
        dbCursor.execute("SELECT name FROM tasks")
        names = dbCursor.fetchall()
        for e in names:
            e = str(e)[2:-3]
            if e in self.input:
                self.assistant.databank.taskDone(e)
                return self.output.format(e)

    def add(self):
        try:
            name = self.input[self.input.index("add task") + 9: self.input.index("until") - 1]
            date = self.input[self.input.index("until") + 6:]
        except:
            name = self.input[self.input.index("add task") + 9:]
            date = "the end of time"

        self.assistant.databank.addTask(name, date)
        return self.output.format(name)

    def delete(self):
        name = self.input[self.input.index("task") + 5:]
        self.assistant.databank.delTask(name)
        return self.output.format(name)

    def next(self):
        dbCursor = self.assistant.databank.getDbConn().cursor()
        dbCursor.execute("SELECT date FROM tasks")
        dates = dbCursor.fetchall()
        for i in range(len(dates)):
            dates[i] = str(dates[i])[2:-3]
        date = sortDays(dates)[0]

        dbCursor.execute(f"SELECT name FROM tasks WHERE date = '{date.lower()}'")
        names = dbCursor.fetchall()
        return self.output.format(str(names)[3:-4], date)

    def delDone(self):
        names = []
        rows = self.assistant.databank.getTable("tasks")
        for l in rows:
            if l[2] == 1:
                self.assistant.databank.delTask(l[0])
                names.append(l[0])
        if len(names) == 1:
            return self.output.format(names[0])
        else:
            return self.output.format(", ".join(names))
