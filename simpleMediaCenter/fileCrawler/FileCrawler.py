import os
import logging

class FileCrawler():
    workingDir=''
    dirlist = []
    filelist = []

    def __init__(self,startDirectory='~'):
        self.setWorkingDir(os.path.expanduser(startDirectory))
        
    def getDirList(self):
        return self.dirlist
    
    def getFileList(self):
        return self.filelist
        
    def getWorkingDir(self):
        return self.workingDir

            
        
    def setWorkingDir(self, newWorkingDir):
        if(os.path.isdir(newWorkingDir)):
            self.workingDir = newWorkingDir
            list = os.listdir(self.workingDir)
            self.dirlist = ['..']
            self.filelist = []
            for entry in list:
                testentry = os.path.join(self.workingDir,entry)
                #logging.debug(testentry + " " + str(os.path.isfile(testentry)))
                if(os.path.isfile(testentry)):
                    self.filelist.append(entry)
                else:
                    self.dirlist.append(entry)
        else:
            return False
        return True
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("testing FileCrawler")
    filecrawler = FileCrawler()