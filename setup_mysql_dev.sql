-- This SQL script sets up a MySQL development environment
-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant all privileges on the development database to the user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
-- Grant select privileges on the performance schema for monitoring
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
