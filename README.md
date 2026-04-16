# Zebra RFID Reader Applications - Complete Guide

> **🤖 GitHub Copilot Users:** This repo includes custom agents and skills to streamline Zebra RFID development! See [COPILOT_CUSTOMIZATIONS.md](COPILOT_CUSTOMIZATIONS.md) for setup and usage.

> **⚡ Quick Build:** See [Quick Build Commands](#quick-build-commands) section below for the working build command.

---

## 📚 Table of Contents

- [Overview](#overview)
- [FX Series Critical Requirements](#fx-series-critical-requirements)
- [DA App Example (sample-filter)](#da-app-example-sample-filter)
- [Non-DA App Example (hello-world)](#non-da-app-example-hello-world)
- [Building Packages](#building-packages)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Overview

This repository contains examples and tools for developing applications on Zebra FX Series RFID readers:

1. **Data Analytics (DA) Apps** - Process RFID tag data using the pyziotc module
2. **Non-DA Apps** - Standard Python background services for monitoring, integration, etc.

Both types are packaged as Debian (.deb) installers and deployed to the reader.

---

## ⚠️ FX Series Critical Requirements

**MUST FOLLOW** these naming and structure rules or your app **will not start**:

### 1. Package Name Must Use Hyphens

```
✅ CORRECT: sample-filter
❌ WRONG:   sample_filter
```

Package names can only contain lowercase letters, numbers, and hyphens (`-`). No underscores!

### 2. **Python Script Name Must Match Package Name** ⭐ CRITICAL

```
Package: sample-filter
Scripts: start_sample-filter.sh, stop_sample-filter.sh
Python:  sample-filter.py  ← Must match package name!
```

**Why This M atters:**
- The start script references `/apps/sample-filter.py`
- If your Python file is `sample_filter.py`, the app won't start
- This is **required by FX Series readers** for the app to show "green" (running) status

### 3. Script Names Must Match Package Name

```
Package: myapp
Required scripts:
  - start_myapp.sh
  - stop_myapp.sh
```

### 4. Control File Must End with Newline

The DEBIAN/control file **must** end with a blank line after the last field:

```
Package: sample-filter
Version: 1.0.0
...
APP_TYPE: DA
← BLANK LINE HERE (required)
```

### 5. Correct File Permissions

```bash
Scripts (.sh):  0755 (rwxr-xr-x) - Executable by all
Python (.py):   0644 (rw-r--r--) - Readable by all
DEBIAN folder:  0755 (rwxr-xr-x) - Accessible
```

**Building packages on Windows with WSL ensures these permissions are correct automatically.**

---

## 📱 DA App Example: sample-filter

**Purpose:** Process RFID tag data using the pyziotc module

### Package Contents

```
sample-filter_1.0.4/
├── DEBIAN/
│   └── control              # Has APP_TYPE: DA
├── sample-filter.py         # Python script (name matches package!)
├── start_sample-filter.sh   # Startup script
└── stop_sample-filter.sh    # Stop script
```

### Control File (DA App)

```
Package: sample-filter
Version: 1.0.4
Source: base
Priority: optional
Architecture: all
Maintainer: Zebra
Description: RFID tag filter DA app
APP_TYPE: DA                 ← Required for Data Analytics apps
                             ← Blank line required
```

### Features

- ✅ Filters RFID tags by prefix "43"
- ✅ Controls LED (GREEN → RED → AMBER cycling)
- ✅ Sends management events
- ✅ Pass-through configuration (`prefix` command)
- ✅ Processes tag data in real-time
- ✅ Connected to IoT Connector pipeline

### Code Structure

```python
import pyziotc
import json

def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_JSON:
        # Process tag data
        
z = pyziotc.Ziotc()
z.reg_new_msg_callback(new_msg_callback)
```

---

## 🔧 Non-DA App Example: hello-world

**Purpose:** Standard Python background service (no RFID processing)

### Package Contents

```
hello-world_1.0.0/
├── DEBIAN/
│   └── control              # NO APP_TYPE field!
├── hello-world.py           # Python script (name matches package!)
├── start_hello-world.sh     # Startup script
└── stop_hello-world.sh      # Stop script
```

### Control File (Non-DA App)

```
Package: hello-world
Version: 1.0.0
Source: base
Priority: optional
Architecture: all
Maintainer: Zebra
Description: Simple Hello World background service
                             ← NO APP_TYPE: DA
                             ← Blank line still required
```

### Features

- ✅ Prints "Hello World" every 10 seconds
- ✅ Logs to `/tmp/hello_world.log`
- ✅ No pyziotc dependency
- ✅ Can run any Python code
- ✅ Perfect for monitoring, APIs, file processing

### Code Structure

```python
import time
import datetime

def main():
    counter = 0
    while True:
        counter += 1
        print(f"Hello World! Counter: {counter}")
        time.sleep(10)

if __name__ == "__main__":
    main()
```

### Use Cases for Non-DA Apps

1. **System Monitoring** - Check disk space, CPU, memory
2. **External Integration** - Call REST APIs, send data to cloud
3. **File Processing** - Process logs, generate reports
4. **Custom Background Tasks** - Scheduled maintenance, cleanup
5. **Testing/Debugging** - Verify reader functionality

---

## 🆚 DA vs Non-DA Comparison

| Feature | DA App (sample-filter) | Non-DA App (hello-world) |
|---------|------------------------|-------------------------|
| **Control file** | Has `APP_TYPE: DA` | No APP_TYPE field |
| **Imports** | `import pyziotc` | Standard Python only |
| **Purpose** | Process RFID tag data | Any Python task |
| **Connected to** | Radio Control + Gateway | Standalone background service |
| **Tag data access** | ✅ Yes | ❌ No |
| **LED/GPO control** | ✅ Via pyziotc | ❌ No hardware access |
| **Use when** | Filtering tags, RFID logic | Monitoring, APIs, general tasks |
| **Complexity** | Medium (pyziotc API) | Low (standard Python) |

**Both types** follow the same FX Series requirements: hyphenated package names, matching Python filenames, proper permissions.

---

## 🔨 Building Packages

**IMPORTANT:** You're on Windows, so you need a Linux environment to run `dpkg-deb`.

### Quick Build Commands

**CRITICAL:** Package directory must use hyphen (sample-filter), and build must happen on WSL filesystem for proper permissions.

#### Option 1: WSL2 (Recommended)
```powershell
# From PowerShell in C:\DaAps
# Replace VERSION with your version number (e.g., 1.0.1, 1.0.2)
wsl bash -c "rm -rf ~/sample-filter_VERSION && cp -r /mnt/c/DaAps/sample-filter_VERSION ~/ && cd ~ && chmod 0755 sample-filter_VERSION/DEBIAN && chmod +x sample-filter_VERSION/*.sh && dpkg-deb --build -Zgzip sample-filter_VERSION/ && cp sample-filter_VERSION.deb /mnt/c/DaAps/"
```

**Example for version 1.0.1:**
```powershell
wsl bash -c "rm -rf ~/sample-filter_1.0.1 && cp -r /mnt/c/DaAps/sample-filter_1.0.1 ~/ && cd ~ && chmod 0755 sample-filter_1.0.1/DEBIAN && chmod +x sample-filter_1.0.1/*.sh && dpkg-deb --build -Zgzip sample-filter_1.0.1/ && cp sample-filter_1.0.1.deb /mnt/c/DaAps/"
```

#### Option 2: Docker
```powershell
# From PowerShell in C:\DaAps
# Replace VERSION with your version number
docker run --rm -v ${PWD}:/work ubuntu:latest bash -c "cd /work && apt-get update && apt-get install -y dpkg && chmod 0755 sample-filter_VERSION/DEBIAN && chmod +x sample-filter_VERSION/*.sh && dpkg-deb --build -Zgzip sample-filter_VERSION/"
```

**Result:** Creates `sample-filter_VERSION.deb` ready for deployment

### Why These Commands?

1. **WSL filesystem copy**: Fixes Windows permission issues (777 → 0755)
2. **Hyphenated name**: FX readers require hyphens, not underscores
3. **DEBIAN permissions**: Must be 0755 (not 777 from Windows)
4. **Script permissions**: Start/stop scripts need execute (+x)

## 🚀 Deployment Options

### 1. Web Console (Recommended for Production)

1. Open reader admin console: `http://<reader-ip>`
2. Navigate to **Applications** page
3. Click **Browse** and select `sample-filter_1.0.1.deb` (or your version)
4. Click **Install**
5. Click **Start** to run the application
6. Enable **AutoStart** for automatic startup on boot

### 2. SSH Deployment Script

```bash
# From WSL or Git Bash
chmod +x deploy.sh
./deploy.sh <reader-ip>

# Example:
./deploy.sh 192.168.1.100
```

The deploy.sh script will:
- Copy .deb to reader
- Install the package
- Restart userapps service
- Start your application

### 3. Manual SSH Deployment

```bash
# Copy package to reader (use your version)
scp sample-filter_1.0.1.deb rfidadm@<reader-ip>:/tmp/

# SSH into reader
ssh rfidadm@<reader-ip>

# Install package
sudo dpkg -i /tmp/sample-filter_1.0.1.deb

# Restart user apps service
sudo systemctl restart userapps
```

### 4. IoT Connector API

Use the `set_installUserapp` command via MQTT management interface:

```json
{
  "command": "set_installUserapp",
  "payload": {
    "appName": "sample-filter",
    "version": "1.0.1",
    "debFile": "<base64_encoded_deb>"
  }
}
```

**Note:** Use the hyphenated package name (sample-filter) as required by FX Series readers.

See: https://zebradevs.github.io/rfid-ziotc-docs/schemas/raw_mqtt_payloads/

## 🧪 Testing During Development

Use the test script to deploy just the Python file (without full packaging):

```bash
# From WSL or Git Bash
chmod +x test_on_reader.sh
./test_on_reader.sh <reader-ip>

# Then SSH to reader and run manually:
ssh rfidadm@<reader-ip>
cd /apps
python3 sample_filter.py
```

This is useful for rapid iteration before creating the final .deb package.

## 🔧 Application Features

This DA app demonstrates:

1. **Tag Filtering:** Filters RFID tags by prefix "43"
2. **LED Control:** Cycles through GREEN → RED → AMBER colors
3. **Management Events:** Sends async messages to IoT Connector
4. **Pass-through Commands:** Accepts "prefix" command to change filter dynamically

### Changing the Filter Prefix

From IoT Connector or management interface, send pass-through command:

```
prefix 30
```

Response: `prefix set to 30`

## 📊 Verifying Deployment

After deployment, check application status:

```bash
ssh rfidadm@<reader-ip>

# Check if app is running
ps aux | grep sample_filter.py

# View application logs (if configured)
tail -f /tmp/sample_filter.log

# Check userapps service status
sudo systemctl status userapps
```

## 🛠️ Troubleshooting

### App Shows "Stopped" (Red) Even Though Installed

**Most Common Cause:** Python script name doesn't match package name!

```bash
# SSH to reader and check
ssh rfidadm@<reader-ip>
ls -la /apps/

# If you see sample_filter.py but package is sample-filter:
# The app will NOT start!

# Fix: Rename the file
sudo mv /apps/sample_filter.py /apps/sample-filter.py

# Or rebuild the package with correct naming
```

**Why:** FX Series readers expect `/apps/<package-name>.py` to exist. The start script references this exact filename.

### App Shows "Failed" or Won't Start

**Check these in order:**

1. **Python script matches package name**
   ```bash
   # Package: sample-filter
   # Must have: /apps/sample-filter.py (not sample_filter.py)
   ```

2. **Scripts have execute permissions**
   ```bash
   ls -la /apps/*.sh
   # Should show: -rwxr-xr-x (not -rw-r-----)
   
   # Fix if needed:
   sudo chmod 755 /apps/start_*.sh /apps/stop_*.sh
   ```

3. **Check logs for actual error**
   ```bash
   # View userapps service logs
   journalctl -u userapps -n 100 --no-pager
   
   # Try running manually to see error
   cd /apps
   python3 <your-app>.py
   ```

4. **For DA apps: Check pyziotc is available**
   ```bash
   python3 -c "import pyziotc; print('pyziotc OK')"
   ```

### App not starting after installation

```bash
# Check system logs
ssh rfidadm@<reader-ip>
journalctl -u userapps -f
```

### Reinstalling the package

```bash
# Remove old version (use hyphenated package name)
ssh rfidadm@<reader-ip>
sudo dpkg -r sample-filter

# Install new version (use your version number)
sudo dpkg -i /tmp/sample-filter_1.0.1.deb
sudo systemctl restart userapps
```

### Testing LED Control (DA Apps Only)

The sample-filter app cycles LEDs every 5 seconds:
- 5 sec: GREEN LED + "LED set to GREEN" event
- 5 sec: RED LED + "LED set to RED" event  
- 5 sec: AMBER LED + "LED set to YELLOW" event

Watch LED 3 on the reader to verify it's working.

### Common Packaging Errors

| Error | Cause | Solution |
|-------|-------|----------|
| App won't start / shows red | Python file doesn't match package name | Rename `sample_filter.py` → `sample-filter.py` |
| "package name has characters..." | Underscore in package name | Use `sample-filter` not `sample_filter` |
| "missing final newline" | Control file ending | Add blank line after last field |
| "bad permissions 777" | Built on Windows filesystem | Use WSL filesystem (see build commands) |
| Scripts not executable | Permission issue | `chmod 755 /apps/*.sh` |
| DA app can't import pyziotc | Wrong app type or module missing | Verify `APP_TYPE: DA` in control file |

### Verifying Package Structure Before Building

```bash
# Check your package structure
ls -R sample-filter_1.0.0/

# Should show:
# sample-filter_1.0.0/DEBIAN/control
# sample-filter_1.0.0/sample-filter.py         ← Matches package name!
# sample-filter_1.0.0/start_sample-filter.sh
# sample-filter_1.0.0/stop_sample-filter.sh
```

## 📚 References

- **Packaging Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/packaging_and_deployment.html
- **Python DA Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/python/python_guide.html
- **IoT Connector Docs:** https://zebradevs.github.io/rfid-ziotc-docs/
- **Management APIs:** https://zebradevs.github.io/rfid-ziotc-docs/schemas/raw_mqtt_payloads/

## 📝 What's Included

This repository contains:

### Example Applications

1. **sample-filter (DA App)** - RFID tag filtering with LED control
   - Versions: 1.0.0 through 1.0.4
   - Demonstrates pyziotc module usage
   - Tag filtering, LED control, management events

2. **hello-world (Non-DA App)** - Simple background service
   - Version: 1.0.0
   - Basic Python logging example
   - No RFID dependencies

### Documentation

- [README.md](README.md) - This complete guide (DA + Non-DA apps)
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Detailed build steps
- [COPILOT_CUSTOMIZATIONS.md](COPILOT_CUSTOMIZATIONS.md) - AI development tools
- [LINKEDIN_POST.md](LINKEDIN_POST.md) - Social media announcement templates

### Development Tools

- [deploy.sh](deploy.sh) - SSH deployment script
- [test_on_reader.sh](test_on_reader.sh) - Quick testing script
- `.github/agents/` - Copilot packaging agent
- `.github/skills/` - Copilot DA app skill

## 📝 Version History

### sample-filter (DA App)

- **1.0.4** - Fixed permissions (755 for scripts, 644 for Python)
- **1.0.3** - Corrected file permissions in package
- **1.0.2** - Updated timing intervals
- **1.0.1** - Package name corrected to use hyphen per FX Series requirements
- **1.0.0** - Initial release with tag filtering and LED control

### hello-world (Non-DA App)

- **1.0.0** - Initial release demonstrating non-DA app pattern

**Critical Learning:** Python script filenames MUST match the package name (with hyphens). This is required for apps to show "green" status on FX Series readers.

**Note:** Package files follow naming convention: `<package-name>_X.Y.Z.deb` with hyphens, not underscores.

---

## 🎓 Getting Started

### Quick Start for DA Apps

1. Clone this repo
2. Study `sample-filter_1.0.4/` structure
3. Modify `sample-filter.py` for your logic
4. Update version in DEBIAN/control
5. Build with WSL command (see above)
6. Deploy to reader

### Quick Start for Non-DA Apps

1. Clone this repo
2. Study `hello-world_1.0.0/` structure
3. Create your Python script (any functionality)
4. **Important:** Name your `.py` file to match your package name
5. Remove `APP_TYPE: DA` from control file
6. Build and deploy

### Using GitHub Copilot

See [COPILOT_CUSTOMIZATIONS.md](COPILOT_CUSTOMIZATIONS.md) for AI-powered development:
- Auto-generate DA apps with `/zebra-rfid-python-app` skill
- Auto-package apps with `@zebra-package-python` agent
- Saves hours of manual coding and packaging

---

**Repository:** https://github.com/menugayan/zebra-rfid-da-app-python-sample

**License:** See LICENSE file
