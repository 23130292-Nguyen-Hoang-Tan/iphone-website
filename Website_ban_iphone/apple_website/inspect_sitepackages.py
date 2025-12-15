import os
site = r'C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\Lib\site-packages'
print('listdir sample:', [n for n in os.listdir(site) if n.lower().startswith('pil')][:10])
print('PIL exists', os.path.exists(os.path.join(site,'PIL')))
print('pil exists', os.path.exists(os.path.join(site,'pil')))
print('PIL isdir', os.path.isdir(os.path.join(site,'PIL')))
print('pil isdir', os.path.isdir(os.path.join(site,'pil')))
