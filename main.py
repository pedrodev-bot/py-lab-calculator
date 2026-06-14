import customtkinter as ctk
from PIL import Image
from src import calc

# Theme global settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Laboratory - Accurate Calculator")
        self.geometry("800x600")
        self.resizable(False, False)

        self.setup_background()
        
        self.mode_map= {
            "Mean & Standard Deviation": "mean_std",
            "Full Report (1)": "full_report_1"
        }

        self.descriptions = {
            "placeholder": "Please choose a report or calculator format above to view its description.",
            "mean_std": "Computes mean values and determines uncertainty based on the standard deviation of the mean for multiple trials.",
            "full_report_1": "Generates the final formatted results combining means, standard deviations, and propagated errors for the entire experiment."
        }

        self.version = {
            "version": "1.0.0",
            "version.title": "Physics Laboratory"
        }

        self.build_interface()
    
    def setup_background(self):
        try:
            pil_image = Image.open("assets/fundo_menu.png")
            
            self.bg_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(800, 600)
            )
            
            self.bg_label = ctk.CTkLabel(
                self, 
                image=self.bg_image, 
                text=""
            )
            
        except Exception as e:
            print(f"Background error: {e}")
            self.bg_label = ctk.CTkLabel(self, text="", fg_color="#1a1a1a")

        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def build_interface(self):
        self.content_frame = ctk.CTkFrame(
            self.bg_label,
            fg_color="#121212",
            bg_color="transparent",
            corner_radius=0,
            border_width=2,
            border_color="#121212"
        )
        self.content_frame.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.9)
        self.content_frame.pack_propagate(False)
        
        # Footer
        self.build_footer(self.content_frame)

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Analysis Module",
            font=("Geist", 26, "bold"),
            text_color="white",
            fg_color="transparent"
        )
        title.pack(pady=(40, 0))

        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Uncertainty Calculator",
            font=("Geist", 13, "bold"),
            text_color="#3a7ebf", 
            fg_color="transparent"
        )
        subtitle.pack(pady=(0, 25))

        controls_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        controls_container.place(relx=0.5, rely=0.55, anchor="center")
        # Instruction
        instruction = ctk.CTkLabel(
            controls_container,
            text="Select report or calculator format:",
            font=("Inter", 13),
            text_color="gray70",
            fg_color="transparent"
        )
        instruction.pack(pady=(10, 5))

        # Dropdown menu
        self.report_menu = ctk.CTkOptionMenu(
            controls_container,
            values=["Mean & Standard Deviation", "Full Report (1)"],
            width=210,
            height=35,
            fg_color="#1f538d",
            button_color="#14375e",
            button_hover_color="#1e538d",

            dropdown_fg_color="#121212",
            dropdown_hover_color="#1f538d",
            dropdown_text_color="white",
            dropdown_font=("Inter", 12),

            command=self.update_description
        )
        self.report_menu.pack(pady=5)
        self.report_menu.set("Select a format...")
        self.report_menu.pack(pady=10)

        self.descriptions_label = ctk.CTkLabel(
            controls_container,
            text=self.descriptions["placeholder"],
            font=("Inter", 11, "italic"),
            text_color="gray50",
            wraplength=200,
            justify="center"
        )
        self.descriptions_label.pack(pady=(0, 15))

        # Start button
        btn_start = ctk.CTkButton(
            controls_container,
            text="Start",
            width=160,
            height=40,
            font=("Arial", 14, "bold"),
            command=self.start_calculator
        )
        btn_start.pack(pady=(40, 20))

    def update_description(self, current_choice):
        mode_id = self.mode_map.get(current_choice, "placeholder")

        new_text = self.descriptions.get(mode_id, "")
        self.descriptions_label.configure(
            text=new_text,
            text_color="gray50",
            font=("Inter", 11, "italic")
        )

    def resize_background(self, width, height):
        try:
            pil_image = Image.open("assets/fundo_menu_2.png")
            self.bg_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(width, height)
            )
            self.bg_label.configure(image=self.bg_image)
        except Exception as e:
            print(f"Warning - Error to resize background: {e}")

    def go_back_to_menu(self):
        if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
            self.content_frame.destroy()

        original_width = 800
        original_height = 600
        self.geometry(f"{original_width}x{original_height}")

        self.resize_background(original_width, original_height)

        self.build_interface()

    def build_footer(self, parent_frame):
        footer_text=f"{self.version["version"]} | {self.version["version.title"]}"

        footer = ctk.CTkLabel(
            parent_frame,
            text=footer_text,
            font=("Inter", 11),
            text_color="gray40",
            fg_color="transparent"
        )
        footer.pack(side="bottom", pady=10)

    def start_calculator(self):
        choice = self.report_menu.get()

        if choice == "Select a format...":
            self.descriptions_label.configure(
                text="⚠️ Please select a report format before starting.",
                text_color="#ff4c4c",
                font=("Inter", 11, "bold")
            )
            return
        
        mode_id = self.mode_map.get(choice)
        print(f"System log: Initialization requested for '{choice}' mode.")

        self.content_frame.destroy()

        new_width = 1024
        new_height = 720
        self.geometry(f"{new_width}x{new_height}")

        self.resize_background(new_width, new_height)

        if choice == "Mean & Standard Deviation":
            self.build_mean_std_screen()

    def animate_resize(self, target_w, target_h, steps=20):
        current_w = self.winfo_width()
        current_h = self.winfo_height()

        step_w = (target_w - current_w) / steps
        step_h = (target_h - current_h) / steps

        def update_size(i):
            if i < steps:
                new_w = int(current_w + step_w * i)
                new_h = int(current_h + step_h * i)
                self.geometry(f"{new_w}x{new_h}")
                self.after(10, lambda: update_size(i + 1))
            else:
                self.geometry(f"{target_w}x{target_h}")
            
        update_size(0)

    def build_mean_std_screen(self):
        self.content_frame = ctk.CTkFrame(
            self.bg_label, 
            fg_color="#121212", 
            bg_color="transparent",
            corner_radius=0, 
            border_width=2,
            border_color="#121212"
        )
        self.content_frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.85, anchor="center")
        self.content_frame.pack_propagate(False)

        # Footer
        self.build_footer(self.content_frame)

        # Back button
        btn_back = ctk.CTkButton(
            self.content_frame,
            text="← Back",
            width=80,
            height=30,
            fg_color="#2b2b2b",
            hover_color="#3d3d3d",
            font=("Inter", 12, "bold"),
            command=self.go_back_to_menu
        )
        btn_back.place(x=20, y=20) # Coordenadas fixas para ficar perfeito no canto

        # Titles
        title = ctk.CTkLabel(
            self.content_frame,
            text="Mean & Standard Deviation",
            font=("Inter", 26, "bold"),
            text_color="white"
        )
        title.pack(pady=(40, 5))

        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Uncertainty Analysis",
            font=("Inter", 14, "bold"),
            text_color="#3a7ebf"
        )
        subtitle.pack(pady=(0, 20))

        # Data entry
        instruction = ctk.CTkLabel(
            self.content_frame,
            text="Enter dataset values (separated by spaces, commas, or new lines):",
            font=("Inter", 13),
            text_color="gray70"
        )
        instruction.pack(pady=(10, 5))

        # Text box
        self.textbox_data = ctk.CTkTextbox(
            self.content_frame,
            width=300,
            height=150,
            fg_color="#1a1a1a",
            border_color="#000000",
            border_width=2
        )
        self.textbox_data.pack(pady=10)

        # Calculator button
        btn_calc = ctk.CTkButton(
            self.content_frame,
            text="Calculate Statistics",
            width=220,
            height=45,
            font=("Arial", 15, "bold"),
            command=self.calculate_mean_std
        )
        btn_calc.pack(pady=(20, 20))

        # Result area
        self.result_label = ctk.CTkLabel(
            self.content_frame,
            text="Awaiting data...",
            font=("Inter", 14),
            text_color="gray50",
            justify="center"
        )
        self.result_label.pack(pady=10)

    def calculate_mean_std(self):
        try:
            raw_data = self.textbox_data.get("1.0", "end-1c")

            if not raw_data.strip():
                self.result_label.configure(
                    text="⚠️ Please enter the dataset.",
                    text_color="#ff4c4c",
                    font=("Inter", 14, "bold")
                )
                return
            
            n, mean, std, u_mean = calc.uncertainty(raw_data)

            result_text = (
                f"Samples (n) : {n}\n"
                f"Mean (x̄)    : {mean:.4f}\n"
                f"Std Dev (s) : {std:.4f}\n"
                f"Uncertainty : {u_mean:.4f}"
            )

            self.result_label.configure(
                text=result_text,
                text_color="#f8f9fa",
                font=("Consolas", 16),
                justify="left"
            )

        except ValueError:
            self.result_label.configure(
                text="⚠️ Error: Ensure you enter at least 2 valid numbers.",
                text_color="#ff4c4c",
                font=("Inter", 14, "bold")
            )

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()