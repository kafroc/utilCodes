import subprocess
import sublist3r
import sys
import os

if len(sys.argv) <= 1:
    print("usage: python3 subdomain2ip.py domain")
    exit(1)

# sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
domain = sys.argv[1]
savefile = domain + '_subdomains.txt'

if os.path.exists(savefile):
    with open(savefile, 'r') as fp:
        subdomains = fp.read().split('\n')
else:
    subdomains = sublist3r.main(domain, 40, savefile, ports=None,
                                silent=False, verbose=False, enable_bruteforce=False, engines=None)

print(subdomains)

ret = {}
for domain in subdomains:
    if domain == '':
        continue
    print('Dig ' + domain + ' ...')
    cmdres = subprocess.check_output(['dig', domain, 'A']).decode().split('\n')
    for res in cmdres:
        if res == '' or res[0] == ';':
            continue
        tmp = res.split()

        if len(tmp) < 5 or (tmp[3] != 'A' and tmp[3] != 'SOA'):
            continue

        if domain not in ret:
            ret[domain] = [tmp[4]]
        else:
            ret[domain].append(tmp[4])

for domain in subdomains:
    if domain == '':
        continue
    print(domain + ' (' + '; '.join(ret[domain]) + ')')
