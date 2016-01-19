import xml.etree.ElementTree as ET

class RecentVideos():

   def __init__(self, controller, path):
      self.filePath = path
      self.controller = controller

   def existRecentFile(self):
      if not pathMod.isfile(self.filePath):
         with open(self.filePath, 'w') as recentVideosFile:
            recentVideosFile.write('<data></data>')
      
   def loadRecentFile(self, filesTree):
      self.existRecentFile()
      self.recentVideos = recentVideos = ET.parse(self.filePath)
      self.recentVideosRoot = recentVideosRoot = recentVideos.getroot()
      filepath = self.controller.browseInitialDir
      for video in recentVideosRoot.findall('film'):
         title = video.findtext('filename')
         lastOpen = video.findtext('lastopen')
         videoId = video.findtext('id')
         filepath = video.findtext('filepath')
         filesTree.addFile(videoId, title, lastOpen)
      
	  self.filePath = filepath
      self.controller.browseInitialDir = filepath
      
      video = recentVideosRoot.find('./film[last()]')
      lastFile = self.lastFile
      if video is not None:
         lastFile['id'] = video.findtext('id')
         lastFile['fullpath'] = video.findtext('fullpath')
         lastFile['filepath'] = video.findtext('filepath')
         lastFile['filename'] = video.findtext('filename')
         lastFile['lastopen'] = video.findtext('lastopen')