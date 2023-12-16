import re
import time
import models
from datetime import datetime

from subprocess import Popen, PIPE


class mouse_status(object):
    def __init__(self):
        self.deltaX = None
        self.deltaY = None
        self.start_x = None
        self.start_y = None
        self.stop = False
        models.create_table()

    @staticmethod
    def get_activityname():

        root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
        stdout, stderr = root.communicate()
        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)

        if m is not None:

            window_id = m.group(1)

            windowname = None
            window = Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=PIPE)
            stdout, stderr = window.communicate()
            wmatch = re.match(b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout)
            if wmatch is not None:
                windowname = wmatch.group('name').decode('UTF-8').strip('"')

            processname1, processname2 = None, None
            process = Popen(['xprop', '-id', window_id, 'WM_CLASS'], stdout=PIPE)
            stdout, stderr = process.communicate()
            pmatch = re.match(b'WM_CLASS\(\w+\) = (?P<name>.+)$', stdout)
            if pmatch is not None:
                processname1, processname2 = pmatch.group('name').decode('UTF-8').split(', ')
                processname1 = processname1.strip('"')
                processname2 = processname2.strip('"')

            return {
                'windowname': windowname,
                'processname1': processname1,
                'processname2': processname2
            }

        return {
            'windowname': None,
            'processname1': None,
            'processname2': None
        }

    def update(self, x=None, y=None, button=None):
        self.deltaX = x - self.start_x if self.start_x else 0
        self.start_x = x
        self.deltaY = y - self.start_y if self.start_y else 0
        self.start_y = y

        a = self.get_activityname()
        process = (f'The mouse is located: {a["processname2"]} {a["processname1"]} {a["windowname"""]}')
        data = [x, y, self.deltaX, self.deltaY, datetime.now(), button.value if button else -1, process]
        models.insert_data(data=data)
        # print(x, self.deltaX, y, self.deltaY, datetime.now(), button.value if button else -1, process)

    @staticmethod
    def listener_sleep():
        time.sleep(3)

    def on_move(self, x, y):
        if self.stop:
            return False
        self.update(x=x, y=y)
        # threading.Thread(target=self.listener_sleep).start()

    def on_click(self, x, y, button, pressed):
        if self.stop:
            return False
        if pressed:
            self.update(x=x, y=y, button=button)

    def on_press(self, key):
        try:
            if key.name == 'esc':
                self.stop = True
        finally:
            return self.stop
