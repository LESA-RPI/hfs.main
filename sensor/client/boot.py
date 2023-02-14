print("[INFO] Booting device...")

PRODUCTION = False
CHECK_FOR_UPDATES = True
LAN_SSID = "SLERC3"
LAN_PASSWORD = "ganlightemittingdiode"
GITHUB_URL = "https://github.com/LESA-RPI/hfs.main"
DEV_VERSION_FILE = "https://raw.githubusercontent.com/LESA-RPI/hfs.main/dev-deploy/sensor/client/DEVELOPER_VERSION"
GITHUB_SRC_DIR = "sensor/client"
UPDATE_SUB_DIR = False
GITHUB_BRANCH = "dev-deploy"

from machine import Pin

# get the config file, if it exists
try:
    import json
    with open("config.json", "r") as file:
        config = json.load(file)
        CHECK_FOR_UPDATES = config["check-for-updates"]
        LAN_SSID = config["lan-ssid"]
        LAN_PASSWORD = config["lan-password"]
        GITHUB_URL = config["github-url"]
        UPDATE_SUB_DIR = config["update-sub-dir"]
        GITHUB_SRC_DIR = config["github-src-dir"]
        DEV_VERSION_FILE = config["dev-version-file"]
except Exception as e:
    print("[WARNING] No valid config.json file found, using default options ({})".format(e))
# check for updates
if (CHECK_FOR_UPDATES):
    print("[INFO] Checking for updates...")
    #try: 
        # monitor memory
    import time, machine, network, gc
    import ota_update.updater as ota #import ota_updater# ota# OTAUpdater
    time.sleep(1)
    print('[INFO] Memory free {}'.format(gc.mem_free()))
    # connect to interweb
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('[INFO] Connecting to network...')
        sta_if.active(True)
        sta_if.connect(LAN_SSID, LAN_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('[INFO] Connected to', LAN_SSID)
    print('[INFO] Network config {}'.format(sta_if.ifconfig()))
    # download and install an update if availible
    ota_updater = ota.OTAUpdater(GITHUB_URL, github_src_dir=GITHUB_SRC_DIR, dev_version_url=DEV_VERSION_FILE, update_sub_dir=UPDATE_SUB_DIR, main_dir=GITHUB_BRANCH)
    update = ota_updater.dev_install_update_if_available()
    del(ota_updater)
    if (update):
        print("[INFO] Upgrade complete, reseting...")
        machine.reset()
    #except Exception as e:
    #    print("WARNING: Update failed ({})".format(e))

