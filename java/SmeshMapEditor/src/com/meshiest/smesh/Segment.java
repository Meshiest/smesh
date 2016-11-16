package com.meshiest.smesh;

import java.awt.Graphics2D;
import java.awt.Point;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;

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
  
  public static ArrayList<Segment> fromJSONArray(JSONArray arr) {
    ArrayList<Segment> segs = new ArrayList<>();
    for(int i = 0; i < arr.length(); i++) {
      try {
        JSONArray segment = arr.getJSONArray(i);
        segs.add(new Segment(
          new Point(segment.getJSONArray(0).getInt(0), segment.getJSONArray(0).getInt(1)),
          new Point(segment.getJSONArray(1).getInt(0), segment.getJSONArray(1).getInt(1))
        ));
      } catch (JSONException e) {
        e.printStackTrace();
      }
    }
    return segs;
  }
}
