import os
import customtkinter as ctk
import pyautogui
import pygetwindow
from tkinter import filedialog
from PIL import ImageTk, Image
from predictions import predict

# global variables
project_folder = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(project_folder, "images")

filename = ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bone Fracture Detection")
        self.geometry("500x740")
        self.configure(bg="#1E1E1E")  # Dark gray professional background

        self.head_frame = ctk.CTkFrame(master=self, fg_color="#2C3E50")  # Elegant dark blue header
        self.head_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.main_frame = ctk.CTkFrame(master=self, fg_color="#1E1E1E")  # Keeping the main area dark gray
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.head_label = ctk.CTkLabel(master=self.head_frame, text="Bone Fracture Detection",
                                       font=(ctk.CTkFont("Roboto"), 18, "bold"), text_color="white")
        self.head_label.pack(pady=20, padx=10, anchor="nw", side="left")

        img1 = ctk.CTkImage(Image.open(os.path.join(folder_path, "info.png")))
        self.img_label = ctk.CTkButton(master=self.head_frame, text="", image=img1, command=self.open_image_window,
                                       width=40, height=40, fg_color="#34495E", hover_color="#5D6D7E")  # Classy Blue shades
        self.img_label.pack(pady=10, padx=10, anchor="nw", side="right")

        self.info_label = ctk.CTkLabel(master=self.main_frame,
                                       text="Upload an X-ray image for bone fracture detection.",
                                       wraplength=300, font=(ctk.CTkFont("Roboto"), 16, "italic"),
                                       text_color="#D3D3D3")  # Light gray for contrast
        self.info_label.pack(pady=10, padx=10)

        self.upload_btn = ctk.CTkButton(master=self.main_frame, text="Upload Image", command=self.upload_image,
                                        fg_color="#3498DB", hover_color="#2980B9")  # Elegant blue with a darker hover
        self.upload_btn.pack(pady=5, padx=1)

        self.frame2 = ctk.CTkFrame(master=self.main_frame, fg_color="#2C3E50", width=256, height=256)  
        self.frame2.pack(pady=10, padx=1)

        img = Image.open(os.path.join(folder_path, "Question_Mark.jpg"))
        img_resized = img.resize((256, 256))
        img = ImageTk.PhotoImage(img_resized)

        self.img_label = ctk.CTkLabel(master=self.frame2, text="", image=img)
        self.img_label.pack(pady=10, padx=1)

        self.predict_btn = ctk.CTkButton(master=self.main_frame, text="Predict", command=self.predict_gui,
                                         fg_color="#3498DB", hover_color="#2980B9")  # Consistent blue for buttons
        self.predict_btn.pack(pady=5, padx=1)

        self.result_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#2C3E50", width=200, height=100)
        self.result_frame.pack(pady=5, padx=5)

        self.res1_label = ctk.CTkLabel(master=self.result_frame, text="", text_color="white", font=("Arial", 16))
        self.res1_label.pack(pady=5, padx=20)

        self.res2_label = ctk.CTkLabel(master=self.result_frame, text="", text_color="white")
        self.res2_label.pack(pady=5, padx=20)

        self.save_btn = ctk.CTkButton(master=self.result_frame, text="Save Result", command=self.save_result,
                                      fg_color="#3498DB", hover_color="#2980B9")
        self.save_btn.pack_forget()  # Initially hidden

        self.save_label = ctk.CTkLabel(master=self.result_frame, text="", text_color="white")

    def upload_image(self):
        global filename
        f_types = [("All Files", "*.*")]
        filename = filedialog.askopenfilename(filetypes=f_types, initialdir=folder_path)
        self.res2_label.configure(text="")
        self.res1_label.configure(text="")
        self.img_label.configure(self.frame2, text="", image="")
        img = Image.open(filename)
        img_resized = img.resize((256, 256))
        img = ImageTk.PhotoImage(img_resized)
        self.img_label.configure(self.frame2, image=img, text="")
        self.img_label.image = img
        self.save_btn.pack_forget()
        self.save_label.pack_forget()

    def predict_gui(self):
        global filename
        bone_type_result = predict(filename)
        result = predict(filename, bone_type_result)

        if result == 'fractured':
            self.res2_label.configure(text_color="red", text="Result: Fractured", font=(ctk.CTkFont("Roboto", 16, "bold")))
        else:
            self.res2_label.configure(text_color="lightgreen", text="Result: Normal", font=(ctk.CTkFont("Roboto", 16, "bold")))

        self.res1_label.configure(text=f"Type: {bone_type_result}", text_color="white", font=(ctk.CTkFont("Roboto", 16)))
        self.save_btn.pack(pady=10, padx=1)
        self.save_label.pack(pady=5, padx=20)

    def save_result(self):
        tempdir = filedialog.asksaveasfilename(defaultextension=".png", initialdir=os.path.join(project_folder, 'PredictResults/'))
        if tempdir:
            window = pygetwindow.getWindowsWithTitle('Bone Fracture Detection')[0]
            screenshot = pyautogui.screenshot()
            screenshot.save(tempdir)
            self.save_label.configure(text_color="WHITE", text="Saved!", font=(ctk.CTkFont("Roboto", 16, "bold")))

    def open_image_window(self):
        im = Image.open(os.path.join(folder_path, "rules.jpeg"))
        im = im.resize((700, 700))
        im.show()

app = App()
app.mainloop()
