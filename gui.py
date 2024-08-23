import customtkinter as ctk
import keyboard
from controller import MacroController
from config import Config

# Create a Config instance with default values
config = Config()

# Initialize the MacroController with the config
controller = MacroController(config)

# Create GUI using customtkinter
ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Change the color theme

root = ctk.CTk()  # Use CTk for the main window
root.title("Macro Configurator")

# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Capture key press for Macro Key
def capture_macro_key():
    key = keyboard.read_event().name
    macro_key_var.set(key)
    config.macro_key = key
    config.saved_macro_key = key
    print(f"Macro Key set to: {key}")

# Capture key press for Toggle Key
def capture_toggle_key():
    key = keyboard.read_event().name 
    toggle_key_var.set(key)
    config.toggle_key = key
    print(f"Toggle Key set to: {key}")

# Macro Key setting
ctk.CTkLabel(main_frame, text="Macro Key:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
macro_key_var = ctk.StringVar(value=controller.config.macro_key)
macro_key_entry = ctk.CTkEntry(main_frame, textvariable=macro_key_var, width=150, state="disabled")
macro_key_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
macro_key_button = ctk.CTkButton(main_frame, text="Set Macro Key", command=capture_macro_key)
macro_key_button.grid(row=0, column=2, padx=10, pady=5)

# Toggle Key setting
ctk.CTkLabel(main_frame, text="Toggle Key:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
toggle_key_var = ctk.StringVar(value=controller.config.toggle_key)
toggle_key_entry = ctk.CTkEntry(main_frame, textvariable=toggle_key_var, width=150, state="disabled")
toggle_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
toggle_key_button = ctk.CTkButton(main_frame, text="Set Toggle Key", command=capture_toggle_key)
toggle_key_button.grid(row=1, column=2, padx=10, pady=5)

# Sleep Time setting
ctk.CTkLabel(main_frame, text="Sleep Time (seconds):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
sleep_time_var = ctk.StringVar(value=controller.config.sleep_time)
sleep_time_entry = ctk.CTkEntry(main_frame, textvariable=sleep_time_var, width=150)
sleep_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Apply button
apply_button = ctk.CTkButton(main_frame, text="Apply", command=lambda: controller.apply_settings(
    macro_key_var.get(), toggle_key_var.get(), float(sleep_time_var.get())))
apply_button.grid(row=3, column=0, columnspan=3, pady=10)

# Run the GUI
root.mainloop()
