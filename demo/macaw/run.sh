#!/bin/bash
mongod --fork --logpath /app/mongod.log --dbpath /app/mongodb
cd /app/macaw/macaw
