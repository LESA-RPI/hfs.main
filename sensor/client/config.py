
CHECK_FOR_UPDATES = True
LAN_SSID = "SLERC3"
LAN_PASSWORD = "ganlightemittingdiode"
GITHUB_URL = "https://github.com/LESA-RPI/hfs.main"
DEV_VERSION_FILE = "https://raw.githubusercontent.com/LESA-RPI/hfs.main/dev-deploy/sensor/client/DEVELOPER_VERSION"
GITHUB_SRC_DIR = "sensor/client"
UPDATE_SUB_DIR = False
GITHUB_BRANCH = "dev-deploy"

# we can do this because python only runs a file on import once!
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
        GITHUB_BRANCH = config["github-branch"]
except Exception as e:
    print("[WARNING] No valid config.json file found, using default options ({})".format(e))
