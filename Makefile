
#### Local development helpers

dev-up:
	docker-compose up --build -d

build:
	docker-compose up --build
# Cloud run linux docker image build
cloud-build:
	docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/mgcp-1192365-lm04-poc/transcripts/ift:latest . 

cloud-push:
#push to google artifacts registry
	docker push us-central1-docker.pkg.dev/mgcp-1192365-lm04-poc/transcripts/ift:latest