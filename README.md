
# F_Recog-Gate 

# 🔐 Facial Authentication System (Tkinter + MediaPipe)

A secure **facial authentication system** built with **Python**, **Tkinter**, and **MediaPipe**.  
Designed for **educational purposes** (school project) — featuring a modern UI, encrypted storage, and GDPR-friendly principles.

---

## ✨ Features

- 🧠 **Face Recognition with MediaPipe**
- 🔒 **Strong Data Protection**  
  - Stores only **2D landmark coordinates** (no images)  
  - Encrypted using **Fernet symmetric encryption**
- 👤 **User Management**
  - ➕ Register face (with consent)
  - 🔑 Login with face recognition
  - 👀 View registered users
  - ❌ Delete face data anytime
- ⚖️ **GDPR Principles**
  - ✅ Consent required
  - ✅ Encrypted + pseudonymized with UUID
  - ✅ Full user control (view/delete)
  - ✅ Data minimization
  - ✅ Manual retention
- 🎨 **Modern UI**
  - Dark theme with ttk
  - Status bar for live feedback
  - Keyboard shortcuts:
    - ⏎ Enter → Register  
    - 🔐 Ctrl+L → Login  
    - 🗑️ Ctrl+Delete → Delete  

---

## 📂 Project Structure

```
facial-auth/
│── registered_faces/        # 🔑 Encrypted face data (.pkl files)
│── facial_auth.log          # 📝 Log file of actions
│── main.py                  # 🚀 Main program entry (GUI + logic)
│── README.md                # 📘 Documentation
```

---

## 🛠️ Requirements

- Python 3.8+  
- Install dependencies:

```bash
pip install opencv-python mediapipe cryptography numpy
```

---

## 🚀 How to Run

1. Start the app:

```bash
python main.py
```

2. In the GUI:
   - ✍️ Enter your name
   - ✅ Tick consent box
   - 🟢 **Register Face** → Press `c` to capture, `q` to quit camera  
   - 🔑 **Login with Face** → Face the camera directly  
   - ❌ **Delete Face Data** → Enter name + delete  
   - 📋 **View Registered Users** → Show all users  

---

## 📝 Logs

All important actions (register, login, delete) are stored in:

```
facial_auth.log
```

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  
It is **not production-ready** and must not be used for real-world security systems.

---

## 🎨 Preview 
<img width="1365" height="861" alt="s3" src="https://github.com/user-attachments/assets/9459166a-b4a8-485c-b52d-244bb80cbf01" />
<img width="1228" height="826" alt="s2" src="https://github.com/user-attachments/assets/33026dd8-b9d0-41e3-8eb8-8c7ef009f4b4" />
<img width="705" height="750" alt="s1" src="https://github.com/user-attachments/assets/4fc6cb2c-df8d-4068-8c82-ec72a3541da7" />


