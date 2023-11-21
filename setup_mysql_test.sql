-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS bus_test_db;
CREATE USER IF NOT EXISTS 'bus_test'@'localhost' IDENTIFIED BY 'bus_test_pwd';
GRANT ALL PRIVILEGES ON `bus_test_db`.* TO 'bus_test'@'localhost';
FLUSH PRIVILEGES;
