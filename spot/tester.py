import time
from SpotController import SpotController


def empty_handler():
    pass


sc = SpotController("admin", "2zqa8dgw7lor", "192.168.50.3")

sc.lease_control()
sc.power_on_stand_up()
time.sleep(3)
sc.power_off_sit_down()

sc.move_to_draw(start_drawing_trigger_handler=empty_handler, end_drawing_trigger_handler=empty_handler,
                xx=[0, 400, 400, 0, 0], yy=[0, 0, 300, 300, 0])
