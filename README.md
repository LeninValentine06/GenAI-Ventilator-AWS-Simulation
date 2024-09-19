# GenAI-Ventilator-AWS-Simulation

This project demonstrates an IoT-based temperature monitoring system using AWS IoT Core. The system collects temperature data and publishes it to an MQTT topic using secure communication with AWS services.

## Features
- **MQTT Connection**: Secure connection to AWS IoT Core using Mutual TLS authentication.
- **Temperature Data Publishing**: Sends simulated temperature data to an MQTT topic on AWS IoT.
- **AWS IoT Integration**: The system utilizes AWS IoT services to enable real-time data transmission.
  
## Project Structure

```bash
GenAI-Ventilator-AWS-Simulation/
  │───README.md
  │
  │───ESP32_prototype.ino
  │
  ├───lambda
  │       sendmessage.py
  │       TemperatureDataProcessor.py
  │       WebSocketConnect.py
  │       WebSocketDisconnect.PY
  │
  ├───simulation
  │       ventilator_simulation.py
  │
  └───streamlit_app
          streamlit_app.py
```


## Prerequisites

To run this project, ensure you have the following:

1. **AWS IoT Core Account**:
   - Set up an AWS IoT Core account if you don't have one.
   - Create a Thing and generate the necessary credentials (X.509 client certificate and private key).
   - Download the Amazon Root CA certificate.

2. **AWS IoT Device Credentials**:
   - Obtain the following files from AWS IoT:
     - **Client Certificate** (`certificate.pem.crt`)
     - **Private Key** (`private.pem.key`)
     - **Amazon Root CA Certificate** (`AmazonRootCA1.pem`)

3. **Python 3.6+**:
   - Ensure Python 3.6 or higher is installed on your machine.

4. **AWS IoT SDK for Python**:
   - Install the required AWS IoT SDK by running:
     ```bash
     pip install awsiotsdk awscrt
     ```

5. **Streamlit**:
   - Install Streamlit for the web dashboard:
     ```bash
     pip install streamlit
     ```

## Setup

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/GenAI-Ventilator-AWS-Simulation.git 
    ```

2. Navigate to the project directory:
     ```bash
     cd GenAI-Ventilator-AWS-Simulation
    ```

3. Update the ventilator_simulation.py script with your AWS IoT Core details:

    Replace `ENDPOINT` with your AWS IoT Core endpoint.
    Set `CLIENT_ID` with a unique client ID for your device.
    Provide the correct file paths for `PATH_TO_CERTIFICATE`, `PATH_TO_PRIVATE_KEY`, and `PATH_TO_AMAZON_ROOT_CA_1`.

4. Place your AWS IoT credentials (certificate, private key, and root CA) in the certificates folder.

5. Deploy AWS Lambda functions:
        - WebSocketConnect.py: Handles new WebSocket connections.
        - WebSocketDisconnect.py: Handles WebSocket disconnections.
        - TemperatureDataProcessor.py: Processes incoming temperature data.
        - sendmessage.py: Sends messages via WebSocket.

## Streamlit Application Setup

1. Navigate to the `streamlit_app/` directory:
   ```bash
   cd streamlit_app
   ```
2. Run the Streamlit app to visualize the ventilator data:
    ```bash
    streamlit run streamlit_app.py
    ```
3. Open your web browser and navigate to the local Streamlit server (typically http://localhost:8501). You will be able to see real-time ventilator data visualized.

## Running the Project

1. To start publishing temperature data to AWS IoT, run the following command:

    ```bash
    python ventilator_simulation.py
    ```
     The script will simulate ventilator readings and publish them to the MQTT topic on AWS IoT.

2. Simultaneously, launch the Streamlit app to visualize the data in real-time:

    ```bash
    streamlit run streamlit_app/streamlit_app.py
    ```
3. Open the displayed URL (usually http://localhost:8501) in your browser to view the real-time dashboard, which shows:
        - Temperature Data: Real-time graphs of the temperature readings.
        - System Metrics: Other relevant metrics from the ventilator simulation.

## ESP32 Prototype
Circuit Diagram
![image](https://github.com/user-attachments/assets/b1360a70-c371-453e-8fbe-706e1e438967)

