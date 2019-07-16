import queue
import subprocess as sb
import threading

cmd = ("/usr/local/sbin/os/get-cdp -_ systems1%|egrep -v 'gurg-off|old|windows"
       "|repo|oob|systemsdb|hostname'")

sys_hosts = sb.Popen(
    cmd, shell=True, stdout=sb.PIPE).communicate()[0].decode().splitlines()
# sys_hosts = ('fileserve1.hk', )
q = queue.Queue()

for h in sys_hosts:
    q.put(h)


def run_sync(q):
    while not q.empty():
        host = q.get()
        cmd = ("/usr/bin/rsync -q -avz ~/.zshrc ~/.zshrc_work"
               " ~/.bashrc ~/.bashrc_work ~/.vim ~/.vimrc ~/.pythonrc"
               " {}:~/".format(host))
        sb.run(cmd, shell=True)


threads = [threading.Thread(target=run_sync, args=(q,)) for _ in range(20)]
for th in threads:
    th.start()

for th in threads:
    th.join()

# with ThreadingGroup(*sys_hosts) as tg:
#     tg.run('rm -f ~/work_zshrc')
#     tg.run('rm -f local_machine_settings.rc')
