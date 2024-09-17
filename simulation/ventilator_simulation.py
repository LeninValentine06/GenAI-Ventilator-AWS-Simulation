from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define AWS IoT Core endpoint and MQTT connection parameters
ENDPOINT = "your-iot-endpoint"  # Replace with your AWS IoT Core endpoint
CLIENT_ID = "DorionDevice"  # Replace with your client ID

# Paths to your certificate, private key, and Amazon root CA
PATH_TO_CERTIFICATE = r"/path/to/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = r"/path/to/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = r"/path/to/AmazonRootCA1.pem"

# MQTT topic and message settings
TOPIC = "dorion/temperature"  # Replace with your desired topic
RANGE = 10  # Number of messages to publish

# Spin up necessary AWS IoT MQTT resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

# Create MQTT connection
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERTIFICATE,
    pri_key_filepath=PATH_TO_PRIVATE_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6
)

# Connect to AWS IoT Core
print(f"Connecting to {ENDPOINT} with client ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# Publish messages to the topic
print('Begin Publish')
for i in range(RANGE):
    # Create temperature data payload for each publish
    temperature_data = {"TEMPERATURE": i + 1}
    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(temperature_data),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print(f"Published: '{json.dumps(temperature_data)}' to the topic: '{TOPIC}'")
    t.sleep(0.1)  # Delay between messages

print('Publish End')

# Disconnect from AWS IoT Core
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
