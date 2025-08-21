import tkinter as tk
from tkinter import messagebox
from tkinter import ttk   # NEW: ttk for modern widgets
import cv2
import numpy as np
import mediapipe as mp
import os
import pickle
import time
import uuid
import hashlib
from cryptography.fernet import Fernet
import logging

# Purpose: This system processes facial landmarks for secure user authentication in a school project.
# GDPR Compliance:
# - Data Protection: Facial landmarks are encrypted using Fernet symmetric encryption.
# - Pseudonymization: User names are replaced with UUIDs in stored files.
# - Consent: Users must confirm consent before registration.
# - User Control: Users can delete their data and view registered users.
# - Data Minimization: Only 2D landmark coordinates are stored, not raw images.
# - Retention: Data persists until manually deleted by the user to balance usability and security.

# Setup logging
logging.basicConfig(filename='facial_auth.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Generate encryption key (in memory, not stored)
key = Fernet.generate_key()
cipher = Fernet(key)

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Directory for registered faces
REGISTERED_FACES_DIR = "registered_faces"
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)
    os.chmod(REGISTERED_FACES_DIR, 0o700)  # Restrict directory access

# Store name-to-UUID mapping (in memory, reloaded on startup)
name_to_uuid = {}
def load_name_to_uuid():
    for filename in os.listdir(REGISTERED_FACES_DIR):
        if filename.endswith(".pkl"):
            unique_id = filename.split('.')[0]
            # Note: We can't recover the name without a persistent mapping.
            # In a production system, store an encrypted name-to-UUID mapping.
            pass

load_name_to_uuid()

def capture_face(name, consent_given):
    if not consent_given:
        messagebox.showerror("Consent Required", "You must consent to data processing.")
        return False, None

    cap = cv2.VideoCapture(0)
    face_mesh_model = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    registered_face = None
    existing_name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access camera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh_model.process(frame_rgb)
        display_frame = cv2.flip(frame, 1)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                flipped_landmarks = landmarks
                for lm in flipped_landmarks.landmark:
                    lm.x = 1.0 - lm.x
                mp_drawing.draw_landmarks(
                    display_frame,
                    flipped_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1)
                )
                cv2.putText(display_frame, "Press 'c' to capture or 'q' to quit",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Register Face", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') and results.multi_face_landmarks:
            landmarks = np.array([[lm.x, lm.y] for lm in results.multi_face_landmarks[0].landmark])

            check_start = time.time()
            while time.time() - check_start < 3:
                check_frame = display_frame.copy()
                cv2.putText(check_frame, "Checking image...",
                            (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.imshow("Register Face", check_frame)
                cv2.waitKey(1)

            for filename in os.listdir(REGISTERED_FACES_DIR):
                if filename.endswith(".pkl"):
                    with open(os.path.join(REGISTERED_FACES_DIR, filename), "rb") as f:
                        encrypted_data = f.read()
                    try:
                        decrypted_data = cipher.decrypt(encrypted_data)
                        stored_face = pickle.loads(decrypted_data)
                    except:
                        continue
                    if landmarks.shape != stored_face.shape:
                        continue
                    diff = np.linalg.norm(landmarks - stored_face)
                    if diff < 0.8:
                        for stored_name, stored_uuid in name_to_uuid.items():
                            if stored_uuid == filename.split('.')[0]:
                                existing_name = stored_name
                                break
                        break

            if existing_name:
                messagebox.showerror("Registration Failed",
                                    f"Face already registered as {existing_name}")
                logging.info(f"Attempted registration for {name}, matched existing face: {existing_name}")
                break
            else:
                registered_face = landmarks
                unique_id = uuid.uuid4().hex
                name_to_uuid[name] = unique_id
                filename = os.path.join(REGISTERED_FACES_DIR, f"{unique_id}.pkl")
                pickled_data = pickle.dumps(registered_face)
                encrypted_data = cipher.encrypt(pickled_data)
                with open(filename, "wb") as f:
                    f.write(encrypted_data)
                messagebox.showinfo("Success", f"Face registered for {name}")
                logging.info(f"Registered new face for {name} with ID {unique_id}")
                break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return registered_face is not None, existing_name

def detect_and_identify_face():
    cap = cv2.VideoCapture(0)
    face_mesh_model = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    face_name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access camera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh_model.process(frame_rgb)
        display_frame = cv2.flip(frame, 1)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                flipped_landmarks = landmarks
                for lm in flipped_landmarks.landmark:
                    lm.x = 1.0 - lm.x
                mp_drawing.draw_landmarks(
                    display_frame,
                    flipped_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1)
                )
                landmarks = np.array([[lm.x, lm.y] for lm in landmarks.landmark])
                cv2.putText(display_frame, "Face detected, please face camera",
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                for filename in os.listdir(REGISTERED_FACES_DIR):
                    if filename.endswith(".pkl"):
                        with open(os.path.join(REGISTERED_FACES_DIR, filename), "rb") as f:
                            encrypted_data = f.read()
                        try:
                            decrypted_data = cipher.decrypt(encrypted_data)
                            registered_face = pickle.loads(decrypted_data)
                        except:
                            continue
                        if landmarks.shape != registered_face.shape:
                            continue
                        diff = np.linalg.norm(landmarks - registered_face)
                        if diff < 0.8:
                            unique_id = filename.split('.')[0]
                            for name, stored_uuid in name_to_uuid.items():
                                if stored_uuid == unique_id:
                                    face_name = name
                                    break
                            cv2.putText(display_frame, f"Identified: {face_name}",
                                        (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            break

                if face_name:
                    cv2.imshow("Login", display_frame)
                    cv2.waitKey(1000)
                    break

        if not results.multi_face_landmarks:
            cv2.putText(display_frame, "No face detected, please face camera",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(display_frame, "Press 'q' to quit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Login", display_frame)

        if face_name:
            logging.info(f"Successful login for {face_name}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return face_name

def delete_face(name):
    if name not in name_to_uuid:
        messagebox.showerror("Error", "Name not registered")
        return
    unique_id = name_to_uuid[name]
    filename = os.path.join(REGISTERED_FACES_DIR, f"{unique_id}.pkl")
    if os.path.exists(filename):
        os.remove(filename)
        del name_to_uuid[name]
        messagebox.showinfo("Success", f"Face data for {name} deleted")
        logging.info(f"Deleted face data for {name}")
    else:
        messagebox.showerror("Error", "Face data not found")

def view_registered_users():
    if not name_to_uuid:
        messagebox.showinfo("Registered Users", "No users registered")
    else:
        users = "\n".join(name_to_uuid.keys())
        messagebox.showinfo("Registered Users", f"Registered users:\n{users}")
        logging.info("Viewed registered users")

# -----------------------------
# Modernized UI (ttk-based only)
# -----------------------------
def register_face_gui():
    # ------ Window & Theme ------
    window = tk.Tk()
    window.title("Facial Authentication")
    window.geometry("480x520")
    window.minsize(440, 480)
    window.configure(bg="#0f172a")  # subtle dark background

    # Use a modern ttk theme if available; fallback to 'clam'
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Global style tweaks
    style.configure("TFrame", background="#0f172a")
    style.configure("Header.TLabel", foreground="#e2e8f0", background="#0f172a", font=("Segoe UI", 18, "bold"))
    style.configure("Sub.TLabel", foreground="#94a3b8", background="#0f172a", font=("Segoe UI", 10))
    style.configure("TLabel", foreground="#e2e8f0", background="#0f172a", font=("Segoe UI", 10))
    style.configure("TButton", font=("Verdera", 10, "bold"), padding=10)
    style.map("TButton", foreground=[("disabled", "#94a3b8")])
    style.configure("TCheckbutton", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
    style.configure("TEntry", padding=6)

    # Main container
    container = ttk.Frame(window, padding=20)
    container.pack(fill="both", expand=True)

    # ------ Header ------
    header = ttk.Label(container, text="Facial Authentication", style="Header.TLabel")
    header.pack(anchor="w")

    sub = ttk.Label(
        container,
        text="Secure login with encrypted facial landmarks.\nYou control your data at all times.",
        style="Sub.TLabel",
        justify="left"
    )
    sub.pack(anchor="w", pady=(4, 16))

    # Divider
    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=8)

    # ------ Name + Consent Card ------
    card = ttk.Frame(container, padding=16, style="TFrame")
    card.pack(fill="x", expand=False, pady=6)

    name_row = ttk.Frame(card)
    name_row.pack(fill="x", pady=(0, 10))
    ttk.Label(name_row, text="Display name").pack(side="left")
    name_var = tk.StringVar()
    name_entry = ttk.Entry(name_row, textvariable=name_var, width=30)
    name_entry.pack(side="left", padx=(10, 0))

    consent_var = tk.BooleanVar(value=False)
    consent = ttk.Checkbutton(
        card,
        text="I consent to processing my facial data for authentication",
        variable=consent_var
    )
    consent.pack(anchor="w")

    # Small privacy note
    privacy = ttk.Label(
        card,
        text="Privacy: Only 2D facial landmarks are stored (no images). Data is encrypted and persists until you delete it.",
        style="Sub.TLabel",
        wraplength=420,
        justify="left"
    )
    privacy.pack(anchor="w", pady=(8, 0))

    # ------ Actions Card ------
    actions = ttk.Frame(container, padding=16, style="TFrame")
    actions.pack(fill="x", expand=False, pady=6)

    # Callbacks
    def set_status(msg):
        status_var.set(msg)
        window.update_idletasks()

    def register_face():
        name = name_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Please enter a name")
            return
        if name in name_to_uuid:
            messagebox.showerror("Error", "Name already registered")
            return
        if not consent_var.get():
            messagebox.showerror("Consent Required", "You must consent to data processing")
            return
        set_status("Opening camera for registration…")
        success, existing_name = capture_face(name, consent_var.get())
        if success:
            messagebox.showinfo("Registration", f"Face registered for {name}")
            set_status(f"Registered {name}.")
        elif existing_name:
            # Message already shown in capture_face
            set_status("Registration blocked: face already exists.")
        else:
            messagebox.showerror("Registration Failed", "No face captured")
            set_status("Registration failed.")

    def login():
        set_status("Opening camera for login…")
        name = detect_and_identify_face()
        if name:
            messagebox.showinfo("Login", f"Welcome, {name}!")
            set_status(f"Logged in as {name}.")
        else:
            messagebox.showerror("Login Failed", "Face not recognized. Try facing the camera directly.")
            set_status("Login failed.")

    def delete():
        name = name_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Please enter a name")
            return
        delete_face(name)
        set_status(f"Deleted data for {name}.")

    def view_users():
        view_registered_users()
        set_status("Displayed registered users.")

    # Buttons row 1
    row1 = ttk.Frame(actions)
    row1.pack(fill="x", pady=(0, 8))
    ttk.Button(row1, text="Register Face", command=register_face).pack(side="left")
    ttk.Button(row1, text="Login with Face", command=login).pack(side="left", padx=8)

    # Buttons row 2
    row2 = ttk.Frame(actions)
    row2.pack(fill="x")
    ttk.Button(row2, text="Delete Face Data", command=delete).pack(side="left")
    ttk.Button(row2, text="View Registered Users", command=view_users).pack(side="left", padx=8)

    # ------ Shortcuts / Hints ------
    hints = ttk.Label(
        container,
        text="Tips: During camera windows, press 'c' to capture or 'q' to quit.",
        style="Sub.TLabel"
    )
    hints.pack(anchor="w", pady=(10, 0))

    # ------ Footer / Status bar ------
    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=8)
    status_var = tk.StringVar(value="Ready.")
    status_bar = ttk.Label(container, textvariable=status_var, style="Sub.TLabel", anchor="w")
    status_bar.pack(fill="x")

    # Focus & keybindings for speed
    name_entry.focus_set()
    window.bind("<Return>", lambda e: register_face())
    window.bind("<Control-l>", lambda e: login())
    window.bind("<Control-Delete>", lambda e: delete())

    window.mainloop()

# Entry point
if __name__ == "__main__":
    register_face_gui()
