for name in ('PIL','pil'):
    try:
        m = __import__(name)
        print(name, 'imported from', getattr(m,'__file__', None))
    except Exception as e:
        print('Import', name, 'failed:', type(e).__name__, e)
