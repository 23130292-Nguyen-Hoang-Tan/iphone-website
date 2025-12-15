import importlib.util
print('spec PIL', importlib.util.find_spec('PIL'))
print('spec pil', importlib.util.find_spec('pil'))
import sys
print(sys.path[:3])
