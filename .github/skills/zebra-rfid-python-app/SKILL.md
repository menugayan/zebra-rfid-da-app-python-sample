---
name: zebra-rfid-python-app
description: 'Create Zebra Data Analytics (DA) applications for RFID readers using Python and pyziotc module. Use when: developing RFID DA apps, filtering tag data, controlling reader hardware (LED/GPO/GPI), processing RFID messages, configuring reader via pass-through callbacks, sending management events, integrating with Zebra IoT Connector.'
argument-hint: 'Describe the DA app functionality (e.g., filter tags, control LED, handle GPI events)'
---

# Zebra RFID Python Data Analytics App Development

Create Python-based Data Analytics (DA) applications for Zebra RFID readers using the `pyziotc` (Zebra IoT Connector) module. These apps run directly on the reader to filter, analyze, and act on RFID tag data.

## When to Use

- **Developing RFID DA applications** on Zebra readers
- **Filtering tag data** before sending to gateway
- **Controlling hardware**: LEDs, GPOs, or monitoring GPIs
- **Processing RFID messages** (tag reads, GPI events)
- **Configuring apps** via pass-through callbacks
- **Managing reader** via local REST APIs
- **Sending asynchronous events** to management interfaces

## Core Architecture

DA apps sit between Radio Control (tag reader) and Reader Gateway (network interface):

```
Radio Control → DA Python App → Reader Gateway → Cloud/Network
```

## Minimal App Structure

Every DA app requires these three core steps:

### 1. Define New Message Callback

This function processes all incoming tag data and GPI events:

```python
def new_msg_callback(msg_type, msg_in):
    """
    Called when new messages arrive from Radio Control.
    
    Args:
        msg_type: pyziotc.MSG_IN_JSON (tag data) or pyziotc.MSG_IN_GPI (GPI event)
        msg_in: bytearray containing the message
    """
    if msg_type == pyziotc.MSG_IN_JSON:
        # Process tag data
        msg_in_json = json.loads(msg_in)
        tag_id = msg_in_json["data"]["idHex"]
        
        # Example: filter and forward
        if tag_id.startswith("38"):
            z.send_next_msg(pyziotc.MSG_OUT_DATA, 
                          bytearray("Filtered: " + msg_in, 'utf-8'))
    
    elif msg_type == pyziotc.MSG_IN_GPI:
        # Process GPI event
        print("GPI event received:", msg_in)
```

### 2. Create Ziotc Object

Opens connections to IoT Connector components:

```python
import pyziotc
import json

z = pyziotc.Ziotc()
```

### 3. Register Callback

Registers your callback function:

```python
z.reg_new_msg_callback(new_msg_callback)
```

**Note**: Unlike legacy module, `loop.run_forever()` is NOT required.

## Message Types Reference

### Input Message Types

| Type | Value | Description | Format |
|------|-------|-------------|--------|
| `MSG_IN_JSON` | 0 | Tag information | JSON (decoded from bytearray) |
| `MSG_IN_GPI` | 6 | GPI event | JSON (decoded from bytearray) |

**Tag JSON Structure**:
```json
{
  "data": {
    "idHex": "E2003412A45E5E2001820000",
    "rssi": -45,
    "antenna": 1,
    ...
  }
}
```

### Output Message Types

Send messages using `z.send_next_msg(msg_type, msg_out)`:

| Type | Value | Description | Destination |
|------|-------|-------------|-------------|
| `MSG_OUT_DATA` | 3 | Tag/filtered data | Reader Gateway → Data Interface |
| `MSG_OUT_CTRL` | 4 | Management events | Reader Gateway → Management Interface |
| `MSG_OUT_GPO` | 5 | Hardware control | GPO/LED control |

## Common Patterns

### Pattern 1: Tag Filtering by Prefix

```python
import pyziotc
import json

prefix = "E200"  # EPC prefix to filter

def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_JSON:
        msg_in_json = json.loads(msg_in)
        tag_id_hex = msg_in_json["data"]["idHex"]
        
        if tag_id_hex.startswith(prefix):
            z.send_next_msg(pyziotc.MSG_OUT_DATA, 
                          bytearray(msg_in, 'utf-8'))

z = pyziotc.Ziotc()
z.reg_new_msg_callback(new_msg_callback)
```

### Pattern 2: Pass-Through Configuration

Enables runtime configuration via Management Command/Response interface:

```python
def passthru_callback(msg_in):
    """
    Processes configuration commands sent to the DA app.
    MUST return a bytearray response.
    """
    global prefix
    parts = msg_in.split(b" ")
    
    if parts[0] == b"prefix":
        if len(parts) == 1:
            # Query current value
            response = f"prefix set to {prefix}"
        else:
            # Update value
            prefix = parts[1].decode('utf-8')
            response = f"prefix updated to {prefix}"
        return bytearray(response, 'utf-8')
    else:
        return b"unrecognized command"

z.reg_pass_through_callback(passthru_callback)
```

### Pattern 3: LED Control

Control reader LED (LED 3 is the App LED):

```python
import time

# Define LED states
led_green = bytearray(json.dumps({
    "type": "LED",
    "color": "GREEN",
    "led": 3
}), "utf-8")

led_red = bytearray(json.dumps({
    "type": "LED",
    "color": "RED",
    "led": 3
}), "utf-8")

led_amber = bytearray(json.dumps({
    "type": "LED",
    "color": "AMBER",
    "led": 3
}), "utf-8")

# Cycle colors
while True:
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_green)
    time.sleep(1)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_red)
    time.sleep(1)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_amber)
    time.sleep(1)
```

**Available Colors**: `GREEN`, `RED`, `AMBER`, `OFF`  
**Controllable LED**: Only LED 3 (App LED)

### Pattern 4: GPO Control

Control General Purpose Outputs:

```python
# Define GPO states
gpo_high = bytearray(json.dumps({
    "type": "GPO",
    "state": "HIGH",
    "pin": 1
}), "utf-8")

gpo_low = bytearray(json.dumps({
    "type": "GPO",
    "state": "LOW",
    "pin": 1
}), "utf-8")

# Toggle GPO
while True:
    z.send_next_msg(pyziotc.MSG_OUT_GPO, gpo_high)
    time.sleep(1)
    z.send_next_msg(pyziotc.MSG_OUT_GPO, gpo_low)
    time.sleep(1)
```

### Pattern 5: GPI Event Monitoring

Receive notifications when GPI pins change state:

```python
def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_GPI:
        gpi_event = json.loads(msg_in)
        print("GPI event:", gpi_event)
        # Process GPI state change

z = pyziotc.Ziotc()
z.enableGPIEvents()  # Enable GPI notifications
z.reg_new_msg_callback(new_msg_callback)
```

### Pattern 6: Asynchronous Management Events

Send custom events to management interface:

```python
import time

# Create custom event
version_msg = bytearray(json.dumps({
    "source": "My DA App",
    "version": "1.0",
    "timestamp": time.time(),
    "message": "App started"
}), "utf-8")

z.send_next_msg(pyziotc.MSG_OUT_CTRL, version_msg)
```

### Pattern 7: Reader Control via REST API

Control reader using local REST APIs:

```python
import http.client
from http.client import HTTPConnection

# Query reader status
c = HTTPConnection("127.0.0.1")
c.request('GET', '/cloud/status')
res = c.getresponse()
data = res.read()
print(data)

# Additional REST endpoints available for:
# - Starting/stopping reads
# - Configuring antennas
# - Setting RF power
# - Accessing reader settings
```

**REST API Documentation**: See [Local REST APIs](https://zebradevs.github.io/rfid-ziotc-docs/api_ref/local_rest/index.html)

## Complete Example: Production-Ready DA App

Combines filtering, LED control, pass-through config, and management events:

```python
import pyziotc
import json
import time

# Global configuration
prefix = "E200"

def passthru_callback(msg_in):
    """Handle configuration commands"""
    global prefix
    parts = msg_in.split(b" ")
    
    if parts[0] == b"prefix":
        if len(parts) == 1:
            response = f"prefix={prefix}"
        else:
            prefix = parts[1].decode('utf-8')
            response = f"prefix updated to {prefix}"
        return bytearray(response, 'utf-8')
    
    return b"Unknown command. Available: prefix [value]"

def new_msg_callback(msg_type, msg_in):
    """Process tag data and GPI events"""
    if msg_type == pyziotc.MSG_IN_JSON:
        msg_in_json = json.loads(msg_in)
        tag_id_hex = msg_in_json["data"]["idHex"]
        
        # Filter tags by prefix
        if tag_id_hex.startswith(prefix):
            # Forward filtered data
            z.send_next_msg(pyziotc.MSG_OUT_DATA, 
                          bytearray(msg_in, 'utf-8'))
            
            # Flash LED green on match
            z.send_next_msg(pyziotc.MSG_OUT_GPO, led_green)
        else:
            # Flash LED red on reject
            z.send_next_msg(pyziotc.MSG_OUT_GPO, led_red)
    
    elif msg_type == pyziotc.MSG_IN_GPI:
        # Log GPI events
        event_msg = bytearray(json.dumps({
            "source": "DA App",
            "type": "GPI_EVENT",
            "data": json.loads(msg_in)
        }), "utf-8")
        z.send_next_msg(pyziotc.MSG_OUT_CTRL, event_msg)

# LED state definitions
led_green = bytearray(json.dumps({
    "type": "LED", "color": "GREEN", "led": 3
}), "utf-8")

led_red = bytearray(json.dumps({
    "type": "LED", "color": "RED", "led": 3
}), "utf-8")

led_amber = bytearray(json.dumps({
    "type": "LED", "color": "AMBER", "led": 3
}), "utf-8")

# Initialize
z = pyziotc.Ziotc()
z.enableGPIEvents()
z.reg_new_msg_callback(new_msg_callback)
z.reg_pass_through_callback(passthru_callback)

# Send startup notification
startup_msg = bytearray(json.dumps({
    "source": "DA App",
    "event": "STARTED",
    "config": {"prefix": prefix}
}), "utf-8")
z.send_next_msg(pyziotc.MSG_OUT_CTRL, startup_msg)

# Heartbeat LED (runs in main thread)
while True:
    z.send_next_msg(pyziotc.MSG_OUT_GPO, led_amber)
    time.sleep(2)
```

## Development Workflow

1. **Write the Python script** following the patterns above
2. **Package the app** for deployment (see packaging section below)
3. **Upload to reader** via web interface or REST API
4. **Test filtering and hardware control**
5. **Configure via pass-through** commands as needed
6. **Monitor management events** for diagnostics

## Packaging for FX Series Readers

Python DA apps must be packaged as Debian (.deb) packages for deployment to FX Series readers. There are two types of packages:

### Python DA Package Structure

For **Python Data Analytics apps** (like the ones created with this skill):

**Requirements**:
1. **Package name**: Use hyphens, not underscores (e.g., `sample-filter` not `sample_filter`)
2. **Python script**: The `.py` file (e.g., `sample_filter.py`)
3. **Start script**: `start_<appname>.sh` that invokes `python3 /apps/<appname>.py &`
4. **Stop script**: `stop_<appname>.sh` that kills the Python process
5. **DEBIAN/control**: Metadata file with `APP_TYPE: DA` field
6. **Execution**: Runs with `rfidadm` user privileges (non-root)

**Directory Structure** (for app named `sample-filter`):
```
sample-filter_1.0.0/
├── DEBIAN/
│   └── control              (Package metadata)
├── sample_filter.py         (Your Python DA app)
├── start_sample-filter.sh   (Starts: python3 /apps/sample_filter.py &)
└── stop_sample-filter.sh    (Kills Python process)
```

**Control File Requirements**:
```
Package: sample-filter       # Hyphens only, matches folder name
Version: 1.0.0              # Semantic versioning
Source: base
Priority: optional
Architecture: all           # Python is platform-independent
Maintainer: Your Name
Description: Brief description of DA app functionality
APP_TYPE: DA               # REQUIRED for Data Analytics apps
                           # Must end with newline
```

### Binary Executable Package Structure (Reference)

For **compiled binary apps** (not typical for DA apps):

1. **Binary executable**: ELF 32-bit LSB executable, ARM, version 1, GNU/Linux compatible
2. **Binary name**: Must match package name (e.g., package `myapp-1` requires binary `myapp-1`)
3. **Start script**: `start_myapp-1.sh` to launch the binary
4. **Stop script**: `stop_myapp-1.sh` to terminate the binary
5. **Execution**: Runs with `rfidadm` user privileges (limited, non-root)

### Critical Packaging Rules

- ✅ **Package name**: Use lowercase alphanumeric + hyphens only (e.g., `tag-filter`, `led-controller`)
- ❌ **No underscores**: `sample_filter` will fail, use `sample-filter`
- ✅ **Script naming**: `start_<package-name>.sh` and `stop_<package-name>.sh` must match package name
- ✅ **DEBIAN permissions**: Directory must be `0755`, not `777`
- ✅ **File location**: Apps install to `/apps/` directory on reader
- ✅ **User context**: Apps run as `rfidadm` user (not root), limited privileges
- ✅ **Final newline**: Control file must end with a newline after `APP_TYPE: DA`

### Building the Package

**On Windows (WSL Required)**:
```bash
# Copy to WSL filesystem (fixes permission issues)
wsl bash -c "rm -rf ~/myapp_1.0.0 && cp -r /mnt/c/path/to/myapp_1.0.0 ~/ && cd ~ && chmod 0755 myapp_1.0.0/DEBIAN && chmod +x myapp_1.0.0/*.sh && dpkg-deb --build -Zgzip myapp_1.0.0/ && cp myapp_1.0.0.deb /mnt/c/path/to/output/"
```

**On Linux**:
```bash
chmod 0755 myapp_1.0.0/DEBIAN
chmod +x myapp_1.0.0/*.sh
dpkg-deb --build -Zgzip myapp_1.0.0/
```

### Common Packaging Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "package name has characters that aren't lowercase alphanums or '-+.'" | Underscore in package name | Use hyphens: `sample-filter` not `sample_filter` |
| "missing final newline" | Control file doesn't end with newline | Add blank line at end of control file |
| "bad permissions 777" | DEBIAN directory has wrong permissions | Run on WSL filesystem, or `chmod 0755 DEBIAN` |
| "rfidadm user cannot execute" | Script needs execute permissions | `chmod +x start_*.sh stop_*.sh` |

### Package Naming Examples

**Correct**:
- `tag-filter_1.0.0.deb` → Package: `tag-filter`
- `led-controller_2.1.3.deb` → Package: `led-controller`
- `inventory-app_1.0.0.deb` → Package: `inventory-app`

**Incorrect**:
- `tag_filter_1.0.0.deb` → ❌ Underscores not allowed
- `TagFilter_1.0.0.deb` → ❌ Uppercase not allowed
- `tag filter_1.0.0.deb` → ❌ Spaces not allowed

### rfidadm User Privileges

Python DA apps run with `rfidadm` user account, which has:

✅ **Allowed**:
- Read/write to `/apps/` directory
- Network access (HTTP, MQTT, cloud connections)
- Local REST API calls to `127.0.0.1`
- LED and GPO control via pyziotc
- GPI event monitoring
- File I/O in `/apps/` and `/tmp/`

❌ **Not Allowed**:
- Root/sudo access
- System configuration changes
- Direct hardware access (use pyziotc APIs instead)
- Modifying system files outside `/apps/`

## Important Notes

- **All messages are bytearrays**: Always encode strings with `bytearray(text, 'utf-8')`
- **JSON parsing required**: Incoming messages must be decoded with `json.loads()`
- **Pass-through must return**: The callback MUST return a bytearray response
- **LED 3 only**: Only LED 3 (App LED) can be controlled by user apps
- **No loop.run_forever()**: Not required in current pyziotc module
- **Local REST API**: Use `127.0.0.1` for local reader control
- **Resident modules**: `pyziotc`, `json`, `time`, `http.client` are available on reader

## Quick Reference Checklist

When creating a DA app, ensure:

- [ ] Import `pyziotc` and `json`
- [ ] Define `new_msg_callback(msg_type, msg_in)` with proper handling for `MSG_IN_JSON` and optionally `MSG_IN_GPI`
- [ ] Create `Ziotc()` object
- [ ] Register callback with `reg_new_msg_callback()`
- [ ] Use `send_next_msg()` to output filtered data
- [ ] If using GPI: call `enableGPIEvents()`
- [ ] If using config: define and register `passthru_callback()` that returns bytearray
- [ ] All message payloads are bytearrays
- [ ] LED control uses LED 3 only
- [ ] Test with actual reader hardware

## Additional Resources

- **Full Documentation**: [Zebra IoT Connector Docs](https://zebradevs.github.io/rfid-ziotc-docs/)
- **Python API Reference**: [API Docs](https://zebradevs.github.io/rfid-ziotc-docs/user_apps/python/api_ref.html)
- **Local REST APIs**: [REST Interface](https://zebradevs.github.io/rfid-ziotc-docs/api_ref/local_rest/index.html)
- **Packaging & Deployment**: [Deployment Guide](https://zebradevs.github.io/rfid-ziotc-docs/user_apps/packaging_and_deployment.html)
- **Management Events Schema**: [Event Formats](https://zebradevs.github.io/rfid-ziotc-docs/schemas/async_event_schema/index.html)
- **Tag Data Events**: [Tag Schemas](https://zebradevs.github.io/rfid-ziotc-docs/schemas/tag_data_events/index.html)

## Example Prompts

Try these prompts to use this skill:

- "Create a Zebra DA app that filters tags starting with '3008'"
- "Write a Python RFID app that controls the LED based on tag RSSI values"
- "Build a DA app with pass-through configuration for dynamic prefix filtering"
- "Generate a Zebra RFID app that monitors GPI events and sends alerts"
- "Create a production DA app with filtering, LED control, and management events"
