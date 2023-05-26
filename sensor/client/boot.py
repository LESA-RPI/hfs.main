print("[INFO] Booting device...")

from machine import Pin
import esp

# get the config file
import config

# check for updates
if (config.CHECK_FOR_UPDATES):
    import git_update
    git_update.update()
else:
    print("[INFO] Skipped check for update")

#result = esp.esp_wifi_stop()