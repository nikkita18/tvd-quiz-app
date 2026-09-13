-- Database Schema for TVD Quiz App (b12_app)
-- Compatible with MySQL 8.x, TiDB, Railway, Aiven, PlanetScale, MariaDB

CREATE DATABASE IF NOT EXISTS b12_app;
USE b12_app;

-- 1. User Table
CREATE TABLE IF NOT EXISTS `user` (
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Quiz Questions Table
CREATE TABLE IF NOT EXISTS `quiz` (
  `quesID` int NOT NULL AUTO_INCREMENT,
  `level` int DEFAULT NULL,
  `ques` mediumtext,
  `opt1` mediumtext,
  `opt2` mediumtext,
  `answer` int DEFAULT NULL,
  PRIMARY KEY (`quesID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Scorecard / Leaderboard Table
CREATE TABLE IF NOT EXISTS `scorecard` (
  `scorecardID` int NOT NULL AUTO_INCREMENT,
  `userEmail` varchar(255) DEFAULT NULL,
  `level` int DEFAULT NULL,
  `score` int DEFAULT NULL,
  `playDate` date DEFAULT NULL,
  PRIMARY KEY (`scorecardID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
