import logging

from controller.system_controller import SystemController

if __name__ == '__main__':
    while True:
        try:
            SystemController().start_system()
        except Exception as error:
            logging.exception(str(error))
            print('[!] Tivemos um problema inesperado no sistema!')
