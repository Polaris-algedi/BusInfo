-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS bus_dev_db;
CREATE USER IF NOT EXISTS 'bus_dev'@'localhost' IDENTIFIED BY 'bus_dev_pwd';
GRANT ALL PRIVILEGES ON `bus_dev_db`.* TO 'bus_dev'@'localhost';
FLUSH PRIVILEGES;
