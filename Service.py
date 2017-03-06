import socket

from datetime import datetime


class Service:
    @staticmethod
    def check_connection(host, port, timeout):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True

        except Exception as exc:
            print exc.message
            return False

    @staticmethod
    def write_to_log(message):
        pass
        # with open('/log', 'a+') as file:
        #     file.write('\n' + format(datetime.now()) +
        #                ' : ' + message)
        #     file.write('\n===========================================================================')

