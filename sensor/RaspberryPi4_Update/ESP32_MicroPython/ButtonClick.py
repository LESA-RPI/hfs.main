from machine import Pin
from time import sleep

print('Initialization')

led = Pin(21, Pin.OUT)    # 22 number in is Output
push_button = Pin(18, Pin.IN)  # 23 number pin is input

while True:
  
  logic_state = push_button.value()
  if logic_state == True:     # if pressed the push_button
      led.value(0)             # led will turn ON
      #print('ON')
      sleep(0.25)

  elif logic_state == False:                       # if push_button not pressed
      led.value(1)             # led will turn OFF
      print('Button has been clicked')
      sleep(0.25)

