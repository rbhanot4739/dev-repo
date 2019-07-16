#!/usr/bin/env python3.7

from hardware import (MappingError, SerialError, SerialPasswordError,
                      serial_console_checker)

if __name__ == '__main__':
    try:
        print(serial_console_checker())
    except MappingError:
        print("No avocent entry found for host !")
    except SerialError:
        print("Console Down")
    except SerialPasswordError:
        print("Incorrect password ! Please try again !")
