package main

import (
	"fmt"
	"html"
	"log"
	"net/http"
	"os/exec"
)

func sendTmuxCommand(command string) error {
	cmd := exec.Command("tmux", "send-keys", "-t", "bento1", "python3 dc.py 1 1", "C-m")
	return cmd.Run()
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
	err := sendTmuxCommand("echo 'Root page accessed'")
	if err != nil {
		log.Printf("Error sending tmux command: %v", err)
	}
}

func handleHi(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi")
	err := sendTmuxCommand("echo 'Hi page accessed'")
	if err != nil {
		log.Printf("Error sending tmux command: %v", err)
	}
}

func main() {
	http.HandleFunc("/", handleRoot)
	http.HandleFunc("/hi", handleHi)

	log.Println("Server starting on :3389")
	log.Fatal(http.ListenAndServe(":3389", nil))
}
