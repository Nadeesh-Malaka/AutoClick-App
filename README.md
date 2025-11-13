# 🎯 Auto Clicker Pro - Advanced Automation Tool

A professional-grade automated screen clicking application for Windows with modern UI, comprehensive safety systems, scheduling capabilities, multiple click points, and advanced configuration options.

## 🌟 What Makes This Special

- **🎨 Modern Professional UI** - Clean, compact interface with intuitive controls
- **🛡️ Multiple Emergency Stops** - 6 different ways to stop clicking instantly
- **🎯 Visual Point Selection** - See exactly where you're clicking with preview system
- **⏰ Precise Scheduling** - Set exact times for automation to begin
- **📊 Real-time Monitoring** - Live feedback and comprehensive logging
- **⚡ Lightning Fast** - Millisecond precision with 50ms response times

## Features

### ✅ Core Features Implemented

1. **Click Automation**
   - Click specific points on the screen automatically
   - Support for multiple click points
   - Manual coordinate entry or point-and-click selection

2. **Click Frequency Settings**
   - Unlimited clicks mode
   - Set specific number of clicks (1-N times)
   - Configurable intervals between clicks
   - Adjustable delays between different click points

3. **Scheduled Start Time**
   - Set exact time for clicks to begin (e.g., 8:00 PM)
   - Precise timing based on system clock
   - Automatic scheduling for next day if time has passed

4. **Graphical User Interface**
   - Intuitive GUI for all settings
   - Point-and-click interface for selecting screen locations
   - Manual coordinate entry option
   - Real-time status updates

5. **Settings Management**
   - Save and load settings for future use
   - JSON-based configuration storage
   - Reset to default settings option

### � Modern UI Features

- **�🎯 Professional Interface**: Modern, compact design with emoji icons and clean typography
- **📱 Scrollable Layout**: Responsive interface that adapts to content
- **🌈 Color-Coded Status**: Visual indicators with modern color scheme (Blue/Green/Orange/Red)
- **⚡ Real-time Updates**: Live status indicators and current time display
- **🎮 Intuitive Controls**: Logical grouping with clear visual hierarchy

### 🛡️ Advanced Safety System

- **🚨 6 Emergency Stop Methods**: Multiple failsafes for maximum safety
- **⚡ 50ms Response Time**: Lightning-fast emergency detection
- **🎯 Visual Confirmation**: See exactly where clicks will happen before adding points
- **📁 File-Based Backup**: Emergency stop via batch file for ultimate reliability
- **🔍 Point Preview System**: Red crosshair markers show exact click locations

### 🎯 Bonus Features Implemented

- **🔔 System Notifications**: Desktop alerts when clicking starts/stops/completes
- **🔄 Background Operation**: Runs silently once scheduled, no user interaction needed
- **📋 Activity Logging**: Comprehensive logs with timestamps in GUI and file
- **💾 Settings Persistence**: Save/load configurations with JSON storage
- **🎪 Error Handling**: Robust error recovery with user-friendly feedback

## Installation

### Prerequisites

1. **Python 3.7+** installed on your system
2. **pip** package manager

### Install Dependencies

Open Command Prompt or PowerShell and navigate to the application directory, then run:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install tkinter pyautogui threading datetime json configparser plyer
```

## Usage

### Starting the Application

1. Open Command Prompt or PowerShell
2. Navigate to the application directory:
   ```bash
   cd "C:\Users\Nadeesh Malaka\Desktop\auto clicker"
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Setting Up Click Points

**Method 1: Visual Point Selection (Recommended)**
1. Click "**+ Add Point**" button
2. **Fullscreen overlay appears** with crosshair cursor and semi-transparent red background
3. **See live coordinates** as you move the mouse around
4. **Click anywhere** on screen to select that location
5. **Confirmation dialog** shows exact coordinates (X: 1234, Y: 567)
6. Click "**🔍 Preview**" to see a red marker exactly where the click will happen
7. Click "**✅ Add This Point**" to confirm, or "**❌ Cancel**" to abort

**Method 2: Manual Coordinate Entry**
1. Enter X and Y coordinates in the compact entry fields (separated by ×)
2. Click "**Add**" to add the point directly

**Method 3: Import from Settings**
- Load previously saved configurations with all your favorite click points

### Configuring Click Settings

1. **Click Mode**:
   - **Unlimited clicks**: Continues clicking indefinitely
   - **Set number of clicks**: Specify exact number (1-999999)

2. **Timing Settings**:
   - **Interval between clicks**: Delay between each click cycle
   - **Delay between points**: Delay when moving between different points

### Scheduling

1. **Immediate Start**: Clicks begin as soon as you press "Start Clicking"

2. **Scheduled Start**:
   - Select "Schedule for specific time"
   - Set the hour (0-23) and minute (0-59)
   - If the time has passed today, it will schedule for tomorrow

### Running the Clicker

1. Configure your click points and settings
2. Choose immediate or scheduled start
3. Click "Start Clicking"
4. Use "Stop" button to halt execution at any time

### Settings Management

- **Save Settings**: Saves current configuration to `autoclicker_settings.json`
- **Load Settings**: Automatically loads saved settings on startup
- **Reset Settings**: Restores all settings to default values

## 📁 File Structure

```
📂 auto clicker/
├── 🐍 main.py                        # Main application file (970+ lines)
├── 🚀 run_autoclicker.bat           # Easy Windows launcher
├── ⚡ run_autoclicker.ps1           # PowerShell launcher
├── 🌐 test_webpage.html             # Interactive test page
└── 📖 README.md                     # This comprehensive guide
```

## 🛡️ Comprehensive Safety System

### 🚨 **6 Emergency Stop Methods** (50ms Response Time)

1. **🔴 Mouse Failsafe** - Move mouse to top-left corner (PyAutoGUI built-in)
2. **⌨️ ESC Key** - Press Escape key for instant stop
3. **🎯 F12 Key** - Press F12 for emergency stop
4. **💻 Ctrl+C** - Standard interrupt command
5. **🚨 Emergency Button** - Big red "EMERGENCY" button always visible in UI
6. **📁 File-Based Stop** - Double-click `EMERGENCY_STOP.bat` (works even if app is unresponsive)

### 🎯 **Visual Safety Features**

- **🔍 Point Preview**: See red crosshair markers exactly where clicks will happen
- **✅ Confirmation Dialogs**: Verify every action before execution
- **📱 Real-time Status**: Color-coded status indicators show current state
- **📋 Activity Logging**: Track every click with timestamps for accountability

### 🔒 **Input Protection**

- **✅ Input Validation**: Prevents invalid settings and coordinates
- **🛑 Graceful Error Handling**: User-friendly error messages and recovery
- **⚠️ Confirmation Prompts**: Prevents accidental dangerous operations
- **🎮 Focus Management**: Maintains keyboard focus for emergency stops

## Logging

The application maintains detailed logs:
- **GUI Log**: Real-time log display in the application
- **File Log**: Persistent log saved to `autoclicker_log.txt`
- **Timestamps**: All actions logged with precise timestamps

## System Notifications

The app uses system notifications to inform you:
- When scheduled clicking is about to start
- When clicking has completed
- Total number of clicks performed

## 🚨 Emergency Procedures

### **If App Won't Stop (CRITICAL)**

1. **🖱️ Move mouse to top-left corner** (Most reliable - built into PyAutoGUI)
2. **📁 Double-click `EMERGENCY_STOP.bat`** (File-based stop - works always)
3. **⌨️ Press ESC, F12, or Ctrl+C** (Keyboard shortcuts)
4. **🚨 Click EMERGENCY button** (In app interface)
5. **💻 Task Manager**: Ctrl+Shift+Esc → End Python process (Last resort)

### **Testing Emergency Stops**

Before using unlimited mode, **always test**:
1. Start clicking with 2-3 clicks in limited mode
2. Try each emergency method to ensure they work
3. Only use unlimited mode after confirming emergency stops work

## 🔧 Troubleshooting

### ❌ Common Issues & Solutions

1. **🐍 "Module not found" errors**
   - **Solution**: Install dependencies: `pip install -r requirements.txt`
   - **Alternative**: Install individually: `pip install pyautogui plyer`

2. **🖱️ Clicking doesn't work or misses targets**
   - **Check**: Use point preview to verify coordinates are correct
   - **Verify**: Target application/window is accessible and visible
   - **Confirm**: Screen resolution hasn't changed since adding points
   - **Test**: Try manual clicking at the coordinates first

3. **⏰ Scheduled time doesn't trigger**
   - **Check**: System time is correct (uses 24-hour format)
   - **Ensure**: Application remains running and visible
   - **Verify**: Time zone settings are correct
   - **Note**: Uses exact system time, not approximate

4. **🚨 Emergency stops don't work**
   - **Primary**: Use mouse failsafe (move to top-left corner)
   - **Backup**: Double-click `EMERGENCY_STOP.bat` file
   - **Check**: App has keyboard focus (click on app window)
   - **Last resort**: Use Task Manager (Ctrl+Shift+Esc)

5. **📁 Permission errors on log files**
   - **Solution**: Run as administrator if needed
   - **Check**: Folder write permissions in auto clicker directory
   - **Alternative**: Move app to Documents folder

### Performance Tips

- Use reasonable intervals (minimum 0.1 seconds recommended)
- Limit number of click points for better performance
- Close unnecessary applications during long clicking sessions

## Technical Details

- **Built with**: Python 3, tkinter, pyautogui
- **Threading**: Uses separate threads for clicking to maintain UI responsiveness
- **Precision**: Millisecond-level timing accuracy for scheduling
- **Cross-compatibility**: Designed for Windows but adaptable to other platforms

## Legal Notice

This software is for legitimate automation purposes only. Users are responsible for ensuring their use complies with applicable terms of service and laws. Do not use for cheating, spamming, or other malicious activities.

## 🌟 Additional Features

### 🧪 Test Mode
- **Interactive Test Page**: Run `start_test_server.py` for browser-based testing
- **Real-time Statistics**: Live click tracking and timing analysis
- **Coordinate Display**: See exact click locations as they happen
- **Safe Testing Environment**: Practice without affecting other applications

### 📊 Performance Monitoring
- **Activity Logging**: Detailed logs of all clicking sessions
- **Click Statistics**: Track accuracy, timing, and success rates
- **Error Tracking**: Automatic logging of issues and recoveries
- **Session History**: Complete record of all automation activities

### 🔧 Power User Features
- **Batch Operations**: Import/export click point configurations
- **Hotkey Customization**: Modify keyboard shortcuts in settings
- **Advanced Scheduling**: Complex time-based automation patterns
- **Multi-Monitor Support**: Works across multiple screen setups

## 📞 Support & Contributing

### 🐛 Reporting Issues
Found a bug or have a feature request? 
1. Check the troubleshooting section first
2. Test emergency stops before reporting
3. Include log files when reporting issues
4. Describe steps to reproduce the problem

### 🤝 Contributing
Contributions welcome! Areas for improvement:
- Additional emergency stop methods
- UI/UX enhancements
- Cross-platform compatibility
- Performance optimizations

## 📄 License

This project is provided as-is for educational and legitimate automation purposes.

## 📈 Project Stats

- **Lines of Code**: 970+ (main.py)
- **Dependencies**: 6 core packages
- **Safety Methods**: 6 emergency stop systems
- **UI Elements**: Modern, accessible interface
- **Documentation**: Comprehensive user guide

---

**⚠️ Remember**: Always test emergency stops before using unlimited clicking mode. Your safety and system stability are paramount!