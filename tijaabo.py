import subprocess

def list_disks():
    flashs = []
    try:
        # Run the `lsblk` command to get the list of block devices
        result = subprocess.run(['lsblk', '-o', 'NAME,TYPE,SIZE,MOUNTPOINT,LABEL'], capture_output=True, text=True)
        output = result.stdout
        
        # Split the output into lines and filter out the header
        lines = output.splitlines()
        headers = lines[0]
        device_lines = lines[1:]
        
        # Iterate over each device line to filter and display disk devices
        print("Disks connected:")
        for line in device_lines:
            columns = line.split()
            if len(columns) >= 2 and columns[1] == 'disk':
                name = columns[0]
                size = columns[2] if len(columns) > 2 else 'Unknown'
                mountpoint = columns[3] if len(columns) > 3 else 'Not Mounted'
                label = columns[4] if len(columns) > 4 else 'No Label'
                flashs.append("/dev/"+name)
        return flashs
    except Exception as e:
        print(f"An error occurred: {e}")


import subprocess
import os

def identify_flash_drive():
    count = 0
    flashs = list_disks()
    for i in flashs:
        count += 1
        print(count,".",i)
    select = int(input("select one of theme : "))
    if select-1 <= len(flashs):
        flash_drive = flashs[select-1]
    return flash_drive.strip()

def write_image_to_flash(image_path, flash_drive):
    # Warning: This will overwrite the flash drive, so be very careful.
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")
    
    # Ensure the flash drive is not mounted or in use
    subprocess.run(['umount', flash_drive], stderr=subprocess.PIPE, check=False)
    
    # Write the image to the flash drive
    try:
        subprocess.run(['sudo','dd', f'if={image_path}', f'of={flash_drive}', 'bs=4M', 'status=progress'], check=True)
        print("Image written successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    image_path = input("Enter the path to the OS image file: ")
    flash_drive = identify_flash_drive()
    write_image_to_flash(image_path, flash_drive)