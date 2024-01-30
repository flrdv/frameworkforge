package main

import "fmt"

func main() {
	frameworks, err := getFrameworks("go")
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(frameworks)
}
