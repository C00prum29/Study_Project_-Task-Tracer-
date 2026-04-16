package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type Task struct {
	TaskID      string `json:"Task ID"`
	Description string `json:"description"`
	Status      string `json:"status"`
	CreatedAt   string `json:"created_at"`
	UpdatedAt   string `json:"updated_at"`
}

var baseDir, _ = os.Getwd()
var folder = filepath.Join(baseDir, "data")
var filePath = filepath.Join(folder, "tasks.json")

func ensureFile() {
	os.MkdirAll(folder, os.ModePerm)

	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		file, _ := os.Create(filePath)
		defer file.Close()
		file.Write([]byte("{}"))
	}
}

func loadTasks() map[string]Task {
	file, err := os.ReadFile(filePath)
	if err != nil {
		return map[string]Task{}
	}

	var tasks map[string]Task
	err = json.Unmarshal(file, &tasks)
	if err != nil {
		fmt.Println("tasks.json повреждён. Создаётся новый файл.")
		return map[string]Task{}
	}

	return tasks
}

func saveTasks(tasks map[string]Task) {
	data, _ := json.MarshalIndent(tasks, "", "  ")
	os.WriteFile(filePath, data, 0644)
}

func now() string {
	return time.Now().Format(time.RFC3339)
}

func checkTaskExists(taskID string, tasks map[string]Task) bool {
	if _, ok := tasks[taskID]; !ok {
		fmt.Printf("Task %s not found\n", taskID)
		return false
	}
	return true
}

func printTask(task Task) {
	fmt.Println("Task ID:", task.TaskID)
	fmt.Println("Description:", task.Description)
	fmt.Println("Status:", task.Status)
	fmt.Println("Created at:", task.CreatedAt)
	fmt.Println("Updated at:", task.UpdatedAt)
	fmt.Println()
}

// COMMANDS

func add(description string) {
	tasks := loadTasks()
	taskID := fmt.Sprintf("%d", len(tasks)+1)

	task := Task{
		TaskID:      taskID,
		Description: description,
		Status:      "to do",
		CreatedAt:   now(),
		UpdatedAt:   now(),
	}

	tasks[taskID] = task
	saveTasks(tasks)

	fmt.Println("Task added successfully.")
}

func deleteTask(taskID string) {
	tasks := loadTasks()

	if !checkTaskExists(taskID, tasks) {
		return
	}

	delete(tasks, taskID)
	saveTasks(tasks)

	fmt.Printf("Task %s deleted successfully\n", taskID)
}

func update(taskID, description string) {
	tasks := loadTasks()

	if !checkTaskExists(taskID, tasks) {
		return
	}

	task := tasks[taskID]
	task.Description = description
	task.UpdatedAt = now()

	tasks[taskID] = task
	saveTasks(tasks)

	fmt.Printf("Task %s updated successfully\n", taskID)
}

func markStatus(taskID, status string) {
	tasks := loadTasks()

	if !checkTaskExists(taskID, tasks) {
		return
	}

	task := tasks[taskID]
	task.Status = status
	task.UpdatedAt = now()

	tasks[taskID] = task
	saveTasks(tasks)

	fmt.Printf("Task %s marked as %s\n", taskID, status)
}

func listTasks() {
	tasks := loadTasks()

	if len(tasks) == 0 {
		fmt.Println("No tasks found.")
		return
	}

	for _, task := range tasks {
		printTask(task)
	}
}

func listByStatus(status string) {
	tasks := loadTasks()

	found := false
	for _, task := range tasks {
		if task.Status == status {
			printTask(task)
			found = true
		}
	}

	if !found {
		fmt.Printf("No tasks with status %s found\n", status)
	}
}

// ENTRY POINT

func main() {
	ensureFile()

	if len(os.Args) < 2 {
		fmt.Println("Usage: [add|delete|update|mark|list|list-status]")
		return
	}

	command := os.Args[1]

	switch command {
	case "add":
		if len(os.Args) < 3 {
			fmt.Println("Usage: add <description>")
			return
		}
		add(os.Args[2])

	case "delete":
		if len(os.Args) < 3 {
			fmt.Println("Usage: delete <task_id>")
			return
		}
		deleteTask(os.Args[2])

	case "update":
		if len(os.Args) < 4 {
			fmt.Println("Usage: update <task_id> <description>")
			return
		}
		update(os.Args[2], os.Args[3])

	case "mark":
		if len(os.Args) < 4 {
			fmt.Println("Usage: mark <task_id> <status>")
			return
		}
		markStatus(os.Args[2], os.Args[3])

	case "list":
		listTasks()

	case "list-status":
		if len(os.Args) < 3 {
			fmt.Println("Usage: list-status <status>")
			return
		}
		listByStatus(os.Args[2])

	default:
		fmt.Println("Unknown command")
	}
}
