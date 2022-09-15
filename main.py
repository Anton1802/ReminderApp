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


class Reminder(FloatLayout):

    task = {}

    def save_task(self, instance, title, description, time):
        if self.time_valid(time.text):
            id = len(self.task) + 1
            self.task[id] = {
                        'title': title.text, 'description': description.text,
                        'time': time.text
                        }
            button = Button(
                        text=f"Task: {self.task[id]['title']}",
                        size_hint_y=None,
                        on_press=lambda x: self.show_task(
                            id=id,
                            instance=button
                            ),
                        )
            self.task_list.add_widget(button)
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
        self.task_time = task_time
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

    def show_task(self, instance, id):
        print(self.task[id])

    def time_valid(self, text):
        return re.search('^[0-9]{2}:[0-9]{2}$', text)


class ReminderApp(App):
    def build(self):
        return Reminder()


if __name__ == '__main__':
    ReminderApp().run()
