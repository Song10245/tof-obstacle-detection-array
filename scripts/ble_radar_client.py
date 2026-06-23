#!/usr/bin/env python3
"""BLE radar visualisation template for a 10-sensor ToF ring.

Replace DEVICE_NAME and CHAR_UUID with your public-safe identifiers or pass them
through environment variables.
"""

import asyncio
import os
import numpy as np
import matplotlib.pyplot as plt
from bleak import BleakClient, BleakScanner

DEVICE_NAME = os.getenv("TOF_DEVICE_NAME", "VL53L1X_ToF_Array")
CHAR_UUID = os.getenv("TOF_CHAR_UUID", "00000000-0000-0000-0000-000000000000") # Public-safe example values. Replace using environment variables for real hardware.
NUM_SENSORS = 10

fig = None
ax = None


def parse_packet(data: bytearray):
    """Parse packet into millimetre readings.

    This template supports comma-separated text packets such as:
    b"100,120,130,140,150,160,170,180,190,200"
    """
    try:
        values = [float(x) for x in data.decode().strip().split(',')]
    except Exception:
        return None
    if len(values) != NUM_SENSORS:
        return None
    return values


def update_plot(values):
    global fig, ax
    angles = np.linspace(0, 2 * np.pi, NUM_SENSORS, endpoint=False)
    vals = np.asarray(values, dtype=float)
    angles = np.r_[angles, angles[0]]
    vals = np.r_[vals, vals[0]]

    if fig is None or ax is None:
        fig, ax = plt.subplots(subplot_kw={"polar": True})
    ax.clear()
    ax.set_title("ToF obstacle distance ring")
    ax.set_yticklabels([])
    ax.plot(angles, vals, lw=2)
    ax.fill(angles, vals, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([f"{int(np.rad2deg(a))}°" for a in angles[:-1]])
    plt.pause(0.01)


def notification_handler(_, data):
    values = parse_packet(data)
    if values is not None:
        update_plot(values)


async def main():
    devices = await BleakScanner.discover()
    target = next((d for d in devices if d.name == DEVICE_NAME), None)
    if target is None:
        raise RuntimeError(f"Device {DEVICE_NAME!r} not found")
    async with BleakClient(target.address) as client:
        await client.start_notify(CHAR_UUID, notification_handler)
        while True:
            await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
