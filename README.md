# Learning by Annotations - Learning Platform based on images

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/JamesNeumann/learning-by-annotations/build-push) ![GitHub](https://img.shields.io/github/license/JamesNeumann/learning-by-annotations)

## Getting Started

To get started clone the repository. Afterwards the environmental veriables need to be set. The `.env.sample` shows all neccessary variables.

### Development

To be able to develop the frontend additional environment variables need to be set. A `.env.sample` can be found in the frontend folder. Normally all Apis should be available under `localhost` and their corresponding ports.

To start the development environment run

```bash
docker-compose -f docker-compose.dev up
```

To rebuild all docker containers run

```bash
docker-compose -f docker-compose.dev up --build
```
