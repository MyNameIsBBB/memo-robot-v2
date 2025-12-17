# MEMO-BOT Client

This folder contains the client-side code to run on the Robot (Raspberry Pi or Laptop connected to Arduino).

## Structure

-   `robot_client.py`: Main entry point. Connects to server, manages data flow.
-   `config.py`: Configuration settings (IP, Ports, Camera settings).
-   `services/`:
    -   `serial_manager.py`: Handles Arduino Serial communication.
    -   `camera_manager.py`: Handles Webcam capture and optimization.

## Setup

1. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Check Configuration**
   Open `config.py` and set:

    - `SERVER_IP`: IP of the Server PC.
    - `SERIAL_PORT_NAME`: Your Arduino port.

3. **Run Client**
    ```bash
    python robot_client.py
    ```
    _Note: Ensure you are in the `client` directory._

## Arduino Command Map

The client expects the Server to send these strings, which are forwarded to Serial:

-   `WALK_FORWARD`
-   `WALK_BACKWARD`
-   `TURN_LEFT`
-   `TURN_RIGHT`
-   `STOP`
