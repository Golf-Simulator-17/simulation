import asyncio
import logging
import struct
import csv
import os

from readingData import *

from bleak import BleakClient, BleakScanner, discover
from datetime import datetime

import threading


UART_SERVICE_UUID = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
UART_RX_CHAR_UUID = "49535343-8841-43F4-A8D4-ECBE34729BB3"
UART_TX_CHAR_UUID = "49535343-1E4D-4BD9-BA61-23C647249616"


RECEIVED = False
ACK_1 = False
ACK_2 = False
devices_dict = {}
devices_list = []

async def scan(breadboard): 
    try:
        if (False):
            device = await BleakScanner.find_device_by_name("PmodBLE-66FD")
        else:
            device = await BleakScanner.find_device_by_name("RN4871-A909")
        
        if not device:
            raise Exception("Could not find device")

        return device
    except Exception as e:
        print(e)

async def scan2():
    dev = await discover()
    for i in range(0,len(dev)):
        #Print the devices discovered
        # print("[" + str(i) + "]" + dev[i].address,dev[i].name,dev[i].metadata["uuids"])
        #Put devices information into list
        devices_dict[dev[i].address] = []
        devices_dict[dev[i].address].append(dev[i].name)
        devices_dict[dev[i].address].append(dev[i].metadata["uuids"])
        # if "RN4871" in dev[i].name:
        print("[" + str(len(devices_list)) + "]" + dev[i].address,dev[i].name,dev[i].metadata["uuids"])
        devices_list.append(dev[i].address)

        

async def send_data(client, data):
    # print("Sending data", data)
    if (client.is_connected):
        await client.write_gatt_char(UART_RX_CHAR_UUID, data=data.encode(), response=None)
    else:
        raise Exception("Client not connected")
    
async def receive_data(client):
    await client.start_notify(UART_TX_CHAR_UUID, notification_handler)
    await asyncio.sleep(1)
    await client.stop_notify(UART_TX_CHAR_UUID)

def notification_handler(sender, data):
    global RECEIVED
    RECEIVED = True
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"hit_info/receivedData{timestamp}.csv"


    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        print(data)
        for x in split_into_chunks(data, 4):
            original_values = [str(y) for y in x]
            hex_string = ''.join('{:02x}'.format(y) for y in x)
            hex_bytes = bytes.fromhex(hex_string)
            decimal_value = struct.unpack('f', hex_bytes)[0]
            csv_writer.writerow([decimal_value])

def start_ack_handler(sender, data):
    global ACK_1
    # print(data)
    if data == b'ack1':
        ACK_1 = True

def end_ack_handler(sender, data):
    global ACK_2
    print(data)
    if data == b'ack2':
        ACK_2 = True

async def recevie_ack_1(client):
    await client.start_notify(UART_TX_CHAR_UUID, start_ack_handler)
    await asyncio.sleep(1)
    await client.stop_notify(UART_TX_CHAR_UUID)

async def recevie_ack_2(client):
    await client.start_notify(UART_TX_CHAR_UUID, end_ack_handler)
    await asyncio.sleep(1)
    await client.stop_notify(UART_TX_CHAR_UUID)

def split_into_chunks(byte_array, chunk_size):
    return [byte_array[i:i+chunk_size] for i in range(0, len(byte_array), chunk_size)]


async def run(device):
    global RECEIVED
    global ACK_1
    async with BleakClient(str(device)) as client:
        while (True):
            print("Device connected somewhat . . .! Waiting for hit . . .")
            while ACK_1 == False:
                RECEIVED = False
                print("Sending iiiii")
                await send_data(client, "iiiiiiiiii")
                await recevie_ack_1(client)

            print("Device connected! Waiting for hit . . .")
            while RECEIVED == False:
                ACK_1 = False
                await receive_data(client)

            await send_data(client, "cccccccccc")
            await send_data(client, "cccccccccc")
            await send_data(client, "cccccccccc")

            print("Hit received! Simulation time!")

def gui_process():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files_processed = []
    while True:
        for file in os.listdir("hit_info"):
            start = file.find("_") + 1
            number = file[start:-4]
            # print("Number:", numb?er)
            if int (number) > int(timestamp):
                if file not in files_processed:
                    files_processed.append(file)
                    print("Processing file:", file)
                    start_simulation(file)

def bitch():
    print("Finding device . . .")
    done = True
    # Build an event loop
    while(done):
        loop = asyncio.get_event_loop()
    # Run the discover event
        loop.run_until_complete(scan2())

    # # let user chose the device
        if len(devices_list) == 1:
            index = 1
        else:
            index = input('please select device from 0 to ' + str(len(devices_list)) + "or -1 to rescan :")
            index = int(index)
            if(index != -1):
                address = devices_list[index]
                print("Address is " + address)
                print(type(address))
                done = False

    # device = asyncio.run(address)
    # print(device)
    asyncio.run(run(address))

if __name__ == "__main__":
    print('''
    ###     ###    ###         ###               ###    ###    #   ##    #  ##   ###         ###   ######     ###       ###  
   ####    #####  ###         ####              ####  ####    ### ###   ##  ##  ###         ####  ######     #####     ####  
  ##  #   ##  ##   ##        ##                ##  #    ##    #######   ##  ##   ##        ## ##    ##      ##  ##    ## ##  
 ##      ##   ##   ##       ##                ##        ##    ## # ##   ##  ##   ##       ##  ##    ##     ##   ##   ##  ##  
##  ###  ##   ##   ##   #  ######            #######    ##    ##   ##  ###  ##   ##   #  #######    ##     ##   ##  #####    
##    #  ##  ##    ##  ##  ##                     ##    ##    ##   ##  ##   ##   ##  ##  ##   ##    ##     ##  ##   ##  ##   
#######   ####    #######  ##                #######    ###   ##   ##  #######  #######  ##   ##    ###     ####    ##   ##  
                                                       ##                                          ##                       
          ''')
    #t1 = threading.Thread(target=gui_process)
    #t1.start()
    run_gui()
    bitch()

    # device = asyncio.run(address)
    # print(device)
    asyncio.run(run(address))


    # if os.path.exists(csv_filename):
    #     root = tk.Tk()
    #     root.title("Golf Simulator")
    #     root.geometry("800x600")

    #     # Load and set the background image
    #     background_image = Image.open("golf_course.webp")
    #     background_photo = ImageTk.PhotoImage(background_image)
    #     background_label = tk.Label(root, image=background_photo)
    #     background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #     # Welcome Message
    #     root = tk.Tk()
    #     root.title("Golf Simulator")
    #     root.geometry("800x600")

    #     # Load and set the background image
    #     background_image = Image.open("golf_course.webp")
    #     background_photo = ImageTk.PhotoImage(background_image)
    #     background_label = tk.Label(root, image=background_photo)
    #     background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #     # Welcome Message
    #     welcome_label = tk.Label(root, text="Welcome to the Golf Simulator", font=("Arial", 24), bg="white")
    #     welcome_label.pack(pady=20)

    #     # Start and Stop Simulation buttons
    #     start_button = ttk.Button(root, text="Start Simulation", command=start_simulation(csv_filename))
    #     start_button.pack(pady=10)  # Adding padding for spacing

    #     stop_button = ttk.Button(root, text="Stop Simulation", command=stop_simulation)
    #     stop_button.pack(pady=10)  # Adding padding for spacing

    #     root.mainloop()


