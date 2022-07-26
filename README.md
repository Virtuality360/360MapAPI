# To Run As Is
Set up the dotenv file\
Run `uvicorn src.api:api`

# To Run in a container
Set up dotenv file\
From the root folder:\
Run `docker build -t {image-name} .`\
Run `docker run -d --name {container-name} -p 80:80 {image-name}`
Requests can then be made to localhost
View documentation at localhost:80/docs

# Set up Database Connection Secrets
Edit the dotenv file int ./src/database/
The format to fill out is
```
PGUSER={username}
PGPASSWORD={password}
PGDATABSE={database-name}
PGHOST={host}
PGPORT={port-number}
```