from backend.models import OrderLog

import time

def main():
    while(True):
        logs = OrderLog.objects.all()
        for log in logs:
            print(log.id)
            time.sleep(0.5)
    

