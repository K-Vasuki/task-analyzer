const apiBase = "http://127.0.0.1:8000/api/tasks";
const taskForm = document.getElementById("taskForm");
const tasksTableBody = document.getElementById("tasksTableBody");
const modeSelect = document.getElementById("modeSelect");
const message = document.getElementById("message");

let tasks = []; // local cache

// Load all tasks
async function loadTasks() {
    try {
        const res = await fetch(`${apiBase}/`);
        tasks = await res.json();
        renderTasks(tasks);
    } catch (err) {
        message.textContent = "Error loading tasks.";
    }
}

// Render tasks in table
function renderTasks(taskList) {
    tasksTableBody.innerHTML = "";
    taskList.forEach(task => {
        const row = document.createElement("tr");
        // Color coding
        let priorityClass = "low";
        if(task.score >= 15) priorityClass = "high";
        else if(task.score >= 8) priorityClass = "medium";

        row.innerHTML = `
            <td>${task.title}</td>
            <td>${task.due_date || '-'}</td>
            <td>${task.estimated_hours}</td>
            <td>${task.importance}</td>
            <td>${(task.dependencies || []).join(', ')}</td>
            <td class="${priorityClass}">${task.score || '-'}</td>
            <td>${task.reason || ''}</td>
            <td>
                <button onclick="editTask('${task.id}')">Edit</button>
                <button onclick="deleteTask('${task.id}')">Delete</button>
            </td>
        `;
        tasksTableBody.appendChild(row);
    });
}

// Add / Update task
taskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("taskId").value;
    const taskData = {
        title: document.getElementById("title").value,
        due_date: document.getElementById("due_date").value,
        estimated_hours: parseFloat(document.getElementById("estimated_hours").value) || 1,
        importance: parseInt(document.getElementById("importance").value) || 5,
        dependencies: document.getElementById("dependencies").value.split(',').map(s=>s.trim()).filter(s=>s)
    };

    const method = id ? "PUT" : "POST";
    const url = id ? `${apiBase}/${id}/` : `${apiBase}/`;

    try {
        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(taskData)
        });
        if(res.ok){
            taskForm.reset();
            document.getElementById("taskId").value = "";
            loadTasks();
            message.textContent = id ? "Task updated!" : "Task added!";
        } else {
            message.textContent = "Failed to add/update task.";
        }
    } catch (err) {
        message.textContent = "Error communicating with server.";
    }
});

// Edit task
function editTask(id) {
    const task = tasks.find(t => t.id === id);
    if(!task) return;
    document.getElementById("taskId").value = task.id;
    document.getElementById("title").value = task.title;
    document.getElementById("due_date").value = task.due_date || '';
    document.getElementById("estimated_hours").value = task.estimated_hours;
    document.getElementById("importance").value = task.importance;
    document.getElementById("dependencies").value = (task.dependencies || []).join(", ");
}

// Delete task
async function deleteTask(id) {
    if(!confirm("Are you sure to delete this task?")) return;
    try {
        const res = await fetch(`${apiBase}/${id}/`, { method: "DELETE" });
        if(res.ok){
            loadTasks();
            message.textContent = "Task deleted!";
        } else {
            message.textContent = "Failed to delete task.";
        }
    } catch (err) {
        message.textContent = "Error communicating with server.";
    }
}

// Analyze tasks
document.getElementById("analyzeBtn").addEventListener("click", async () => {
    const mode = modeSelect.value;
    try {
        const res = await fetch(`${apiBase}/analyze/?mode=${mode}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });
        const analyzed = await res.json();
        renderTasks(analyzed);
        message.textContent = "Tasks analyzed!";
    } catch (err) {
        message.textContent = "Error analyzing tasks.";
    }
});

// Suggest top 3
document.getElementById("suggestBtn").addEventListener("click", async () => {
    const mode = modeSelect.value;
    try {
        const res = await fetch(`${apiBase}/suggest/?mode=${mode}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });
        const top3 = await res.json();
        renderTasks(top3);
        message.textContent = "Top 3 tasks suggested!";
    } catch (err) {
        message.textContent = "Error suggesting tasks.";
    }
});

// Initial load
loadTasks();
