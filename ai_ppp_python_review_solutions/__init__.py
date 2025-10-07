__version__ = '1.1'

import datetime

class Todo:
    """
    Represents a single To-Do item. Stores task name, date, and completion status.
    """
    def __init__(self, task, date, completed=False):
        self.set_task(task)
        self.set_date(date)
        self.set_completed(completed)

    def get_task(self):
        return self._task

    def get_date(self):
        return self._date

    def is_completed(self):
        return self._completed

    def set_task(self, new_task):
        self._task = new_task

    def set_date(self, new_date):
        if not isinstance(new_date, datetime.date):
            raise TypeError("Date must be a datetime.date object.")
        self._date = new_date

    def set_completed(self, status):
        self._completed = status

    def toggle_completion(self):
        self._completed = not self._completed

    def to_dict(self):
        """Converts the Todo object to dictionary format."""
        return {
            'task': self.get_task(),
            'date': self.get_date(),
            'completed': self.is_completed()
        }

    def __str__(self):
        status_char = '+' if self.is_completed() else '-'
        date_str = self.get_date().strftime('%Y-%m-%d')
        return f"[{status_char}] {date_str}: {self.get_task()}"

class TodoList:
    """
    Manages a collection of Todo objects for a specific list.
    """
    def __init__(self, name, items=[]):
        self._name = name
        self._items = items

    def get_name(self):
        return self._name

    def get_items(self):
        return self._items
    
    def set_name(self, new_name):
        self._name = new_name

    def set_items(self, new_items):
        self._items = new_items

    def add_task(self, task_name, date):
        new_todo = Todo(task=task_name, date=date)
        self._items.append(new_todo)

    def remove_task(self, index):
        if 0 <= index < len(self.get_items()):
            self._items.pop(index)
        else:
            raise IndexError("Index out of range.")

    def mark_complete(self, index, status=True):
        if 0 <= index < len(self.get_items()):
            self.get_items()[index].set_completed(status)
        else:
            raise IndexError("Index out of range.")

    def save_to_file(self, file_path):
        dict_list = []
        for item in self.get_items():
            dict_list.append(item.to_dict())
        write_todo_list(file_path, dict_list)

    def load_from_file(self, file_path):
        dict_list = read_todo_list(file_path)
        items = []
        for d in dict_list:
            new_todo = Todo(d['task'], d['date'], d['completed'])
            items.append(new_todo)
        self.set_items(items)

    def __str__(self):
        to_return = f"--- {self.get_name()}'s To-Do List ({len(self.get_items())} Tasks) ---\n"
        if not self.get_items():
            return to_return + "The list is currently empty."

        for i, item in enumerate(self.get_items()):
            status_char = '+' if item.is_completed() else '-'
            date_str = item.get_date().strftime('%Y-%m-%d')
            to_return += f"[{i+1}] [{status_char}] {date_str}: {item.get_task()}\n"

        return to_return


def get_integer_input(prompt, min_val=1, max_val=float('inf')):
    while True:
        try:
            choice = input(prompt).strip()
            if not choice:
                return None  # None if you just press enter 
            val = int(choice)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_date_input(prompt):
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return None
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31).")

def write_todo_list(file_path, todos):
    with open(file_path, 'w') as f:
        f.write("To Do:\n")
        for item in todos:
            date_str = item['date'].strftime('%Y-%m-%d')
            status = 'x' if item['completed'] else 'o'
            f.write(f"{status} {date_str}: {item['task']}\n")

def read_todo_list(file_path):
    todos = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines or lines[0].strip() != "To Do:":
            raise ValueError("Invalid file format. 'To Do:' not found.")

        for line in lines[1:]:
            try:
                status_date, task = line.split(':')
                task = task.strip()
                
                parts = status_date.strip().split(' ')
                status_char = parts[0]
                date_str = parts[1]

                date_obj = datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
                completed = True if status_char == 'x' else False

                todos.append({
                    'task': task.strip(),
                    'date': date_obj,
                    'completed': completed
                })
            except (ValueError, IndexError):
                raise ValueError(f"Invalid line format: {line}")
    return todos
