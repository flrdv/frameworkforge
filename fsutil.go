package main

import (
	"os"
	"path/filepath"
)

const (
	frameworksDir = "frameworks"
	casesDir      = "cases"
)

type Framework struct {
	Name string
	Path string
	pid  int
}

func (f *Framework) String() string {
	return f.Name
}

func getFrameworks(language string) (frameworks []*Framework, err error) {
	dirs, err := os.ReadDir(filepath.Join(frameworksDir, language))
	if err != nil {
		return nil, err
	}

	for _, dir := range dirs {
		frameworks = append(frameworks, &Framework{
			Name: dir.Name(),
			Path: filepath.Join(frameworksDir, language, dir.Name()),
		})
	}

	return frameworks, nil
}
