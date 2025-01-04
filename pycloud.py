import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageTk
import os
from PIL import Image as PILImage  # For resizing with Resampling.LANCZOS
from collections import Counter
import random

class UltimateWordCloudApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ultimate WordCloud Generator")
        
        # ---------- Appearance Settings (Cozy Feminine Theme) ----------
        self.bg_color_app   = "#2A2B2E"  # Main background color
        self.bg_color_frame = "#3D3E42"  # Frame background
        self.fg_color_text  = "#FFFFFF"  # Text color
        self.accent_color   = "#B85CB7"  # Accent color (buttons, highlights)
        
        # Configure the main window
        self.master.config(bg=self.bg_color_app)
        
        # ---------- Frames for Layout ----------
        self.settings_frame = tk.Frame(self.master, bg=self.bg_color_frame, padx=10, pady=10)
        self.settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.preview_frame = tk.Frame(self.master, bg=self.bg_color_app, padx=10, pady=10)
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ---------- Word Cloud Settings Section ----------
        # 1) File selection (Text File)
        self.label_file = tk.Label(
            self.settings_frame, text="Text File:", 
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_file.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_file = tk.Entry(self.settings_frame, width=30)
        self.entry_file.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.button_browse_text = tk.Button(
            self.settings_frame, text="Browse...", 
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.browse_text_file
        )
        self.button_browse_text.grid(row=0, column=2, padx=5, pady=5)
        
        # 2) Excluded words
        self.label_exclude = tk.Label(
            self.settings_frame, 
            text="Exclude Words (comma-separated):",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_exclude.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_exclude = tk.Entry(self.settings_frame, width=30)
        self.entry_exclude.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        # 3) Use Built-in English Stopwords?
        self.use_stopwords_var = tk.BooleanVar(value=False)
        self.check_use_stopwords = tk.Checkbutton(
            self.settings_frame, text="Use Default English Stopwords",
            bg=self.bg_color_frame, fg=self.fg_color_text,
            selectcolor=self.bg_color_frame, variable=self.use_stopwords_var
        )
        self.check_use_stopwords.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # 4) Background color
        self.label_bg_color = tk.Label(
            self.settings_frame, text="Background Color (hex):",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_bg_color.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_bg_color = tk.Entry(self.settings_frame, width=30)
        self.entry_bg_color.insert(0, "#FFFFFF")  # Default
        self.entry_bg_color.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        self.button_bg_color = tk.Button(
            self.settings_frame, text="Pick BG Color", 
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.pick_bg_color
        )
        self.button_bg_color.grid(row=3, column=2, padx=5, pady=5)

        # 5) Font color(s)
        self.label_color = tk.Label(
            self.settings_frame, text="Font Color(s) (comma-separated):",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_color.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_color = tk.Entry(self.settings_frame, width=30)
        self.entry_color.insert(0, "#000000")  # Default
        self.entry_color.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # (Optional) color picker for a single color - can append to entry
        self.button_color_picker = tk.Button(
            self.settings_frame, text="Pick Text Color",
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.pick_text_color
        )
        self.button_color_picker.grid(row=4, column=2, padx=5, pady=5)

        # 6) Sliders: Max Words
        self.label_max_words = tk.Label(
            self.settings_frame, text="Max Words:",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_max_words.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        
        self.slider_max_words = tk.Scale(
            self.settings_frame, from_=10, to=500, orient=tk.HORIZONTAL,
            bg=self.bg_color_frame, fg=self.fg_color_text, highlightthickness=0
        )
        self.slider_max_words.set(200)
        self.slider_max_words.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # 7) Sliders: Max Font Size
        self.label_max_font_size = tk.Label(
            self.settings_frame, text="Max Font Size:",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_max_font_size.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        
        self.slider_max_font_size = tk.Scale(
            self.settings_frame, from_=10, to=200, orient=tk.HORIZONTAL,
            bg=self.bg_color_frame, fg=self.fg_color_text, highlightthickness=0
        )
        self.slider_max_font_size.set(60)
        self.slider_max_font_size.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # 8) Collocations checkbox
        self.collocations_var = tk.BooleanVar(value=True)
        self.check_collocations = tk.Checkbutton(
            self.settings_frame, text="Enable Collocations",
            bg=self.bg_color_frame, fg=self.fg_color_text,
            selectcolor=self.bg_color_frame, variable=self.collocations_var
        )
        self.check_collocations.grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # 9) Random seed entry
        self.label_random_state = tk.Label(
            self.settings_frame, text="Random Seed (optional):",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_random_state.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_random_state = tk.Entry(self.settings_frame, width=10)
        self.entry_random_state.grid(row=8, column=1, sticky="w", padx=5, pady=5)

        # 10) Custom TTF Font (optional)
        self.label_font_file = tk.Label(
            self.settings_frame, text="Custom Font (TTF):",
            bg=self.bg_color_frame, fg=self.fg_color_text
        )
        self.label_font_file.grid(row=9, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_font_file = tk.Entry(self.settings_frame, width=30)
        self.entry_font_file.grid(row=9, column=1, sticky="w", padx=5, pady=5)
        
        self.button_browse_font = tk.Button(
            self.settings_frame, text="Browse Font...",
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.browse_font_file
        )
        self.button_browse_font.grid(row=9, column=2, padx=5, pady=5)

        # ---------- Extra Buttons ----------
        # Show Top 10 Words
        self.button_show_frequencies = tk.Button(
            self.settings_frame, text="Show Top 10 Words",
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.show_top_frequencies
        )
        self.button_show_frequencies.grid(row=10, column=0, columnspan=3, pady=5)
        
        # Generate & Preview
        self.button_generate = tk.Button(
            self.settings_frame, text="Generate WordCloud",
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.generate_wordcloud
        )
        self.button_generate.grid(row=11, column=0, columnspan=3, pady=10)

        # Save WordCloud
        self.button_save = tk.Button(
            self.settings_frame, text="Save WordCloud",
            bg=self.accent_color, fg=self.fg_color_text,
            command=self.save_wordcloud
        )
        self.button_save.grid(row=12, column=0, columnspan=3, pady=5)

        # ---------- Preview Area ----------
        self.preview_label = tk.Label(self.preview_frame, bg=self.bg_color_app)
        self.preview_label.pack(expand=True, fill=tk.BOTH)
        
        # Store the last generated WordCloud image object
        self.wordcloud_image = None

    # ------------------- Helper Methods -------------------
    def browse_text_file(self):
        """Allows user to browse and select a text file."""
        filename = filedialog.askopenfilename(
            title="Select a Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, filename)
    
    def browse_font_file(self):
        """Allows user to browse for a TTF font file."""
        fontname = filedialog.askopenfilename(
            title="Select a TTF Font",
            filetypes=[("TrueType Font", "*.ttf"), ("All Files", "*.*")]
        )
        if fontname:
            self.entry_font_file.delete(0, tk.END)
            self.entry_font_file.insert(0, fontname)
    
    def pick_bg_color(self):
        """Open a color chooser and set the chosen background color into entry_bg_color."""
        chosen_color, _ = colorchooser.askcolor()
        if chosen_color:  # user didn't cancel
            # Convert (R, G, B) to #RRGGBB
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(chosen_color[0]), int(chosen_color[1]), int(chosen_color[2])
            )
            self.entry_bg_color.delete(0, tk.END)
            self.entry_bg_color.insert(0, hex_color)
    
    def pick_text_color(self):
        """Open a color chooser and append the chosen color to font color(s) entry."""
        chosen_color, _ = colorchooser.askcolor()
        if chosen_color:
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(chosen_color[0]), int(chosen_color[1]), int(chosen_color[2])
            )
            # If there's already content, append with comma. Otherwise just insert the new color
            existing = self.entry_color.get().strip()
            if existing:
                self.entry_color.delete(0, tk.END)
                self.entry_color.insert(0, existing + ", " + hex_color)
            else:
                self.entry_color.insert(0, hex_color)

    # ------------------- Word Cloud Methods -------------------
    def generate_wordcloud(self):
        """Generates the word cloud from the selected file and displays a preview."""
        file_path = self.entry_file.get().strip()
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid text file.")
            return
        
        # Read text content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_data = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read file:\n{e}")
            return
        
        # Excluded words
        exclude_words = [
            w.strip().lower() for w in self.entry_exclude.get().split(",") if w.strip()
        ]
        stopwords = set(exclude_words)
        
        # If using built-in STOPWORDS
        if self.use_stopwords_var.get():
            stopwords = stopwords.union(STOPWORDS)
        
        # Parse color inputs
        bg_color = self.entry_bg_color.get().strip()
        color_list = [c.strip() for c in self.entry_color.get().split(",") if c.strip()]

        # Additional sliders & checkboxes
        max_words = self.slider_max_words.get()
        max_font_size = self.slider_max_font_size.get()
        collocations_flag = self.collocations_var.get()

        # Random seed (optional)
        random_state_val = None
        random_state_input = self.entry_random_state.get().strip()
        if random_state_input:
            try:
                random_state_val = int(random_state_input)
            except ValueError:
                messagebox.showwarning(
                    "Warning", 
                    "Random Seed must be an integer. Ignoring user input."
                )
        
        # Optional custom font
        font_path_str = self.entry_font_file.get().strip()
        if font_path_str and not os.path.exists(font_path_str):
            messagebox.showwarning(
                "Warning", 
                "Font file not found. Ignoring custom font."
            )
            font_path_str = None
        
        # Create custom color function
        if len(color_list) == 1:
            # If there's only one color, use that for all words
            single_color = color_list[0]
            def color_func(*args, **kwargs):
                return single_color
        else:
            # If there are multiple colors, pick one randomly for each word
            def color_func(*args, **kwargs):
                return random.choice(color_list)
        
        # Generate the WordCloud
        wc = WordCloud(
            width=800,
            height=600,
            background_color=bg_color,
            stopwords=stopwords,
            color_func=color_func,
            max_words=max_words,
            max_font_size=max_font_size,
            collocations=collocations_flag,
            random_state=random_state_val,
            font_path=font_path_str if font_path_str else None
        ).generate(text_data)
        
        # Convert to image
        self.wordcloud_image = wc.to_image()
        
        # Resize for preview
        preview_width = 400
        preview_height = 300
        preview_img = self.wordcloud_image.resize(
            (preview_width, preview_height), 
            PILImage.Resampling.LANCZOS
        )
        
        self.preview_photo = ImageTk.PhotoImage(preview_img)
        
        self.preview_label.config(image=self.preview_photo)
        self.preview_label.image = self.preview_photo  # Keep a reference
    
    def show_top_frequencies(self):
        """Displays the top 10 most frequent words (after excludes) in a popup."""
        file_path = self.entry_file.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid text file.")
            return
        
        # Read text content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_data = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read file:\n{e}")
            return
        
        words = text_data.split()
        
        # Exclude user-specified words
        exclude_words = [w.strip().lower() for w in self.entry_exclude.get().split(",") if w.strip()]
        cleaned_words = [w for w in words if w.lower() not in exclude_words]
        
        # If using built-in STOPWORDS
        if self.use_stopwords_var.get():
            cleaned_words = [w for w in cleaned_words if w.lower() not in STOPWORDS]
        
        # Count frequencies
        freq = Counter(cleaned_words).most_common(10)
        if not freq:
            messagebox.showinfo("Top 10 Words", "No words found or everything was excluded!")
            return
        
        # Format results
        freq_text = "\n".join(f"{word}: {count}" for word, count in freq)
        messagebox.showinfo("Top 10 Most Frequent Words", freq_text)
    
    def save_wordcloud(self):
        """Saves the current word cloud image to a file."""
        if not self.wordcloud_image:
            messagebox.showinfo("Info", "No WordCloud generated yet. Please generate one first.")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Save WordCloud as",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
        )
        if save_path:
            try:
                self.wordcloud_image.save(save_path)
                messagebox.showinfo("Success", f"WordCloud saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to save file:\n{e}")

def main():
    root = tk.Tk()
    app = UltimateWordCloudApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
