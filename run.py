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

from c3toc import C3TOCAPI
from pyfis.ibis import SerialIBISMaster

from _config import *


def main():
    display = SerialIBISMaster(CONFIG_IBIS_PORT)
    toc = C3TOCAPI()
    
    while True:
        try:
            trains = toc.get_trains()['trains']
            if CONFIG_TRAIN in trains:
                display.DS009(trains[CONFIG_TRAIN]['next_stop']['name'])
            else:
                display.DS009("CCCamp 2023")
            time.sleep(10)
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
