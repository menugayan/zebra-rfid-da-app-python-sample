# Building sample-filter Debian Package on Windows

**IMPORTANT:** FX Series readers require:
- Package name with **hyphens** (sample-filter, not sample_filter)
- DEBIAN directory permissions: 0755 (not 777)
- Control file must end with newline after `APP_TYPE: DA`

Since you're on Windows, you need a Linux environment to run `dpkg-deb`. Choose one of the options below:

## Option 1: WSL2 (Recommended)

### First-time WSL Setup:
```powershell
# Run in PowerShell as Administrator
wsl --install Ubuntu
# Restart your computer when prompted
```

### Build the Package:
```powershell
# Use the one-liner from "Quick Build Commands" section above
# It handles all steps: copy, permissions, build, and copy back

# OR do it step-by-step:
wsl

# Now in WSL bash:
rm -rf ~/sample-filter_1.0.1
cp -r /mnt/c/DaAps/sample-filter_1.0.1 ~/
cd ~
chmod 0755 sample-filter_1.0.1/DEBIAN
chmod +x sample-filter_1.0.1/*.sh

# Install dpkg if needed (first time only):
sudo apt-get update && sudo apt-get install -y dpkg

# Build the package:
dpkg-deb --build -Zgzip sample-filter_1.0.1/

# Copy .deb back to Windows:
cp sample-filter_1.0.1.deb /mnt/c/DaAps/
exit
```

## Option 2: Docker

### Build with Docker (no installation needed):
```powershell
# Run from PowerShell in C:\DaAps directory
# Replace VERSION with your version (e.g., 1.0.1, 1.0.2)

docker run --rm -v ${PWD}:/work ubuntu:latest bash -c "cd /work && apt-get update && apt-get install -y dpkg && chmod 0755 sample-filter_VERSION/DEBIAN && chmod +x sample-filter_VERSION/*.sh && dpkg-deb --build -Zgzip sample-filter_VERSION/"
```

**Note:** Docker method may still have permission issues on some Windows configurations. WSL method is more reliable.

## Final Steps

After building, you should have: `sample-filter_1.0.1.deb` (or your version)

**Verify package:**
```powershell
Get-Item sample-filter_*.deb | Select-Object Name, Length, LastWriteTime | Format-Table
```

### Make helper scripts executable (in WSL or Git Bash):
```bash
chmod +x deploy.sh test_on_reader.sh
```

## Quick Build Commands

**CRITICAL:** These commands copy to WSL filesystem to fix Windows permission issues (777 → 0755).

### WSL Method (Recommended):
```powershell
# Complete one-liner (from PowerShell in C:\DaAps)
# Replace VERSION with your version (e.g., 1.0.1, 1.0.2, 1.0.3)
wsl bash -c "rm -rf ~/sample-filter_VERSION && cp -r /mnt/c/DaAps/sample-filter_VERSION ~/ && cd ~ && chmod 0755 sample-filter_VERSION/DEBIAN && chmod +x sample-filter_VERSION/*.sh && dpkg-deb --build -Zgzip sample-filter_VERSION/ && cp sample-filter_VERSION.deb /mnt/c/DaAps/"
```

**Example for version 1.0.1:**
```powershell
wsl bash -c "rm -rf ~/sample-filter_1.0.1 && cp -r /mnt/c/DaAps/sample-filter_1.0.1 ~/ && cd ~ && chmod 0755 sample-filter_1.0.1/DEBIAN && chmod +x sample-filter_1.0.1/*.sh && dpkg-deb --build -Zgzip sample-filter_1.0.1/ && cp sample-filter_1.0.1.deb /mnt/c/DaAps/"
```

**Example for version 1.0.2:**
```powershell
wsl bash -c "rm -rf ~/sample-filter_1.0.2 && cp -r /mnt/c/DaAps/sample-filter_1.0.2 ~/ && cd ~ && chmod 0755 sample-filter_1.0.2/DEBIAN && chmod +x sample-filter_1.0.2/*.sh && dpkg-deb --build -Zgzip sample-filter_1.0.2/ && cp sample-filter_1.0.2.deb /mnt/c/DaAps/"
```

### Docker Method:
```powershell
# Complete one-liner (from PowerShell in C:\DaAps)
# Replace VERSION with your version
docker run --rm -v ${PWD}:/work ubuntu:latest bash -c "cd /work && apt-get update && apt-get install -y dpkg && chmod 0755 sample-filter_VERSION/DEBIAN && chmod +x sample-filter_VERSION/*.sh && dpkg-deb --build -Zgzip sample-filter_VERSION/"
```

### Why This Command Structure?

1. **`rm -rf ~/sample-filter_VERSION`** - Clean any old builds
2. **`cp -r /mnt/c/DaAps/sample-filter_VERSION ~/`** - Copy to WSL filesystem (fixes permissions)
3. **`chmod 0755 sample-filter_VERSION/DEBIAN`** - Set correct DEBIAN dir permissions (required)
4. **`chmod +x sample-filter_VERSION/*.sh`** - Make scripts executable
5. **`dpkg-deb --build -Zgzip`** - Build the package
6. **`cp sample-filter_VERSION.deb /mnt/c/DaAps/`** - Copy back to Windows

### Common Errors Fixed:

- ❌ "bad permissions 777" → Fixed by copying to WSL filesystem
- ❌ "package name has characters..." → Use hyphens: sample-filter
- ❌ "missing final newline" → Control file must end with blank line
