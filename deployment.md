
# deployment.md

```markdown
# Deployment Guide for Task & Habit Tracker (Phase Two)

This document describes how to deploy the web application (with PWA and offline features) and how to package the Kivy mobile client for Android, iOS, and desktop (Windows/macOS/Linux).

## 1. Web Application Deployment on Render

The web app is built with FastAPI and includes PWA enhancements (manifest, service worker, offline sync) as well as IPFS integration for storing task data.

### Prerequisites
- A GitHub (or GitLab) repository containing the latest code.
- Environment variables defined in a `.env` file (see sample below):
  ```ini
  DB_URL=sqlite:///./tracker.db
  SECRET_KEY=mysecretkey
  ADMIN_KEY=supersecretadminkey
  ```

## Steps to Deploy

1. **Push Code to GitHub/GitLab:**
   - Ensure that your repository is up-to-date with all Phase Two changes (PWA files, offline-sync, IPFS integration, etc.).

2. **Set Up CI/CD with GitHub Actions:**
   - Your repository contains a `.github/workflows/ci.yml` file that runs tests on every push to the `main` branch.
   - Confirm that tests pass by checking the GitHub Actions dashboard.

3. **Create a New Web Service on Render:**
   - Log in to [Render](https://render.com/).
   - Click on **"New"** and select **"Web Service"**.
   - Connect your repository and select the appropriate branch (typically `main`).
   - **Build Command:**

     ```bash
     pip install -r requirements.txt
     ```

   - **Start Command:**

     ```bash
     uvicorn application.main:app --host 0.0.0.0 --port 8000
     ```

   - **Environment Variables:**
     - In the Render dashboard, add the following variables:
       - `DB_URL`
       - `SECRET_KEY`
       - `ADMIN_KEY`

4. **Access the Live Web App:**
   - Once deployed, Render will assign a URL (e.g., `https://your-task-habit-tracker.onrender.com`).
   - Verify that the web app loads correctly, the manifest is available, and service worker registration works.

## 2. Mobile Application Deployment (Kivy Client)

The mobile client is built using Kivy and can be packaged for Android, iOS, and desktop platforms.

### A. Android (APK) Packaging with Buildozer

1. **Set Up a Linux Environment:**
   - Buildozer works best on Linux. If you are on Windows, use Windows Subsystem for Linux (WSL) or a Linux VM.

2. **Install Buildozer and Dependencies:**

   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-setuptools git zip unzip openjdk-8-jdk
   pip install --upgrade buildozer
   pip install cython
   ```

3. **Initialize Buildozer in the `mobile/` Directory:**

   ```bash
   cd mobile
   buildozer init
   ```

   - Edit the generated `buildozer.spec` file:
     - Set `title`, `package.name`, and `package.domain`.
     - Under `requirements`, include at least: `kivy, requests`.
     - Set any required Android permissions.

4. **Build the APK:**

   ```bash
   buildozer -v android debug
   ```

   - When the build completes, the APK will be located in the `bin/` directory.

5. **Install the APK on an Android Device or Emulator:**

   ```bash
   adb install bin/your_app-debug.apk
   ```

### B. iOS Packaging with Kivy-ios

1. **Use macOS:**
   - Packaging for iOS must be done on macOS.

2. **Install Kivy-ios:**
   - Follow the instructions at [kivy-ios GitHub](https://github.com/kivy/kivy-ios) to install and build the Xcode project.

3. **Generate and Build the Xcode Project:**
   - Create an Xcode project from your Kivy app.
   - Open the project in Xcode, build, and archive to produce an IPA file.

### C. Desktop (Windows, macOS, Linux) Packaging with PyInstaller

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Package the App:**
   - From the `mobile/` directory (or a separate desktop version), run:

     ```bash
     pyinstaller --onefile main.py
     ```

   - The executable will be created in the `dist/` folder.
   - Adjust the spec file as needed to include all Kivy resources.

## 3. IPFS Integration

The application uses IPFS to optionally store task data. Ensure that:

- You have installed the IPFS HTTP client (`pip install ipfshttpclient`).
- A local IPFS daemon is running on `localhost:5001` (start it with `ipfs daemon`).
- The function `store_task_on_ipfs` in `application/utils.py` is working as expected.

## 4. Environment and Configuration

- **.env File:**  
  Make sure your local `.env` file includes all required variables. In production on Render, set these via the dashboard.
- **Static Files:**  
  All PWA assets (manifest, service worker, offline-sync scripts) should be in the `static/` folder.
- **Service Worker:**  
  Verify that the service worker is registered by checking your browser’s Application tab.

## 5. Summary

- Deploy the web app on Render using the provided build and start commands.
- Package the mobile client for Android using Buildozer, for iOS with Kivy-ios, and for desktop with PyInstaller.
- Test IPFS integration locally before relying on it in production.
- Use environment variables for configuration and ensure your static assets are correctly served.

Follow these steps to deploy your enhanced Task & Habit Tracker across web and mobile platforms.

---
