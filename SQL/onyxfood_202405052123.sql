﻿--
-- Script was generated by Devart dbForge Studio for MySQL, Version 10.0.60.0
-- Product home page: http://www.devart.com/dbforge/mysql/studio
-- Script date 05.05.2024 21:23:37
-- Server version: 8.0.36
--

--
-- Disable foreign keys
--
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

--
-- Set SQL mode
--
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

--
-- Set character set the client will use to send SQL statements to the server
--
SET NAMES 'utf8';

DROP DATABASE IF EXISTS main;

CREATE DATABASE main
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

--
-- Set default database
--
USE main;

--
-- Create table `account_types`
--
CREATE TABLE account_types (
  id int NOT NULL AUTO_INCREMENT,
  type varchar(50) NOT NULL,
  access_levels int NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
AUTO_INCREMENT = 6,
AVG_ROW_LENGTH = 3276,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create table `users`
--
CREATE TABLE users (
  id int NOT NULL AUTO_INCREMENT,
  email varchar(130) NOT NULL,
  phone varchar(15) NOT NULL,
  name varchar(45) NOT NULL,
  second_name varchar(45) NOT NULL,
  password varchar(255) NOT NULL,
  region varchar(50) DEFAULT NULL,
  city varchar(50) DEFAULT NULL,
  street varchar(70) DEFAULT NULL,
  house char(20) DEFAULT NULL,
  account_type int NOT NULL,
  theme varchar(20) DEFAULT NULL,
  last_failed_login datetime DEFAULT NULL,
  login_attempts int NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
AUTO_INCREMENT = 7,
AVG_ROW_LENGTH = 16384,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE users
ADD CONSTRAINT FK_users_account_type FOREIGN KEY (account_type)
REFERENCES account_types (id);

--
-- Create table `organizations`
--
CREATE TABLE organizations (
  id int NOT NULL AUTO_INCREMENT,
  owner_id int NOT NULL,
  name varchar(50) NOT NULL,
  region varchar(50) DEFAULT NULL,
  city varchar(50) DEFAULT NULL,
  street varchar(70) DEFAULT NULL,
  house char(20) DEFAULT NULL,
  INN varchar(14) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
AUTO_INCREMENT = 8,
AVG_ROW_LENGTH = 8192,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE organizations
ADD CONSTRAINT FK_restaurants_owner_id FOREIGN KEY (owner_id)
REFERENCES users (id) ON DELETE CASCADE;

--
-- Create table `restaurants`
--
CREATE TABLE restaurants (
  id int NOT NULL,
  name varchar(50) DEFAULT NULL,
  org_id int NOT NULL,
  region varchar(50) DEFAULT NULL,
  city varchar(50) DEFAULT NULL,
  street varchar(50) DEFAULT NULL,
  house varchar(20) DEFAULT NULL,
  couriers tinyint NOT NULL DEFAULT 1,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
AVG_ROW_LENGTH = 16384,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE restaurants
ADD CONSTRAINT FK_restaraunts_org_id FOREIGN KEY (org_id)
REFERENCES organizations (id) ON DELETE CASCADE;

--
-- Create table `tickets`
--
CREATE TABLE tickets (
  id int NOT NULL,
  user_id int NOT NULL,
  restaurant_id int NOT NULL,
  message json NOT NULL,
  completed tinyint(1) NOT NULL DEFAULT 0,
  date_time datetime NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE tickets
ADD CONSTRAINT FK_tickets_restaurant_id FOREIGN KEY (restaurant_id)
REFERENCES restaurants (id) ON DELETE CASCADE;

--
-- Create foreign key
--
ALTER TABLE tickets
ADD CONSTRAINT FK_tickets_user_id FOREIGN KEY (user_id)
REFERENCES users (id) ON DELETE CASCADE;

--
-- Create table `food_items`
--
CREATE TABLE food_items (
  id int NOT NULL,
  org_id int NOT NULL,
  name varchar(50) NOT NULL,
  description varchar(255) DEFAULT NULL,
  ingridients varchar(255) NOT NULL,
  stop_list tinyint(1) DEFAULT NULL,
  price decimal(19, 2) UNSIGNED DEFAULT NULL,
  cooking_time int UNSIGNED NOT NULL,
  week binary(7) DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE food_items
ADD CONSTRAINT FK_food_items_org_id FOREIGN KEY (org_id)
REFERENCES organizations (id) ON DELETE CASCADE;

--
-- Create table `reviews`
--
CREATE TABLE reviews (
  id int NOT NULL,
  restaurant_id int DEFAULT NULL,
  food_item_id int DEFAULT NULL,
  courier_id int DEFAULT NULL,
  user_id int NOT NULL,
  review varchar(255) DEFAULT NULL,
  mark decimal(10, 0) NOT NULL,
  date_time datetime NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE reviews
ADD CONSTRAINT FK_reviews_courier_id FOREIGN KEY (courier_id)
REFERENCES users (id) ON DELETE CASCADE;

--
-- Create foreign key
--
ALTER TABLE reviews
ADD CONSTRAINT FK_reviews_food_item_id FOREIGN KEY (food_item_id)
REFERENCES food_items (id);

--
-- Create foreign key
--
ALTER TABLE reviews
ADD CONSTRAINT FK_reviews_restaurant_id FOREIGN KEY (restaurant_id)
REFERENCES restaurants (id) ON DELETE CASCADE;

--
-- Create foreign key
--
ALTER TABLE reviews
ADD CONSTRAINT FK_reviews_user_id FOREIGN KEY (user_id)
REFERENCES users (id);

--
-- Create table `couriers_shifts`
--
CREATE TABLE couriers_shifts (
  id int NOT NULL,
  shift_started datetime NOT NULL,
  shift_ended datetime DEFAULT NULL,
  courier_id int NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE couriers_shifts
ADD CONSTRAINT FK_available_couriers_courier FOREIGN KEY (courier_id)
REFERENCES users (id) ON DELETE CASCADE;

--
-- Create table `order_statuses`
--
CREATE TABLE order_statuses (
  id int NOT NULL,
  description varchar(255) NOT NULL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create table `orders`
--
CREATE TABLE orders (
  id int NOT NULL,
  datetime datetime NOT NULL,
  status int NOT NULL,
  user_id int NOT NULL,
  courier_id int DEFAULT NULL,
  restaurant_id int NOT NULL,
  coordinates json NOT NULL,
  delivery_time int DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb3,
COLLATE utf8mb3_general_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE orders
ADD CONSTRAINT FK_orders_courier FOREIGN KEY (courier_id)
REFERENCES users (id);

--
-- Create foreign key
--
ALTER TABLE orders
ADD CONSTRAINT FK_orders_restaurant FOREIGN KEY (restaurant_id)
REFERENCES restaurants (id);

--
-- Create foreign key
--
ALTER TABLE orders
ADD CONSTRAINT FK_orders_status FOREIGN KEY (status)
REFERENCES order_statuses (id);

--
-- Create foreign key
--
ALTER TABLE orders
ADD CONSTRAINT FK_orders_user_id FOREIGN KEY (user_id)
REFERENCES users (id) ON DELETE CASCADE;

--
-- Create table `food_items_to_orders`
--
CREATE TABLE food_items_to_orders (
  id int NOT NULL AUTO_INCREMENT,
  order_id int NOT NULL,
  food_item_id int NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE food_items_to_orders
ADD CONSTRAINT FK_food_items_to_orders_food_item_id FOREIGN KEY (food_item_id)
REFERENCES food_items (id);

--
-- Create foreign key
--
ALTER TABLE food_items_to_orders
ADD CONSTRAINT FK_food_items_to_orders_order_id FOREIGN KEY (order_id)
REFERENCES orders (id);

--
-- Create table `categories`
--
CREATE TABLE categories (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create table `food_items_to_categories`
--
CREATE TABLE food_items_to_categories (
  id int NOT NULL AUTO_INCREMENT,
  food_item_id int NOT NULL,
  category_id int NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create foreign key
--
ALTER TABLE food_items_to_categories
ADD CONSTRAINT FK_food_items_to_categories_category_id FOREIGN KEY (category_id)
REFERENCES categories (id);

--
-- Create foreign key
--
ALTER TABLE food_items_to_categories
ADD CONSTRAINT FK_food_items_to_categories_food_item_id FOREIGN KEY (food_item_id)
REFERENCES food_items (id);

--
-- Create table `users_to_organizations`
--
CREATE TABLE users_to_organizations (
  user_id int NOT NULL,
  org_id int NOT NULL,
  access_type int DEFAULT NULL
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Create table `organization_access_types`
--
CREATE TABLE organization_access_types (
  id int NOT NULL,
  description varchar(255) NOT NULL,
  PRIMARY KEY (id, description)
)
ENGINE = INNODB,
CHARACTER SET utf8mb4,
COLLATE utf8mb4_0900_ai_ci,
ROW_FORMAT = DYNAMIC;

--
-- Restore previous SQL mode
--
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

--
-- Enable foreign keys
--
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;