import device_sensor as sensor # sensor.readAndSend(server, pipe)
import device_pins as pins

# entry point for the program
# run this program once and only once, server will decide how to loop
async def run(server, pipe, frequency, sampleSize):    
    print("[prgm_distance] start")
    # pipe.write("data")
    sensor.readSonar
    pipe.notify(server)
    print("[prgm_distance] stop")