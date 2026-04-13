import pyziotc
import json
import time

prefix = "43"

def passthru_callback(msg_in):
    """Handle configuration commands"""
    global prefix
    parts = msg_in.split(b" ")  # Split on bytes, not string
    print(parts)

    if parts[0] == b"prefix":  # Compare with bytes
        if len(parts) == 1:
            response = "prefix set to {}".format(prefix)
            response = bytearray(response, 'utf-8')
        else:
            prefix = parts[1].decode('utf-8')  # Decode bytes to string
            response = "prefix set to {}".format(prefix)
            response = bytearray(response, 'utf-8')
    else:
        response = b"unrecognized command"

    return response

def new_msg_callback(msg_type, msg_in):
    """Process tag data"""
    if msg_type == pyziotc.MSG_IN_JSON:  # Correct constant
        msg_in_json = json.loads(msg_in)
        tag_id_hex = msg_in_json["data"]["idHex"]

        if tag_id_hex.startswith(prefix):
            # Forward filtered data
            z.send_next_msg(pyziotc.MSG_OUT_DATA, bytearray(msg_in, 'utf-8'))

# Initialize Ziotc object - use consistent variable name 'z'
z = pyziotc.Ziotc()
z.reg_new_msg_callback(new_msg_callback)
z.reg_pass_through_callback(passthru_callback)

# LED state definitions
led_green_msg = bytearray(json.dumps({"type":"LED","color":"GREEN","led":3}), "utf-8")
led_yellow_msg = bytearray(json.dumps({"type":"LED","color":"AMBER","led":3}), "utf-8")
led_red_msg = bytearray(json.dumps({"type":"LED","color":"RED","led":3}), "utf-8")

# Async management event messages
async_msg_red = bytearray(json.dumps({"source":"Sample DA app","message":"LED set to RED"}), "utf-8")
async_msg_green = bytearray(json.dumps({"source":"Sample DA app","message":"LED set to GREEN"}), "utf-8")
async_msg_yellow = bytearray(json.dumps({"source":"Sample DA app","message":"LED set to YELLOW"}), "utf-8")

# Main loop - cycle LED colors and send management events
while True:
    time.sleep(5)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_green_msg)
    z.send_next_msg(pyziotc.MSG_OUT_CTRL, async_msg_green)
    time.sleep(5)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_red_msg)
    z.send_next_msg(pyziotc.MSG_OUT_CTRL, async_msg_red)
    time.sleep(5)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_yellow_msg)
    z.send_next_msg(pyziotc.MSG_OUT_CTRL, async_msg_yellow)
