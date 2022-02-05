
import os
class File:
  def __init__(self, filename, parent):
    self.filename = filename
    self.parent = parent
    
class Folder:
  def __init__(self, foldername, parent=None):
    self.foldername = foldername
    self.subFolders = []
    self.files = []
    self.parent = parent
    if parent!=None:
      parent.subFolders.append(self)
  
  def newFile(self, file):
      file = File(file, self)
      self.files.append(file)
      return file
  
   
  def mkdir(self, foldername):
    for f in self.subFolders:
      if f.foldername==foldername:
        print("This subfolder already exists!")
        return False
    subFolder = Folder(foldername, self)
    print("New Subfolder created!")
    return subFolder
    
   
  def dir(self):
    print(self.foldername+ ":")
    if self.parent!=None:
      print(" + .." )
    for folder in self.subFolders:
      print(" + " + folder.foldername)
    for file in self.files:
      print(" - " + file.filename)
  
  
  def delete(self,filename):
    for folder in self.subFolders:
      if folder.foldername == filename:
          self.subFolders.remove(folder)
          print(filename + " has been deleted!")
          return True
    #Not a folder could be a file
    for file in self.files:
      if file.filename == filename:
          self.files.remove(file)
          print(filename + " has been deleted!")
          return True
    print("Could not delete file or folder. File or folder not found.")      
    return False
  
    
  def rename(self,filename, newname):
    for folder in self.subFolders:
      if folder.foldername == filename:
          folder.foldername = newname
          print(filename + " has been renamed!")
          return True
    #Not a subfolder could be a file...
    for file in self.files:
      if file.filename == filename:
          file.filename = newname
          print(filename + " has been renamed!")
          return True
    print("Could not rename file or folder. File or folder not found.")      
    return False    

  
     
  def cd(self, foldername):
    if foldername=="..":
      if self.parent==None:
        print("Invalid operation. This is the root folder.")
        return False
      else:
        return self.parent
    for f in self.subFolders:
      if f.foldername==foldername:
        return f
    print("Subfolder does not exist.")
    return False  

# A function to display all acceptable instructions
def help():
  print()
  print(" ----------------- HELP ----------------")
  print("HELP - View list of isntructions.")
  print("CLS - Clear the screen.")
  print("DIR - List files and folders in current folder/directory.")
  print("CD foldername - To navigate to a subfolder.")
  print("CD .. - To navigate to the parent folder.")
  print("MKDIR foldername - To create a subfolder.")
  print("RENAME name newname - To rename a subfolder or a file.")
  print("DEL name - To delete a subfolder or a file.")
  print("EXIT - Quit.")
  print(" ---------------------------------------")
  print()
  
# A function to clear the screen  
def cls():
  os.system('cls' if os.name == "nt" else "clear")

root = Folder("./")
myDocuments = root.mkdir("myDocuments")
myPictures = root.mkdir("myPictures")
myVideos = root.mkdir("myVideos")
maths = myDocuments.mkdir("Maths")
computerscience = myDocuments.mkdir("ComputerScience")
english = myDocuments.mkdir("English")
photos = myPictures.mkdir("Photos")
cartoons = myPictures.mkdir("Cartoons")
file1 = myDocuments.newFile("timetable.doc")
file2 = photos.newFile("sea.jpg")
file3 = photos.newFile("house.jpg")
file4 = photos.newFile("cat.jpg")
file5 = cartoons.newFile("mickey.png")
file6 = cartoons.newFile("bugs-bunny.png")
file7 = english.newFile("essay.doc")
file5 = computerscience.newFile("hello-world.py")
file7 = computerscience.newFile("space-invader.py")
file8 = computerscience.newFile("pacman.py")
file9 = maths.newFile("primary-numbers.txt")
cls()

#Start DOS Emulator!
currentFolder= root
currentFolder.dir()

while True:
  print("Type HELP to view list of instructions...")
  instruction = input("?").split(" ")
  if instruction[0].upper()=="EXIT":
    print("Good bye!")
    break
  
  elif instruction[0].upper()=="HELP":
    help()
    
  elif instruction[0].upper()=="CLS":
    cls()    
    
  elif instruction[0].upper()=="DIR":
    currentFolder.dir()
    
  elif instruction[0].upper()=="DEL":
    if len(instruction)<2:
      print("You must specify a file name or a folder name when using the DEL instruction.")
    else:  
      currentFolder.delete(instruction[1])
  elif instruction[0].upper()=="RENAME":
    if len(instruction)<3:
      print("You must specify a file name or a folder name and a new name when using the DEL instruction.")
    else:  
      currentFolder.rename(instruction[1],instruction[2])      
      
  elif instruction[0].upper()=="CD":
    if len(instruction)<2:
      print("You must specify a folder name when using the CD instruction.")
    else:  
      foldername = instruction[1]
      subFolder = currentFolder.cd(foldername)
      if subFolder!=False:
        currentFolder=subFolder
        print("Current Folder: " + currentFolder.foldername)
        
  elif instruction[0].upper()=="MKDIR":
    if len(instruction)<2:
      print("You must specify a folder name when using the MKDIR instruction.")
    else:  
      foldername = instruction[1]
      currentFolder.mkdir(foldername)    
      
  else:
    print("Invalid Instruction... Type a valid isntruction or HELP for a full list of instructions.")

      