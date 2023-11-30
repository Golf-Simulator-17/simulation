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


#
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

def split_into_chunks(byte_array, chunk_size):
    return [byte_array[i:i+chunk_size] for i in range(0, len(byte_array), chunk_size)]

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

#ACK Stuff
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

async def scan(breadboard): 
    try:
        if (False):
            device = await BleakScanner.find_device_by_name("PmodBLE-66FD")
        else:
            device = await BleakScanner.find_device_by_name("RN4871-FB29")
        
        if not device:
            raise Exception("Could not find device")

        return device
    except Exception as e:
        print(e)


#CONNECTING TO DEVICE
async def run(device):
    global RECEIVED
    global ACK_1
    print("test")
    async with BleakClient("884A8A08-4F22-6E5B-ED06-A6A4F2895B01") as client:
        while (True):
            print(client.is_connected)
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
    t1 = threading.Thread(target=gui_process)
    t1.start()
    print("Finding device . . .")
    device = asyncio.run(scan(breadboard=False))
    print(device)
    asyncio.run(run(device))