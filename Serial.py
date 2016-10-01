from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, pyqtSignal

class Serial(QSerialPort):

    # Signal
    readyRead = pyqtSignal([str], [int])

    def __init__(self, port_loc="/dev/ttyACM0", baud_rate=9600, parent=None):
        super(Serial, self).__init__(parent)
        self.parent = parent
        self.setBaudRate(baud_rate)
        self.setDataBits(self.Data8)
        self.setParity(self.NoParity)
        self.setStopBits(self.OneStop)
        self.setFlowControl(self.NoFlowControl)
        self.setPortName(port_loc)
        self.setReadBufferSize(1)

        # signal: ready to read, slot: format data
        super(Serial, self).readyRead.connect(self.__format_data)

    def setBaudRate_str(self, baud_rate:str):
        super(Serial, self).setBaudRate(int(baud_rate))

    def __format_data(self):
        try:
            data = self.readAll().data().decode('ascii')
            self.readyRead[str].emit(data)
            self.readyRead[int].emit(int(data))
        except ValueError:
            pass

    def read(self) -> bytes:
        while self.waitForReadyRead(0) is False :
            pass

        byte = super(Serial, self).read(1)
        return byte

    def write(self, data:bytes):
        super(Serial, self).write(data)
        self.flush()

    def write_line(self, data:str):
        for character in data:
            self.write(character.encode("ascii"))

    @staticmethod
    def get_available_ports_systemLocations_and_manufacturers():
        available_ports = QSerialPortInfo.availablePorts()
        ports_info = []

        for port in available_ports:
            ports_info.append( (port.systemLocation(), port.manufacturer()) )

        return ports_info

    def on_new_portName(self, port):
        if self.isOpen() is True:
            self.close()

        self.setPortName(port)

        if self.open() is False:
            print("Can't open port %s" % self.portName())

    def open(self):
        if super(Serial, self).open(QIODevice.ReadWrite) is True:
            return True

        else:
            return False