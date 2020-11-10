import paramiko

HOST = '192.168.1.2'
PORT = 22
USERNAME = 'root'
PASSWORD = 'toor'


def fetch_port_list(sshcli):
    portsinfo = []
    pi = {}
    portlist = []
    addrlist = {}

    cmd = "netstat -tulnp | awk '{print $4}'"
    stdin, stdout, stderr = sshcli.exec_command(cmd)
    cmdouts = stdout.read().decode().split('\n')[2:-1]
    for line in cmdouts:
        port = int(line.split(':')[-1])
        skipportlen = -1 * (len(str(port)) + 1)
        laddr = line[:skipportlen]

        if port not in portlist:
            portlist.append(port)

        if str(port) in addrlist:
            addrlist[str(port)].append(laddr)
        else:
            addrlist[str(port)] = [laddr]

    for i in portlist:
        pi['port'] = i
        pi['listen'] = addrlist[str(i)]
        portsinfo.append(pi.copy())

    portsinfo = sorted(portsinfo, key=lambda x: x['port'])
    # print(portsinfo)
    return portsinfo.copy()


def fetch_pid_and_service(sshcli, portsinfo):
    tcpcmd = "netstat -tlnp | awk '{print $4,$7}'"
    udpcmd = "netstat -ulnp | awk '{print $4,$6}'"
    stdin, stdout, stderr = sshcli.exec_command(tcpcmd)
    tcpouts = stdout.read().decode().split('\n')[2:]
    stdin, stdout, stderr = sshcli.exec_command(udpcmd)
    udpouts = stdout.read().decode().split('\n')[2:]
    cmdouts = tcpouts + udpouts
    for pi in portsinfo:
        for out in cmdouts:
            out = out.split(' ')
            if len(out) == 0 or out[0] == '':
                continue

            if int(out[0].split(':')[-1]) == pi['port']:
                try:
                    pi['PID'] = int(out[1].split('/')[0])
                    pi['Service'] = out[1].split('/')[1]
                except Exception as exp:
                    print(exp)

    # print(portsinfo)
    return portsinfo


def fetch_execution_cmd(sshcli, portsinfo):
    for pi in portsinfo:
        print(pi)
        pid = pi['PID']

        """
        cmd = "ps -f -p %d" % pid
        stdin, stdout, stderr = sshcli.exec_command(cmd)
        out = stdout.read().decode()

        try:
            pi['execmd'] = ''.join(out.split('\n')[-2][48:])
        except Exception as e:
            print(e)
        """

        cmd = 'ls -al /proc/%d/exe' % pid
        # print(cmd)
        stdin, stdout, stderr = sshcli.exec_command(cmd)
        out = stdout.read().decode()
        # print(out)
        pi['procexe'] = ''.join(out.split(' ')[-1])[:-1]

        cmd = 'cat /proc/%d/cmdline' % pid
        stdin, stdout, stderr = sshcli.exec_command(cmd)
        out = stdout.read().decode()
        pi['proccmdline'] = out


if __name__ == "__main__":

    sshcli = paramiko.SSHClient()
    sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshcli.connect(hostname=HOST, port=PORT,
                   username=USERNAME, password=PASSWORD)

    portsinfo = fetch_port_list(sshcli)
    fetch_pid_and_service(sshcli, portsinfo)
    fetch_execution_cmd(sshcli, portsinfo)

    for info in portsinfo:
        outputformat = "Port: %d\nPID: %d\nprocexe: %s\nproccmdline: %s\nlistenip: %s\n\n" % (
            info['port'], info['PID'], info['procexe'], info['proccmdline'], info['listen'])
        print(outputformat)

    sshcli.close()
