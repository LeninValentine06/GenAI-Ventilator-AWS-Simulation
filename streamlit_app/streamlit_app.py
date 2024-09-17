import streamlit as st
import websocket
import json
import threading
import queue

# WebSocket URL
WS_URL = "your-websocket-url"

# Initialize session state
if 'temperature' not in st.session_state:
    st.session_state.temperature = None

if 'raw_message' not in st.session_state:
    st.session_state.raw_message = None

# Create a queue for thread-safe communication
message_queue = queue.Queue()

def is_valid_json(data):
    """Function to validate the format of the received JSON message."""
    required_keys = ["temperature"]
    return all(key in data for key in required_keys)

def on_message(ws, message):
    try:
        # Parse the outer message as JSON
        outer_data = json.loads(message)
        # Add message to the queue
        message_queue.put(outer_data)
    except json.JSONDecodeError as e:
        st.error(f"Received malformed JSON: {e}")

def on_error(ws, error):
    st.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    st.warning(f"WebSocket connection closed: {close_status_code}, {close_msg}")

def on_open(ws):
    st.success("WebSocket connection established")

def websocket_thread():
    """Function to start the WebSocket connection in a separate thread."""
    ws = websocket.WebSocketApp(WS_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

def main():
    st.title("IoT Data Monitor")

    # Start WebSocket connection in a separate thread if not already started
    if 'websocket_started' not in st.session_state:
        st.session_state.websocket_started = True
        threading.Thread(target=websocket_thread, daemon=True).start()

    # Check for new messages and update session state
    while not message_queue.empty():
        outer_data = message_queue.get()
        if 'message' in outer_data:
            try:
                inner_message = json.loads(outer_data['message'])
                if is_valid_json(inner_message):
                    st.session_state.temperature = inner_message['temperature']
                    st.session_state.raw_message = outer_data
                else:
                    st.error("Invalid JSON format received in 'message' field")
            except json.JSONDecodeError as e:
                st.error(f"Received malformed JSON in 'message' field: {e}")
        else:
            st.error("No 'message' field in the received data")

    # Display raw JSON message
    if st.session_state.raw_message is not None:
        st.subheader("Raw Incoming JSON")
        st.write("Raw JSON as dictionary:")
        st.write(st.session_state.raw_message)
        st.write("Raw JSON as string:")
        st.write(json.dumps(st.session_state.raw_message, indent=4))

    # Display temperature
    if st.session_state.temperature is not None:
        st.metric("Temperature", f"{st.session_state.temperature}°C")
    else:
        st.text("Waiting for temperature data...")

    # Add a manual refresh button (optional)
    if st.button("Refresh"):
        st.rerun()

if __name__ == "__main__":
    main()
