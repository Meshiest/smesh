package com.meshiest.smesh;

import java.awt.Graphics2D;
import java.awt.Point;

public class Segment {

  public Point a, b;
  public Segment(Point a, Point b) {
    this.a = a;
    this.b = b;
  }
  
  public void draw(Graphics2D g) {
    g.drawLine(a.x, a.y, b.x, b.y);
  }
  
  public String toString() {
    return "[\n" +
           "  [" + a.x + ", " + a.y + "],\n" +
           "  [" + b.x + ", " + b.y + "]\n" +
           "]";
     
  }
}
