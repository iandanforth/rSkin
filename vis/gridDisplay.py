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
import serial
import math

# Heatmap color scheme we'll use
from heatmap import Heatmap

def main():
  # Initialize the game engine
  pygame.init()
   
  # Set the width and height of the screen
  small = 1
  if small:
    ## [width, height] God damn stupid
    size=[600,500]
    boxH = 16
    boxW = 20
  else:
    size=[1200,1000]
    boxH = 32
    boxW = 40

  screen=pygame.display.set_mode(size)
  
  # Give the window a name
  pygame.display.set_caption("rSkin Pressure Grid")
   
  # Clear the screen and set the screen background
  white = (255,255,255)
  screen.fill(white)
  
  # Establish the connection to our teensy board
  ser = serial.Serial('/dev/tty.usbmodem12341', 9600, timeout=1)
  
  # Map the incoming columns to the physical columns on the rSkin
  fleshRef = [27,
              0,
              1,
              3,
              2,
              4,
              5,
              26,
              25,
              24,
              23,
              6,
              7,
              8,
              9,
              10,
              11,
              12,
              13,
              22,
              21,
              20,
              18,
              19,
              17,
              16,
              15,
              14]
  
  '''
  Before rendering to the screen we'll build a matrix of values representing
  one frame.
  
  Format: frame[(rows, cols)]
  '''
  frame = {}
  
  # Loop until the user clicks the close button.
  done = False

  while done==False:
       
      # User did something
      for event in pygame.event.get():
        # If user clicked close
        if event.type == pygame.QUIT:
          # Flag that we are done so we exit this loop 
          done=True
          
      # Read in our latest values from our USB port - a '\n' terminated line
      vals = ser.readline().strip().split(',')
      
      # Take off the first item which contains the column number
      try:
        col = int(vals.pop(0))
      except ValueError:
        raise Exception('Lost connection to teensy, please reconnect')
        
      # Remap that column number. Input cols are indexed from 1
      try:
        col = fleshRef[col]
      except IndexError:
        continue

      # Sync the frame with the output (wait for a row 0 to come along)
      if not frame and col != 0:
        continue
      
      # Clear out the frame every time we hit a 0 row after that
      if frame and col == 0:
        frame = {}
      
      # Create a matrix that re-alligns the incoming lists into columns
      for i, val in enumerate(vals):
        row = 27 - i
        frame[(row, col)] = int(val)
      
      # Once we have a full frame, update the screen
      if len(frame) == 784:
        
        # Draw the frame internally
        for row in range(28):
          for col in range(28):
            val = frame[(row,col)]  
            val = rescaleInput(val)
            color = Heatmap[255 - val]
            # Calculate where to draw our box
            x = (col * boxW) + (1 * col) + 5
            y = (row * boxH) + (1 * row) + 5
            # Draw to the buffer
            pygame.draw.rect(screen,color,[x, y, boxW, boxH])
    
        # Render the frame to the display
        pygame.display.flip()
 
  # Be IDLE friendly
  pygame.quit()

def rescaleInput(val):
  '''
  Maps an incoming range of 0 - 700 to 0 - 255 for display as grayscale
  '''
  ratio = val / 700
  val = ratio * 255
  if val < 0:
    val = 0
  if val > 255:
    val = 255
  val = math.floor(val)
  
  return int(val)

if __name__ == '__main__':
  main()
