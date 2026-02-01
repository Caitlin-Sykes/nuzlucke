## Getting Started
### Requirements
- Python 3.14
- Docker
### Installation

#### Production Environment
1. Go to `pokemon_data_loader/`
2. Rename the .env.example file to .env
3. **!IMPORTANT!** change the values for "POSTGRES_USER" and "POSTGRES_PASSWORD" to your postgres UNIQUE credentials
4. navigate to `database/`
5. either run `./startup.ps1` or run `docker-compose up`
#### Development Environment
1. Go to pokemon_data_loader
2. go into .env and comment out `DB_HOST=/var/run/postgresql` and uncomment `DB_HOST="localhost"`
3. optionally, you can change "POSTGRES_USER" and "POSTGRES_PASSWORD" to something unique. 
4. run `pip install -r requirements.txt`
5. you can now debug in your IDE

### To reset the DB
- run `./reset.ps1` or `docker-compose down -v`   && `docker-compose up -d`

### To teardown the DB
- run `./teardown.ps1` or `docker-compose down`

