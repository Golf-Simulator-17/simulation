import asyncio
import logging
import struct
import csv 

from bleak import discover
from bleak import BleakClient
import bleak
import time

UART_SERVICE_UUID = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
UART_RX_CHAR_UUID = "49535343-8841-43F4-A8D4-ECBE34729BB3"
UART_TX_CHAR_UUID = "49535343-1E4D-4BD9-BA61-23C647249616"
TEST_CHAR = "49535343-4c8a-39b3-2f49-511cff073b7e"
new_address = "40:84:32:58:FB:05"

#address = "B900376F-4577-CA3A-EC9E-E3836929A78A"

devices_dict = {}
devices_list = []
receive_data = []
csv_filename = "received_data" + time.ctime() + ".csv"
fmt = '<d'
#To discover BLE devices nearby 
async def scan():
    dev = await discover()
    for i in range(0,len(dev)):
        #Print the devices discovered
        print("[" + str(i) + "]" + dev[i].address,dev[i].name,dev[i].metadata["uuids"])
        #Put devices information into list
        devices_dict[dev[i].address] = []
        devices_dict[dev[i].address].append(dev[i].name)
        devices_dict[dev[i].address].append(dev[i].metadata["uuids"])
        devices_list.append(dev[i].address)

def split_into_chunks(byte_array, chunk_size):
    return [byte_array[i:i+chunk_size] for i in range(0, len(byte_array), chunk_size)]

#An easy notify function, just print the recieve data
def notification_handler(sender, data):
    #print(data)
    print(', '.join('{:02x}'.format(x) for x in data))
    #csv_writer.writerow((', '.join('{:02x}'.format(x) for x in data)))
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
    
        for x in split_into_chunks(data, 4):
            original_values = [str(y) for y in x]
            # print(original_values)
            hex_string = ''.join('{:02x}'.format(y) for y in x)
            # print(hex_string)
            hex_bytes = bytes.fromhex(hex_string)
            decimal_value = struct.unpack('f', hex_bytes)[0]
            # print(decimal_value)
            csv_writer.writerow([decimal_value, hex_bytes])


    # print("x: " + str(x))
    # print(struct.unpack('f', x))
    # print(type(data))
    # print("receving")
    # st_bytes = data.decode('ascii')
    # print(int.from_bytes(data, byteorder="little", signed=True))
    # print(data)

    # print(st_bytes)

async def run(address, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))

        for service in client.services:
            log.info("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                log.info(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                # for descriptor in char.descriptors:
                #     value = await client.read_gatt_descriptor(descriptor.handle)
                #     log.info(
                #         "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                #             descriptor.uuid, descriptor.handle, bytes(value)
                #         )
                #     )

                #Characteristic uuid
        CHARACTERISTIC_UUID = UART_TX_CHAR_UUID
        try:
            print("awakening . . .")
            await client.write_gatt_char(UART_RX_CHAR_UUID, data="iiiiiiiiii".encode(), response=None)
            while True:
                try:
                    print("receiving . . .")
                # Notify the data from the device
                # await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                # await asyncio.sleep(5.0)
                # await client.stop_notify(CHARACTERISTIC_UUID)
                # print("send")
                    # await client.write_gatt_char(UART_RX_CHAR_UUID, data="aa55332211".encode(), response=None)
                    await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                    # await client.write_gatt_char(CHARACTERISTIC_UUID, input().encode(), response=True)
                    await asyncio.sleep(0.5)  # Sleeping just to make sure the response is not missed...
                    await client.stop_notify(CHARACTERISTIC_UUID)
                except KeyboardInterrupt:
                    print("sleeping ... ")
                    await client.write_gatt_char(UART_RX_CHAR_UUID, data="cccccccccc".encode(), response=None)
                
            
        except KeyboardInterrupt:
            print("Exiting...")

if __name__ == "__main__":
    print("Connecting to Bluetooth module...")

    # # Build an event loop
    # loop = asyncio.get_event_loop()
    # # Run the discover event
    # loop.run_until_complete(scan())

    # # let user chose the device
    # index = input('please select device from 0 to ' + str(len(devices_list)) + ":")
    # index = int(index)
    # address = devices_list[index]
    # print("Address is " + address)

    # # Run notify event
    # loop = asyncio.get_event_loop()
    # loop.set_debug(True) 
    # loop.run_until_complete(run(address, True))


    try:
        asyncio.run(run(new_address, True))
    except(bleak.exc.BleakDeviceNotFoundError):
        print("Device not found. Are you sure it's on?")
    
    csv_file.close()
