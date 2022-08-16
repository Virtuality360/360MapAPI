# To Run As Is
Set up the dotenv file\
Run `uvicorn src.api:api`

This project uses psycopg3
As of this writing, binary packages are not available for M1 processors

Be careful when creating queries without any filters
Trying to access too large a database may cause issues
During testing, pulling the geoJSON for 7 million records caused system instability

# To Run in a container
Set up dotenv file\
From the root folder:\
Run `docker-compose build`\
Run `docker-compose up`
Requests can then be made to localhost
View documentation at localhost:8882/docs

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