CREATE DATABASE IF NOT EXISTS second_hand_house
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE second_hand_house;

CREATE TABLE IF NOT EXISTS house (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  city VARCHAR(64) NOT NULL,
  district VARCHAR(64),
  community VARCHAR(128),
  total_price DOUBLE,
  unit_price DOUBLE,
  area DOUBLE,
  room_count INT,
  hall_count INT,
  floor VARCHAR(64),
  orientation VARCHAR(64),
  decoration VARCHAR(64),
  build_year INT,
  source_url VARCHAR(768) NOT NULL,
  crawl_time DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_house_source_url (source_url),
  KEY idx_house_city_district (city, district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS crawl_log (
  id INT PRIMARY KEY AUTO_INCREMENT,
  task_name VARCHAR(128) NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME,
  success_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  status VARCHAR(32) DEFAULT 'running',
  error_message TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
