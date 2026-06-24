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
            "Exp 2: Parallel Plates": "exp2_plates"
        }

        self.descriptions = {
            "placeholder": "Please choose a report or calculator format above to view its description.",
            "mean_std": "Computes mean values and determines uncertainty based on the standard deviation of the mean for multiple trials.",
            "exp2_plates": "Processes Tables 1 and 2, calculates 1/d, performs linear regression, and finds vacuum permittivity."
        }

        self.version = {
            "version": "1.1.0",
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
            values=["Mean & Standard Deviation", "Exp 2: Parallel Plates"],
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
        elif choice == "Exp 2: Parallel Plates":
            self.build_exp2_plates_screen()

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

    def build_exp2_plates_screen(self):
        self.content_frame = ctk.CTkFrame(
            self.bg_label,
            fg_color="#121212",
            bg_color="transparent",
            corner_radius=0,
            border_width=2,
            border_color="#121212"
        )
        self.content_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.9, anchor="center")
        self.content_frame.pack_propagate(False)

        self.build_footer(self.content_frame)

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
        btn_back.place(x=20, y=20)

        title = ctk.CTkLabel(
            self.content_frame,
            text="Experiment 2: Parallel Plates",
            font=("Inter", 26, "bold"),
            text_color="white"
        )
        title.pack(pady=(20, 5))

        # Constants Frame
        constants_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent")
        constants_frame.pack(pady=10)

        ctk.CTkLabel(constants_frame, text="C residual (pF):").grid(row=0, column=0, padx=5)
        self.entry_c_res = ctk.CTkEntry(constants_frame, width=80)
        self.entry_c_res.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(constants_frame, text="σ C residual:").grid(row=0, column=2, padx=5)
        self.entry_sig_c_res = ctk.CTkEntry(constants_frame, width=80)
        self.entry_sig_c_res.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(constants_frame, text="Diameter (m):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_diam = ctk.CTkEntry(constants_frame, width=80)
        self.entry_diam.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(constants_frame, text="σ Diameter (m):").grid(row=1, column=2, padx=5, pady=5)
        self.entry_sig_diam = ctk.CTkEntry(constants_frame, width=80)
        self.entry_sig_diam.grid(row=1, column=3, padx=5, pady=5)

        # Data Entry
        instruction = ctk.CTkLabel(
            self.content_frame,
            text="Enter data rows: d1 d2 d3 C_medida σ_C_medida\n(Separate values by space, one measurement per line)",
            font=("Inter", 13),
            text_color="gray70"
        )
        instruction.pack(pady=(10, 5))

        self.textbox_exp2 = ctk.CTkTextbox(
            self.content_frame,
            width=500,
            height=150,
            fg_color="#1a1a1a",
            border_color="#000000",
            border_width=2
        )
        self.textbox_exp2.pack(pady=5)

        btn_calc = ctk.CTkButton(
            self.content_frame,
            text="Process Report Data",
            width=220,
            height=40,
            font=("Arial", 15, "bold"),
            command=self.calculate_exp2_plates
        )
        btn_calc.pack(pady=10)

        self.result_exp2 = ctk.CTkTextbox(
            self.content_frame,
            width=600,
            height=200,
            fg_color="#1a1a1a",
            font=("Consolas", 14),
            text_color="#f8f9fa"
        )
        self.result_exp2.pack(pady=10)

    def calculate_exp2_plates(self):
        try:
            # 1. Get constants
            c_res = float(self.entry_c_res.get().replace(',', '.'))
            sig_c_res = float(self.entry_sig_c_res.get().replace(',', '.'))
            diam = float(self.entry_diam.get().replace(',', '.'))
            sig_diam = float(self.entry_sig_diam.get().replace(',', '.'))
            c0 = float(self.entry_c0.get().replace(',', '.')) if self.entry_c0.get() else 0.0
            cpapel = float(self.entry_cpapel.get().replace(',', '.')) if self.entry_cpapel.get() else 0.0

            # 2. Get and parse textbox data
            raw_data = self.textbox_exp2.get("1.0", "end-1c").strip().split('\n')
            
            d1_list, d2_list, d3_list, c_med_list, sig_med_list = [], [], [], [], []
            
            for line in raw_data:
                if not line.strip(): continue
                vals = [float(x.replace(',', '.')) for x in line.split()]
                if len(vals) != 5:
                    raise ValueError("Each line must have exactly 5 values.")
                
                d1_list.append(vals[0])
                d2_list.append(vals[1])
                d3_list.append(vals[2])
                c_med_list.append(vals[3])
                sig_med_list.append(vals[4])

            # 3. Process Table 1 & 2
            tab1 = calc.process_table1(d1_list, d2_list, d3_list, c_med_list, sig_med_list, c_res, sig_c_res)
            
            d_means = [row[0] for row in tab1]
            sig_ds = [row[1] for row in tab1]
            c_caps = [row[2] for row in tab1]
            sig_cs = [row[3] for row in tab1]

            tab2 = calc.process_table2(d_means, sig_ds, c_caps, sig_cs)
            
            w_list = [row[0] for row in tab2]
            sig_w_list = [row[1] for row in tab2]

            # 4. Linear Regression & Permittivity
            # Convert w (1/mm to 1/m) by multiplying by 1000
            w_list_SI = [w * 1000 for w in w_list] 

            # Convert Capacitance (pF to F) by multiplying by 1e-12
            c_caps_SI = [c * 1e-12 for c in c_caps]
            sig_cs_SI = [s * 1e-12 for s in sig_cs]
            a, sig_a, b, sig_b = calc.linear_least_squares(w_list_SI, c_caps_SI, sig_cs_SI)
            eps0, sig_eps0 = calc.calculate_permittivity(a, sig_a, diam, sig_diam)

            # 5. Format Output
            out = "1. REGRESSION RESULTS\n"
            out += f"Angular (a) : {a:.4e} ± {sig_a:.4e}\n"
            out += f"Linear  (b) : {b:.4f} ± {sig_b:.4f}\n"
            out += f"Epsilon_0   : {eps0:.4e} ± {sig_eps0:.4e} F/m\n\n"
            
            out += "2. PROCESSED DATA for TABLE 1 (Copy to Report) ---\n"
            out += "d_mean (mm)   | σ_d (mm)    | C_cap (pF)  | σ_C_cap (pF)\n"
            out += "-"*60 + "\n"
            for row in tab1:
                out += f"{row[0]:<13.4f} | {row[1]:<11.4f} | {row[2]:<11.4f} | {row[3]:<12.4f}\n"
            out += "\n"

            out += "3. PROCESSED DATA for TABLE 2 (Copy to Report)\n"
            out += "w (1/d)       | σ_w         | C_cap (pF)  | σ_C_cap (pF)\n"
            out += "-"*55 + "\n"
            for row in tab2:
                w_m = row[0] * 1000
                sig_w_m = row[1] * 1000
                out += f"{w_m:<13.4f} | {sig_w_m:<11.4f} | {row[2]:<11.4f} | {row[3]:<11.4f}\n"

            self.result_exp2.delete("1.0", "end")
            self.result_exp2.insert("1.0", out)

        except ValueError as e:
            self.result_exp2.delete("1.0", "end")
            self.result_exp2.insert("1.0", f"⚠️ Input Error: {e}\nCheck if all fields are filled correctly.")
        except Exception as e:
            self.result_exp2.delete("1.0", "end")
            self.result_exp2.insert("1.0", f"⚠️ Processing Error: {e}")

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()