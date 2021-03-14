# import easygui as g  # 导入EasyGui模块

# # fileopenbox()函数的返回值是你选择的那个文件的具体路径
# str1 = g.fileopenbox('open file', 'E:/music')
# # msgbox()是测试用的，可以不用写
# g.msgbox(str1)


# import win32ui
 
# # 0代表另存为对话框，1代表打开文件对话框
# dlg = win32ui.CreateFileDialog(1)
 
# # 默认目录
# dlg.SetOFNInitialDir('C:/') 
 
# # 显示对话框
# dlg.DoModal()
 
# # 获取用户选择的文件全路径
# filename = dlg.GetPathName()

# import tkFileDialog
# fname = tkFileDialog.askopenfilename()
# print(fname)
import tkinter
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw()
filepath = filedialog.askdirectory() #:选择目录，返回目录名
print(filepath)