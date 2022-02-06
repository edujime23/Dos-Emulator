import io
import os
from asyncio import get_event_loop
from aiohttp import ClientSession, ClientConnectionError
from functools import wraps
from inspect import isasyncgenfunction, iscoroutinefunction

class Cache(object):
    def __init__(self) -> None:
        self.cache = {}
        super().__init__()
    
    
    def add_cache(self, title : str, data):
        assert title is not None
        assert data is not None
        assert title not in self.cache

        self.cache[title] = data

        return None

    def get_cahce(self, Id : str):
        assert Id in self.cache
        data = self.cache[Id]
        return data
    
    def __del__(self):
        self.cache = {}
        del self.cache
        
    


__cache__ = Cache()
        

 

def cache(maxsize=128):
    cache = {}
    
    def decorator(func):
        @wraps(func)
        async def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                if iscoroutinefunction(func) or isasyncgenfunction(func):
                    return await func(*args, **kwargs)
                elif not iscoroutinefunction(func) and not isasyncgenfunction(func):
                    return func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache:
                return cache[key]
            if iscoroutinefunction(func) or isasyncgenfunction(func):
                res = await func(*args, **kwargs)
            elif not iscoroutinefunction(func) and not isasyncgenfunction(func):
                res = func(*args, **kwargs)

            if len(cache) > maxsize:
                del cache[list(cache.keys())[0]]
                cache[key] = res

            __cache__.add_cache(res,key)
               
                
            return res

        return inner

    return decorator

class HTTPSession(ClientSession):
    """ Abstract class for aiohttp. """
    
    def __init__(self, loop=None) -> None:
        super().__init__(loop=loop or get_event_loop())

    def __del__(self) -> None:
        if not self.closed:
            self.loop.run_until_complete(self.close())
            self.loop.close()
 

        return 
       

            

session = HTTPSession()

@cache()
async def query(url, method="get", res_method="text", *args, **kwargs):
    async with getattr(session, method.lower())(url, *args, **kwargs) as res:
        return await getattr(res, res_method)()


async def get(url, *args, **kwargs):
    return await query(url, "get", *args, **kwargs)
 

async def post(url, *args, **kwargs):
    return await query(url, "post", *args, **kwargs)

async def delete(url, *args, **kwargs):
    return await query(url, "delete", *args, **kwargs)

async def patch(url, *args, **kwargs):
    return await query(url, "patch", *args, **kwargs)

async def put(url, *args, **kwargs):
    return await query(url, "put", *args, **kwargs)
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
  print("REQUEST url method res_method - To make a HTTP request")
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

print("-----------------------------")
print("Dos-Emulator")
print("type HELP to see all commands")
print("-----------------------------")

currentFolder= root
currentFolder.dir()

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
          
  elif instruction[0].upper()=="REQUEST":
    url = instruction[1]
    method = instruction[2]
    res_method = instruction[3]
    try:
      if method.upper()=="GET": print(get(url, res_method=res_method))
      elif method.upper()=="PUT": print(put(url, res_method=res_method))
      elif method.upper()=="POST": print(post(url, res_method=res_method))
      elif method.upper()=="DELETE": print(delete(url, res_method=res_method))
      elif method.upper()=="PATCH": print(patch(url, res_method=res_method))
      else: print({"Invalif METHOD": "AVABLE METHODS:GET, PUT, DELETE, POST, PATCH"})
    except:
      raise ClientConnectionError("Can't connect to the url") 
    
  else:
    print("Invalid Instruction... Type a valid isntruction or HELP for a full list of instructions.")
  print("\n")




      