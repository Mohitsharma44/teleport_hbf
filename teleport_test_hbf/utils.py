import os

PID_FILE_PATH = "/var/run/hbf.pid"

def get_hbf_pid():
    pid = None
    if os.path.exists(PID_FILE_PATH):
        with open(PID_FILE_PATH, "r") as fh:
            pid = fh.read()
        if not(pid and os.path.isdir(f"/proc/{pid}")):
            remove_hbf_pid()
    return pid

def write_hbf_pid():
    pid = str(os.getpid())
    with open(PID_FILE_PATH, "w") as fh:
        fh.write(pid)

def remove_hbf_pid():
    os.remove(PID_FILE_PATH)
