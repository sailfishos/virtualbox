## @file
# Install distribution package.
#
# Copyright (c) 2011, Intel Corporation. All rights reserved.<BR>
#
# This program and the accompanying materials are licensed and made available 
# under the terms and conditions of the BSD License which accompanies this 
# distribution. The full text of the license may be found at 
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#
"""
Install a distribution package
"""
##
# Import Modules
#
import os.path
from os import chmod
from os import SEEK_SET
from os import SEEK_END
import stat
import md5
from sys import stdin
from sys import platform
from shutil import rmtree
from shutil import copyfile
from traceback import format_exc
from platform import python_version

from Logger import StringTable as ST
from Logger.ToolError import UNKNOWN_ERROR
from Logger.ToolError import FILE_UNKNOWN_ERROR
from Logger.ToolError import OPTION_MISSING
from Logger.ToolError import UPT_ALREADY_INSTALLED_ERROR
from Logger.ToolError import FatalError
from Logger.ToolError import ABORT_ERROR
from Logger.ToolError import CODE_ERROR
from Logger.ToolError import FORMAT_INVALID
from Logger.ToolError import FILE_TYPE_MISMATCH
import Logger.Log as Logger

from Library.Misc import CheckEnvVariable
from Library.Misc import Sdict
from Library.Misc import ConvertPath
from Library.ParserValidate import IsValidInstallPath
from Xml.XmlParser import DistributionPackageXml
from GenMetaFile.GenDecFile import PackageToDec
from GenMetaFile.GenInfFile import ModuleToInf
from Core.PackageFile import PackageFile
from Core.PackageFile import FILE_NOT_FOUND
from Core.PackageFile import FILE_CHECKSUM_FAILURE
from Core.PackageFile import CreateDirectory
from Core.DependencyRules import DependencyRules
from Library import GlobalData

## InstallNewPackage
#
# @param WorkspaceDir:   Workspace Directory
# @param Path:           Package Path
# @param CustomPath:     whether need to customize path at first
#
def InstallNewPackage(WorkspaceDir, Path, CustomPath = False):
    if os.path.isabs(Path):
        Logger.Info(ST.MSG_RELATIVE_PATH_ONLY%Path)
    elif CustomPath:
        Logger.Info(ST.MSG_NEW_PKG_PATH)
    else:
        Path = ConvertPath(Path)
        Path = os.path.normpath(Path)
        FullPath = os.path.normpath(os.path.join(WorkspaceDir, Path))
        if os.path.exists(FullPath):
            Logger.Info(ST.ERR_DIR_ALREADY_EXIST%FullPath)
        else:
            return Path

    Input = stdin.readline()
    Input = Input.replace('\r', '').replace('\n', '')
    if Input == '':
        Logger.Error("InstallPkg", UNKNOWN_ERROR, ST.ERR_USER_INTERRUPT)
    Input = Input.replace('\r', '').replace('\n', '')
    return InstallNewPackage(WorkspaceDir, Input, False)


## InstallNewModule
#
# @param WorkspaceDir:   Workspace Directory
# @param Path:           Standalone Module Path
# @param PathList:       The already installed standalone module Path list
#
def InstallNewModule(WorkspaceDir, Path, PathList = None):
    if PathList == None:
        PathList = []
    Path = ConvertPath(Path)
    Path = os.path.normpath(Path)
    FullPath = os.path.normpath(os.path.join(WorkspaceDir, Path))
    if os.path.exists(FullPath) and FullPath not in PathList:
        Logger.Info(ST.ERR_DIR_ALREADY_EXIST%Path)
    elif Path == FullPath:
        Logger.Info(ST.MSG_RELATIVE_PATH_ONLY%FullPath)
    else:
        return Path
    
    Input = stdin.readline()
    Input = Input.replace('\r', '').replace('\n', '')
    if Input == '':
        Logger.Error("InstallPkg", UNKNOWN_ERROR, ST.ERR_USER_INTERRUPT)
    Input = Input.replace('\r', '').replace('\n', '')
    return InstallNewModule(WorkspaceDir, Input, PathList)

    
## InstallNewFile
#
# @param WorkspaceDir:   Workspace Direction
# @param File:      File
#
def InstallNewFile(WorkspaceDir, File):
    FullPath = os.path.normpath(os.path.join(WorkspaceDir, File))
    if os.path.exists(FullPath):
        Logger.Info(ST.ERR_FILE_ALREADY_EXIST %File)
        Input = stdin.readline()
        Input = Input.replace('\r', '').replace('\n', '')
        if Input == '':
            Logger.Error("InstallPkg", UNKNOWN_ERROR, ST.ERR_USER_INTERRUPT)
        Input = Input.replace('\r', '').replace('\n', '')
        return InstallNewFile(WorkspaceDir, Input)
    else:
        return File

## UnZipDp
#
# UnZipDp
#
def UnZipDp(WorkspaceDir, Options, DataBase):
    ContentZipFile = None
    Logger.Quiet(ST.MSG_UZIP_PARSE_XML)
    DpPkgFileName = Options.PackageFile
    DistFile = PackageFile(DpPkgFileName)
    
    DpDescFileName, ContentFileName = GetDPFile(DistFile.GetZipFile())
    
    GlobalData.gUNPACK_DIR = os.path.normpath(os.path.join(WorkspaceDir, ".tmp"))
    DistPkgFile = DistFile.UnpackFile(DpDescFileName,
        os.path.normpath(os.path.join(GlobalData.gUNPACK_DIR, DpDescFileName)))
    if not DistPkgFile:
        Logger.Error("InstallPkg", FILE_NOT_FOUND, ST.ERR_FILE_BROKEN %DpDescFileName)
    
    #
    # Generate distpkg
    #
    DistPkgObj = DistributionPackageXml()
    DistPkg = DistPkgObj.FromXml(DistPkgFile)
    if DistPkg.Header.RePackage == '':
        DistPkg.Header.RePackage = False
    if DistPkg.Header.ReadOnly == '':
        DistPkg.Header.ReadOnly = False
    
    #
    # prepare check dependency
    #
    Dep = DependencyRules(DataBase)
    #
    # Check distribution package installed or not
    #
    if Dep.CheckDpExists(DistPkg.Header.GetGuid(),
        DistPkg.Header.GetVersion()):
        Logger.Error("InstallPkg", UPT_ALREADY_INSTALLED_ERROR,
            ST.WRN_DIST_PKG_INSTALLED)
    #
    # Check distribution dependency (all module dependency should be
    # satisfied)
    #
    if not Dep.CheckDpDepexSatisfied(DistPkg):
        Logger.Error("InstallPkg", UNKNOWN_ERROR,
            ST.ERR_PACKAGE_NOT_MATCH_DEPENDENCY,
            ExtraData=DistPkg.Header.Name)
    #
    # unzip contents.zip file
    #
    ContentFile = DistFile.UnpackFile(ContentFileName,
        os.path.normpath(os.path.join(GlobalData.gUNPACK_DIR, ContentFileName)))
    if not ContentFile:
        Logger.Error("InstallPkg", FILE_NOT_FOUND,
            ST.ERR_FILE_BROKEN % ContentFileName)

    FilePointer = open(ContentFile, "rb")
    #
    # Assume no archive comment.
    #
    FilePointer.seek(0, SEEK_SET)
    FilePointer.seek(0, SEEK_END)
    #
    # Get file size
    #                
    FileSize = FilePointer.tell()
    FilePointer.close()
               
    if FileSize != 0:        
        ContentZipFile = PackageFile(ContentFile)

    #
    # verify MD5 signature when existed
    #
    if DistPkg.Header.Signature != '':
        Md5Sigature = md5.new(open(ContentFile, 'rb').read())
        if DistPkg.Header.Signature != Md5Sigature.hexdigest():
            ContentZipFile.Close()
            Logger.Error("InstallPkg", FILE_CHECKSUM_FAILURE,
                ExtraData=ContentFile)

    return DistPkg, Dep, ContentZipFile, DpPkgFileName

## GetPackageList
#
# GetPackageList
#
def GetPackageList(DistPkg, Dep, WorkspaceDir, Options, ContentZipFile, ModuleList, PackageList):
    NewDict = Sdict()
    for Guid, Version, Path in DistPkg.PackageSurfaceArea:
        PackagePath = Path
        Package = DistPkg.PackageSurfaceArea[Guid, Version, Path]
        Logger.Info(ST.MSG_INSTALL_PACKAGE % Package.GetName())
        if Dep.CheckPackageExists(Guid, Version):
            Logger.Info(ST.WRN_PACKAGE_EXISTED %(Guid, Version))
        NewPackagePath = InstallNewPackage(WorkspaceDir, PackagePath, Options.CustomPath)
        InstallPackageContent(PackagePath, NewPackagePath, Package, ContentZipFile, Dep, WorkspaceDir, ModuleList, 
                              DistPkg.Header.ReadOnly)
        PackageList.append(Package)
        
        NewDict[Guid, Version, Package.GetPackagePath()] = Package
    
    #
    # Now generate meta-data files, first generate all dec for package
    # dec should be generated before inf, and inf should be generated after
    # all packages installed, else hard to resolve modules' package
    # dependency (Hard to get the location of the newly installed package)
    #
    for Package in PackageList:
        FilePath = PackageToDec(Package)
        Md5Sigature = md5.new(open(str(FilePath), 'rb').read())
        Md5Sum = Md5Sigature.hexdigest()
        if (FilePath, Md5Sum) not in Package.FileList:
            Package.FileList.append((FilePath, Md5Sum))
    
    return NewDict

## GetModuleList
#
# GetModuleList
#
def GetModuleList(DistPkg, Dep, WorkspaceDir, ContentZipFile, ModuleList):
    #
    # ModulePathList will keep track of the standalone module path that
    # we just installed. If a new module's path in that list 
    # (only multiple INF in one directory will be so), we will 
    # install them directly. If not, we will try to create a new directory 
    # for it.
    #
    ModulePathList = []   
    
    #
    # Check module exist and install
    #
    Module = None
    NewDict = Sdict()        
    for Guid, Version, Name, Path in DistPkg.ModuleSurfaceArea:
        ModulePath = Path
        Module = DistPkg.ModuleSurfaceArea[Guid, Version, Name, Path]
        Logger.Info(ST.MSG_INSTALL_MODULE % Module.GetName())
        if Dep.CheckModuleExists(Guid, Version, Name, Path):
            Logger.Quiet(ST.WRN_MODULE_EXISTED %Path)
        #
        # here check for the multiple inf share the same module path cases:
        # they should be installed into the same directory
        #
        ModuleFullPath = \
        os.path.normpath(os.path.join(WorkspaceDir, ModulePath))
        if ModuleFullPath not in ModulePathList:
            NewModulePath = InstallNewModule(WorkspaceDir, ModulePath, ModulePathList)
            NewModuleFullPath = os.path.normpath(os.path.join(WorkspaceDir, NewModulePath))
            ModulePathList.append(NewModuleFullPath)
        else:
            NewModulePath = ModulePath
        
        InstallModuleContent(ModulePath, NewModulePath, '', Module, ContentZipFile, WorkspaceDir, ModuleList, None, 
                             DistPkg.Header.ReadOnly)
        #
        # Update module
        #
        Module.SetModulePath(Module.GetModulePath().replace(Path, NewModulePath, 1))
        
        NewDict[Guid, Version, Name, Module.GetModulePath()] = Module

    #
    # generate all inf for modules
    #
    for (Module, Package) in ModuleList:
        FilePath = ModuleToInf(Module)
        Md5Sigature = md5.new(open(str(FilePath), 'rb').read())
        Md5Sum = Md5Sigature.hexdigest()
        if Package:
            if (FilePath, Md5Sum) not in Package.FileList:
                Package.FileList.append((FilePath, Md5Sum))
        else:
            if (FilePath, Md5Sum) not in Module.FileList:
                Module.FileList.append((FilePath, Md5Sum))
    
    return NewDict

## GenToolMisc
#
# GenToolMisc
#
#
def GenToolMisc(DistPkg, WorkspaceDir, ContentZipFile):
    ToolObject = DistPkg.Tools
    MiscObject = DistPkg.MiscellaneousFiles
    DistPkg.FileList = []
    FileList = []
    ToolFileNum = 0
    FileNum = 0
    RootDir = WorkspaceDir
    
    #
    # FileList stores both tools files and misc files
    # Misc file list must be appended to FileList *AFTER* Tools file list
    #
    if ToolObject:
        FileList += ToolObject.GetFileList()
        ToolFileNum = len(ToolObject.GetFileList())
        if 'EDK_TOOLS_PATH' in os.environ:
            RootDir = os.environ['EDK_TOOLS_PATH']
    if MiscObject:
        FileList += MiscObject.GetFileList()
    for FileObject in FileList:
        FileNum += 1
        if FileNum > ToolFileNum:
            #
            # Misc files, root should be changed to WORKSPACE
            #
            RootDir = WorkspaceDir
        File = ConvertPath(FileObject.GetURI())
        ToFile = os.path.normpath(os.path.join(RootDir, File))
        if os.path.exists(ToFile):
            Logger.Info( ST.WRN_FILE_EXISTED % ToFile )
            #
            # ask for user input the new file name
            #
            Logger.Info( ST.MSG_NEW_FILE_NAME)
            Input = stdin.readline()
            Input = Input.replace('\r', '').replace('\n', '')
            OrigPath = os.path.split(ToFile)[0]
            ToFile = os.path.normpath(os.path.join(OrigPath, Input))
        FromFile = os.path.join(FileObject.GetURI())
        Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, DistPkg.Header.ReadOnly, FileObject.GetExecutable())
        DistPkg.FileList.append((ToFile, Md5Sum))

## Tool entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
# @param  Options: command Options
#
def Main(Options = None):
    ContentZipFile, DistFile = None, None

    try:
        DataBase = GlobalData.gDB        
        CheckEnvVariable()
        WorkspaceDir = GlobalData.gWORKSPACE
        if not Options.PackageFile:
            Logger.Error("InstallPkg", OPTION_MISSING, ExtraData=ST.ERR_SPECIFY_PACKAGE)
        
        #
        # unzip dist.pkg file
        #
        DistPkg, Dep, ContentZipFile, DpPkgFileName = UnZipDp(WorkspaceDir, Options, DataBase)

        #
        # PackageList, ModuleList record the information for the meta-data
        # files that need to be generated later
        #
        PackageList = []
        ModuleList = []
        DistPkg.PackageSurfaceArea = GetPackageList(DistPkg, Dep, WorkspaceDir, Options, 
                                                    ContentZipFile, ModuleList, PackageList)

        DistPkg.ModuleSurfaceArea = GetModuleList(DistPkg, Dep, WorkspaceDir, ContentZipFile, ModuleList)       
        
        
        GenToolMisc(DistPkg, WorkspaceDir, ContentZipFile)
        
        #
        # copy "Distribution File" to directory $(WORKSPACE)/conf/upt
        #
        DistFileName = os.path.split(DpPkgFileName)[1]
        DestDir = os.path.normpath(os.path.join(WorkspaceDir, GlobalData.gUPT_DIR))
        CreateDirectory(DestDir)
        DestFile = os.path.normpath(os.path.join(DestDir, DistFileName))
        if os.path.exists(DestFile):
            FileName, Ext = os.path.splitext(DistFileName)
            NewFileName = FileName + '_' + DistPkg.Header.GetGuid() + '_' + DistPkg.Header.GetVersion() + Ext
            DestFile = os.path.normpath(os.path.join(DestDir, NewFileName))
            if os.path.exists(DestFile):
                #
                # ask for user input the new file name
                #
                Logger.Info( ST.MSG_NEW_FILE_NAME_FOR_DIST)
                Input = stdin.readline()
                Input = Input.replace('\r', '').replace('\n', '')
                DestFile = os.path.normpath(os.path.join(DestDir, Input))
        copyfile(DpPkgFileName, DestFile)
        NewDpPkgFileName = DestFile[DestFile.find(DestDir) + len(DestDir) + 1:]

        #
        # update database
        #
        Logger.Quiet(ST.MSG_UPDATE_PACKAGE_DATABASE)
        DataBase.AddDPObject(DistPkg, NewDpPkgFileName, DistFileName, 
                       DistPkg.Header.RePackage)
        
        ReturnCode = 0
        
    except FatalError, XExcept:
        ReturnCode = XExcept.args[0]
        if Logger.GetLevel() <= Logger.DEBUG_9:
            Logger.Quiet(ST.MSG_PYTHON_ON % (python_version(),
                platform) + format_exc())
    except KeyboardInterrupt:
        ReturnCode = ABORT_ERROR
        if Logger.GetLevel() <= Logger.DEBUG_9:
            Logger.Quiet(ST.MSG_PYTHON_ON % (python_version(),
                platform) + format_exc())
    except:
        ReturnCode = CODE_ERROR
        Logger.Error(
                    "\nInstallPkg",
                    CODE_ERROR,
                    ST.ERR_UNKNOWN_FATAL_INSTALL_ERR % Options.PackageFile,
                    ExtraData=ST.MSG_SEARCH_FOR_HELP,
                    RaiseError=False
                    )
        Logger.Quiet(ST.MSG_PYTHON_ON % (python_version(),
            platform) + format_exc())

    finally:
        Logger.Quiet(ST.MSG_REMOVE_TEMP_FILE_STARTED)
        if DistFile:
            DistFile.Close()
        if ContentZipFile:
            ContentZipFile.Close()
        if GlobalData.gUNPACK_DIR:
            rmtree(GlobalData.gUNPACK_DIR)
            GlobalData.gUNPACK_DIR = None
        Logger.Quiet(ST.MSG_REMOVE_TEMP_FILE_DONE)

    if ReturnCode == 0:
        Logger.Quiet(ST.MSG_FINISH)
    
    return ReturnCode

## InstallModuleContent method
#
# If this is standalone module, then Package should be none,
# ModulePath should be ''
#   @param  FromPath: FromPath
#   @param  NewPath: NewPath
#   @param  ModulePath: ModulePath
#   @param  Module: Module
#   @param  ContentZipFile: ContentZipFile
#   @param  WorkspaceDir: WorkspaceDir
#   @param  ModuleList: ModuleList
#   @param  Package: Package
#
def InstallModuleContent(FromPath, NewPath, ModulePath, Module, ContentZipFile,
    WorkspaceDir, ModuleList, Package = None, ReadOnly = False):
    
    if NewPath.startswith("\\") or NewPath.startswith("/"):
        NewPath = NewPath[1:]
    
    if not IsValidInstallPath(NewPath):
        Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%NewPath) 
           
    NewModuleFullPath = os.path.normpath(os.path.join(WorkspaceDir, NewPath,
        ConvertPath(ModulePath)))
    Module.SetFullPath(os.path.normpath(os.path.join(NewModuleFullPath,
        ConvertPath(Module.GetName()) + '.inf')))
    Module.FileList = []
    
    for MiscFile in Module.GetMiscFileList():
        if not MiscFile:
            continue
        for Item in MiscFile.GetFileList():
            File = Item.GetURI()
            if File.startswith("\\") or File.startswith("/"):
                File = File[1:]
            
            if not IsValidInstallPath(File):
                Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%File)
                      
            FromFile = os.path.join(FromPath, ModulePath, File)
            Executable = Item.GetExecutable()            
            ToFile = os.path.normpath(os.path.join(NewModuleFullPath, ConvertPath(File)))
            Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly, Executable)
            if Package and ((ToFile, Md5Sum) not in Package.FileList):
                Package.FileList.append((ToFile, Md5Sum))
            elif Package:
                continue
            elif (ToFile, Md5Sum) not in Module.FileList:
                Module.FileList.append((ToFile, Md5Sum))
    for Item in Module.GetSourceFileList():
        File = Item.GetSourceFile()
        if File.startswith("\\") or File.startswith("/"):
            File = File[1:]
            
        if not IsValidInstallPath(File):
            Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%File) 
                               
        FromFile = os.path.join(FromPath, ModulePath, File)
        ToFile = os.path.normpath(os.path.join(NewModuleFullPath, ConvertPath(File)))
        Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly)
        if Package and ((ToFile, Md5Sum) not in Package.FileList):
            Package.FileList.append((ToFile, Md5Sum))
        elif Package:
            continue
        elif (ToFile, Md5Sum) not in Module.FileList:
            Module.FileList.append((ToFile, Md5Sum))
    for Item in Module.GetBinaryFileList():
        FileNameList = Item.GetFileNameList()
        for FileName in FileNameList:              
            File = FileName.GetFilename()          
            if File.startswith("\\") or File.startswith("/"):
                File = File[1:]
                
            if not IsValidInstallPath(File):
                Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%File)

            FromFile = os.path.join(FromPath, ModulePath, File)
            ToFile = os.path.normpath(os.path.join(NewModuleFullPath, ConvertPath(File)))
            Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly)       
            if Package and ((ToFile, Md5Sum) not in Package.FileList):
                Package.FileList.append((ToFile, Md5Sum))
            elif Package:
                continue
            elif (ToFile, Md5Sum) not in Module.FileList:
                Module.FileList.append((ToFile, Md5Sum))
    
    InstallModuleContentZipFile(ContentZipFile, FromPath, ModulePath, WorkspaceDir, NewPath, Module, Package, ReadOnly,
                                ModuleList)

## InstallModuleContentZipFile
#
# InstallModuleContentZipFile
#
def InstallModuleContentZipFile(ContentZipFile, FromPath, ModulePath, WorkspaceDir, NewPath, Module, Package, ReadOnly,
                                ModuleList):
    #
    # Extract other files under current module path in content Zip file but not listed in the description 
    #
    if ContentZipFile:
        for FileName in ContentZipFile.GetZipFile().namelist():
            FileName = os.path.normpath(FileName)
            CheckPath = os.path.normpath(os.path.join(FromPath, ModulePath))
            if FileUnderPath(FileName, CheckPath):
                if FileName.startswith("\\") or FileName.startswith("/"):
                    FileName = FileName[1:]
                    
                if not IsValidInstallPath(FileName):
                    Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%FileName)
                                                   
                FromFile = FileName
                ToFile = os.path.normpath(os.path.join(WorkspaceDir, 
                        ConvertPath(FileName.replace(FromPath, NewPath, 1))))
                CheckList = Module.FileList
                if Package:
                    CheckList += Package.FileList
                for Item in CheckList:
                    if Item[0] == ToFile:
                        break
                else:
                    Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly)
                    if Package and ((ToFile, Md5Sum) not in Package.FileList):
                        Package.FileList.append((ToFile, Md5Sum))
                    elif Package:
                        continue
                    elif (ToFile, Md5Sum) not in Module.FileList:
                        Module.FileList.append((ToFile, Md5Sum))            
    
    ModuleList.append((Module, Package))

## FileUnderPath
#  Check whether FileName started with directory specified by CheckPath 
#
# @param FileName: the FileName need to be checked
# @param CheckPath: the path need to be checked against
# @return:  True or False  
#
def FileUnderPath(FileName, CheckPath):
    FileName = FileName.replace('\\', '/')
    FileName = os.path.normpath(FileName)
    CheckPath = CheckPath.replace('\\', '/')
    CheckPath = os.path.normpath(CheckPath)
    if FileName.startswith(CheckPath):
        RemainingPath = os.path.normpath(FileName.replace(CheckPath, '', 1))
        while RemainingPath.startswith('\\') or RemainingPath.startswith('/'):
            RemainingPath = RemainingPath[1:]
        if FileName == os.path.normpath(os.path.join(CheckPath, RemainingPath)):
            return True
    
    return False

## InstallFile
#  Extract File from Zipfile, set file attribute, and return the Md5Sum
#
# @return:  True or False  
#
def InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly, Executable=False):
    if not ContentZipFile or not ContentZipFile.UnpackFile(FromFile, ToFile):
        Logger.Error("UPT", FILE_NOT_FOUND, ST.ERR_INSTALL_FILE_FROM_EMPTY_CONTENT%FromFile)

    if ReadOnly:
        if not Executable:
            chmod(ToFile, stat.S_IREAD)
        else:
            chmod(ToFile, stat.S_IREAD|stat.S_IEXEC)
    elif Executable:
        chmod(ToFile, stat.S_IREAD|stat.S_IWRITE|stat.S_IEXEC)
    else:
        chmod(ToFile, stat.S_IREAD|stat.S_IWRITE)
                
    Md5Sigature = md5.new(open(str(ToFile), 'rb').read())
    Md5Sum = Md5Sigature.hexdigest()
    return Md5Sum
        
## InstallPackageContent method
#
#   @param  FromPath: FromPath
#   @param  ToPath: ToPath
#   @param  Package: Package
#   @param  ContentZipFile: ContentZipFile
#   @param  Dep: Dep
#   @param  WorkspaceDir: WorkspaceDir
#   @param  ModuleList: ModuleList
#
def InstallPackageContent(FromPath, ToPath, Package, ContentZipFile, Dep,
    WorkspaceDir, ModuleList, ReadOnly = False):
    if Dep:
        pass
    Package.FileList = []
    
    if ToPath.startswith("\\") or ToPath.startswith("/"):
        ToPath = ToPath[1:]
    
    if not IsValidInstallPath(ToPath):
        Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%ToPath)     

    if FromPath.startswith("\\") or FromPath.startswith("/"):
        FromPath = FromPath[1:]
    
    if not IsValidInstallPath(FromPath):
        Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%FromPath)   
    
    PackageFullPath = os.path.normpath(os.path.join(WorkspaceDir, ToPath))
    for MiscFile in Package.GetMiscFileList():
        for Item in MiscFile.GetFileList():
            FileName = Item.GetURI()
            if FileName.startswith("\\") or FileName.startswith("/"):
                FileName = FileName[1:]
                
            if not IsValidInstallPath(FileName):
                Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%FileName)
                            
            FromFile = os.path.join(FromPath, FileName)
            Executable = Item.GetExecutable()
            ToFile =  (os.path.join(PackageFullPath, ConvertPath(FileName)))
            Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly, Executable)
            if (ToFile, Md5Sum) not in Package.FileList:
                Package.FileList.append((ToFile, Md5Sum))
    PackageIncludeArchList = [] 
    for Item in Package.GetPackageIncludeFileList():
        FileName = Item.GetFilePath()
        if FileName.startswith("\\") or FileName.startswith("/"):
            FileName = FileName[1:]
            
        if not IsValidInstallPath(FileName):
            Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%FileName) 
                   
        FromFile = os.path.join(FromPath, FileName)
        ToFile = os.path.normpath(os.path.join(PackageFullPath, ConvertPath(FileName)))
        RetFile = ContentZipFile.UnpackFile(FromFile, ToFile)
        if RetFile == '':
            #
            # a non-exist path in Zipfile will return '', which means an include directory in our case
            # save the information for later DEC creation usage and also create the directory
            #
            PackageIncludeArchList.append([Item.GetFilePath(), Item.GetSupArchList()])
            CreateDirectory(ToFile)
            continue
        if ReadOnly:
            chmod(ToFile, stat.S_IREAD)
        else:
            chmod(ToFile, stat.S_IREAD|stat.S_IWRITE)            
        Md5Sigature = md5.new(open(str(ToFile), 'rb').read())
        Md5Sum = Md5Sigature.hexdigest()
        if (ToFile, Md5Sum) not in Package.FileList:
            Package.FileList.append((ToFile, Md5Sum))
    Package.SetIncludeArchList(PackageIncludeArchList)
    
    for Item in Package.GetStandardIncludeFileList():
        FileName = Item.GetFilePath()
        if FileName.startswith("\\") or FileName.startswith("/"):
            FileName = FileName[1:]
            
        if not IsValidInstallPath(FileName):
            Logger.Error("UPT", FORMAT_INVALID, ST.ERR_FILE_NAME_INVALIDE%FileName) 
                    
        FromFile = os.path.join(FromPath, FileName)
        ToFile = os.path.normpath(os.path.join(PackageFullPath, ConvertPath(FileName)))
        Md5Sum = InstallFile(ContentZipFile, FromFile, ToFile, ReadOnly)
        if (ToFile, Md5Sum) not in Package.FileList:
            Package.FileList.append((ToFile, Md5Sum))

    #
    # Update package
    #
    Package.SetPackagePath(Package.GetPackagePath().replace(FromPath,
        ToPath, 1))
    Package.SetFullPath(os.path.normpath(os.path.join(PackageFullPath,
        ConvertPath(Package.GetName()) + '.dec')))

    #
    # Install files in module
    #
    Module = None
    ModuleDict = Package.GetModuleDict()
    for ModuleGuid, ModuleVersion, ModuleName, ModulePath in ModuleDict:
        Module = ModuleDict[ModuleGuid, ModuleVersion, ModuleName, ModulePath]
        InstallModuleContent(FromPath, ToPath, ModulePath, Module,
            ContentZipFile, WorkspaceDir, ModuleList, Package, ReadOnly)

## GetDPFile method
#
#   @param  ZipFile: A ZipFile
#
def GetDPFile(ZipFile):
    ContentFile = ''
    DescFile = ''
    for FileName in ZipFile.namelist():
        if FileName.endswith('.content'):
            if not ContentFile:
                ContentFile = FileName
                continue
        elif FileName.endswith('.pkg'):
            if not DescFile:
                DescFile = FileName
                continue
        else:
            continue
        
        Logger.Error("PackagingTool", FILE_TYPE_MISMATCH,
            ExtraData=ST.ERR_DIST_FILE_TOOMANY)
    if not DescFile or not ContentFile:
        Logger.Error("PackagingTool", FILE_UNKNOWN_ERROR,
            ExtraData=ST.ERR_DIST_FILE_TOOFEW)
    return DescFile, ContentFile

