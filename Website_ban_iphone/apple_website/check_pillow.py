try:
    import PIL
    print('PIL:', PIL.__file__)
except Exception as e:
    print('Import error:', type(e).__name__, e)
import sys
print('sys.executable=', sys.executable)
print('sys.path=', sys.path)
print('Python version=', sys.version)
