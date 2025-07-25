@echo off
pyinstaller main.py --onedir --noconsole ^
--hidden-import=easyocr ^
--hidden-import=torch ^
--hidden-import=torchvision ^
--hidden-import=PIL ^
--hidden-import=scipy ^
--hidden-import=cv2 ^
--hidden-import=pdf2image ^
--hidden-import=reportlab ^
--hidden-import=pyzbar ^
--collect-all=easyocr ^
--collect-all=reportlab ^
--collect-all=pyzbar ^
--add-data="FolderTemplates;FolderTemplates" ^
--add-data="Tabs;Tabs" ^
--add-data="Resources;Resources" ^
--icon=Resources/Images/hexel_icon.ico
pause
