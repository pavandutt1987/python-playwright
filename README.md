# 🎭 Playwright Practice Studio (Multi-Language IDE)

A complete local browser-based practice & automation platform for **Python**, **TypeScript**, and **JavaScript** Playwright test engineers.

---

## 🚀 Quick Start (Windows)

### Step 1: 1-Click Setup (First time only)
Double-click `setup.bat` or run:
```powershell
pip install -r requirements.txt
npm install
python -m playwright install chromium
```

### Step 2: 1-Click Launch
Double-click `start.bat` or run:
```powershell
python -m uvicorn app.server:app --host 127.0.0.1 --port 8000
```
This automatically launches the studio at **http://localhost:8000**.

---

## 🌟 Key Features

1. **Multi-Language Runner**:
   - 🐍 **Python**: Powered by `async_playwright` and native async event loop.
   - 🔷 **TypeScript**: Powered by `tsx` on the fly (zero manual compilation required).
   - 🟨 **JavaScript**: Powered by native Node.js.

2. **Full VS Code Dark Monaco Editor**:
   - Syntax highlighting, auto-completion, bracket matching, code formatting.
   - Hotkey `Ctrl + Enter` to run scripts instantly.
   - Hotkey `Ctrl + S` to save snippets into your personal knowledge base.

3. **👁️ Headed vs. ⚡ Headless Toggle**:
   - Run in **Headed** mode to watch the browser launch on your desktop in real-time.
   - Run in **Headless** mode for lightning-fast headless verification.

4. **Real-Time Terminal Output & Process Management**:
   - Live stdout / stderr streaming with milliseconds counter.
   - **Stop Button**: Terminate hung loops or long waits cleanly at any moment.

5. **🗂️ History & Saved Snippets Library**:
   - Automatic execution history tracking with status badges (`SUCCESS` / `FAILED`).
   - Save custom snippets with tags, search by title/keyword, star favorites, and 1-click restore.

6. **🎯 Built-in Offline Playground Targets (`/playground`)**:
   - `1. Login Authentication` (`/playground/login.html`) – Test IDs, role locators, form validation.
   - `2. Dynamic Tables & AJAX` (`/playground/dynamic-tables.html`) – Table filtering, dynamic row count, awaiting asynchronous network responses.
   - `3. Frames & Shadow DOM` (`/playground/iframes-shadowdom.html`) – Frame locators and open Shadow DOM piercing.
   - `4. Alerts & Popups` (`/playground/alerts-popups.html`) – JS dialogs (`dialog.accept()`) and multi-tab context capturing.
   - `5. File Upload Automation` (`/playground/file-upload.html`) – Input files and drag & drop file upload.
   - `6. Network & API Mocking` (`/playground/network-mocking.html`) – Intercepting and mocking routes with `page.route()`.

---

## ⌨️ Shortcuts & Cheatsheet

| Shortcut | Action |
|---|---|
| `Ctrl + Enter` | Run code in current language |
| `Ctrl + S` | Open "Save Snippet" modal |
| `✨ Format` | Auto-format code in Monaco editor |
| `☰ Drawer` | Slide open/close History and Target Sandbox |
