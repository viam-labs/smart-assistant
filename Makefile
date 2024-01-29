all: install build bundle

.PHONY: build
build:
	./pw pdm build

install:
	./pw pdm install

bundle:
	tar -czf module.tar.gz *.sh dist .env

clean:
	rm module.tar.gz

start:
	./pw pdm start
