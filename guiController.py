import tkinter.filedialog as fileDialog
from tkinter import Tk, N, S, W, E, StringVar, BooleanVar
from tkinter.ttk import Frame, Button, Style
from subprocess import *

from menuBar import MenuBar
from filesTree import FilesTree
from langManager import _
from data.defaultOpt import *

class OmxGui(Frame):
   
   def __init__(self, parent, argv):
      
      Frame.__init__(self, parent, padding=(3,6,3,12), style="TFrame")
      
      self.parent = parent
      
      self.initData()
      
      self.initUI()
      
      if len(argv) > 1:
         try:
            self.updateAndPlayVideo(argv[1])
         except FileNotFoundError:
            self.logDebug('File Not Found')
      
   def initData(self):
      self.browseInitialDir = def_initialDir
      
      self.recentFile = def_recentFile
      
      self.menuOutputAudio = StringVar()
      self.menuOutputAudio.set(def_menuOutputAudio)
      
      self.menuVideoRefresh = BooleanVar()
      self.menuVideoRefresh.set(def_menuVideoRefresh)
      
      self.menuBgBlack = BooleanVar()
      self.menuBgBlack.set(def_menuBgBlack)
      
      self.maxRecentVideos = def_maxRecentVideos
      
      self.moreOptions = def_moreOptions
      
      self.playProcess = None

   def initUI(self):
      
      self.parent.title('OMX GUI')
      
      self.parent.bind("<Key>", self.keyEvt)
      
      # ---- STYLE ----
      
      Style().theme_use('default')

      Style().configure("TFrame", background="white")
      Style().configure("TButton", font="12", padding=(5,1,5,1), background="#4285F4", foreground="white")
      Style().configure("TEntry", font="12", padding=(5,3,5,2))
      Style().configure("TLabel", background="white")
      Style().map('TButton',
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '!disabled', '#3367d6'), ('active', '#3b78e7')],
                 highlightcolor=[('focus','#4285F4')],
                 relief=[('pressed', '!disabled', 'flat')])
      Style().configure('Treeview', foreground='#333', background="white", highlightthickness='0')
      Style().map('Treeview',
                 foreground=[('focus', '#000')],
                 background=[('focus', '#F5F5F5')])

      # ---- MENU ----
      self.menubar = menubar = MenuBar(self, self.parent)
      
      # ---- TREE ----
      self.filesTree = filesTree = FilesTree(self)
      self.filesTree.loadRecentFile()
      
      # ---- BUTTONS ----
      bBrowse = Button(self, text=_("browse"), width="6", command=self.openVideo)
      bPlay = Button(self, text=_("play"), width="6", command=self.playVideo)
      
      # ---- GRID ----
      self.grid(column=0, row=0, sticky=(N, E, W, S))
      filesTree.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=(N,W,E))
      bBrowse.grid(column=0, row=2, sticky=(N,W))
      bPlay.grid(column=0, row=2, sticky=(N,W), padx=70)
      
      self.parent.columnconfigure(0, weight=1)
      self.parent.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)
      self.columnconfigure(1, weight=1)
      self.rowconfigure(0, weight=1)
      self.rowconfigure(1, weight=1)
      
      self.centerWindow()
      
   def centerWindow(self):
      self.parent.update_idletasks()
      
      w = self.parent.winfo_reqwidth() + 20
      h = self.parent.winfo_reqheight() + 20
      sw = self.parent.winfo_screenwidth()
      sh = self.parent.winfo_screenheight()

      x = (sw - w)/4
      y = (sh - h)/4
      self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))
      self.parent.resizable(False,False)
      self.parent.focus_force()
      self.parent.lift()
   
   def quitProgram(self):
      self.parent.quit()

   def clearRecentVideos(self):
      self.filesTree.clearRecentVideos()

   def updateRecentVideos(self, fullpath):
      self.filesTree.updateRecentVideos(fullpath)

   def updateAndPlayVideo(self, fullpath):
      self.updateRecentVideos(fullpath)
      self.playVideo()

   def openVideo(self):
      fullpath = fileDialog.askopenfilename(
         title=_('open.file')
         ,initialdir=self.browseInitialDir)
      self.updateAndPlayVideo(fullpath)
      
   def playVideo(self):
      lastFile = self.filesTree.getLastFile()
      if lastFile is not None and lastFile['fullpath'] is not '':
         outputAudio = '-o ' + self.menuOutputAudio.get() + ' '
         adjustVideo = '-r ' if self.menuVideoRefresh.get() else ''
         bgBlack = '-b ' if self.menuBgBlack.get() else ''
         moreOptions = self.moreOptions
         fPath = lastFile['fullpath'].replace(' ', '\ ')
         cmdStr = 'omxplayer ' + outputAudio + adjustVideo + bgBlack + moreOptions + fPath
         
         self.logDebug(cmdStr)
         self.playProcess = Popen(['bash', '-c', cmdStr], stdin=PIPE, bufsize = 1)
         self.parent.after(5000, lambda: self.parent.focus_force())
   
   def keyEvt(self, event):
      self.logDebug('char: ' + event.char + ' --- key simbol: ' + event.keysym + ' ---  key code: ' + str(event.keycode))
      #if self.playProcess is not None and self.playProcess.stdin.closed is not True:
      if self.playProcess is not None and self.checkProcessPipe():
         # right
         if event.keysym == 'Right':
            self.playProcess.stdin.write(bytes('^[[C', 'UTF-8'))
         # left
         elif event.keysym == 'Left':
            self.playProcess.stdin.write(bytes('^[[D', 'UTF-8'))
         # up
         elif event.keysym == 'Up':
            self.playProcess.stdin.write(bytes('^[[A', 'UTF-8'))
         # down
         elif event.keysym == 'Down':
            self.playProcess.stdin.write(bytes('^[[B', 'UTF-8'))
         elif event.char == 'x':
            self.playProcess.kill()
            self.playProcess = None
         else:
            self.playProcess.stdin.write(bytes(event.char, 'UTF-8'))
         self.playProcess.stdin.flush()
         self.parent.focus_force()
   
   def checkProcessPipe(self):
      try:
         self.playProcess.stdin.read()
         return True
      except IOError:
         try:
            self.playProcess.stdin.close()
         except IOError:
            pass
      self.playProcess = None
      return False
   
   def logDebug(self, msg):
      if isDebug and msg is not None:
         print(str(msg))