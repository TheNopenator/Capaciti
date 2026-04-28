from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from bleak import BleakScanner
import math

app = Flask(__name__)

CORS(app)

TX_POWER=-47
N=2

def rssi_to_distance(rssi):
    return 10 ** ((TX_POWER - rssi) / (10 * N))

async def scan_ble(max_distance=5):
    print("Scanning for BLE devices...")

    devices = await BleakScanner.discover(return_adv=True)
    print(f"Total devices discovered: {len(devices)}")

    nearby = set()

    for address, (device, adv) in devices.items():
        distance = rssi_to_distance(adv.rssi)
        print(f"Device {address}: RSSI={adv.rssi}, Distance={distance:.2f}m")
        if distance <= max_distance:
            nearby.add(address)
            print(f"  -> Added to nearby (within {max_distance}m)")

    num_people = math.ceil(len(nearby) / 2.0)
    print(f"Nearby devices: {len(nearby)}, Estimated people: {num_people}")

    return {
        "devices_within_range": len(nearby),
        "estimated_people": num_people,
        "max_distance": max_distance,
        "device_addresses": list(nearby)
    }

@app.route("/scan", methods=["GET"])
def scan():
    try:
        max_distance = float(request.args.get("max_distance", 5))
    except ValueError:
        return jsonify({"error": "Invalid max_distance"}), 400
    
    result = asyncio.run(scan_ble(max_distance))
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="172.20.10.5", port=8000, debug=True)
