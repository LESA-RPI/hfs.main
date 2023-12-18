import machine
import ssd1306

# Pin assignments
i2c = machine.I2C(scl=machine.Pin(3), sda=machine.Pin(2)) # D3 for SCL, D2 for SDA

# OLED dimensions
oled_width = 128
oled_height = 64

# Initialize the OLED display
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Clear the display
oled.fill(0)

# Add text
oled.text('Hello World!', 0, 0)
oled.text('MicroPython', 0, 10)

# Display the text
oled.show()
