<<<<<<< HEAD
# F_Recog-Gate
=======
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

## 🎨 Preview (Optional)

You can add screenshots here to make the README look even cooler:

```
![UI Preview](https://via.placeholder.com/600x400.png?text=Facial+Auth+UI+Preview)
```

---
>>>>>>> 8c427ac (Facial Recognition Auth System)
