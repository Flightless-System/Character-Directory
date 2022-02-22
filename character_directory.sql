-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema character_directory
-- -----------------------------------------------------
-- Database for the Character Directory project I'm creating to show what I've learned in the Python course. Is a site meant for light content, not to become a big project, just to wrap my head around things and see if I can do it.

-- -----------------------------------------------------
-- Schema character_directory
--
-- Database for the Character Directory project I'm creating to show what I've learned in the Python course. Is a site meant for light content, not to become a big project, just to wrap my head around things and see if I can do it.
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `character_directory` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `character_directory` ;

-- -----------------------------------------------------
-- Table `character_directory`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `character_directory`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `name` VARCHAR(255) NULL,
  `pronouns` VARCHAR(10) NULL,
  `birthday` DATE NULL,
  `twitter` VARCHAR(255) NULL,
  `about_me` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `character_directory`.`characters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `character_directory`.`characters` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `age` INT NULL,
  `gender` VARCHAR(255) NULL,
  `pronouns` VARCHAR(10) NULL,
  `species` VARCHAR(255) NULL,
  `alignment` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_characters_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_characters_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `character_directory`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `character_directory`.`favorites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `character_directory`.`favorites` (
  `character_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`character_id`, `user_id`),
  INDEX `fk_characters_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_characters_has_users_characters1_idx` (`character_id` ASC) VISIBLE,
  CONSTRAINT `fk_characters_has_users_characters1`
    FOREIGN KEY (`character_id`)
    REFERENCES `character_directory`.`characters` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_characters_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `character_directory`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
