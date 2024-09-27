package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os/exec"
)

const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
    <title>Command Buttons</title>
</head>
<body>
    <h1>Command Buttons</h1>
    <form action="/command" method="POST">
        <button type="submit" name="cmd" value="python3 dc.py 1 1">Run Python Script 1</button>
    </form>
    <form action="/command" method="POST">
        <button type="submit" name="cmd" value="python3 dc.py 1 0">Run Python Script 2</button>
    </form>
    <p>{{.Message}}</p>
</body>
</html>
`

func sendTmuxCommand(command string) error {
	cmd := exec.Command("tmux", "send-keys", "-t", "bento1", command, "C-m")
	return cmd.Run()
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.New("page").Parse(htmlTemplate))
	tmpl.Execute(w, struct{ Message string }{""})
}

func handleCommand(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	command := r.FormValue("cmd")
	err := sendTmuxCommand(command)

	tmpl := template.Must(template.New("page").Parse(htmlTemplate))
	message := "Command sent successfully"
	if err != nil {
		message = fmt.Sprintf("Error sending command: %v", err)
	}
	tmpl.Execute(w, struct{ Message string }{message})
}

func main() {
	http.HandleFunc("/", handleRoot)
	http.HandleFunc("/command", handleCommand)

	log.Println("Server starting on :3389")
	log.Fatal(http.ListenAndServe(":3389", nil))
}
