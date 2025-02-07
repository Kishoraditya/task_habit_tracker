import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder

# Load the Kivy language file
Builder.load_file('mobile/app.kv')

API_BASE_URL = "https://your-task-habit-tracker.onrender.com/api"  # Update with your actual base URL

class LoginScreen(Screen):
    status_message = StringProperty("")
    
    def do_login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        data = {"email": email, "password": password}
        try:
            response = requests.post(f"{API_BASE_URL}/login", json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    self.manager.current = "dashboard"
                    self.manager.get_screen("dashboard").user = result.get("user")
                else:
                    self.status_message = "Invalid credentials"
            else:
                self.status_message = "Login failed"
        except Exception as e:
            self.status_message = f"Error: {e}"

class DashboardScreen(Screen):
    user = {}
    tasks = ListProperty([])
    status_message = StringProperty("")
    
    def on_enter(self):
        self.fetch_tasks()
    
    def fetch_tasks(self):
        try:
            response = requests.get(f"{API_BASE_URL}/tasks")
            if response.status_code == 200:
                result = response.json()
                self.tasks = result.get("tasks", [])
            else:
                self.status_message = "Failed to fetch tasks"
        except Exception as e:
            self.status_message = f"Error: {e}"
    
    def add_task(self):
        title = self.ids.new_task_input.text
        data = {"title": title}
        try:
            response = requests.post(f"{API_BASE_URL}/tasks", json=data)
            if response.status_code == 200:
                self.fetch_tasks()
                self.ids.new_task_input.text = ""
            else:
                self.status_message = "Failed to add task"
        except Exception as e:
            self.status_message = f"Error: {e}"

class TaskTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        return sm

if __name__ == '__main__':
    TaskTrackerApp().run()
