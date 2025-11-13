# Advanced Auto Clicker App

A comprehensive automated screen clicking application for Windows with scheduling, multiple click points, and advanced configuration options.

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

### 🎯 Bonus Features Implemented

- **System Notifications**: Alerts when clicking starts/stops
- **Background Operation**: Runs without user interaction once scheduled
- **Activity Logging**: Comprehensive logs of all actions with timestamps
- **Real-time Status**: Current time display and status indicators
- **Error Handling**: Robust error handling and user feedback

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

**Method 1: Point and Click**
1. Click "Add Click Point" button
2. The window will minimize
3. Click on the desired location on your screen
4. The coordinates will be automatically added

**Method 2: Manual Entry**
1. Enter X and Y coordinates in the manual entry fields
2. Click "Add" to add the point

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

## File Structure

```
auto clicker/
├── main.py                    # Main application file
├── requirements.txt           # Python dependencies
├── autoclicker_settings.json  # Saved settings (created automatically)
├── autoclicker_log.txt       # Activity log file (created automatically)
└── README.md                 # This file
```

## Safety Features

- **Failsafe**: Move mouse to top-left corner to emergency stop
- **Input Validation**: Prevents invalid settings
- **Error Handling**: Graceful error handling with user feedback
- **Confirmation Dialogs**: Prevents accidental actions

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

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Install required dependencies: `pip install -r requirements.txt`

2. **Clicking doesn't work**
   - Check if coordinates are valid
   - Ensure target application/window is accessible
   - Verify screen resolution hasn't changed

3. **Scheduled time doesn't trigger**
   - Check system time is correct
   - Ensure application remains running
   - Verify AM/PM time format (uses 24-hour format)

4. **Permission errors on log files**
   - Run as administrator if needed
   - Check folder write permissions

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

## License

This project is provided as-is for educational and legitimate automation purposes.