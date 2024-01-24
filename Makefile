.PHONY: build
build:
	./pw pdm build

install:
	./pw pdm install

bundle:
	tar -czf module.tar.gz *.sh dist

clean:
	rm module.tar.gz
