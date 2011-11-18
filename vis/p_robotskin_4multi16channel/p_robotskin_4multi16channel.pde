/*
  Based on Serial Graphing Sketch by Tom Igoe
  Language: Processing
*/

import processing.serial.*;

boolean fontInitialized = false;  // whether the font's been initialized
Serial myPort;                    // The serial port

int rows = 28;
int cols = 28;
int[][] rSkinArray = new int[rows][cols]; // adding +1 to the cols accounts for the row number

// set max and min for incoming values:
int incomingMin = 100;
int incomingMax = 700;

// re-maps incoming column values to their location on the skin
int[][] fleshRef = {
//{skin }  
{0,27},
{1,0},
{2,1},
{3,3},
{4,2},
{5,4},
{6,5},
{7,26},
{8,25},
{9,24},
{10,23},
{11,6},
{12,7},
{13,8},
{14,9},
{15,10},
{16,11},
{17,12},
{18,13},
{19,22},
{20,21},
{21,20},
{22,18},
{23,19},
{24,17},
{25,16},
{26,15},
{27,14}
}; 

float xpos = 0;  // x position of the graph
PFont myFont;  // font for writing text to the window
 
void setup () {
  size(1000, 600);  // set up the window to whatever size you want:
  // List all the available serial ports:
  println(Serial.list());
  // I know that the first port in the serial list on my mac
  // is always my  Arduino or Wiring module, so I open Serial.list()[0].
  // Open whatever port is the one you're using.
  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 9600);
  myPort.clear();
  // don't generate a serialEvent() until you get a newline (\n) byte:
  myPort.bufferUntil('\n');

  // create a font with the fourth font available to the system:
  myFont = loadFont("Serif-12.vlw"); 
  textFont(myFont,12);

  background(0);
  smooth();
  ellipseMode(CENTER);
  rectMode(CENTER);
}
 
void draw () {
  // nothing happens in the draw loop, 
  // but it's needed to keep the program running
}


// if spacebar pressed then take a screenshot of window and save to code file:
void keyPressed(){
  if (key==' ') saveFrame();
}
