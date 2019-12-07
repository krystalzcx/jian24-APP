import os
import time



def sleep(n_secs):
    time.sleep(n_secs)

def is_superuser():
    env = os.environ["USERNAME"]
    if env == 'admin':
        return True
    else:
        return False

def franchisee_name():
    var = 'superuser'
    if is_superuser()==True:
        var = 'superuser'
    else:
        var = 'not_sure'
    return var


