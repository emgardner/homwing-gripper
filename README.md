# Homwing Gripper

A Python library for controlling Homwing electric grippers using Modbus RTU communication protocol.

## Features

- Asynchronous control of Homwing electric grippers
- Comprehensive status monitoring
- Fault detection and reporting
- Precise position control
- Speed and force control
- Voltage and temperature monitoring

## Installation

```bash
pip install homwing-gripper
```

## Requirements

- Python >= 3.13
- pydantic >= 2.11.3
- pymodbus >= 3.9.1
- pyserial >= 3.5

## Quick Start

```python
import asyncio
from pymodbus.client.serial import AsyncModbusSerialClient
from homwing_gripper import HomwingGripper

async def main():
    # Create a Modbus RTU client
    client = AsyncModbusSerialClient(
        port="/dev/ttyUSB0",  # Adjust to your serial port
        baudrate=115200,
        bytesize=8,
        parity="N",
        stopbits=1,
    )

    # Connect to the client
    await client.connect()

    # Create a gripper instance (address 1)
    gripper = HomwingGripper(client, address=1)

    try:
        # Activate the gripper
        await gripper.activate()
        await gripper.wait_for_activation()

        # Set speed and force
        await gripper.set_speed_force(speed=100, force=50)

        # Move to position (0-255)
        await gripper.move_to_position(position=128)
        await gripper.wait_for_move()

        # Read status
        status = await gripper.read_gripper_status()
        print(f"Gripper status: {status}")

        # Read voltage and temperature
        voltage_temp = await gripper.read_voltage_temperature()
        print(f"Voltage: {voltage_temp.voltage}V, Temperature: {voltage_temp.temperature}°C")

    finally:
        # Stop the gripper
        await gripper.stop()
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Gripper Control

- `activate()`: Enable the gripper
- `stop()`: Stop the gripper
- `move_to_position(position: int)`: Move to a specific position (0-255)
- `set_speed_force(speed: int, force: int)`: Set speed and force parameters
- `execute_move()`: Execute the movement with current parameters
- `wait_for_move()`: Wait until movement is complete
- `wait_for_activation()`: Wait until gripper is activated

### Status Monitoring

- `read_gripper_status()`: Get current gripper status
- `read_fault_position()`: Get fault status and position
- `read_speed_force()`: Get current speed and force
- `read_voltage_temperature()`: Get voltage and temperature readings
- `read_software_version()`: Get software version information

### Status Models

- `GripperStatus`: Current gripper state
- `GripperFaultStatus`: Fault conditions
- `VoltageTemperature`: Voltage and temperature readings
- `SpeedForce`: Current speed and force settings

## Error Handling

The library provides comprehensive fault detection through the `GripperFaultStatus` model, which includes:

- Control command errors
- Communication faults
- Overcurrent conditions
- Voltage abnormalities
- Enabling errors
- Overtemperature conditions
- Self-fault detection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
