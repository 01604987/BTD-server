import threading
from conrols import actions
from processing.data_collection import DC
from processing import complementary_filter, linear_acceleration, filter


def start(exit:threading.Event, data_collection:DC):
    counter = 0
    x_null = 0
    y_null = 0
    while(not exit.is_set()):
        if counter < 10 :
            # get the mean for null line
            return
            
            
        x = 0
        y = 0
        # calculate next x, y movement
        actions.move_mouse_right(x, y)
        counter += 1
        pass
        