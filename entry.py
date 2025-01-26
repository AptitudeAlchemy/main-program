import datetime
from math import floor
import uptime
import psutil as util

def convert(total_bytes) -> str | None:
    amount: float = total_bytes * 0.000001
    unit: str = "MB" if floor(amount) < 1024 else "GB"
    amount = (floor(amount) * 0.001) if unit == 'GB' else amount
    return "{0:.2f} {1}".format(amount, unit)


class Entry:

    _username: str = util.Process().username()
    _ipv4: str = None
    _ipv6: str = None
    _connection_type: str = None
    _uptime: str = "%.2f HRS" % (uptime.uptime() / 3600)
    _date: datetime = datetime.datetime.now()
    _bytes_sent: int = 1
    _bytes_recv: int = 1

    def __init__(self, ip, interface, mac):
        self._ipv4 = ip
        self._ipv6 = mac
        self._connection_type = interface

    def set_username(self, username: str):
        self._username = username

    def get_username(self):
        return self._username


    def set_IPV4(self, ip:str):
        self._ipv4 = ip

    def get_IPV4(self):
        return self._ipv4

    def set_IPV6(self, mac:str):
        self._ipv6 = mac

    def get_IPV6(self):
        return self._ipv6

    def set_connection_type(self, connection_type):
        self._connection_type = connection_type

    def get_connection_type(self):
        return self._connection_type

    def get_uptime(self):
        return self._uptime

    def get_timestamp(self):
        return self._date

    def set_bytes_recv(self, bytes_recv):
        self._bytes_recv = bytes_recv

    def get_bytes_recv(self):
        return self._bytes_recv

    def set_bytes_sent(self, bytes_sent):
        self._bytes_sent = bytes_sent

    def get_bytes_sent(self):
        return self._bytes_sent


    def get_tuple_data(self) -> tuple | None:
        data: tuple = (
            self._username,
            self._ipv4,
            self._connection_type,
            self._ipv6,
            convert(self._bytes_sent),
            convert(self._bytes_recv),
            self._uptime,
            self._date,
        )
        return data

    def __str__(self) -> str:
        return "Entry("\
        f"username: {self._username}, " \
        f"ipv4: {self._ipv4}, " \
        f"ipv6: {self._ipv6}, " \
        f"bytes_sent: {self._bytes_sent}, "\
        f"bytes_recv: {self._bytes_recv}, "\
        f"uptime: {self._uptime}, " \
        f"connection_type: {self._connection_type})"
