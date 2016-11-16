package com.meshiest.smesh;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Main extends JFrame implements ActionListener{
  
  public File smeshPath;
  
  public JMenuItem saveItem, openItem, setFG, setBG, setMG, reloadImages, setPreview, setIcon;
  public JButton showFG, showBG, showMG, showSpawns, showPlatforms, showStatics;
  
  public EditPane editPane;
  
  public Main(File smeshPath) {
    super("Smesh Map Editor");
    this.smeshPath = smeshPath;
    
    setResizable(true);
    setSize(800, 600);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    
    JMenuBar menuBar = new JMenuBar();
    JMenu fileMenu = new JMenu("File");
    fileMenu.setMnemonic('f');
    
    saveItem = new JMenuItem("Save");
    saveItem.setMnemonic('s');
    saveItem.addActionListener(this);
    fileMenu.add(saveItem);

    openItem = new JMenuItem("Open");
    openItem.setMnemonic('o');
    openItem.addActionListener(this);
    fileMenu.add(openItem);
    
    menuBar.add(fileMenu);
    
    JMenu editMenu = new JMenu("Edit");
    editMenu.setMnemonic('e');
    
    setFG = new JMenuItem("Set Foreground");
    setFG.addActionListener(this);
    setFG.setMnemonic('f');
    editMenu.add(setFG);
    
    setMG = new JMenuItem("Set Middleground");
    setMG.addActionListener(this);
    setMG.setMnemonic('m');
    editMenu.add(setMG);
    
    setBG = new JMenuItem("Set Background");
    setBG.addActionListener(this);
    setBG.setMnemonic('b');
    editMenu.add(setBG);
    
    setPreview = new JMenuItem("Set Preview");
    setPreview.addActionListener(this);
    setPreview.setMnemonic('p');
    editMenu.add(setPreview);
    
    setIcon = new JMenuItem("Set Icon");
    setIcon.addActionListener(this);
    setIcon.setMnemonic('i');
    editMenu.add(setIcon);
    
    reloadImages = new JMenuItem("Reload Images");
    reloadImages.addActionListener(this);
    reloadImages.setMnemonic('b');
    editMenu.add(reloadImages);
    
    menuBar.add(editMenu);

    setJMenuBar(menuBar);
    
    JPanel actionPane = new JPanel(new FlowLayout());
    showFG = new JButton("+FG");
    showFG.addActionListener(this);    
    actionPane.add(showFG);
    
    showMG = new JButton("+MG");
    showMG.addActionListener(this);    
    actionPane.add(showMG);
    
    showBG = new JButton("+BG");
    showBG.addActionListener(this);    
    actionPane.add(showBG);
    
    showSpawns = new JButton("+Spawn");
    showSpawns.addActionListener(this);    
    actionPane.add(showSpawns);
    
    showPlatforms = new JButton("+Platform");
    showPlatforms.addActionListener(this);    
    actionPane.add(showPlatforms);
    
    showStatics = new JButton("+Static");
    showStatics.addActionListener(this);    
    actionPane.add(showStatics);
    
    JPanel contentPane = new JPanel(new BorderLayout());
    editPane = new EditPane(this);
    
    contentPane.add(editPane, BorderLayout.CENTER);
    contentPane.add(actionPane, BorderLayout.SOUTH);
    
    setContentPane(contentPane);
    setVisible(true);
  }
  
  @Override
  public void actionPerformed(ActionEvent e) {
    Object obj = e.getSource();

    if (obj.equals(showBG)) {
      editPane.showBG = !editPane.showBG;
      showBG.setText((editPane.showBG ? "+" : "-") + "BG");
    }
    
    if (obj.equals(showMG)) {
      editPane.showMG = !editPane.showMG;
      showMG.setText((editPane.showMG ? "+" : "-") + "MG");
    }
    
    if (obj.equals(showFG)) {
      editPane.showFG = !editPane.showFG;
      showFG.setText((editPane.showFG ? "+" : "-") + "FG");
    }
    
    if (obj.equals(showSpawns)) {
      editPane.showSpawns = !editPane.showSpawns;
      showSpawns.setText((editPane.showSpawns ? "+" : "-") + "Spawn");
    }
    
    if (obj.equals(showPlatforms)) {
      editPane.showPlatforms = !editPane.showPlatforms;
      showPlatforms.setText((editPane.showPlatforms ? "+" : "-") + "Platform");
    }
    
    if (obj.equals(showStatics)) {
      editPane.showStatics = !editPane.showStatics;
      showStatics.setText((editPane.showStatics ? "+" : "-") + "Static");
    }
    
    if (obj.equals(setFG)) {
      editPane.foregroundFile = showSelector(true, false);
      editPane.foreground = editPane.loadImageFromFile(editPane.foregroundFile);
    }
    
    if (obj.equals(setBG)) {
      editPane.backgroundFile = showSelector(true, false);
      editPane.background = editPane.loadImageFromFile(editPane.backgroundFile);
    }
    
    if (obj.equals(setMG)) {
      editPane.middlegroundFile = showSelector(true, false);
      editPane.middleground = editPane.loadImageFromFile(editPane.middlegroundFile);
    }
    
    if (obj.equals(setPreview)) {
      editPane.previewFile = showSelector(true, false);
      editPane.preview = editPane.loadImageFromFile(editPane.previewFile);
    }
    
    if (obj.equals(setIcon)) {
      editPane.iconFile = showSelector(true, false);
      editPane.icon = editPane.loadImageFromFile(editPane.iconFile);
    }
    
    if (obj.equals(reloadImages)) {
      editPane.reloadImages();
    }
    

    
    if(obj.equals(openItem)) {
      File loadFile = showSelector(false, false);
      if(loadFile != null) {
        editPane.loadJSON(loadFile);
      }
    }
    
    if(obj.equals(saveItem)) {
      File loadFile = showSelector(false, true);
      boolean shouldOverwrite = false;
      if(loadFile == null)
        return;
      
      if(loadFile.exists())
        shouldOverwrite = JOptionPane.showConfirmDialog(this, "Do you want to overwrite this file?") == JOptionPane.OK_OPTION;
      else
        shouldOverwrite = true;
      
      if(shouldOverwrite)
        editPane.saveJSON(loadFile);
    }
      
  }
  
  /**
   * Lets a user select an image file or a map json for saving/loading
   * @param isImage
   * @return Path of file
   */
  private File showSelector(boolean isImage, boolean saving) {
    
    File path = new File(smeshPath.getAbsolutePath() + 
        (isImage ? "\\public\\res\\img\\map" : "\\public\\res\\map"));
    JFileChooser chooser = new JFileChooser(path);
    chooser.setDialogTitle(isImage ? "Select Image" : "Select Map File");
    chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
    int result;
    if(saving)
      result = chooser.showSaveDialog(null);
    else
      result = chooser.showOpenDialog(null);
    
    if(result == JFileChooser.APPROVE_OPTION)
      return chooser.getSelectedFile();
    return null;
  }

  public static void main(String[] args) {
    JFileChooser chooser = new JFileChooser();
    chooser.setDialogTitle("Select Smesh Folder");
    chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
    File smeshPath;
    /*do {
      chooser.cancelSelection();
      chooser.showOpenDialog(null);
      smeshPath = chooser.getSelectedFile();
      System.out.println("Path " + smeshPath.getAbsolutePath());
    } while(!new File(smeshPath.getAbsolutePath() + "\\app.py").exists());
    */
    smeshPath = new File("C:\\Users\\Isaac\\Desktop\\Smesh");
    
    new Main(smeshPath);
  }
}
