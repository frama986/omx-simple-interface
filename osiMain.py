#!/usr/bin/env python3

from tkinter import Tk
from guiController import OmxGui
import sys

def main():
   root = Tk()
   root.resizable(False,False)
   app = OmxGui(root, sys.argv)
   root.mainloop()

if __name__ == "__main__":
   main()