package main

import (
	"github.com/indigo-web/indigo"
	"github.com/indigo-web/indigo/http"
	"github.com/indigo-web/indigo/router/inbuilt"
)

func Hello(request *http.Request) *http.Response {
	return http.String(request, "Hello, world!")
}

func Echo(request *http.Request) *http.Response {
	body, err := request.Body.String()
	if err != nil {
		return http.Error(request, err)
	}

	return http.String(request, body)
}

func main() {
	r := inbuilt.New()
	r.Resource("/").
		Get(Hello).
		Post(Echo)

	_ = indigo.New(":8080").Serve(r)
}
