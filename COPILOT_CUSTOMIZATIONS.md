# GitHub Copilot Customizations for Zebra RFID Development

This repository includes custom GitHub Copilot agents and skills to streamline Zebra RFID Data Analytics (DA) application development and packaging.

## 📦 What's Included

### 1. **Zebra RFID Python App Skill** (`zebra-rfid-python-app`)
A comprehensive skill for creating Python DA applications for Zebra FX Series RFID readers using the `pyziotc` module.

**Features:**
- Complete app structure templates with callbacks
- 7 common patterns (filtering, LED/GPO/GPI control, pass-through config, REST API)
- Message type reference tables
- Production-ready code examples
- FX Series packaging requirements
- Development workflow guidance

### 2. **Zebra Package Python Agent** (`zebra-package-python`)
A specialized packaging agent that transforms Python DA apps into Debian .deb installers for FX Series reader deployment.

**Features:**
- Auto-detects and validates Python DA apps
- Generates start/stop shell scripts automatically
- Creates proper Debian package structure
- Handles FX Series naming requirements (hyphens vs underscores)
- Fixes Windows permission issues for dpkg-deb
- Generates deployment helper scripts
- Comprehensive error handling and troubleshooting

---

## 🚀 Installation

### Prerequisites
- **VS Code** with **GitHub Copilot** extension (Chat enabled)
- **Workspace** with this repository cloned

### Setup Instructions

#### Option 1: Automatic (Repository-Scoped)

When you clone this repository, the customizations are automatically available because they're in the `.github/` folder!

1. **Clone the repository:**
   ```bash
   git clone https://github.com/menugayan/zebra-rfid-da-app-python-sample.git
   cd zebra-rfid-da-app-python-sample
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Start using:** The skill and agent are now available in Copilot Chat!

#### Option 2: Personal Installation (Cross-Project)

To use these customizations across **all your projects**, copy them to your personal Copilot folder:

**Windows:**
```powershell
# Copy skill
Copy-Item -Recurse ".github\skills\zebra-rfid-python-app" "$env:USERPROFILE\.copilot\skills\"

# Copy agent
Copy-Item ".github\agents\zebra-package-python.agent.md" "$env:USERPROFILE\.copilot\agents\"
```

**macOS/Linux:**
```bash
# Copy skill
cp -r .github/skills/zebra-rfid-python-app ~/.copilot/skills/

# Copy agent
mkdir -p ~/.copilot/agents
cp .github/agents/zebra-package-python.agent.md ~/.copilot/agents/
```

---

## 📖 Usage Guide

### Using the Zebra RFID Python App Skill

The skill helps you **create** Python DA applications for Zebra readers.

#### Invocation Methods

**Method 1: Slash Command**
```
/zebra-rfid-python-app create a tag filter app for prefix E200
```

**Method 2: Natural Language**
```
Create a Zebra DA app that filters tags starting with '3008'
```

**Method 3: @workspace Context**
```
@workspace build a Python RFID app that controls LED based on RSSI values
```

#### Example Prompts

- `Create a Zebra DA app that filters tags by prefix "43"`
- `Write a Python RFID app with pass-through configuration`
- `Build a DA app that monitors GPI events and sends alerts`
- `Generate a production DA app with filtering, LED control, and management events`
- `Show me how to control GPO pins in a Zebra DA app`

#### What You Get

The skill provides:
- ✅ Complete working Python code
- ✅ Proper pyziotc module usage
- ✅ Correct message types and bytearrays
- ✅ Callback registration patterns
- ✅ Hardware control examples (LED/GPO/GPI)
- ✅ Error handling and best practices

---

### Using the Zebra Package Python Agent

The agent helps you **package** Python DA apps into deployable .deb installers.

#### Invocation Methods

**Method 1: Agent Selector**
1. Click the agent icon (🤖) in Copilot Chat
2. Select **"zebra-package-python"** from the list
3. Type: `Package my_app.py version 1.0.0`

**Method 2: Direct Mention**
```
@zebra-package-python package sample_filter.py
```

**Method 3: Natural Language (Auto-Invoked)**
```
Package my Python DA app for deployment
```

#### Example Prompts

- `Package sample_filter.py version 1.0.0`
- `Create a Debian package for my tag filter app`
- `Build deployment package from filter_tags.py`
- `Package all DA apps in the workspace`

#### What the Agent Does

1. **Validates** your Python DA app structure
2. **Converts** package naming (underscores → hyphens for FX Series)
3. **Generates** start/stop shell scripts with correct naming
4. **Creates** DEBIAN/control manifest with proper formatting
5. **Builds** directory structure: `appname_version/`
6. **Provides** WSL build commands (handles Windows permission issues)
7. **Generates** `deploy.sh` and `test_on_reader.sh` helper scripts
8. **Gives** deployment instructions (web console, SSH, API)

---

## 🎯 Complete Workflow Example

Here's a full end-to-end example using both customizations:

### Step 1: Create Your DA App

```
/zebra-rfid-python-app Create a DA app that:
- Filters tags with prefix "E200"
- Flashes LED green on match, red on reject
- Supports pass-through config to change prefix
- Sends management events
```

**Result:** Complete Python file `inventory_filter.py`

### Step 2: Test Your App (Optional)

Save the file, then test locally:
```bash
python inventory_filter.py
# Test with mock data or on a development reader
```

### Step 3: Package for Deployment

```
@zebra-package-python package inventory_filter.py version 1.0.0
```

**Result:** 
- `inventory-filter_1.0.0/` directory structure
- Working build command for WSL
- `inventory-filter_1.0.0.deb` package file
- Deployment helper scripts

### Step 4: Deploy to Reader

Use the generated package:
```bash
# Via web console: Upload inventory-filter_1.0.0.deb
# Or via SSH:
scp inventory-filter_1.0.0.deb rfidadm@<reader-ip>:/tmp/
ssh rfidadm@<reader-ip> "sudo dpkg -i /tmp/inventory-filter_1.0.0.deb"
```

---

## 🔑 Key Features & Benefits

### Automated FX Series Compliance

Both customizations ensure your apps meet Zebra FX Series reader requirements:

- ✅ **Package naming:** Automatic underscore → hyphen conversion
- ✅ **Control file format:** Proper `APP_TYPE: DA` with final newline
- ✅ **Script naming:** Start/stop scripts match package name
- ✅ **Permissions:** Handles Windows filesystem → WSL conversion (777 → 0755)
- ✅ **DEBIAN structure:** Correct directory permissions and layout
- ✅ **rfidadm privileges:** Apps designed for non-root execution context

### Time Savings

**Without these customizations:**
- 🕐 Research pyziotc API documentation
- 🕐 Learn message types and bytearray formats
- 🕐 Debug callback registration issues
- 🕐 Trial-and-error with dpkg-deb
- 🕐 Fix permission errors on Windows
- 🕐 Debug package naming validation errors

**With these customizations:**
- ⚡ Generate working code in seconds
- ⚡ Package correctly on first try
- ⚡ Deploy immediately to readers
- ⚡ No manual documentation lookup needed

---

## 🛠️ Customization Details

### Skill: zebra-rfid-python-app

**Location:** `.github/skills/zebra-rfid-python-app/SKILL.md`

**Trigger Keywords:** 
- Zebra, RFID, DA app, pyziotc, tag filter, LED control, GPO, GPI, reader, IoT Connector

**Model Invocation:** Automatic when keywords detected

**User Invocable:** Yes (appears as `/zebra-rfid-python-app` in slash commands)

**Content Includes:**
- Complete DA app structure (3-step minimal pattern)
- 7 production-ready patterns with code examples
- Message type reference tables
- FX Series packaging section
- Development workflow
- Quick reference checklist
- Resource links

### Agent: zebra-package-python

**Location:** `.github/agents/zebra-package-python.agent.md`

**Trigger Keywords:**
- Package, packaging, Debian, .deb, dpkg-deb, deploy, installer, DA app

**Tools:** `[read, edit, execute, search]`

**Model Invocation:** Automatic when keywords detected

**User Invocable:** Yes (appears in agent selector 🤖)

**Workflow:**
1. Detect Python DA apps (scan for pyziotc)
2. Validate structure (callbacks, Ziotc object)
3. Gather metadata (version, description)
4. Generate scripts (start/stop with proper naming)
5. Create control file (with APP_TYPE: DA and final newline)
6. Build directory structure
7. Provide WSL build command
8. Generate deployment helpers

---

## 📝 Troubleshooting

### Skill or Agent Not Appearing

**Check:**
1. Files are in correct locations:
   - `.github/skills/zebra-rfid-python-app/SKILL.md`
   - `.github/agents/zebra-package-python.agent.md`

2. Restart VS Code to reload customizations

3. Check GitHub Copilot extension is active and chat is enabled

4. Try explicitly invoking:
   ```
   /zebra-rfid-python-app help
   ```

### Skill Not Triggering Automatically

Use explicit invocation:
```
/zebra-rfid-python-app [your request]
```

Or mention it:
```
Use the zebra-rfid-python-app skill to create a tag filter
```

### Agent Not Packaging Correctly

Ensure:
- ✅ Your Python file imports `pyziotc`
- ✅ File has proper DA app structure (callbacks, Ziotc object)
- ✅ You're on Windows with WSL installed
- ✅ dpkg is installed in WSL: `wsl sudo apt-get install dpkg`

---

## 🤝 Contributing

Found an issue or have improvements? 

1. **Update the customizations** in `.github/skills/` or `.github/agents/`
2. **Test your changes** with sample DA apps
3. **Update this guide** with new examples or features
4. **Submit a pull request**

---

## 📚 Additional Resources

- **Zebra IoT Connector Docs:** https://zebradevs.github.io/rfid-ziotc-docs/
- **Python DA Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/python/python_guide.html
- **Packaging Guide:** https://zebradevs.github.io/rfid-ziotc-docs/user_apps/packaging_and_deployment.html
- **GitHub Copilot Customization Docs:** https://code.visualstudio.com/docs/copilot/customization

---

## 📄 License

These customizations are provided as-is for use with Zebra RFID reader development. See repository LICENSE for terms.

---

## 🎉 Happy Coding!

With these Copilot customizations, you can go from idea to deployed DA app in minutes instead of hours. Focus on your RFID logic, not boilerplate code and packaging details!
