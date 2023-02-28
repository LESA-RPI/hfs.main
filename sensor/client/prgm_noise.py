
# run this program once and only once, server will decide how to loop
def run(server, pipe, data: int):    
    print("[prgm_noise] start")
    # pipe.write("data")
    pipe.notify(server)
    print("[prgm_noise] stop")