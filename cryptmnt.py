#!/usr/bin/env python3
import subprocess
from os.path import exists

DEFAULT_MOUNT_POINT = "/home/valkyrie/malygos"
INPUT_1 = "\nInput a number to select the desired block device: "

def main():
    block_devices = subprocess.Popen("sudo blkid | grep crypto | awk '{print $1}'", shell=True, stdout=subprocess.PIPE)
    bd_arr = block_devices.communicate()[0].decode('utf-8').split(":\n")

    for n, x in zip(bd_arr, range(1, len(bd_arr))):
        print(f"{x}. {n}")

    if len(bd_arr) > 2:
        while True:
            selected_device = input(INPUT_1)
            try:
                selected_device = int(selected_device)

                if selected_device not in range(1, len(bd_arr)):
                    raise KeyError

            except ValueError:
                print(f'Please input an integer. You input: {type(selected_device)}')
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
                do_decryption(bd_arr, mount_point, selected_device)

        except NameError:
            print("Path does not exist!")
            continue
        break


def do_decryption(bd_arr, mount, device):
    subprocess.run(f"/usr/bin/sudo cryptsetup luksOpen {bd_arr[device-1]} cryptmnt-{bd_arr[device-1].split('/')[2]}", shell=True)
    subprocess.run(f"/usr/bin/sudo mount /dev/mapper/cryptmnt-{bd_arr[device-1].split('/')[2]} {mount}", shell=True)

if __name__ == '__main__':
    main()