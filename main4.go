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
    <form action="/command" method="POST" target="resultFrame">
        <button type="submit" name="cmd" value="python3 dc.py 1 1">Run Python Script 1</button>
    </form>
    <form action="/command" method="POST" target="resultFrame">
        <button type="submit" name="cmd" value="python3 dc.py 1 0">Run Python Script 2</button>
    </form>
    <iframe name="resultFrame" style="border:none;width:100%;height:50px;"></iframe>
</body>
</html>
`

func sendTmuxCommand(command string) error {
	cmd := exec.Command("tmux", "send-keys", "-t", "bento1", command, "C-m")
	return cmd.Run()
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.New("page").Parse(htmlTemplate))
	tmpl.Execute(w, nil)
}

func handleCommand(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	command := r.FormValue("cmd")
	err := sendTmuxCommand(command)

	if err != nil {
		fmt.Fprintf(w, "Error sending command: %v", err)
		return
	}

	fmt.Fprintf(w, "Command sent successfully")
}

func main() {
	http.HandleFunc("/", handleRoot)
	http.HandleFunc("/command", handleCommand)

	log.Println("Server starting on :3389")
	log.Fatal(http.ListenAndServe(":3389", nil))
}
