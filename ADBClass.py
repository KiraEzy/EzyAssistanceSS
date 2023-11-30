import os

import cv2
import subprocess


class AdbSingleton:
    instance = None
    APP_ACTIVITY = "com.xd.ssrpgtw/com.jixin.GameActivity"
    APP_PACKAGE = "com.xd.ssrpgtw"
    # APP_ACTIVITY = "com.boltrend.octopath.tc/com.epicgames.ue4.SplashActivity"
    # APP_PACKAGE = "com.boltrend.octopath.tc"
    def __init__(self, adb_path='', adb_port='', retryCount=5):
        self.deviceConnected = False
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.retry_count = retryCount

    @staticmethod
    def getInstance():
        if AdbSingleton.instance is None:
            AdbSingleton.instance = AdbSingleton()
        return AdbSingleton.instance

    def connectDevice(self, adb_path='', adb_port='', retryCount=5):
        print("connectDevice", adb_path, adb_port, retryCount)
        if adb_path != self.adb_path:
            self.adb_path = adb_path
        if adb_port != self.adb_port:
            self.adb_port = adb_port
        if retryCount != self.retry_count:
            self.retry_count = retryCount
        for i in range(self.retry_count):
            if not self.deviceConnected:
                res = self.adb_connect()
                print("runCmd adb_connect:", res[0])
                if b'connected to' in res[0]:
                    self.setDeviceConnected(True)
                    print("Device Connected")
                    break
                    # sizeMatch = self.get_screen_resolution()
                    # print(sizeMatch)
                    # if sizeMatch:
                    #     x = int(sizeMatch[0])
                    #     y = int(sizeMatch[1])
                    #     self.deviceDimension = [x, y]
                    #     print('Device Dimension:', self.deviceDimension)
                else:
                    self.setDeviceConnected(False)
        return self.deviceConnected;

    def adb_connect(self):
        command = [self.adb_path, "connect", self.adb_port]
        print(" ".join(command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        return [output, error]

    def adb_device(self):
        command = [self.adb_path, "devices"]
        print(" ".join(command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        return [output, error]

    def adb_shell(self, command):
        full_command = [self.adb_path, "-s", self.adb_port, "shell", command]
        print(" ".join(full_command))
        p = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        return [output, error]

    def trigger_key_event(self, key):
        command = ["input", "keyevent", str(key)]
        self.adb_shell(" ".join(command))
    def screen_capture(self, path):
        # ./adb_server.exe -s 127.0.0.1:7555 exec-out screencap -p > ./test/screencap.png
        full_command = [self.adb_path, "-s", self.adb_port, "exec-out", "screencap", "/sdcard/cache.png"]
        print(" ".join(full_command))
        p = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        full_command = [self.adb_path, "-s", self.adb_port, "pull", "/sdcard/cache.png", path]
        print(" ".join(full_command))
        p = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        full_command = [self.adb_path, "-s", self.adb_port, "shell", "rm", "/sdcard/cache.png"]
        print(" ".join(full_command))
        p = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return path

    def swipe(self, posStart, posEnd, duration=None):
        command = ["input", "swipe", str(posStart[0]), str(posStart[1]), str(posEnd[0]), str(posEnd[1])]
        if duration:
            command.append(str(duration))
        self.adb_shell(" ".join(command))

    def tap(self, pos):
        command = ["input", "tap", str(pos[0]), str(pos[1])]
        self.adb_shell(" ".join(command))

    def tap_down(self, pos):
        command = ["input", "touchscreen", "touch", str(pos[0]), str(pos[1])]
        self.adb_shell(" ".join(command))

    def tap_up(self, pos):
        command = ["input", "touchscreen", "release", str(pos[0]), str(pos[1])]
        self.adb_shell(" ".join(command))

    def get_screen_resolution(self):
        output, error = self.adb_shell("wm size")
        print(output)
        resolution_str = output.decode("utf-8").strip().split(" ")[2]
        width, height = map(int, resolution_str.split("x"))
        return (width, height)

    def capture_screen(self, filename):
        # Construct the adb command to capture the screen
        cmd = f"{self.adb_path} -s {self.adb_port} shell screencap -p"

        # Run the command and capture the output
        output = os.popen(cmd).read()

        # Construct the path to save the screenshot
        filepath = os.path.join(os.path.dirname(__file__), "img", filename)

        # Write the output to the file
        with open(filepath, "wb") as f:
            f.write(output)

        return filepath
    def getAllPackages(self):
        output, error = self.adb_shell("pm list packages")
        # outputA, errorA = self.adb_shell("dumpsys package | grep -i 'com.xd.ssrpgtw' | grep Activity")
        outputA, errorA = self.adb_shell("dumpsys package | grep -i 'com.boltrend.octopath.tc' | grep Activity")
        print("Availible Activity: ",outputA)
        output_array = [item[8:] for item in output.decode().split('\r\n')]
        print("res: ", output_array)
        return output_array
    def startApp(self):
        output, error = self.adb_shell("am start -n "+ AdbSingleton.APP_ACTIVITY)
        # output, error = self.adb_shell("am start -n com.xd.ssrpgtw/com.jixin.GameActivity")
        print(output)
        return output
    def setDeviceConnected(self, connected):
        self.deviceConnected = connected

    def isDeviceConnected(self):
        return self.deviceConnected