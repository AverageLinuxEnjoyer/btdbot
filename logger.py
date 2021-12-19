import datetime

def log(*args, **kwargs):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}]",*args, **kwargs)
