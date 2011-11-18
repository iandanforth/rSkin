void serialEvent (Serial myPort) {
  // get the ASCII string:
  String inString = myPort.readStringUntil('\n');
  int x=0;
  int y=0;

  if (inString != null) {  // if it's not empty:
    inString = trim(inString);    // trim off any whitespace:
    int incomingValues[] = int(split(inString, ","));  //split incoming values by comma
    //println(incomingValues.length);

    if (incomingValues.length == cols+1) {  //<= cols+1 && incomingValues.length > 0) {
      
      // start loop at i=1 to skip row count
      for (int i = 1; i < incomingValues.length; i++) {
        //x = incomingValues[0];
        x = fleshRef[incomingValues[0]][1];
        y = rows-(i-1);
        
        // for testing:
        //rSkinArray[y][x] = incomingValues[i];
        //println(rSkinArray[5][10]);
        
        ellipseMode(CENTER);
        rectMode(CENTER);
  
        //shift matrix to account for center mode:
        pushMatrix();
        translate((width/cols)/2, 0); 
        
        //fill rectangle with grayscale and scale the incoming sensor values:
        //float mappedValue = map(incomingValues[i], incomingMin, incomingMax, 0, 255);
        //fill(mappedValue);
        //rect(x*(width/cols), y*(height/rows), (width/cols),(height/rows));
        
        //draw ellipses and scale their widths and heights depending on incoming sensor values:
        float mappedColValue = map(incomingValues[i], 100, 700, 0, width/cols);
        float mappedRowValue = map(incomingValues[i], 100, 700, 0, height/rows);
        fill(255);
        rect(x*(width/cols), y*(height/rows), (width/cols),(height/rows));
        fill(0);
        ellipse(x*(width/cols), y*(height/rows), mappedColValue, mappedRowValue);
        
        // draw rectables to block out the missing grid intersections:
        rectMode(CORNER);
        fill(0);
        rect(17*(width/cols), 0.5*(height/rows),    width-17*(width/cols), 4*(height/rows));
        rect(17*(width/cols), 10.5*(height/rows),   width-17*(width/cols), 8*(height/rows));
        rect(17*(width/cols), 24.5*(height/rows),   width-17*(width/cols), 4*(height/rows));
        
        
        /*
        if(y == 0){
        for(int n=0;n<28;n++){
        text(n, n*(width/cols), height/rows);
        }
        }
        */
        
        popMatrix();
        }
    }
  }
}

