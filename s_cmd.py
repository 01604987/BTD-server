termination = 'end'.encode()
left_swipe = 'CSL'.encode() # Command Swipe Left (CSL)
right_swipe = 'CSR'.encode() # Command Swipe Right (CSR)
mouse_begin = 'mbegin'.encode()
mouse_end = 'mstop'.encode()
mouse_hold = 'mhold'.encode()
mouse_release = 'mrelease'.encode()
# index double tapped is implemented as 2x single tapped in succession
# since index_tapped is bound to left mouse click, there is no need to specify double taps
index_tapped = 'itap'.encode()
middle_tapped = 'mtap'.encode()
# here middle double tapped needs to be specified because middle_tapped is bound to a keyboard shorcut, which means 2x middle_tapped needs a different shortcut
middle_double_tapped = 'm2tap'.encode()
vol_begin = 'vbegin'.encode()
vol_end = 'vstop'.encode()
zoom_begin = 'zbegin'.encode()
zoom_end = 'zstop'.encode()