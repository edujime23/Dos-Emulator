import io
import os

class File:
  def __init__(self, filename, parent):
    self.filename = filename
    self.parent = parent
    self.file = io.TextIOWrapper(io.BytesIO(),"utf-8")

  def open(self, mode : str, data):
    
    def read():
      return self.file.read()

    def write(data):
      self.file.write(data)
      self.file.seek(0)
      return None
      
    data = " ".join(data)
    
    if mode.upper()=="R": return read()
    elif mode.upper()=="W": return write(data=data)

    


    

class Folder:
  def __init__(self, foldername, parent=None):
    self.foldername = foldername
    self.subFolders : list[Folder] = []
    self.files : list[File] = []
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
  print("MKFILE filename - To create a file")
  print("RENAME name newname - To rename a subfolder or a file.")
  print("DEL name - To delete a subfolder or a file.")
  print("EXIT - Quit.")
  print("OPEN filename mode - To open a file and write or read data")
  print(" ---------------------------------------")
  print()
  
# A function to clear the screen  
def cls():
  os.system('cls' if os.name == "nt" else "clear")

root = Folder("./")
Documents = root.mkdir("Documents")
cls()
Pictures = root.mkdir("Pictures")
cls()
Videos = root.mkdir("Videos")
cls()
Music = root.mkdir("Music")
cls()


currentFolder= root
currentFolder.dir()

print("-----------------------------")
print("Dos-Emulator")
print("type HELP to see all commands")
print("-----------------------------")

while True:
  instruction = input(f"root@{os.environ.get('USERNAME')}\n$ ").split(" ")
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

  elif instruction[0].upper()=="MKFILE":
    if len(instruction)<2:
         print("You must specify a folder name when using the MKFILE instruction.")
    else:
      filename = instruction[1]
      currentFolder.newFile(filename)

  elif instruction[0].upper()=="OPEN":
    if len(instruction)<2:
      print("You must specify a folder name when using the OPEN instruction.")

    else:
      filename = instruction[1]
      mode = instruction[2]
      other = instruction
      
      for x in range(3):
        del other[0]
      for file in root.files:
        if file.filename == filename:
          output = file.open(mode,other)
          if output is not None:
            print(output)
          
  else:
    print("Invalid Instruction... Type a valid isntruction or HELP for a full list of instructions.")




      