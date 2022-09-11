#!/usr/bin/python3

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class Reminder(FloatLayout):
    pass


class ReminderApp(App):
    def build(self):
        return Reminder()


if __name__ == '__main__':
    ReminderApp().run()
