// Load localForage from CDN in base.html (see below)

window.addEventListener('online', syncTasks);

function syncTasks() {
  localforage.getItem('offlineTasks').then(tasks => {
    if (tasks && tasks.length > 0) {
      console.log("Syncing offline tasks...", tasks);
      fetch('/sync_tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tasks: tasks })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          localforage.removeItem('offlineTasks');
          console.log('Offline tasks synced successfully.');
        }
      })
      .catch(err => console.error("Error syncing tasks:", err));
    }
  });
}

// Call this function to save a task offline if the server is unreachable
function saveTaskOffline(task) {
  localforage.getItem('offlineTasks').then(tasks => {
    tasks = tasks || [];
    tasks.push(task);
    return localforage.setItem('offlineTasks', tasks);
  });
}
