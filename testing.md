
# testing.md

```markdown
# Testing Guide for Task & Habit Tracker (Phase Two)

This document details how to run tests for the enhanced web application, PWA functionality, offline access, IPFS integration, and provides guidelines for testing the Kivy mobile client.

## 1. Web Application Testing

We use **pytest** along with FastAPI’s TestClient to test various endpoints and functionality.

### 1.1. Running Python Tests

From the project root, run:
```bash
pytest
```

This will execute tests in the `tests/` directory.

## 1.2. Test Cases Overview

- **IPFS Integration:**
  - **File:** `tests/test_ipfs.py`
  - **Test:** Calls `store_task_on_ipfs` with dummy task data and asserts a valid hash is returned.
  
- **PWA Assets & Offline Files:**
  - **File:** `tests/test_pwa.py`
  - **Tests:**
    - Check that `/static/manifest.json` returns a valid JSON with the correct app name and icons.
    - Verify that `/static/js/service-worker.js` loads and contains expected code.

- **Web Endpoints (User Auth and Task CRUD):**
  - **File:** `tests/test_web.py`
  - **Tests:**
    - Landing page loads successfully.
    - User registration and login work as expected (status 302 on success).
    - Task creation, retrieval, and sync endpoint functionality.
  
- **Responsive UI Testing with Selenium:**
  - **File:** `tests/test_responsive.py`
  - **Test:** Uses Selenium WebDriver (Chrome headless) to simulate different screen sizes and verifies that key elements (e.g., the title) are visible.
  - **Prerequisites:**  
    Install Selenium:

    ```bash
    pip install selenium
    ```

    Also ensure you have ChromeDriver installed and in your PATH.

## 2. Manual Testing for Offline and PWA Features

### 2.1. Testing Offline Access

1. **Run the Web App Locally:**

   ```bash
   python manage.py run
   ```

2. **Open Developer Tools in Your Browser:**
   - Navigate to the Application tab.
   - Confirm that the manifest (`/static/manifest.json`) is loaded.
   - Check the Service Worker registration (should be registered from `/static/js/service-worker.js`).
3. **Simulate Offline Mode:**
   - In the Network tab, set the browser to "Offline".
   - Refresh the page and verify that cached pages (landing, login, dashboard) load.
4. **Test Offline Form Submission:**
   - Go to the dashboard.
   - Attempt to create a task while offline.
   - Verify that an alert is shown, the task is saved to local storage via localForage, and later (when you reconnect) the `/sync_tasks` endpoint is called.

### 2.2. Testing IPFS Integration

1. **Start a Local IPFS Daemon:**

   ```bash
   ipfs daemon
   ```

2. **Run the IPFS Test:**
   - Execute `pytest tests/test_ipfs.py` to ensure that a valid IPFS hash is returned.
3. **Manual Verification:**
   - Use an IPFS gateway (e.g., `https://ipfs.io/ipfs/<hash>`) to view the stored task data.

## 3. Mobile Client Testing (Kivy App)

### 3.1. Desktop Testing

- **Run the Kivy App on Desktop:**

  ```bash
  cd mobile
  python main.py
  ```

- Verify that:
  - You can log in and see tasks.
  - Adding a task works.
  - The UI adjusts when you resize the window.

### 3.2. Automated Mobile Testing (Optional)

- Consider using **Appium** for automated testing on mobile devices.
- For now, manual testing on Android, iOS, and desktop is recommended.

### 3.3. Testing Packaging

- **Android:**
  - Build the APK using Buildozer:

    ```bash
    buildozer -v android debug
    ```

  - Install the APK on a device/emulator:

    ```bash
    adb install bin/your_app-debug.apk
    ```

- **Desktop Executable:**
  - Use PyInstaller:

    ```bash
    pyinstaller --onefile main.py
    ```

  - Test the executable on Windows/macOS/Linux.

## 4. Running Selenium Responsive Tests

Run the following command from the project root:

```bash
pytest tests/test_responsive.py
```

This will simulate various screen sizes and verify that the app’s layout is responsive.

## Summary

- **Automated Tests:**  
  Run with `pytest` to cover API endpoints, PWA assets, and IPFS integration.
- **Manual Testing:**  
  Use browser developer tools for offline/PWA features and run the Kivy app manually.
- **Mobile Testing:**  
  Package with Buildozer (Android) or PyInstaller (desktop) and test on respective devices.

---
