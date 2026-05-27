
## Before install:
Before run application you should create .env file with API_TOKEN (you can use generate_token.py script) 
for example:
`API_TOKEN=955740a68f4f247d932eb94753f066f8db318e3e48cc4b1c601299064c6f4bwd`

## Install:
```
docker build -t deploy_server .
docker run -d --name deploy_server -v /var/run/docker.sock:/var/run/docker.sock -p 25381:25381 --env-file .env deploy_server:latest
```