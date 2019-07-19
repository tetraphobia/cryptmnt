#!/usr/bin/env python3
import subprocess
import re
from os.path import exists

DEFAULT_MOUNT_POINT = "/home/valkyrie/malygos"
INPUT_1 = "\nInput a number to select the desired block device: "


def main():
    bd_str = subprocess.Popen(['/usr/bin/sudo', 'blkid'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    bd_arr = re.findall(r"^(.*):.*crypto_LUKS.*PARTLABEL=\"(.*)\" .*$", bd_str, re.MULTILINE)

    for n, x in zip(bd_arr, range(1, len(bd_arr) + 1)):
        print(f"{x}. {n[0]} \"{n[1]}\"")

    if len(bd_arr) > 1:
        while True:
            selected_device = input(INPUT_1)
            try:
                selected_device = int(selected_device)

                if selected_device not in range(1, len(bd_arr[0])):
                    raise KeyError

            except ValueError:
                print(f'Please input an integer from 1 to {len(bd_arr[0])}.')
                continue

            except KeyError:
                print(f'Block device not found in the list above. Try again.')
                continue
            break
    else:
        selected_device = 1
        print(f"{INPUT_1}1")

    while True:
        try:
            mount_point = input(f"Input desired mount point (Default {DEFAULT_MOUNT_POINT}): ")
            if mount_point == "":
                mount_point = DEFAULT_MOUNT_POINT

            if not exists(mount_point):
                raise NameError
            else:
                do_decryption(bd_arr[0], mount_point, selected_device)

        except NameError:
            print("Path does not exist!")
            continue
        break


def do_decryption(bd_arr, mount, device):
    subprocess.run(['/usr/bin/sudo', 'cryptsetup', 'luksOpen', bd_arr[device-1], f"cryptmnt-{bd_arr[device-1].split('/')[2]}"])
    subprocess.run(['/usr/bin/sudo', 'mount', f"/dev/mapper/cryptmnt-{bd_arr[device-1].split('/')[2]}", mount])


if __name__ == '__main__':
    main()