import os
import psutil
from app import app_env

'The facility that prevents running multiple instances'
class SelfDetect:
    path: str = ''
    def detect(self):
        self.path = os.path.join('', 'pid.log')
        if os.path.exists(self.path):
            fp = open(self.path,'r')
            split_flag = fp.read().strip().split('/')
            if len(split_flag) < 2:
                return False
            pid, identifier = split_flag[0], split_flag[1]
            fp.close()
            try:
                target_pid = int(pid)
                pid_iter = psutil.process_iter()
                for pid in pid_iter:
                    if pid.pid == target_pid and pid.name() == identifier:
                        return True
                return False
            except:
                return False
        else:
            return False
    def write(self):
        pid = os.getpid()
        fp = open(self.path, 'w')
        fp.write(str(pid) + '/' + app_env.get_program_basename())
        fp.close()
    def clean(self):
        if os.path.exists(self.path):
            os.unlink(self.path)
