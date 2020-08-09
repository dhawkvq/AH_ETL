Migrate script to transform current users and properties


Script does rely on having postgres locally open



## Migrate current json data to postgres
```bash
# make sure to be located inside of migration folder
cd ./migration

# grant youself permission to execute file 
chmod +x migrate.sh

# and run the script
./migrate.sh

```