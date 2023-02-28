import device_sensor as sensor # sensor.readAndSend(server, pipe)

# entry point for the program
# run this program once and only once, server will decide how to loop
def run(server, pipe, data: int):    
    print("[prgm_distance] start")
    # pipe.write("data")
    pipe.notify(server)
    print("[prgm_distance] stop")