from data.lang import messageResources as MR
from data.defaultOpt import def_lang

class LangManager():

   language = def_lang
   resources = MR[def_lang]
   
   @classmethod
   def getText(cls, k, default=''):
      msg = cls.resources.get(k)
      if msg is None:
         return default
      return msg
   
def _(k):
   return LangManager.getText(k, k)