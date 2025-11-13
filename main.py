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
        self.root.title("🎯 Auto Clicker Pro")
        self.root.geometry("500x700")
        self.root.resizable(True, True)
        
        # Configure modern style
        self.setup_modern_style()
        
        # Initialize variables
        self.click_points = []
        self.is_running = False
        self.click_thread = None
        self.scheduled_time = None
        self.settings_file = "autoclicker_settings.json"
        self.emergency_stop = False
        
        # Setup emergency stop mechanisms
        self.setup_emergency_stops()
        
        # Setup logging
        self.setup_logging()
        
        # Disable pyautogui fail-safe (optional)
        pyautogui.FAILSAFE = True
        
        # Create GUI
        self.create_gui()
        
        # Load settings if they exist
        self.load_settings()
    
    def setup_modern_style(self):
        """Configure modern UI styling"""
        style = ttk.Style()
        
        # Configure modern colors
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#64748b',    # Gray
            'success': '#10b981',      # Green
            'warning': '#f59e0b',      # Orange
            'danger': '#ef4444',       # Red
            'light': '#f8fafc',        # Light gray
            'dark': '#1e293b'          # Dark gray
        }
        
        # Configure styles
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.colors['dark'])
        style.configure('Section.TLabelframe.Label', font=('Segoe UI', 10, 'bold'))
        style.configure('Primary.TButton', font=('Segoe UI', 9, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 9))
        style.configure('Danger.TButton', font=('Segoe UI', 9))
    
    def setup_logging(self):
        """Setup logging for action tracking"""
        logging.basicConfig(
            filename='autoclicker_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_emergency_stops(self):
        """Setup multiple emergency stop mechanisms"""
        # Bind keyboard shortcuts to main window and all events
        self.root.bind_all('<Escape>', self.emergency_stop_handler)
        self.root.bind_all('<F12>', self.emergency_stop_handler)
        self.root.bind_all('<Control-c>', self.emergency_stop_handler)
        self.root.bind_all('<Control-q>', self.emergency_stop_handler)
        self.root.bind_all('<Key-Escape>', self.emergency_stop_handler)
        self.root.bind_all('<KeyPress-Escape>', self.emergency_stop_handler)
        
        # Also bind to the root window directly
        self.root.bind('<Escape>', self.emergency_stop_handler)
        self.root.bind('<F12>', self.emergency_stop_handler)
        
        # Ensure the window can receive keyboard events
        self.root.focus_set()
        
        # Make sure keyboard focus is maintained
        def maintain_focus():
            if self.is_running:
                try:
                    self.root.focus_force()
                except:
                    pass
            self.root.after(1000, maintain_focus)  # Check every second
        
        maintain_focus()
        
        # Enable pyautogui failsafe (move mouse to top-left corner)
        pyautogui.FAILSAFE = True
        
        # Start emergency stop monitor thread with keyboard monitoring
        self.start_emergency_monitor()
        
        self.log_message("🛡️ Emergency stops active: ESC, F12, Ctrl+C, Ctrl+Q, or mouse to top-left corner")
    
    def emergency_stop_handler(self, event=None):
        """Handle emergency stop from keyboard"""
        self.trigger_emergency_stop()
        return "break"
    
    def start_emergency_monitor(self):
        """Start monitoring for emergency conditions"""
        def monitor():
            while True:
                try:
                    if self.is_running:
                        # Check mouse position for failsafe
                        mouse_x, mouse_y = pyautogui.position()
                        if mouse_x <= 5 and mouse_y <= 5:
                            self.trigger_emergency_stop()
                            
                        # Check for keyboard state using Windows API if available
                        try:
                            import ctypes
                            # Check ESC key (VK_ESCAPE = 0x1B)
                            if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
                                self.trigger_emergency_stop()
                            # Check F12 key (VK_F12 = 0x7B)  
                            if ctypes.windll.user32.GetAsyncKeyState(0x7B) & 0x8000:
                                self.trigger_emergency_stop()
                            # Check Ctrl+C (Ctrl = 0x11, C = 0x43)
                            if (ctypes.windll.user32.GetAsyncKeyState(0x11) & 0x8000) and (ctypes.windll.user32.GetAsyncKeyState(0x43) & 0x8000):
                                self.trigger_emergency_stop()
                        except:
                            pass  # Fallback to other methods if ctypes not available
                        
                        # Check for emergency stop file
                        if os.path.exists("EMERGENCY_STOP"):
                            self.trigger_emergency_stop()
                            try:
                                os.remove("EMERGENCY_STOP")
                            except:
                                pass
                    
                    time.sleep(0.05)  # Check every 50ms for faster response
                except:
                    break
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def trigger_emergency_stop(self):
        """Trigger emergency stop from any source"""
        if self.is_running:
            self.emergency_stop = True
            self.is_running = False
            self.log_message("🚨 EMERGENCY STOP ACTIVATED!")
            try:
                self.root.after(0, self.force_stop_clicking)
            except:
                # If we can't schedule in main thread, force stop immediately
                self.force_stop_clicking()
    
    def force_stop_clicking(self):
        """Force stop all clicking operations immediately"""
        self.emergency_stop = True
        self.is_running = False
        
        # Update UI immediately
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.update_status("🚨 EMERGENCY STOPPED", "danger")
        
        # Show emergency notification
        self.show_notification("Emergency Stop", "Auto clicker stopped immediately!")
        
        # Log the emergency stop
        self.log_message("🚨 Emergency stop executed - All clicking stopped immediately")
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Configure root window
        self.root.configure(bg='#f8fafc')
        
        # Main scrollable frame
        canvas = tk.Canvas(self.root, bg='#f8fafc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main frame with modern padding
        main_frame = ttk.Frame(scrollable_frame, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Modern header with status
        self.create_header(main_frame, 0)
        
        # Create main sections in a compact layout
        self.create_click_points_section(main_frame, 1)
        self.create_settings_and_schedule_section(main_frame, 2)  # Combined section
        self.create_control_section(main_frame, 3)
        self.create_log_section(main_frame, 4)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_header(self, parent, row):
        """Create modern header with title and status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        # App title with icon
        title_label = ttk.Label(header_frame, text="🎯 Auto Clicker Pro", style="Title.TLabel")
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Status indicator
        self.status_frame = ttk.Frame(header_frame)
        self.status_frame.grid(row=0, column=1, sticky=tk.E)
        
        self.status_indicator = tk.Label(self.status_frame, text="●", fg=self.colors['success'], 
                                       font=('Segoe UI', 12), bg='#f8fafc')
        self.status_indicator.grid(row=0, column=0, padx=(0, 5))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", foreground=self.colors['success'])
        self.status_label.grid(row=0, column=1)
        
        # Current time
        self.current_time_label = ttk.Label(header_frame, text="", 
                                          font=('Segoe UI', 8), foreground=self.colors['secondary'])
        self.current_time_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        self.update_current_time()
    
    def create_click_points_section(self, parent, row):
        """Create compact click points section"""
        points_frame = ttk.LabelFrame(parent, text="📍 Click Points", padding="8", style="Section.TLabelframe")
        points_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        points_frame.columnconfigure(0, weight=1)
        
        # Top controls - horizontal layout
        controls_frame = ttk.Frame(points_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        controls_frame.columnconfigure(2, weight=1)
        
        # Add point button
        ttk.Button(controls_frame, text="+ Add Point", 
                  command=self.add_click_point, style="Primary.TButton").grid(row=0, column=0, padx=(0, 8))
        
        # Manual entry - compact
        coord_frame = ttk.Frame(controls_frame)
        coord_frame.grid(row=0, column=1, padx=(0, 8))
        
        self.x_entry = ttk.Entry(coord_frame, width=6, font=('Segoe UI', 8))
        self.x_entry.grid(row=0, column=0, padx=(0, 2))
        
        ttk.Label(coord_frame, text="×", font=('Segoe UI', 8)).grid(row=0, column=1, padx=2)
        
        self.y_entry = ttk.Entry(coord_frame, width=6, font=('Segoe UI', 8))
        self.y_entry.grid(row=0, column=2, padx=(2, 0))
        
        ttk.Button(coord_frame, text="Add", 
                  command=self.add_manual_point, width=6).grid(row=0, column=3, padx=(5, 0))
        
        # Action buttons
        action_frame = ttk.Frame(controls_frame)
        action_frame.grid(row=0, column=2, sticky=tk.E)
        
        ttk.Button(action_frame, text="Remove", 
                  command=self.remove_click_point, width=8).grid(row=0, column=0, padx=(0, 3))
        ttk.Button(action_frame, text="Clear", 
                  command=self.clear_all_points, width=8).grid(row=0, column=1)
        
        # Compact points list
        self.points_listbox = tk.Listbox(points_frame, height=4, font=('Consolas', 9),
                                       selectmode=tk.SINGLE, activestyle='dotbox')
        self.points_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Points counter
        self.points_counter = ttk.Label(points_frame, text="No points added", 
                                      font=('Segoe UI', 8), foreground=self.colors['secondary'])
        self.points_counter.grid(row=2, column=0, sticky=tk.W)
    
    def create_settings_and_schedule_section(self, parent, row):
        """Create combined settings and schedule section"""
        # Main container with two columns
        main_container = ttk.Frame(parent)
        main_container.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        
        # Left column - Click Settings
        settings_frame = ttk.LabelFrame(main_container, text="⚙️ Settings", padding="8", style="Section.TLabelframe")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Click mode - compact radio buttons
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        self.click_mode = tk.StringVar(value="unlimited")
        ttk.Radiobutton(mode_frame, text="Unlimited", 
                       variable=self.click_mode, value="unlimited").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Limited", 
                       variable=self.click_mode, value="limited").grid(row=0, column=1, sticky=tk.W, padx=(15, 0))
        
        # Settings grid - compact
        ttk.Label(settings_frame, text="Count:", font=('Segoe UI', 8)).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.click_count_var = tk.StringVar(value="100")
        ttk.Entry(settings_frame, textvariable=self.click_count_var, width=8, font=('Segoe UI', 8)).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(settings_frame, text="Interval (s):", font=('Segoe UI', 8)).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.interval_var = tk.StringVar(value="1.0")
        ttk.Entry(settings_frame, textvariable=self.interval_var, width=8, font=('Segoe UI', 8)).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(settings_frame, text="Point delay (s):", font=('Segoe UI', 8)).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.point_delay_var = tk.StringVar(value="0.1")
        ttk.Entry(settings_frame, textvariable=self.point_delay_var, width=8, font=('Segoe UI', 8)).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Right column - Schedule
        schedule_frame = ttk.LabelFrame(main_container, text="⏰ Schedule", padding="8", style="Section.TLabelframe")
        schedule_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Schedule mode
        self.schedule_mode = tk.StringVar(value="immediate")
        ttk.Radiobutton(schedule_frame, text="Start now", 
                       variable=self.schedule_mode, value="immediate").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Radiobutton(schedule_frame, text="Schedule", 
                       variable=self.schedule_mode, value="scheduled").grid(row=1, column=0, sticky=tk.W, pady=(0, 8))
        
        # Time selection - compact
        time_frame = ttk.Frame(schedule_frame)
        time_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(time_frame, text="Time:", font=('Segoe UI', 8)).grid(row=0, column=0, sticky=tk.W)
        
        self.hour_var = tk.StringVar(value="20")
        self.minute_var = tk.StringVar(value="00")
        
        hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=4, 
                                  textvariable=self.hour_var, format="%02.0f", font=('Segoe UI', 8))
        hour_spinbox.grid(row=0, column=1, padx=(5, 2))
        
        ttk.Label(time_frame, text=":", font=('Segoe UI', 8)).grid(row=0, column=2)
        
        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=4, 
                                    textvariable=self.minute_var, format="%02.0f", font=('Segoe UI', 8))
        minute_spinbox.grid(row=0, column=3, padx=(2, 0))
    
    def create_control_section(self, parent, row):
        """Create compact control section"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Controls", padding="8", style="Section.TLabelframe")
        control_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # Main controls
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, pady=(0, 8))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Clicking", 
                                      command=self.start_clicking, style="Primary.TButton", width=15)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Stop", 
                                     command=self.stop_clicking, state="disabled", 
                                     style="Danger.TButton", width=10)
        self.stop_button.grid(row=0, column=1, padx=(0, 5))
        
        # Emergency stop button (always visible)
        self.emergency_button = ttk.Button(button_frame, text="🚨 EMERGENCY", 
                                          command=self.trigger_emergency_stop,
                                          width=12)
        self.emergency_button.grid(row=0, column=2)
        self.emergency_button.configure(style="Danger.TButton")
        
        # Emergency instructions
        emergency_info = ttk.Label(control_frame, 
                                 text="🛡️ Emergency Stops: ESC • F12 • Ctrl+C • Mouse to corner • EMERGENCY.bat", 
                                 font=('Segoe UI', 8), foreground=self.colors['secondary'])
        emergency_info.grid(row=1, column=0, pady=(5, 8))
        
        # Settings management
        settings_button_frame = ttk.Frame(control_frame)
        settings_button_frame.grid(row=2, column=0)
        
        ttk.Button(settings_button_frame, text="💾", 
                  command=self.save_settings, width=4).grid(row=0, column=0, padx=(0, 3))
        ttk.Button(settings_button_frame, text="📂", 
                  command=self.load_settings, width=4).grid(row=0, column=1, padx=(0, 3))
        ttk.Button(settings_button_frame, text="🔄", 
                  command=self.reset_settings, width=4).grid(row=0, column=2)
    
    def create_log_section(self, parent, row):
        """Create compact log section"""
        log_frame = ttk.LabelFrame(parent, text="📋 Activity Log", padding="8", style="Section.TLabelframe")
        log_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log header with clear button
        log_header = ttk.Frame(log_frame)
        log_header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        log_header.columnconfigure(0, weight=1)
        
        self.log_status = ttk.Label(log_header, text="Ready to start...", 
                                  font=('Segoe UI', 8), foreground=self.colors['secondary'])
        self.log_status.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(log_header, text="Clear", 
                  command=self.clear_log, width=8).grid(row=0, column=1, sticky=tk.E)
        
        # Compact log text
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_text_frame, height=6, wrap=tk.WORD, 
                               font=('Consolas', 8), bg='#f8fafc', relief='flat', bd=1)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def update_current_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%H:%M:%S - %b %d")
        self.current_time_label.config(text=current_time)
        self.root.after(1000, self.update_current_time)
    
    def add_click_point(self):
        """Add a click point with visual confirmation"""
        self.show_point_selector()
    
    def show_point_selector(self):
        """Show point selection window with visual feedback"""
        # Create fullscreen overlay window
        overlay = tk.Toplevel(self.root)
        overlay.title("Select Click Point")
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-alpha', 0.3)  # Semi-transparent
        overlay.configure(bg='red')
        overlay.attributes('-topmost', True)
        
        # Create crosshair cursor
        overlay.config(cursor='crosshair')
        
        # Instructions label
        instruction_label = tk.Label(
            overlay, 
            text="🎯 CLICK ANYWHERE TO SET POINT\n\n• Click to select location\n• Press ESC to cancel\n• Move mouse to see coordinates",
            font=('Segoe UI', 16, 'bold'),
            bg='black',
            fg='white',
            padx=20,
            pady=15
        )
        instruction_label.place(relx=0.5, rely=0.1, anchor='center')
        
        # Coordinate display
        coord_label = tk.Label(
            overlay,
            text="Position: (0, 0)",
            font=('Consolas', 14, 'bold'),
            bg='black',
            fg='yellow',
            padx=10,
            pady=5
        )
        coord_label.place(relx=0.5, rely=0.2, anchor='center')
        
        def update_coordinates(event):
            coord_label.config(text=f"Position: ({event.x_root}, {event.y_root})")
        
        def on_click(event):
            # Get actual screen coordinates
            x, y = event.x_root, event.y_root
            overlay.destroy()
            
            # Show confirmation dialog
            self.confirm_click_point(x, y)
        
        def on_escape(event):
            overlay.destroy()
            self.log_message("Point selection cancelled")
        
        # Bind events
        overlay.bind('<Button-1>', on_click)
        overlay.bind('<Motion>', update_coordinates)
        overlay.bind('<Escape>', on_escape)
        overlay.bind('<KeyPress-Escape>', on_escape)
        
        # Focus the overlay
        overlay.focus_set()
        overlay.grab_set()
        
        self.log_message("Point selection mode active - Click anywhere to set point")
    
    def confirm_click_point(self, x, y):
        """Show confirmation dialog with point preview"""
        # Create confirmation window
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirm Click Point")
        confirm_window.geometry("400x300")
        confirm_window.resizable(False, False)
        confirm_window.configure(bg='#f8fafc')
        confirm_window.attributes('-topmost', True)
        
        # Center the window
        confirm_window.update_idletasks()
        x_pos = (confirm_window.winfo_screenwidth() // 2) - 200
        y_pos = (confirm_window.winfo_screenheight() // 2) - 150
        confirm_window.geometry(f"400x300+{x_pos}+{y_pos}")
        
        # Title
        title_label = tk.Label(
            confirm_window,
            text="🎯 Confirm Click Point",
            font=('Segoe UI', 14, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        title_label.pack(pady=15)
        
        # Coordinates display
        coord_frame = tk.Frame(confirm_window, bg='#f8fafc')
        coord_frame.pack(pady=10)
        
        tk.Label(
            coord_frame,
            text="Selected Position:",
            font=('Segoe UI', 10, 'bold'),
            bg='#f8fafc'
        ).pack()
        
        tk.Label(
            coord_frame,
            text=f"X: {x}, Y: {y}",
            font=('Consolas', 12, 'bold'),
            bg='#e2e8f0',
            fg='#2563eb',
            padx=10,
            pady=5
        ).pack(pady=5)
        
        # Preview button
        preview_btn = tk.Button(
            confirm_window,
            text="🔍 Preview Click Location",
            font=('Segoe UI', 10),
            bg='#64748b',
            fg='white',
            padx=20,
            pady=5,
            command=lambda: self.preview_click_location(x, y)
        )
        preview_btn.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(confirm_window, bg='#f8fafc')
        button_frame.pack(pady=20)
        
        def confirm_add():
            self.click_points.append((x, y))
            self.update_points_listbox()
            self.log_message(f"✅ Added click point: ({x}, {y})")
            confirm_window.destroy()
        
        def cancel_add():
            confirm_window.destroy()
            self.log_message("❌ Click point cancelled")
        
        # Confirm button
        confirm_btn = tk.Button(
            button_frame,
            text="✅ Add This Point",
            font=('Segoe UI', 10, 'bold'),
            bg='#10b981',
            fg='white',
            padx=20,
            pady=8,
            command=confirm_add
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            font=('Segoe UI', 10),
            bg='#ef4444',
            fg='white',
            padx=20,
            pady=8,
            command=cancel_add
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = tk.Label(
            confirm_window,
            text="Use 'Preview' to see a marker at the click location\nbefore confirming the point.",
            font=('Segoe UI', 8),
            bg='#f8fafc',
            fg='#64748b'
        )
        instructions.pack(pady=10)
        
        # Focus and grab
        confirm_window.focus_set()
        confirm_window.grab_set()
    
    def preview_click_location(self, x, y):
        """Show a temporary marker at the click location"""
        # Create a small marker window
        marker = tk.Toplevel()
        marker.title("Click Point Preview")
        marker.geometry("60x60")
        marker.configure(bg='red')
        marker.overrideredirect(True)  # Remove window decorations
        marker.attributes('-topmost', True)
        
        # Position marker at click location
        marker.geometry(f"60x60+{x-30}+{y-30}")
        
        # Create crosshair marker
        canvas = tk.Canvas(marker, width=60, height=60, bg='red', highlightthickness=0)
        canvas.pack()
        
        # Draw crosshair
        canvas.create_line(0, 30, 60, 30, fill='white', width=3)  # Horizontal
        canvas.create_line(30, 0, 30, 60, fill='white', width=3)  # Vertical
        canvas.create_oval(25, 25, 35, 35, outline='white', width=3)  # Center circle
        
        # Add text
        canvas.create_text(30, 45, text="CLICK", fill='white', font=('Arial', 8, 'bold'))
        
        # Auto-destroy after 3 seconds
        marker.after(3000, marker.destroy)
        
        self.log_message(f"🎯 Preview marker shown at ({x}, {y})")
    
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
            self.points_listbox.insert(tk.END, f"{i:2d}. ({x:4d}, {y:4d})")
        
        # Update counter
        count = len(self.click_points)
        if count == 0:
            self.points_counter.config(text="No points added")
        elif count == 1:
            self.points_counter.config(text="1 point added")
        else:
            self.points_counter.config(text=f"{count} points added")
    
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
        self.emergency_stop = False  # Reset emergency stop flag
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        if self.schedule_mode.get() == "immediate":
            self.update_status("Running...", "primary")
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
                self.update_status(f"Scheduled for {scheduled_time.strftime('%H:%M')}", "warning")
                
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
        self.emergency_stop = True  # Set emergency flag for immediate stop
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.update_status("Stopped", "danger")
        self.log_message("⏹ Clicking stopped by user")
    
    def update_status(self, message, status_type="success"):
        """Update status indicator and message"""
        color_map = {
            "success": self.colors['success'],
            "warning": self.colors['warning'], 
            "danger": self.colors['danger'],
            "primary": self.colors['primary']
        }
        
        color = color_map.get(status_type, self.colors['success'])
        self.status_label.config(text=message, foreground=color)
        self.status_indicator.config(fg=color)
        self.log_status.config(text=message)
    
    def scheduled_click_worker(self):
        """Worker thread for scheduled clicking"""
        while self.is_running and self.scheduled_time:
            current_time = datetime.now()
            if current_time >= self.scheduled_time:
                self.update_status("Running...", "primary")
                self.log_message(f"Scheduled clicking started at {current_time.strftime('%H:%M:%S')}")
                self.show_notification("Auto Clicker Started", "Scheduled clicking has begun!")
                self.click_worker()
                break
            time.sleep(0.1)  # Check every 100ms for precision
    
    def click_worker(self):
        """Worker thread for clicking with emergency stop checks"""
        try:
            click_count = 0
            max_clicks = None
            
            if self.click_mode.get() == "limited":
                max_clicks = int(self.click_count_var.get())
            
            interval = float(self.interval_var.get())
            point_delay = float(self.point_delay_var.get())
            
            self.log_message(f"Starting clicks - Mode: {self.click_mode.get()}, "
                           f"Count: {self.click_count_var.get()}, Max: {max_clicks}, "
                           f"Interval: {interval}s, Points: {len(self.click_points)}")
            
            while self.is_running and not self.emergency_stop:
                # Check emergency stop before each cycle
                if self.emergency_stop or not self.is_running:
                    self.log_message(f"Stopping due to emergency_stop: {self.emergency_stop}, is_running: {self.is_running}")
                    break
                    
                if max_clicks and click_count >= max_clicks:
                    self.log_message(f"Stopping due to max_clicks reached: {click_count} >= {max_clicks}")
                    break
                
                self.log_message(f"Starting click cycle {click_count + 1}, max_clicks: {max_clicks}")
                
                # Click each point
                for point_index, (x, y) in enumerate(self.click_points):
                    # Multiple emergency stop checks
                    if self.emergency_stop or not self.is_running:
                        break
                    
                    try:
                        # Check emergency stop right before clicking
                        if self.emergency_stop or not self.is_running:
                            break
                            
                        pyautogui.click(x, y)
                        click_count += 1
                        self.log_message(f"Clicked point {point_index + 1}: ({x}, {y}) - Total clicks: {click_count}")
                        
                        if max_clicks and click_count >= max_clicks:
                            break
                        
                        # Emergency stop check during delay
                        if point_delay > 0 and point_index < len(self.click_points) - 1:
                            # Split delay into smaller chunks for faster emergency response
                            delay_chunks = max(1, int(point_delay * 10))  # 0.1s chunks
                            for _ in range(delay_chunks):
                                if self.emergency_stop or not self.is_running:
                                    break
                                time.sleep(point_delay / delay_chunks)
                            
                    except pyautogui.FailSafeException:
                        self.emergency_stop = True
                        self.log_message("🚨 PyAutoGUI Failsafe triggered - mouse moved to corner!")
                        break
                    except Exception as e:
                        self.log_message(f"Error clicking point ({x}, {y}): {str(e)}")
                
                if max_clicks and click_count >= max_clicks:
                    self.log_message(f"Reached max clicks after point loop: {click_count} >= {max_clicks}")
                    break
                
                self.log_message(f"Completed click cycle, total clicks: {click_count}, waiting for interval: {interval}s")
                
                # Emergency stop check during main interval
                if self.is_running and not self.emergency_stop and interval > 0:
                    # Split interval into smaller chunks for faster emergency response
                    interval_chunks = max(1, int(interval * 10))  # 0.1s chunks
                    for _ in range(interval_chunks):
                        if self.emergency_stop or not self.is_running:
                            break
                        time.sleep(interval / interval_chunks)
            
            # Finished (either completed or emergency stopped)
            if self.emergency_stop:
                self.root.after(0, self.force_stop_clicking)
            else:
                self.root.after(0, self.clicking_finished, click_count)
            
        except pyautogui.FailSafeException:
            self.emergency_stop = True
            self.log_message("🚨 PyAutoGUI Failsafe triggered!")
            self.root.after(0, self.force_stop_clicking)
        except Exception as e:
            self.log_message(f"Error in click worker: {str(e)}")
            self.root.after(0, self.clicking_finished, 0)
    
    def clicking_finished(self, total_clicks):
        """Called when clicking is finished"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.update_status(f"Completed - {total_clicks} clicks", "success")
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
        
        # Add to GUI log (if GUI is created)
        try:
            if hasattr(self, 'log_text') and self.log_text:
                self.log_text.insert(tk.END, log_entry)
                self.log_text.see(tk.END)
        except:
            pass  # GUI not ready yet
        
        # Add to file log
        try:
            self.logger.info(message)
        except:
            pass  # Logger not ready yet
    
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
            self.click_count_var.set("100")
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
    
    # Center the window and set modern appearance
    root.update_idletasks()
    width, height = 500, 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(450, 600)
    
    root.mainloop()

if __name__ == "__main__":
    main()