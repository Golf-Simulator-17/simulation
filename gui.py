# from tkinter import *
# import asyncio
# import logging

# from bleak import discover
# from bleak import BleakClient
# import bleak

UART_SERVICE_UUID = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
UART_RX_CHAR_UUID = "49535343-8841-43F4-A8D4-ECBE34729BB3"
UART_TX_CHAR_UUID = "49535343-1E4D-4BD9-BA61-23C647249616"
TEST_CHAR = "49535343-4c8a-39b3-2f49-511cff073b7e"
maham_address = "B900376F-4577-CA3A-EC9E-E3836929A78A"
sam_address = "44:B7:D0:2D:66:FD"
new_address = "40:84:32:58:FB:05"


# async def run(address, debug=False):
#     print("running")
#     log = logging.getLogger(__name__)
#     if debug:
#         import sys

#         log.setLevel(logging.DEBUG)
#         h = logging.StreamHandler(sys.stdout)
#         h.setLevel(logging.DEBUG)
# #         log.addHandler(h)
#     async with BleakClient(address) as client:
#         try:
#             while toggle_connection_button.config("text")[-1] != "DISCONNECTED":
#                 # if send_to_ble_button.config("text")[-1] == "SENDING":
#                 send_data = input().encode()
#                 print("sending: " + str(send_data))
#                 await client.write_gatt_char(UART_RX_CHAR_UUID, data=send_data, response=None) # change to textbox input
#                 # else:
#                     # await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
#                     # await asyncio.sleep(5.0)
#                     # await client.stop_notify(CHARACTERISTIC_UUID)
#         except KeyboardInterrupt:
#             print("Exiting . . .")



# def toggle_sleep():
#     if toggle_sleep_button.config('text')[-1] == "ON": # turn off
#         toggle_sleep_button.config(text="OFF")
#         toggle_sleep_button.config(bg="#ff0000")
#         toggle_sleep_button.config(activebackground="#cc0000")
#         # send sleep to BLE
#     else: # turn on
#         toggle_sleep_button.config(text="ON")
#         toggle_sleep_button.config(bg="#33cc33")
#         toggle_sleep_button.config(activebackground="#29a329")
 
 
# def toggle_connection():
#     if toggle_connection_button.config('text')[-1] == "CONNECTED": # turn off
#         toggle_connection_button.config(text="DISCONNECTED")
#         toggle_connection_button.config(bg="#ff0000")
#         toggle_connection_button.config(activebackground="#cc0000")
#         # send sleep to BLE
#     elif toggle_connection_button.config('text')[-1] == "DISCONNECTED": # turn on
#         toggle_connection_button.config(text="CONNECTING")
#         toggle_connection_button.config(bg="#808080")
#         toggle_connection_button.config(activebackground="#808080")
#         # asyncio.run(run(address, True))
#         # send wake to BLE       # send wake to BLE

# root = Tk()
# root.title("Golf Simulator")
# root.geometry("500x500")

# toggle_sleep_button = Button(text="OFF", 
#                              width=10, 
#                              command=toggle_sleep, 
#                              bg="#ff0000",
#                              activebackground="#cc0000")
# toggle_sleep_button.pack(pady=10)

# toggle_connection_button = Button(text="DISCONNECTED", 
#                              width=10, 
#                              command=toggle_connection, 
#                              bg="#ff0000",
#                              activebackground="#cc0000")
# toggle_connection_button.pack(pady=10)

# root.mainloop()

# while True:
#     print("testing")
    
#     if toggle_connection_button.config('text')[-1] == "CONNECTING":
#         print("coonecting")
#         asyncio.run(run(address, True))
        
        
        

        
# if toggle_sleep_button.config('text')[-1] == "ON":
#     # read data from BLE
#     pass





import asyncio
from bleak import *
import tkinter as tk
import time

async def start_window():
    my_window = MyWindow(asyncio.get_event_loop())
    await my_window.show()

class MyWindow(tk.Tk):
    def __init__(self, loop):
        super().__init__()
        self.title = "Golf Simulator"
        self.loop = loop
        self.root = tk.Tk()
        self.bleIsConnected = False

        
        self.ble_connection = tk.Button(self, text="BLE disconnected")
        self.ble_connection["command"] = self.toggle_connection
        self.ble_connection.pack()

    def bleThread(self):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            while(1):
                time.sleep(0.05) 
                if (self.cancelTasks):
                    self.blePingTask.cancel()
                    self.bleConnectTask.cancel()
                    self.cancelTasks = False
                if ((self.loop.is_running() == False) and (self.runLoopForever)):
                    self.loop.run_forever()
        except:
            pass

    def connectBle(self, address):
            self.bleConnectTask = self.loop.create_task(self.bleConnectAsync(address))
            # self.blePingTask = self.loop.create_task(self.pingBleAsync())
            self.loop.run_forever()

    async def bleConnectAsync(self, address):
        print("in connect async" + self.bleIsConnected)
        if (self.bleIsConnected == False):
            async with BleakClient(address) as self.bleClient:
                print("connecting")
                self.bleIsConnected = await self.bleClient.is_connected()
                if (self.bleIsConnected):
                    # self.bleToMainQueue.put(serialcommands.BLE_CONNECTED)
                    # await self.bleClient.start_notify(TX_FIFO_CHARACTERISTIC, self.notification_handler) 
                    # self.bleClient.set_disconnected_callback(self.disconnection_handler)
                    self.message_label.config(text="BLE CONNECTED")
                    self.runLoopForever = True
                    while True:
                        if (self.disconnectBle):
                            # await self.bleClient.stop_notify(TX_FIFO_CHARACTERISTIC) 
                            await self.bleClient.disconnect()
                        await asyncio.sleep(1.0, loop = self.loop)
                        self.loop.stop()
                else:
                    # self.bleToMainQueue.put(serialcommands.BLE_NOT_CONNECTED
                    self.message_label.config(text="BLE DISCONNECTED")
                    pass


    async def bleSendAsync(self, data):
        await self.bleClient.write_gatt_char(UART_RX_CHAR_UUID, data, response=False)
                




        
        # other stuff

    def toggle_connection(self):
        print("here?")
        self.connectBle(new_address)


    async def show(self):
        while True:
            self.root.update()

            # other stuff

            await asyncio.sleep(0.1)

asyncio.run(start_window())