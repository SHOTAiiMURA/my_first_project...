-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`GameGroup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GameGroup` (
  `group_id` INT NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE INDEX `group_id_UNIQUE` (`group_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Team` (
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Role` (
  `name` VARCHAR(50) NOT NULL,
  `team_name` VARCHAR(50) NOT NULL,
  `fortune_teller_team` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  INDEX `fk_Role_Team_idx` (`team_name` ASC) VISIBLE,
  INDEX `fk_Role_Team1_idx` (`fortune_teller_team` ASC) VISIBLE,
  CONSTRAINT `fk_Role_Team`
    FOREIGN KEY (`team_name`)
    REFERENCES `mydb`.`Team` (`name`),
  CONSTRAINT `fk_Role_Team1`
    FOREIGN KEY (`fortune_teller_team`)
    REFERENCES `mydb`.`Team` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Player` (
  `user_id` VARCHAR(50) NOT NULL,
  `name` INT NOT NULL,
  `role_name` VARCHAR(50) NULL DEFAULT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  INDEX `fk_Player_Role1_idx` (`role_name` ASC) VISIBLE,
  INDEX `fk_Player_GameGroup1_idx` (`group_id` ASC) VISIBLE,
  CONSTRAINT `fk_Player_GameGroup1`
    FOREIGN KEY (`group_id`)
    REFERENCES `mydb`.`GameGroup` (`group_id`),
  CONSTRAINT `fk_Player_Role1`
    FOREIGN KEY (`role_name`)
    REFERENCES `mydb`.`Role` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Setting`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Setting` (
  `group_id` INT NOT NULL,
  `role_name` VARCHAR(50) NOT NULL,
  `num` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`group_id`, `role_name`),
  INDEX `fk_Setting_Role1_idx` (`role_name` ASC) VISIBLE,
  INDEX `fk_Setting_GameGroup1_idx` (`group_id` ASC) VISIBLE,
  CONSTRAINT `fk_Setting_GameGroup1`
    FOREIGN KEY (`group_id`)
    REFERENCES `mydb`.`GameGroup` (`group_id`),
  CONSTRAINT `fk_Setting_Role1`
    FOREIGN KEY (`role_name`)
    REFERENCES `mydb`.`Role` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`SettingTemplate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`SettingTemplate` (
  `player_num` INT NOT NULL,
  `role_name` VARCHAR(50) NOT NULL,
  `role_num` INT NOT NULL,
  PRIMARY KEY (`player_num`, `role_name`),
  INDEX `fk_SettingTemplate_Role1_idx` (`role_name` ASC) VISIBLE,
  CONSTRAINT `fk_SettingTemplate_Role1`
    FOREIGN KEY (`role_name`)
    REFERENCES `mydb`.`Role` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Priority`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Priority` (
  `priority` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`priority`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `line_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`line_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Task`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Task` (
  `task_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  `duration` INT NULL,
  `state` CHAR(2) NOT NULL,
  `due_date` DATETIME NULL,
  `end_time` DATETIME NULL,
  `start_time` DATETIME NULL,
  `extended_time` INT NOT NULL DEFAULT 0,
  `priority` VARCHAR(10) NULL,
  `line_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`task_id`),
  UNIQUE INDEX `task_id_UNIQUE` (`task_id` ASC) VISIBLE,
  INDEX `fk_Task_Priority1_idx` (`priority` ASC) VISIBLE,
  INDEX `fk_Task_User1_idx` (`line_id` ASC) VISIBLE,
  CONSTRAINT `fk_Task_Priority1`
    FOREIGN KEY (`priority`)
    REFERENCES `mydb`.`Priority` (`priority`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Task_User1`
    FOREIGN KEY (`line_id`)
    REFERENCES `mydb`.`User` (`line_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
