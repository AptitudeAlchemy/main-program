import psutil as util
from ctypes import windll
from entry import Entry, convert
from threading import Thread
import json
from logger import write_log

messageBox: any = windll.user32.MessageBoxW

def check_connectivity() -> bool | None: 

    flag: bool = False
    connected_devices: dict = {}

    interfaces: dict =  util.net_io_counters(pernic=True)
    if 'Wi-Fi' not in interfaces.keys():
        write_log("WI-FI interface is not installed in this system.")

    interfaces_status: dict = util.net_if_stats() 

    for key, value in interfaces_status.items():
        interface_name: str = key.lower()
        
        # Checking the system is connected via WI-FI or not
        if value.isup and (interface_name == 'wi-fi' or interface_name == 'wlan'):
            connected_devices[key] = interfaces_status[key]
            bytes_recv = interfaces[key].bytes_recv
            bytes_send = interfaces[key].bytes_sent
            fetch_info_and_write(key, bytes_send, bytes_recv)

            flag = True
            new_thread: Thread = Thread(target=show_alert,
                                        args=("You're connected to Wi-Fi. Please try switching to LAN.",))
            new_thread.start()

        elif value.isup and interface_name.startswith('eth'):
            connected_devices[key] = interfaces_status[key]
            bytes_recv = interfaces[key].bytes_recv
            bytes_sent = interfaces[key].bytes_sent
            fetch_info_and_write(key, bytes_sent, bytes_recv)
            flag = True
    
    return flag

def show_alert(message: str) -> bool | None:
    messageBox(0, message, "Connectivity status", 1)
    return

def fetch_info_and_write(key, bytes_sent, bytes_recv) -> bool | None:
    con: list = util.net_if_addrs()[key]
    ipv4: str = con[1].address
    ipv6: str = con[2].address

    record: Entry = Entry(ipv4, key, ipv6)
    record.set_bytes_recv(bytes_recv)
    record.set_bytes_sent(bytes_sent)

    if write_data_server(record):
        print("Data wrote to server!")
        write_log("Date wrote to server!")
    else:
        print("Unable to write the data to server!")
        write_log("Unable to write the data to server!")

    return

def write_data_server(record: Entry) -> bool | None:
    API = 'https://aptitudealchemy.pythonanywhere.com/entry/add'

    # "username": "Madhan M",
    # "ip_address": "192.168.0.168",
    # "mac_address": "fsf43gr34c-f42-cat4-afr4",
    # "uptime": "2 hrs",
    # "bytes_send": "3244bytes",
    # "connection_type": "LAN",
    # "bytes_recv": "23563 bytes"

    import requests

    try:

        payload: dict = {
            'username':record.get_username(),
            'ip_address':record.get_IPV4(),
            'mac_address':record.get_IPV6(),
            'uptime':record.get_uptime(),
            'bytes_sent':convert(record.get_bytes_sent()),
            'bytes_recv':convert(record.get_bytes_recv()),
            'connection_type':record.get_connection_type()
        }
        response = requests.post(API, headers={'content-type':'application/json'}, json=payload)

        if not response.status_code == 200:
            return False

        write_log("Request success")
        return True

    except Exception as exception:
        print(exception)

    return False

