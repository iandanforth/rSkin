#!/usr/bin/python

'''
This script connects to a specified USB port and listens for the output
of rSkin.

It then displays that output as a grid with each box representing 
the location of a touch and its intensity

---Original Attribution of sample file---
Sample Python/Pygame Programs
Simpson College Computer Science
http://cs.simpson.edu
'''
from __future__ import division

import pygame
import random
import serial

def main():
  # Initialize the game engine
  pygame.init()
   
  # Set the width and height of the screen
  small = 0
  if small:
    size=[500,500]
    box = 16
  else:
    size=[1000,1000]
    box = 32

  screen=pygame.display.set_mode(size)
  
  # Give the window a name
  pygame.display.set_caption("rSkin Pressure Grid")
   
  # Clear the screen and set the screen background
  white = (255,255,255)
  screen.fill(white)

  #Loop until the user clicks the close button.
  done = False
  clock = pygame.time.Clock()

  # Establish the connection to our teensy board
  ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

  # Main loop. Set up values which will change with each iteration
  offsetX = 1
  offsetY = 1
  while done==False:
   
      # This limits the while loop to a max of 10 times per second.
      # Leave this out and we will use all CPU we can.
      #clock.tick(100)
       
      # User did something
      for event in pygame.event.get():
        # If user clicked close
        if event.type == pygame.QUIT:
          # Flag that we are done so we exit this loop 
          done=True 

      # Read in our latest values from our USB port - a '\n' terminated line
      vals = ser.readline().strip().split(',')
      
      # Take off the first item which contains the column number
      column = vals.pop(0)
      
      # If it's blank then there's nothing interesting in this line
      if not column.strip():
        continue
      
      # We only really care about the first few numbers
      castVals = []
      for val in vals:
        try:
          castVals.append(int(val))
        except ValueError:
          castVals.append(0)
      
      # Render the value to a grid on the screen
      for val in castVals:    
        ratio = val / 600
        val = ratio * 255
        if val < 0:
          val = 0
        color = (val, val, val)
        h = w = box
        # Calculate where to draw our box
        x = (offsetX * box) + (1 * offsetX)
        y = (offsetY * box) + (1 * offsetY)
        # Draw to the screen
        pygame.draw.rect(screen,color,[x, y, h, w])
        # Update our offsets
        if offsetX % 28 == 0:
          offsetX = 1
          if offsetY % 28 == 0:
            offsetY = 1
          else:
            offsetY +=1
        else:
          offsetX += 1

      # Go ahead and update the screen with what we've drawn.
      # This MUST happen after all the other drawing commands.
      pygame.display.flip()
 
  # Be IDLE friendly
  pygame.quit ()
  
if __name__ == '__main__':
  main()
