import asyncio
from bleak import BleakScanner
import math

TX_POWER=-47
N=2

def rssi_to_distance(rssi):
    return 10 ** ((TX_POWER - rssi) / (10 * N))

async def main(max_distance=5):
    print("Scanning for BLE devices...")


    devices = await BleakScanner.discover(return_adv=True)

    nearby = set()

    for address, (device, adv) in devices.items():
        distance = rssi_to_distance(adv.rssi)
        if distance <= max_distance:
            nearby.add(address)

    num_people = math.ceil(len(nearby) / 2.0)

    print("\nDevices within",max_distance,"meters:",len(nearby))
    print("\nNum People Estimated:", num_people)

asyncio.run(main(1))
