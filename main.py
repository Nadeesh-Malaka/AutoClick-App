import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyautogui
import threading
import time
import json
import os
from datetime import datetime, timedelta
import logging
from plyer import notification

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Auto Clicker")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.click_points = []
        self.is_running = False
        self.click_thread = None
        self.scheduled_time = None
        self.settings_file = "autoclicker_settings.json"
        
        # Setup logging
        self.setup_logging()
        
        # Disable pyautogui fail-safe (optional)
        pyautogui.FAILSAFE = True
        
        # Create GUI
        self.create_gui()
        
        # Load settings if they exist
        self.load_settings()
    
    def setup_logging(self):
        """Setup logging for action tracking"""
        logging.basicConfig(
            filename='autoclicker_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Auto Clicker", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Click Points Section
        self.create_click_points_section(main_frame, 1)
        
        # Click Settings Section
        self.create_click_settings_section(main_frame, 2)
        
        # Schedule Section
        self.create_schedule_section(main_frame, 3)
        
        # Control Buttons Section
        self.create_control_buttons_section(main_frame, 4)
        
        # Settings Section
        self.create_settings_section(main_frame, 5)
        
        # Log Section
        self.create_log_section(main_frame, 6)
    
    def create_click_points_section(self, parent, row):
        """Create the click points configuration section"""
        # Click Points Frame
        points_frame = ttk.LabelFrame(parent, text="Click Points", padding="10")
        points_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        points_frame.columnconfigure(1, weight=1)
        
        # Add point button
        ttk.Button(points_frame, text="Add Click Point", 
                  command=self.add_click_point).grid(row=0, column=0, padx=(0, 10))
        
        # Manual coordinate entry
        ttk.Label(points_frame, text="Manual Entry (X,Y):").grid(row=0, column=1, sticky=tk.W)
        
        coord_frame = ttk.Frame(points_frame)
        coord_frame.grid(row=0, column=2, padx=10)
        
        self.x_entry = ttk.Entry(coord_frame, width=8)
        self.x_entry.grid(row=0, column=0, padx=2)
        
        ttk.Label(coord_frame, text=",").grid(row=0, column=1)
        
        self.y_entry = ttk.Entry(coord_frame, width=8)
        self.y_entry.grid(row=0, column=2, padx=2)
        
        ttk.Button(coord_frame, text="Add", 
                  command=self.add_manual_point).grid(row=0, column=3, padx=(5, 0))
        
        # Points listbox with scrollbar
        list_frame = ttk.Frame(points_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        
        self.points_listbox = tk.Listbox(list_frame, height=6)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.points_listbox.yview)
        self.points_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.points_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Remove point button
        ttk.Button(points_frame, text="Remove Selected", 
                  command=self.remove_click_point).grid(row=2, column=0, pady=5)
        
        # Clear all points button
        ttk.Button(points_frame, text="Clear All", 
                  command=self.clear_all_points).grid(row=2, column=1, pady=5)
    
    def create_click_settings_section(self, parent, row):
        """Create the click settings section"""
        settings_frame = ttk.LabelFrame(parent, text="Click Settings", padding="10")
        settings_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Click mode selection
        ttk.Label(settings_frame, text="Click Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.click_mode = tk.StringVar(value="unlimited")
        ttk.Radiobutton(settings_frame, text="Unlimited clicks", 
                       variable=self.click_mode, value="unlimited").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(settings_frame, text="Set number of clicks", 
                       variable=self.click_mode, value="limited").grid(row=0, column=2, sticky=tk.W)
        
        # Number of clicks
        ttk.Label(settings_frame, text="Number of clicks:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.click_count_var = tk.StringVar(value="1")
        self.click_count_entry = ttk.Entry(settings_frame, textvariable=self.click_count_var, width=10)
        self.click_count_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Click interval
        ttk.Label(settings_frame, text="Interval between clicks (seconds):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value="1.0")
        ttk.Entry(settings_frame, textvariable=self.interval_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Delay between points
        ttk.Label(settings_frame, text="Delay between points (seconds):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.point_delay_var = tk.StringVar(value="0.1")
        ttk.Entry(settings_frame, textvariable=self.point_delay_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
    
    def create_schedule_section(self, parent, row):
        """Create the schedule section"""
        schedule_frame = ttk.LabelFrame(parent, text="Schedule Settings", padding="10")
        schedule_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Immediate or scheduled
        self.schedule_mode = tk.StringVar(value="immediate")
        ttk.Radiobutton(schedule_frame, text="Start immediately", 
                       variable=self.schedule_mode, value="immediate").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(schedule_frame, text="Schedule for specific time", 
                       variable=self.schedule_mode, value="scheduled").grid(row=0, column=1, sticky=tk.W)
        
        # Time selection
        time_frame = ttk.Frame(schedule_frame)
        time_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Label(time_frame, text="Time (HH:MM):").grid(row=0, column=0, padx=5)
        
        self.hour_var = tk.StringVar(value="20")
        self.minute_var = tk.StringVar(value="00")
        
        hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=5, 
                                  textvariable=self.hour_var, format="%02.0f")
        hour_spinbox.grid(row=0, column=1, padx=2)
        
        ttk.Label(time_frame, text=":").grid(row=0, column=2)
        
        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=5, 
                                    textvariable=self.minute_var, format="%02.0f")
        minute_spinbox.grid(row=0, column=3, padx=2)
        
        # Current time display
        self.current_time_label = ttk.Label(time_frame, text="")
        self.current_time_label.grid(row=0, column=4, padx=20)
        self.update_current_time()
    
    def create_control_buttons_section(self, parent, row):
        """Create the control buttons section"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(control_frame, text="Start Clicking", 
                                      command=self.start_clicking, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", 
                                     command=self.stop_clicking, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready", foreground="green")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=10)
    
    def create_settings_section(self, parent, row):
        """Create the settings save/load section"""
        settings_frame = ttk.LabelFrame(parent, text="Settings Management", padding="10")
        settings_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(settings_frame, text="Save Settings", 
                  command=self.save_settings).grid(row=0, column=0, padx=5)
        ttk.Button(settings_frame, text="Load Settings", 
                  command=self.load_settings).grid(row=0, column=1, padx=5)
        ttk.Button(settings_frame, text="Reset Settings", 
                  command=self.reset_settings).grid(row=0, column=2, padx=5)
    
    def create_log_section(self, parent, row):
        """Create the log display section"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text widget with scrollbar
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_text_frame, height=8, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Log", 
                  command=self.clear_log).grid(row=1, column=0, pady=5)
    
    def update_current_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current: {current_time}")
        self.root.after(1000, self.update_current_time)
    
    def add_click_point(self):
        """Add a click point by clicking on the screen"""
        self.root.withdraw()  # Hide the window
        self.log_message("Click on the desired location on screen...")
        
        # Give user time to position
        time.sleep(2)
        
        try:
            # Get mouse position
            x, y = pyautogui.position()
            self.click_points.append((x, y))
            self.update_points_listbox()
            self.log_message(f"Added click point: ({x}, {y})")
        except Exception as e:
            self.log_message(f"Error adding click point: {str(e)}")
        finally:
            self.root.deiconify()  # Show the window again
    
    def add_manual_point(self):
        """Add a click point manually from coordinates"""
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            self.click_points.append((x, y))
            self.update_points_listbox()
            self.log_message(f"Added manual click point: ({x}, {y})")
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer coordinates")
    
    def remove_click_point(self):
        """Remove selected click point"""
        selection = self.points_listbox.curselection()
        if selection:
            index = selection[0]
            removed_point = self.click_points.pop(index)
            self.update_points_listbox()
            self.log_message(f"Removed click point: {removed_point}")
    
    def clear_all_points(self):
        """Clear all click points"""
        self.click_points.clear()
        self.update_points_listbox()
        self.log_message("Cleared all click points")
    
    def update_points_listbox(self):
        """Update the points listbox display"""
        self.points_listbox.delete(0, tk.END)
        for i, (x, y) in enumerate(self.click_points, 1):
            self.points_listbox.insert(tk.END, f"{i}. ({x}, {y})")
    
    def start_clicking(self):
        """Start the clicking process"""
        if not self.click_points:
            messagebox.showerror("Error", "Please add at least one click point")
            return
        
        try:
            # Validate settings
            if self.click_mode.get() == "limited":
                click_count = int(self.click_count_var.get())
                if click_count <= 0:
                    raise ValueError("Click count must be positive")
            
            interval = float(self.interval_var.get())
            point_delay = float(self.point_delay_var.get())
            
            if interval < 0 or point_delay < 0:
                raise ValueError("Intervals must be non-negative")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid settings: {str(e)}")
            return
        
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        if self.schedule_mode.get() == "immediate":
            self.status_label.config(text="Running...", foreground="blue")
            self.click_thread = threading.Thread(target=self.click_worker)
            self.click_thread.daemon = True
            self.click_thread.start()
        else:
            # Schedule for specific time
            try:
                hour = int(self.hour_var.get())
                minute = int(self.minute_var.get())
                
                now = datetime.now()
                scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # If the time is in the past, schedule for tomorrow
                if scheduled_time <= now:
                    scheduled_time += timedelta(days=1)
                
                self.scheduled_time = scheduled_time
                self.status_label.config(text=f"Scheduled for {scheduled_time.strftime('%H:%M:%S')}", 
                                       foreground="orange")
                
                self.click_thread = threading.Thread(target=self.scheduled_click_worker)
                self.click_thread.daemon = True
                self.click_thread.start()
                
                # Show notification
                self.show_notification("Auto Clicker Scheduled", 
                                     f"Clicking will start at {scheduled_time.strftime('%H:%M:%S')}")
                
            except ValueError:
                messagebox.showerror("Error", "Invalid time format")
                self.stop_clicking()
    
    def stop_clicking(self):
        """Stop the clicking process"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Stopped", foreground="red")
        self.log_message("Clicking stopped by user")
    
    def scheduled_click_worker(self):
        """Worker thread for scheduled clicking"""
        while self.is_running and self.scheduled_time:
            current_time = datetime.now()
            if current_time >= self.scheduled_time:
                self.status_label.config(text="Running...", foreground="blue")
                self.log_message(f"Scheduled clicking started at {current_time.strftime('%H:%M:%S')}")
                self.show_notification("Auto Clicker Started", "Scheduled clicking has begun!")
                self.click_worker()
                break
            time.sleep(0.1)  # Check every 100ms for precision
    
    def click_worker(self):
        """Worker thread for clicking"""
        try:
            click_count = 0
            max_clicks = None
            
            if self.click_mode.get() == "limited":
                max_clicks = int(self.click_count_var.get())
            
            interval = float(self.interval_var.get())
            point_delay = float(self.point_delay_var.get())
            
            self.log_message(f"Starting clicks - Mode: {self.click_mode.get()}, "
                           f"Interval: {interval}s, Points: {len(self.click_points)}")
            
            while self.is_running:
                if max_clicks and click_count >= max_clicks:
                    break
                
                # Click each point
                for point_index, (x, y) in enumerate(self.click_points):
                    if not self.is_running:
                        break
                    
                    try:
                        pyautogui.click(x, y)
                        click_count += 1
                        self.log_message(f"Clicked point {point_index + 1}: ({x}, {y}) - Total clicks: {click_count}")
                        
                        if max_clicks and click_count >= max_clicks:
                            break
                        
                        # Delay between points
                        if point_delay > 0 and point_index < len(self.click_points) - 1:
                            time.sleep(point_delay)
                            
                    except Exception as e:
                        self.log_message(f"Error clicking point ({x}, {y}): {str(e)}")
                
                if max_clicks and click_count >= max_clicks:
                    break
                
                # Delay between click cycles
                if self.is_running and interval > 0:
                    time.sleep(interval)
            
            # Finished
            self.root.after(0, self.clicking_finished, click_count)
            
        except Exception as e:
            self.log_message(f"Error in click worker: {str(e)}")
            self.root.after(0, self.clicking_finished, 0)
    
    def clicking_finished(self, total_clicks):
        """Called when clicking is finished"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text=f"Completed - {total_clicks} clicks", foreground="green")
        self.log_message(f"Clicking completed. Total clicks performed: {total_clicks}")
        self.show_notification("Auto Clicker Completed", f"Finished with {total_clicks} total clicks")
    
    def show_notification(self, title, message):
        """Show system notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Auto Clicker",
                timeout=5
            )
        except Exception as e:
            self.log_message(f"Notification error: {str(e)}")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Add to GUI log
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Add to file log
        self.logger.info(message)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
    
    def save_settings(self):
        """Save current settings to file"""
        settings = {
            "click_points": self.click_points,
            "click_mode": self.click_mode.get(),
            "click_count": self.click_count_var.get(),
            "interval": self.interval_var.get(),
            "point_delay": self.point_delay_var.get(),
            "schedule_mode": self.schedule_mode.get(),
            "hour": self.hour_var.get(),
            "minute": self.minute_var.get()
        }
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            self.log_message("Settings saved successfully")
            messagebox.showinfo("Success", "Settings saved successfully")
        except Exception as e:
            self.log_message(f"Error saving settings: {str(e)}")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        """Load settings from file"""
        if not os.path.exists(self.settings_file):
            return
        
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
            
            self.click_points = settings.get("click_points", [])
            self.click_mode.set(settings.get("click_mode", "unlimited"))
            self.click_count_var.set(settings.get("click_count", "1"))
            self.interval_var.set(settings.get("interval", "1.0"))
            self.point_delay_var.set(settings.get("point_delay", "0.1"))
            self.schedule_mode.set(settings.get("schedule_mode", "immediate"))
            self.hour_var.set(settings.get("hour", "20"))
            self.minute_var.set(settings.get("minute", "00"))
            
            self.update_points_listbox()
            self.log_message("Settings loaded successfully")
            
        except Exception as e:
            self.log_message(f"Error loading settings: {str(e)}")
    
    def reset_settings(self):
        """Reset all settings to default"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings?"):
            self.click_points.clear()
            self.click_mode.set("unlimited")
            self.click_count_var.set("1")
            self.interval_var.set("1.0")
            self.point_delay_var.set("0.1")
            self.schedule_mode.set("immediate")
            self.hour_var.set("20")
            self.minute_var.set("00")
            
            self.update_points_listbox()
            self.log_message("Settings reset to default")

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    
    # Handle window close event
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel("Quit", "Auto clicker is running. Do you want to stop and quit?"):
                app.stop_clicking()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()