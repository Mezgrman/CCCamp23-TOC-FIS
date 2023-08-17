"""
Copyright (C) 2023 Julian Metzler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import traceback

from c3toc import C3TOCAPI
from pyfis.ibis import SerialIBISMaster

from _config import *


def main():
    try:
        display = SerialIBISMaster(CONFIG_IBIS_PORT)
        toc = C3TOCAPI()
        
        trains = toc.get_trains()['trains']
        last_switch = 0
        last_update = 0
        text_page = 0
        
        while True:
            now = time.time()
            if now - last_update >= 10:
                print("Updating")
                try:
                    trains = toc.get_trains()['trains']
                except:
                    trains = []
                last_update = now
            if now - last_switch >= 5:
                if CONFIG_TRAIN in trains:
                    if text_page == 0:
                        display.DS009(trains[CONFIG_TRAIN]['next_stop']['name'])
                        text_page = 1
                    elif text_page == 1:
                        display.DS009("Nächster Halt:")
                        text_page = 0
                else:
                    display.DS009(CONFIG_TRAIN)
                last_switch = now
            time.sleep(1)
    except KeyboardInterrupt:
        raise
    except:
        try:
            display.port.close()
        except:
            pass
        raise


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
            print("Restarting in 10 seconds")
            time.sleep(10)
