from tkinter.ttk import Treeview
from xml.etree.ElementTree import Element
from datetime import datetime
import os.path as pathMod
import xml.etree.ElementTree as ET

class FilesTree(Treeview):

   def __init__(self, controller):
      Treeview.__init__(self, controller)
      
      self.controller = controller
      self.recentFile = controller.recentFile
      self.browseInitialDir = controller.browseInitialDir
      self.maxRecentVideos = controller.maxRecentVideos
      
      self.initLastFile()
      
      self['height'] = 10
      self['selectmode'] = 'browse'
      self['columns'] = ('lastOpen')
      self.column('#0', width=350, anchor='center')
      self.heading('#0', text='File')
      self.column('lastOpen', width=100, anchor='center')
      self.heading('lastOpen', text='Last play')
      
      self.bind("<Double-1>", self.playSelectedVideo)
      self.bind("<ButtonRelease-1>", self.selectVideo)

   def _addFile(self, id, title, lastOpen):
      self.insert('', 0, id, text=title, values=(lastOpen))

   def _clearVideos(self):
      items = self.get_children()
      for item in items:
         self.delete(item)

   def _deleteVideo(self, nth):
      items = self.get_children()
      self.delete(items[nth])

   def _existRecentFile(self):
      if not pathMod.isfile(self.recentFile):
         with open(self.recentFile, 'w') as recentVideosFile:
            recentVideosFile.write('<data></data>')
   
   def loadRecentFile(self):
      self._existRecentFile()
      self.recentVideos = recentVideos = ET.parse(self.recentFile)
      self.recentVideosRoot = recentVideosRoot = recentVideos.getroot()
      filepath = self.browseInitialDir
      for video in recentVideosRoot.findall('film'):
         title = video.findtext('filename')
         lastOpen = video.findtext('lastopen')
         videoId = video.findtext('id')
         filepath = video.findtext('filepath')
         self._addFile(videoId, title, lastOpen)
      
      self.browseInitialDir = filepath
      
      video = recentVideosRoot.find('./film[last()]')
      lastFile = self.lastFile
      if video is not None:
         lastFile['id'] = video.findtext('id')
         lastFile['fullpath'] = video.findtext('fullpath')
         lastFile['filepath'] = video.findtext('filepath')
         lastFile['filename'] = video.findtext('filename')
         lastFile['lastopen'] = video.findtext('lastopen')

   def clearRecentVideos(self):
      for video in self.recentVideosRoot.findall('film'):
         self.recentVideosRoot.remove(video)
         self.recentVideos.write(self.recentFile)
      
      self._clearVideos()
         
      self.initLastFile()
   
   def clearNthFile(self, nth):
      videos = self.recentVideosRoot.findall('film')
      self.recentVideosRoot.remove(videos[len(videos)-nth-1])
      self.recentVideos.write(self.recentFile)
      
      self._deleteVideo(nth)

   def initLastFile(self):
      self.lastFile = {
         'id': '','fullpath': '','filepath': '','filename': '','lastopen': ''}
      return self.lastFile

   def getLastFile(self):
      return self.lastFile

   def _checkMaxRecent(self):
      videos = self.recentVideosRoot.findall('film')
      currentSize = len(videos)
      
      if currentSize >= self.maxRecentVideos:
         self.clearNthFile(self.maxRecentVideos-1)
   
   def updateRecentVideos(self, fullpath):
      if fullpath is not None and fullpath is not '':
         
         self._checkMaxRecent()
         
         td = datetime.today()
         lastFile = self.initLastFile()
         lastFile['id'] = td.timestamp()
         lastFile['fullpath'] = fullpath
         lastFile['filepath'] = pathMod.dirname(fullpath)
         lastFile['filename'] = pathMod.basename(fullpath)
         lastFile['lastopen'] = td.strftime('%d/%m/%Y')
         self._addFile(lastFile['id'], lastFile['filename'], lastFile['lastopen'])

         lastElement = Element('film')
         ET.SubElement(lastElement, 'id').text = str(lastFile['id'])
         ET.SubElement(lastElement, 'fullpath').text = lastFile['fullpath']
         ET.SubElement(lastElement, 'filepath').text = lastFile['filepath']
         ET.SubElement(lastElement, 'filename').text = lastFile['filename']
         ET.SubElement(lastElement, 'lastopen').text = lastFile['lastopen']
         self.recentVideosRoot.append(lastElement)

         self.recentVideos.write(self.recentFile)
         
         self.browseInitialDir = lastFile['filepath']

   def selectVideo(self, event):
      videoId = self.identify_row(event.y)
      if videoId is not '':
         video = self.recentVideosRoot.find("./film[id='"+videoId+"']")
         if video is not None:
            lastFile = self.initLastFile()
            lastFile['id'] = video.findtext('id')
            lastFile['fullpath'] = video.findtext('fullpath')
            lastFile['filepath'] = video.findtext('filepath')
            lastFile['filename'] = video.findtext('filename')
            lastFile['lastopen'] = video.findtext('lastopen')

   def playSelectedVideo(self, event):
      videoId = self.identify_row(event.y)
      if videoId is not '':
         self.controller.playVideo()

   def getSelectedVideoId(self):
      if len(self.selection()) > 0:
         video = self.selection()[0]
         y = self.index(video)