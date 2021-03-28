# IDA text to machine code

with open('IDAtext.txt', 'r') as fp:
    lines = fp.read().split('\n')

    out = '\"'
    cnt = 0
    for line in lines:
        tmp = line.split()
        if len(tmp) == 1:
            continue

        for x in tmp[1:]:
            if len(x) != 2:
                continue
            try:
                tmp = int('0x' + x, 16)
                if tmp >= 0x00 and tmp <= 0xff:
                    out += '\\x' + x 
                    cnt += 1
            except:
                break 
            
    out += '\"'
    
    print("The length of shellcode is %d.\n\nshellcode = %s\n" % (cnt, out))
