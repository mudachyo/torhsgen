import os
import time
import sys

# functions
def hsgen(exter_port:str, local_addr:str, local_port:str):
    hs_address = ""

    # Choosing name for new Hidden Service
    # 
    # Service dir template:
    # HService.n where n is number os service
    obj = os.scandir("/var/lib/tor")
    dirnums = []
    for i in obj:
        if i.is_dir():
            try:
                dirnums.append(int(i.name.split(".")[1]))
            except IndexError:
                continue
    try:
        new_dir_num = max(dirnums) + 1 
    except ValueError:
        new_dir_num = 1
    
    with open("/etc/tor/torrc", "a+") as fs:
        fs.write("\nHiddenServiceDir /var/lib/tor/HService.%d\n" % new_dir_num)
        fs.write("HiddenServicePort %s %s:%s\n" % (exter_port, local_addr, local_port))

    os.system("systemctl restart tor.service")
    time.sleep(1)

    with open("/var/lib/tor/HService.%d/hostname" % new_dir_num, "r") as fs:
        hs_address = fs.read()
    return hs_address


if __name__ == "__main__":
    # Check permissions
    if os.geteuid() != 0:
        exit("Root requiered. Exit.")

    if len(sys.argv) > 2:
        result = hsgen(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        local_addr = str(input("Enter local server address: "))
        local_port = str(input("Enter local port: "))
        exter_port = str(input("Enter external port: "))
        result = hsgen(exter_port, local_addr, local_port)

    print(result, end="")
