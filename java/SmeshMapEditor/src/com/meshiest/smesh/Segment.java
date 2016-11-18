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
  
  public static JSONArray toJSONArray(ArrayList<Segment> segments) {
    JSONArray arr = new JSONArray();
    for(int i = 0; i < segments.size(); i++) {
      JSONArray posArr = new JSONArray(), pointA = new JSONArray(), pointB = new JSONArray();
      Segment seg = segments.get(i);
      pointA.put(seg.a.x);
      pointA.put(seg.a.y);
      pointB.put(seg.b.x);
      pointB.put(seg.b.y);
      posArr.put(pointA);
      posArr.put(pointB);
      System.out.println(i+"ok");
      arr.put(posArr);
    }
    return arr;
  }
}
