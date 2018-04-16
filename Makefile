APP=openid-wargaming
IMAGE=${APP}-image

all: install

doc:
	make -C doc/ html

install:
	pip install .

develop:
	pip install -r requirements.txt -r requirements-dev.txt
	pip install -e .

wip: develop
	py.test -m "wip" -v --cov-report html:.cov_html --cov-report term --cov=${APP}


test: develop
	py.test -vv -m "not wip" --cov-report term --cov-report html:.cov_html --cov=${APP} && pylint -r y ${APP}/


docker-image:
	docker build -t ${IMAGE} --build-arg=make_mode=${MAKE_MODE} .


docker-run: docker
	docker run --name ${APP}-container -v `pwd`:/usr/src/app  -it ${IMAGE} bash


docker-delete:
	docker rmi -f ${IMAGE} || echo "Go"
	docker rm -f ${APP}-container || echo "Go"


docker-test:
	docker rm -f ${APP}-container; echo
	docker build -t ${IMAGE} --build-arg=make_mode=test .


docker-wip:
	docker rm -f ${CONTAINER}-test; echo
	docker build -t ${CONTAINER}-test --build-arg=make_mode=wip .


docker: docker-delete docker-image docker-run


.PHONY: all doc install develop wip test docker-image docker-run docker-delete docker-dev
