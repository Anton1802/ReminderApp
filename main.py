#!/usr/bin/python3

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import re
import pickle


class Reminder(FloatLayout):

    tasks = {}

    def save_task(self, instance, title, description, time):
        if self.time_valid(time.text):
            id = len(self.tasks) + 1
            self.tasks[id] = {
                        'title': title.text, 'description': description.text,
                        'time': time.text
                        }
            button = Button(
                        text=f"Task: {self.tasks[id]['title']}",
                        size_hint_y=None, on_press=self.show_task
                        )
            self.task_list.add_widget(button)
            self.write_t()
        else:
            pop_error = Popup(title="Ошибка!", size_hint=(.8, .7))
            pop_error.add_widget(Label(
             text="Введите время в формате часы:минуты"
            ))
            pop_error.open()

    def add_task(self):
        pop = Popup(size_hint=(.8, .7), title="New Task")
        pop.open()
        layout_main = GridLayout(cols=2)
        layout_box_1 = BoxLayout(orientation="vertical", spacing=5)
        layout_box_2 = BoxLayout(orientation="vertical", spacing=5)
        layout_main.add_widget(layout_box_1)
        layout_main.add_widget(layout_box_2)
        label_task_title = Label(text="Title Task: ", size_hint_y=.1)
        label_task_description = Label(text="Description Task: ",
                                       size_hint_y=.1)
        task_title = TextInput(size_hint_y=.1)
        task_description = TextInput(size_hint_y=.1)
        button_cancel = Button(text="Cancel", size=(100, 50),
                               size_hint_y=None, on_press=pop.dismiss)
        button_add = Button(text="Add", size=(100, 50),
                            size_hint_y=None)
        task_time = TextInput(size_hint_y=.1)
        label_task_time = Label(text="Time Task: ",
                                size_hint_y=.1)
        layout_box_1.add_widget(label_task_title)
        layout_box_1.add_widget(label_task_description)
        layout_box_1.add_widget(label_task_time)
        layout_box_1.add_widget(button_cancel)
        layout_box_2.add_widget(task_title)
        layout_box_2.add_widget(task_description)
        layout_box_2.add_widget(task_time)
        layout_box_2.add_widget(button_add)
        pop.add_widget(layout_main)
        button_add.bind(on_press=lambda x: self.save_task(title=task_title,
                        description=task_description,
                        time=task_time, instance=button_add))
        button_add.bind(on_press=pop.dismiss)

    def show_task(self, instance):
        str = instance.text
        task_title = str.replace('Task: ', '')
        for task in self.tasks:
            if self.tasks[task]['title'] == task_title:
                popup_task = Popup(title=self.tasks[task]['title'],
                                   size_hint=(.7, .8))
                popup_task.add_widget(Label(text="\n Описание: " +
                                            self.tasks[task]['description']
                                            + "\n Время: "
                                            + self.tasks[task]['time']))
                popup_task.open()

    def time_valid(self, text):
        return re.search('^[0-9]{2}:[0-9]{2}$', text)

    def write_t(self):
        with open("tasks.pickle", 'wb') as file:
            pickle.dump(self.tasks, file)

    def read_t(self):
        try:
            with open("tasks.pickle", 'rb') as file:
                while True:
                    self.tasks = pickle.load(file)
        except EOFError:
            pass
        except FileNotFoundError:
            pass
        if len(self.tasks):
            buttons = []
            for task in self.tasks:
                buttons.append(Button(
                             text=f"Task: {self.tasks[task]['title']}",
                             size_hint_y=None))

            for bu in range(len(buttons)):
                buttons[bu].bind(on_press=self.show_task)
                self.task_list.add_widget(buttons[bu])

    def start(self):
        self.read_t()


class ReminderApp(App):
    def build(self):
        reminder = Reminder()
        reminder.start()
        return reminder


if __name__ == '__main__':
    ReminderApp().run()
