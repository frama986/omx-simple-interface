from tkinter import Menu
from langManager import _

class MenuBar(Menu):
   
   def __init__(self, controller, parent):

      parent.option_add('*tearOff', False)
      
      Menu.__init__(self, parent)
      
      menuFile = Menu(self)
      menuEdit = Menu(self)
      menuAudio = Menu(self)
      menuVideo = Menu(self)
      self.add_cascade(menu=menuFile, label=_('file'))
      self.add_cascade(menu=menuEdit, label=_('edit'))
      self.add_cascade(menu=menuAudio, label=_('audio'))
      self.add_cascade(menu=menuVideo, label=_('video'))
      
      menuFile.add_command(label=_('open'), command=controller.openVideo)
      menuFile.add_command(label=_('quit'), command=controller.quitProgram)
      
      menuEdit.add_command(label=_('clear.file.list'), command=controller.clearRecentVideos)
      
      menuAudio.add_command(label=_('output.audio'), state='disabled')
      menuOutputAudio = controller.menuOutputAudio
      menuAudio.add_radiobutton(label=_('hdmi'), variable=menuOutputAudio, value='hdmi')
      menuAudio.add_radiobutton(label=_('local'), variable=menuOutputAudio, value='local')
      menuAudio.add_radiobutton(label=_('both'), variable=menuOutputAudio, value='both')
      
      menuVideoRefresh = controller.menuVideoRefresh
      menuVideo.add_checkbutton(label=_('adjust.framerate'), variable=menuVideoRefresh, onvalue=True, offvalue=False)
      menuBgBlack = controller.menuBgBlack
      menuVideo.add_checkbutton(label=_('background.black'), variable=menuBgBlack, onvalue=True, offvalue=False)
      
      parent['menu'] = self