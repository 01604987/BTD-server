import time
from actions import *

def main():
    # Number of slides to navigate
    num_slides = 4

    # Time delay between each action (in seconds)
    delay_between_actions = 2

    print("Starting slideshow...")
        
    move_mouse_smoothly((400,200), (1200,800), 4)
    move_mouse_smoothly((1200,800), (1000,200), 4)

    '''
    for _ in range(num_slides):
        # Pause for a moment
        time.sleep(delay_between_actions)

        # Trigger next slide action
        next_slide()
        print("Next slide!")

        # Move the mouse a little bit
        move_mouse_right(200, 0)
        print("move mouse right")
        '''
            

    print("Slideshow ended.")
    

if __name__ == "__main__":
    main()