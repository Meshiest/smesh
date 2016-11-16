package com.meshiest.smesh;

import java.awt.Point;
import java.util.ArrayList;

public abstract class UndoOption {
  
   public static UndoOption createSegment(final ArrayList<Segment> arraylist, final int index) {
     return new UndoOption(){
       private final ArrayList<Segment> arr = arraylist;
       private final int i = index;
       public void undo() {
         arr.remove(i);
       }
     };
   }
   
   public static UndoOption createPoint(final ArrayList<Point> arraylist, final int index) {
     return new UndoOption(){
       private final ArrayList<Point> arr = arraylist;
       private final int i = index;
       public void undo() {
         arr.remove(i);
       }
     };
   }
   
   public static UndoOption removePoint(final ArrayList<Point> arraylist, final Point point) {
     return new UndoOption(){
       private final ArrayList<Point> arr = arraylist;
       private final Point p = point;
       public void undo() {
         arr.add(p);
       }
     };
   }
   
   public static UndoOption removeSegment(final ArrayList<Segment> arraylist, final Segment segment) {
     return new UndoOption(){
       private final ArrayList<Segment> arr = arraylist;
       private final Segment seg = segment;
       public void undo() {
         arr.add(seg);
       }
     };
   }
   
   public static UndoOption movePoint(final Point point, final Point lastPosition) {
     return new UndoOption(){
       private final Point p = point;
       private final Point pos = lastPosition;
       public void undo() {
         p.setLocation(pos);
       }
     };
   }
   
   
   public void undo(){};
  
}
