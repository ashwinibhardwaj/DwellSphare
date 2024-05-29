-- Create the database
CREATE DATABASE IF NOT EXISTS dwellsphare;

-- Use the created database
USE dwellsphare;

-- Create the User table
CREATE TABLE IF NOT EXISTS User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL
);

-- Create the Room table
CREATE TABLE IF NOT EXISTS Room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    room_size VARCHAR(50) NOT NULL,
    capacity VARCHAR(50) NOT NULL,
    rent VARCHAR(50) NOT NULL,
    facilities VARCHAR(50) NOT NULL,
    security_fee VARCHAR(50) NOT NULL,
    water_fee VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    image_path VARCHAR(255),
    user VARCHAR(255) NOT NULL,
    ph_no VARCHAR(20) NOT NULL
);

-- Create the UserProfile table
CREATE TABLE IF NOT EXISTS UserProfile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(255),
    ph_no INT
);

-- Create the Review table
CREATE TABLE IF NOT EXISTS Review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    rating INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_message TEXT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(id)
);
