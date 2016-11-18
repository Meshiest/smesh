package com.meshiest.smesh;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.RenderingHints;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


@SuppressWarnings("serial")
public class EditPane extends JPanel implements Runnable, MouseListener, KeyListener, MouseMotionListener, MouseWheelListener {

  private Main main;
  
  public double zoom;
  
  public int editMode;
  
  public ArrayList<Segment> statics, platforms;
  public ArrayList<Point> spawns;
  
  public boolean showFG, showBG, showMG, showSpawns, showStatics, showPlatforms;
  
  public File foregroundFile, backgroundFile, middlegroundFile, previewFile, iconFile;
  public BufferedImage foreground, background, middleground, transparencyBG, preview, icon;
  
  public double offsetX, offsetY;
  
  public boolean dragging, ctrlDown;
  public Point lastDrag, dragStart;
  public int dragType, lastClickType;
  public long lastClick;
  public String mapName;
  
  public Point selectedPoint;
  
  public ArrayList<UndoOption> undos;
  
  public static final int DRAG_TYPE_SCROLL = 1;
  public static final int DRAG_TYPE_STATIC = 2;
  public static final int DRAG_TYPE_STATIC_MOVE = 3;
  public static final int DRAG_TYPE_PLATFORM = 4;
  public static final int DRAG_TYPE_PLATFORM_MOVE = 5;
  
  public EditPane(Main main) {
    this.main = main;
    
    setFocusable(true);
    requestFocus();
    addMouseListener(this);
    addMouseWheelListener(this);
    addMouseMotionListener(this);
    addKeyListener(this);
    
    reset();
    
    generateTransparencyBG();
    
    new Thread(this).start();
  }
  
  public void reset() {
    statics = new ArrayList<>();
    platforms = new ArrayList<>();
    spawns = new ArrayList<>();
    undos = new ArrayList<>();
    
    showFG = true;
    showBG = true;
    showMG = true;
    showSpawns = true;
    showPlatforms = true;
    showStatics = true;
    
    mapName = "Unnamed";
    
    zoom = 0.5;
    offsetX = 0;
    offsetY = 0;
    
    dragging = false;
    dragType = 0;
    dragStart = null;
    lastDrag = null;
    
    previewFile = null;
    preview = null;
    iconFile = null;
    icon = null;
    foregroundFile = null;
    foreground = null;
    backgroundFile = null;
    background = null;
    middlegroundFile = null;
    middleground = null;
  }
  
  public void generateTransparencyBG() {
    transparencyBG = new BufferedImage(1600, 900, BufferedImage.TYPE_INT_ARGB);
    Graphics2D graphics = transparencyBG.createGraphics();
    
    for(int x = 0; x < 32; x++) {
      for(int y = 0; y < 18; y++) {
        graphics.setColor((x + y) % 2 == 0 ? Color.LIGHT_GRAY : Color.GRAY);
        graphics.fillRect(x * 50, y * 50, 50, 50);
      }
    }
  }
  
  @Override
  public void run() {
	long time = System.currentTimeMillis();
    while(true) {
      long curr = System.currentTimeMillis();
      double deltaTime = (curr - time) / 1000.0;
      time = curr;
      try {
        Thread.currentThread();
        Thread.sleep(1);
        requestFocus();
        tick(deltaTime);
        repaint();
      } catch (InterruptedException e) {
        e.printStackTrace();
      }

    }
  }
  
  public void tick(double deltaTime) {
    
  }
  
  public void loadJSON(File jsonFile) {
    reset();
    try {
      FileInputStream fis = new FileInputStream(jsonFile);
      byte[] data = new byte[(int) jsonFile.length()];
      fis.read(data);
      fis.close();
      JSONObject obj = new JSONObject(new String(data, "UTF-8"));
      
      mapName = obj.getString("name");
      previewFile = loadFile(obj.getString("preview"));
      iconFile = loadFile(obj.getString("icon"));
      foregroundFile = loadFile(obj.getString("foreground"));
      middlegroundFile = loadFile(obj.getString("middleground"));
      backgroundFile = loadFile(obj.getString("background"));
      
      platforms = Segment.fromJSONArray(obj.getJSONArray("segments_platform"));
      statics = Segment.fromJSONArray(obj.getJSONArray("segments_static"));
      JSONArray spawnObjs = obj.getJSONArray("spawnpoints");
      for(int i = 0; i < spawnObjs.length(); i++) {
        JSONArray spawn = spawnObjs.getJSONArray(i);
        spawns.add(new Point(spawn.getInt(0), spawn.getInt(1)));
      }
      
      reloadImages();
      
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
  
  public void saveJSON(File jsonFile) {
    try {
      JSONObject obj = new JSONObject();
      obj.put("name", mapName);
      obj.put("preview", previewFile.getName());
      obj.put("icon", iconFile.getName());
      obj.put("foreground", foregroundFile == null ? "" : foregroundFile.getName());
      obj.put("middleground", middlegroundFile == null ? "" : middlegroundFile.getName());
      obj.put("background", backgroundFile == null ? "" : backgroundFile.getName());
      obj.put("segments_platform", Segment.toJSONArray(platforms));
      obj.put("segments_static", Segment.toJSONArray(statics));
      JSONArray spawnpointArr = new JSONArray();
      for(int i = 0; i < spawns.size(); i++) {
        JSONArray posArr = new JSONArray();
        Point spawn = spawns.get(i);
        posArr.put(spawn.x);
        posArr.put(spawn.y);
        spawnpointArr.put(posArr);
      }
      obj.put("spawnpoints", spawnpointArr);
      String output = obj.toString(2);
      FileOutputStream fos = new FileOutputStream(jsonFile);
      fos.write(output.getBytes());
      fos.close();
    } catch (Exception e) {
      JOptionPane.showMessageDialog(this, "Error Saving!");
      e.printStackTrace();
    }
  }
  
  public File loadFile(String path) {
    if(path.length() == 0)
      return null;
    File file = new File(main.smeshPath.getAbsolutePath() + "/public/res/img/map/" + path);
    if(!file.exists())
      return null;
    return file;
  }
  
  public BufferedImage loadImageFromFile(File file) {
    if(file == null)
      return null;
    try {
      return ImageIO.read(file);
    } catch (IOException e) {
      e.printStackTrace();
      return null;
    }
  }
  
  public void reloadImages() {
    foreground = loadImageFromFile(foregroundFile);
    background = loadImageFromFile(backgroundFile);
    middleground = loadImageFromFile(middlegroundFile);
    icon = loadImageFromFile(iconFile);
    preview = loadImageFromFile(previewFile);
  }
  
  public void paintComponent(Graphics graphics) {
    Graphics2D g = (Graphics2D) graphics;
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    int width = getWidth(), height = getHeight();
    
    // simulate the game screen
    BufferedImage screenImage = (BufferedImage) createImage(1600, 900);
    Graphics2D screen = screenImage.createGraphics();
    screen.setStroke(new BasicStroke(5));
    
    screen.drawImage(transparencyBG, 0, 0, null);
    
    if(background != null && showBG)
      screen.drawImage(background, 0, 0, null);
    
    if(middleground != null && showMG)
      screen.drawImage(middleground, 0, 0, null);
    
    if(foreground != null && showFG)
      screen.drawImage(foreground, 0, 0, null);
    
    if(showStatics) {
      screen.setColor(Color.RED);
      drawSegments(screen, statics);
    }
    
    if(showPlatforms) {
      screen.setColor(Color.YELLOW);
      drawSegments(screen, platforms);
    }
    
    if(dragging && dragStart.distance(lastDrag) > 10 && (dragType == DRAG_TYPE_PLATFORM || dragType == DRAG_TYPE_STATIC)) {
      screen.setColor(dragType == DRAG_TYPE_STATIC ? Color.RED : Color.YELLOW);
      Point start = realToScreen(dragStart), end = realToScreen(lastDrag);
      screen.drawLine(start.x, start.y, end.x, end.y);
      screen.setColor(Color.ORANGE);
      screen.drawOval(start.x - 15, start.y - 15, 30, 30);
      screen.drawOval(end.x - 15, end.y - 15, 30, 30);
    }
    
    if(showSpawns)
      drawSpawns(screen);
    
    g.setColor(Color.black);
    g.fillRect(0, 0, width, height);

    g.drawImage(screenImage,
      (int)(offsetX * zoom - 800 * zoom) + width / 2,
      (int)(offsetY * zoom - 450 * zoom) + height / 2,
      (int)(1600 * zoom),
      (int)(900 * zoom),
      null
    );
    
    g.setColor(Color.WHITE);
    g.drawRect(
      (int)(offsetX * zoom - (800 + 220) * zoom) + width / 2,
      (int)(offsetY * zoom - 450 * zoom) + height / 2,
      (int)(200 * zoom),
      (int)(200 * zoom)
    );
    if(icon != null)
      g.drawImage(icon,
        (int)(offsetX * zoom - (800 + 220) * zoom) + width / 2,
        (int)(offsetY * zoom - 450 * zoom) + height / 2,
        (int)(200 * zoom),
        (int)(200 * zoom),
        null
      );
    
    g.drawRect(
      (int)(offsetX * zoom - 800 * zoom) + width / 2,
      (int)(offsetY * zoom - (450 * 2 + 20) * zoom) + height / 2,
      (int)(1600 * zoom),
      (int)(450 * zoom)
     );
    
    if(preview != null)
      g.drawImage(preview,
        (int)(offsetX * zoom - 800 * zoom) + width / 2,
        (int)(offsetY * zoom - (450 * 2 + 20) * zoom) + height / 2,
        (int)(1600 * zoom),
        (int)(preview.getHeight() * zoom),
        null
      );
  }
  
  public Point realToScreen(Point point) {
    int width = getWidth(), height = getHeight();
    return new Point(
     (int)(- offsetX + (point.x - width/2) / zoom + 800),
     (int)(- offsetY + (point.y - height/2) / zoom + 450)
    );
  }
  
  public void drawSegments(Graphics2D screen, ArrayList<Segment> segments) {
    for(int i = 0; i < segments.size(); i++) {
      Segment segment = segments.get(i);
      segment.draw(screen);
      screen.drawOval(segment.a.x - 5, segment.a.y - 5, 10, 10);
      screen.drawOval(segment.b.x - 5, segment.b.y - 5, 10, 10);
    }
  }
  
  public void drawSpawns(Graphics2D screen) {
    screen.setColor(Color.MAGENTA);
    for(int i = 0; i < spawns.size(); i++) {
      Point spawn = spawns.get(i);
      screen.drawOval(spawn.x - 10, spawn.y - 10, 20, 20);
    }
  }
  
  public Point getNear(ArrayList<Segment> segments, Point point) {
    for(int i = 0; i < segments.size(); i++) {
      Segment seg = segments.get(i);
      if(seg.a.distance(point) < 10)
        return seg.a;
      
      if(seg.b.distance(point) < 10)
        return seg.b;
    }
    return null;
  }
  
  public Point getNearPoint(ArrayList<Point> points, Point point) {
    for(int i = 0; i < points.size(); i++) {
      Point p = points.get(i);
      if(p.distance(point) < 10)
        return p;
    }
    return null;
  }
  
  public Segment getNearSegment(ArrayList<Segment> segments, Point point) {
    for(int i = 0; i < segments.size(); i++) {
      Segment seg = segments.get(i);
      if(seg.a.distance(point) < 10 || seg.b.distance(point) < 10)
        return seg;
      }
    return null;
  }

  public void mousePressed(MouseEvent event) {
    dragging = true;
    lastDrag = event.getPoint();
    Point screenPoint = realToScreen(lastDrag);
    long time = System.currentTimeMillis();
    
    int button = event.getButton();
    
    boolean doubleClick = time - lastClick < 200 && lastClickType == button;
    dragStart = lastDrag;
    
    switch(button) {
    case MouseEvent.BUTTON2: // middle click
      dragType = DRAG_TYPE_SCROLL;
      break;
    case MouseEvent.BUTTON1:
      if(doubleClick) {
        if(ctrlDown) {
          Segment seg = getNearSegment(statics, screenPoint);
          if(seg != null) {
            statics.remove(seg);
            undos.add(UndoOption.removeSegment(statics, seg));
          }
        } else {
          dragType = DRAG_TYPE_STATIC_MOVE;
          selectedPoint = getNear(statics, screenPoint);          
        }
      } else {
        dragType = DRAG_TYPE_STATIC;
      }
      break;
    case MouseEvent.BUTTON3:
      if(doubleClick) {
        if(ctrlDown) {
          Segment seg = getNearSegment(platforms, screenPoint);
          if(seg != null) {
            platforms.remove(seg);
            undos.add(UndoOption.removeSegment(platforms, seg));
          }
        } else {
          dragType = DRAG_TYPE_PLATFORM_MOVE;
          selectedPoint = getNear(platforms, screenPoint);
        }
      } else {
        dragType = DRAG_TYPE_PLATFORM;
      }
      break;

    }
    
    lastClickType = button;
    lastClick = time;
  }
  
  public void mouseDragged(MouseEvent event) {
    Point point = event.getPoint();
    double dragDist = Math.hypot(dragStart.x - point.x, dragStart.y - point.y);
    Point screenPoint = realToScreen(lastDrag);
    switch(dragType) {
    case DRAG_TYPE_SCROLL:
      double shiftX = (point.x - lastDrag.x) / zoom;
      double shiftY = (point.y - lastDrag.y) / zoom;
      offsetX += shiftX;
      offsetY += shiftY;
      break;
    case DRAG_TYPE_PLATFORM_MOVE: case DRAG_TYPE_STATIC_MOVE:
      if(selectedPoint != null)
        selectedPoint.setLocation(screenPoint.x, screenPoint.y);
      break;
    }
    lastDrag = point;
  }
  
  public void mouseReleased(MouseEvent event) {
    Point point = event.getPoint();
    double dragDist = Math.hypot(dragStart.x - point.x, dragStart.y - point.y);
    Point screenPoint = realToScreen(lastDrag);
    
    switch(dragType) {
    case DRAG_TYPE_SCROLL:
      break;
    case DRAG_TYPE_STATIC:
      if(dragDist > 10) {
        statics.add(new Segment(realToScreen(dragStart), screenPoint));
        undos.add(UndoOption.createSegment(statics, statics.size()-1));
      }
      break;
    case DRAG_TYPE_PLATFORM:
      if(dragDist > 10) {
        platforms.add(new Segment(realToScreen(dragStart), screenPoint));
        undos.add(UndoOption.createSegment(platforms, platforms.size()-1));
      }
      break;
    case DRAG_TYPE_PLATFORM_MOVE: case DRAG_TYPE_STATIC_MOVE:
      if(screenPoint != null)
        undos.add(UndoOption.movePoint(screenPoint, realToScreen(dragStart)));
      break;
    }
      
    
    dragging = false;
    lastDrag = null;
    dragStart = null;
    dragType = 0;
    
  }
  

  public void mouseWheelMoved(MouseWheelEvent event) {
    int rot = event.getWheelRotation();
    zoom *= Math.pow(2, rot);
    zoom = Math.max(Math.min(8, zoom), 0.0625);    
  }

  public void keyPressed(KeyEvent event) {
    int code = event.getKeyCode();
    switch(code) { 
    case KeyEvent.VK_Z:
      if(event.isControlDown()) {
        if(undos.size() > 0)
          undos.remove(undos.size()-1).undo();
      }
      break;
    case KeyEvent.VK_R:
      if(event.isControlDown()) {
        reloadImages();
      }
    case KeyEvent.VK_SPACE:
      Point point = getMousePosition();
      if(point != null) {
        point = realToScreen(point);
        Point near = getNearPoint(spawns, point);
        if(near != null) {
          spawns.remove(near);
          undos.add(UndoOption.removePoint(spawns, near));
        } else {
          spawns.add(point);
          undos.add(UndoOption.createPoint(spawns, spawns.size()-1));
        }
      }
    }
    ctrlDown = event.isControlDown();
    
  }

 
  public void keyReleased(KeyEvent event) {
    if(event.getKeyCode() == KeyEvent.VK_CONTROL)
      ctrlDown = false;
    
  }
  
  public void mouseMoved(MouseEvent event) { }  


  @Override
  public void keyTyped(KeyEvent arg0) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void mouseClicked(MouseEvent arg0) {
    
  }

  @Override
  public void mouseEntered(MouseEvent arg0) {
    // TODO Auto-generated method stub
    
  }

  @Override
  public void mouseExited(MouseEvent arg0) {
    // TODO Auto-generated method stub
    
  }




}
