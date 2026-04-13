# sample_filter DA App - Deployment Guide

> **🤖 GitHub Copilot Users:** This repo includes custom agents and skills to streamline Zebra RFID development! See [COPILOT_CUSTOMIZATIONS.md](COPILOT_CUSTOMIZATIONS.md) for setup and usage.

> **⚡ Quick Build:** See [Quick Build Commands](#quick-build-commands) section below for the working build command.

## 📦 Package Information

**Package Name:** sample-filter (with hyphen - required by FX Series readers)  
**Current Version:** 1.0.1  
**Type:** Data Analytics (DA)  
**Application:** RFID tag filter that processes tags with prefix "43", cycles LED colors, and sends management events

## 📋 Package Contents

```
sample-filter_1.0.1/
├── DEBIAN/
│   └── control                    # Package metadata (Package: sample-filter)
├── sample_filter.py               # Main DA application
├── start_sample-filter.sh         # Startup script (name matches package)
└── stop_sample-filter.sh          # Stop script (name matches package)
```

**IMPORTANT:** Package name uses **hyphen** (sample-filter), not underscore. This is required by FX Series readers.

## 🔨 Building the .deb Package

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

### Testing LED control

The app cycles LEDs every second:
- 1 sec: GREEN LED + "LED set to GREEN" event
- 1 sec: RED LED + "LED set to RED" event  
- 1 sec: AMBER LED + "LED set to YELLOW" event

Watch LED 3 on the reader to verify it's working.

## 📚 References

- **Packaging Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/packaging_and_deployment.html
- **Python DA Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/python/python_guide.html
- **IoT Connector Docs:** https://zebradevs.github.io/rfid-ziotc-docs/
- **Management APIs:** https://zebradevs.github.io/rfid-ziotc-docs/schemas/raw_mqtt_payloads/

## 📝 Version History

- **1.0.1** - Package name corrected to use hyphen (sample-filter) per FX Series requirements
- **1.0.0** - Initial release
  - Tag filtering by prefix "43"
  - LED color cycling (green/red/amber)
  - Management event messaging
  - Pass-through command support for dynamic prefix changes

**Note:** Latest version package files follow naming convention: `sample-filter_X.Y.Z.deb`
