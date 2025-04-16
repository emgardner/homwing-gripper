from pymodbus.client.serial import AsyncModbusSerialClient
from homwing_gripper import HomwingGripper
import asyncio
import logging
import sys

from homwing_gripper.core import GOBJ, ControlRegister, GSTA


logging.basicConfig(
    level=logging.DEBUG,  # or DEBUG, WARNING, etc.
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Usage
logger = logging.getLogger(__name__)
logger.info("Gripper initialized")


async def main() -> None:
    client = AsyncModbusSerialClient(
        "/dev/tty.usbserial-B001K430", baudrate=115200, timeout=1, retries=0
    )
    await client.connect()
    gripper = HomwingGripper(client, 9)
    #print("", await gripper.read_gripper_status())
    #print("", await gripper.read_fault_position())
    #print("", await gripper.read_speed_force())
    #print("", await gripper.read_voltage_temperature())
    #print("", await gripper.read_software_version())


    await gripper.clear_control_register()
    await gripper.activate()
    while True:
        result = await gripper.read_gripper_status()
        if result.gSTA == GSTA.ACTIVATED:
            break
        await asyncio.sleep(.1)
    await gripper.set_speed_force(255, 20)
    await gripper.move_to_position(0)
    await gripper.wait_for_move()
    await gripper.move_to_position(100)
    await gripper.wait_for_move()
    await gripper.move_to_position(0)
    await gripper.wait_for_move()
    for i in range(0, 255):
        print(i)
        await gripper.move_to_position(i)
        await gripper.wait_for_move()
        input()
    await gripper.move_to_position(0)
    await gripper.wait_for_move()



if __name__ == "__main__":
    asyncio.run(main())
