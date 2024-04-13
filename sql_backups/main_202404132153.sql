﻿--
-- Script was generated by Devart dbForge Studio for MySQL, Version 10.0.60.0
-- Product home page: http://www.devart.com/dbforge/mysql/studio
-- Script date 13.04.2024 21:53:16
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

-- 
-- Dumping data for table users
--
INSERT INTO users VALUES
(4, 'kiramys133@yandex.ru', '+79591273352', 'Mark', 'Bardin', 'scrypt:32768:8:1$E3pmw2lHw8X9QEeF$9c96c00124508ecf23f791e681013a3d18b13ac458c10fd6ff601525030f0a89bcfefa3fac6281133edc3fccf973140f789e6c3ea65778a0b7be9a9e9fc9097d', NULL, NULL, NULL, NULL, NULL, NULL, 0),
(6, 'kiramys1332@yandex.ru', '+79591273353', 'Mark', 'Bardin', 'scrypt:32768:8:1$ylIbaDdWRmifJNZ6$c1b81eb3b1dc9e11aaf889744648641fb749f3a9c204ce67cba5cf37226eaea27238de36cac813e1a3c7e80652ff89db74a28816909e8735279c2432b3b70453', NULL, NULL, NULL, NULL, NULL, NULL, 0);

-- Table main.order_statuses does not contain any data (it is empty)

-- 
-- Dumping data for table organizations
--
INSERT INTO organizations VALUES
(4, 4, 'ООО "СОВА"', NULL, NULL, NULL, NULL, '9406013783', 1),
(7, 4, 'ООО "ЕЖИК"', NULL, NULL, NULL, NULL, '345915768513', 1);

-- 
-- Dumping data for table restaurants
--
INSERT INTO restaurants VALUES
(1, 'LoL', 4, NULL, NULL, NULL, NULL);

-- Table main.orders does not contain any data (it is empty)

-- Table main.menus does not contain any data (it is empty)

-- Table main.food_items does not contain any data (it is empty)

-- Table main.users_to_organizations does not contain any data (it is empty)

-- Table main.tickets does not contain any data (it is empty)

-- Table main.reviews does not contain any data (it is empty)

-- Table main.organization_access_types does not contain any data (it is empty)

-- Table main.food_items_to_orders does not contain any data (it is empty)

-- Table main.food_items_to_menu does not contain any data (it is empty)

-- Table main.available_couriers does not contain any data (it is empty)

-- 
-- Dumping data for table account_types
--
INSERT INTO account_types VALUES
(1, 'user'),
(2, 'courier'),
(3, 'admin'),
(4, 'moderator'),
(5, 'QA');

--
-- Restore previous SQL mode
--
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

--
-- Enable foreign keys
--
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;