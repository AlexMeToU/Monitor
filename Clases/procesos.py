import sys, os.path, ctypes, ctypes.wintypes
'''
Created on 10/02/2014

@author: Admin
'''

class Procesos():
    def __init__(self):
        self.Psapi = ctypes.WinDLL('Psapi.dll')
        self.EnumProcesses = self.Psapi.EnumProcesses
        self.EnumProcesses.restype = ctypes.wintypes.BOOL
        self.GetProcessImageFileName = self.Psapi.GetProcessImageFileNameA
        self.GetProcessImageFileName.restype = ctypes.wintypes.DWORD
    
        self.Kernel32 = ctypes.WinDLL('kernel32.dll')
        self.OpenProcess = self.Kernel32.OpenProcess
        self.OpenProcess.restype = ctypes.wintypes.HANDLE
        self.TerminateProcess = self.Kernel32.TerminateProcess
        self.TerminateProcess.restype = ctypes.wintypes.BOOL
        self.CloseHandle = self.Kernel32.CloseHandle

        self.MAX_PATH = 260
        self.PROCESS_TERMINATE = 0x0001
        self.PROCESS_QUERY_INFORMATION = 0x0400

        self.count = 256

    def Finalizar_Proceso(self):
        print"------------------------Se Listan todos los Procesos------------------------------------------"
        while True:
            ProcessIds = (ctypes.wintypes.DWORD*self.count)()
            cb = ctypes.sizeof(ProcessIds)
            BytesReturned = ctypes.wintypes.DWORD()
            if self.EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned)):
                if BytesReturned.value<cb:
                    break
                else:
                    self.count *= 2
            else:
                sys.exit("Call to EnumProcesses failed")
        
        for index in range(BytesReturned.value / ctypes.sizeof(ctypes.wintypes.DWORD)):
            ProcessId = ProcessIds[index]
            hProcess = self.OpenProcess(self.PROCESS_TERMINATE | self.PROCESS_QUERY_INFORMATION, False, ProcessId)
            if hProcess:
                ImageFileName = (ctypes.c_char*self.MAX_PATH)()
                if self.GetProcessImageFileName(hProcess, ImageFileName, self.MAX_PATH)>0:
                    filename = os.path.basename(ImageFileName.value)
                    print("Proceso: ",format(filename))
                    #if filename == 'taskmgr.exe' or filename == 'explorer.exe':
                    if filename == 'taskmgr.exe':
                        self.TerminateProcess(hProcess, 1)
                        print "Se ejecuto y se cerro proceso taskmgr.exe"
                        break
                self.CloseHandle(hProcess)