-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dbm_project_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dbm_project_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dbm_project_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `dbm_project_db` ;

-- -----------------------------------------------------
-- Table `dbm_project_db`.`authors_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`authors_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`authors_t` (
  `id` INT NOT NULL,
  `name` VARCHAR(240) NULL DEFAULT NULL,
  `location` VARCHAR(240) NULL DEFAULT NULL,
  `authors_tcol` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`companies_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`companies_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`companies_t` (
  `id` INT NOT NULL,
  `name` VARCHAR(240) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`articles_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`articles_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`articles_t` (
  `id` INT NOT NULL,
  `datetime` DATETIME NULL DEFAULT NULL,
  `title` VARCHAR(240) NULL DEFAULT NULL,
  `description` VARCHAR(1200) NULL DEFAULT NULL,
  `text` LONGTEXT NULL DEFAULT NULL,
  `url` VARCHAR(1200) NULL DEFAULT NULL,
  `company_id` INT NOT NULL,
  PRIMARY KEY (`id`, `company_id`),
  INDEX `fk_articles_t_1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_articles_t_1`
    FOREIGN KEY (`company_id`)
    REFERENCES `dbm_project_db`.`companies_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`roles_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`roles_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`roles_t` (
  `id` INT NOT NULL,
  `role` VARCHAR(240) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`article_author_role_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`article_author_role_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`article_author_role_t` (
  `article_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  PRIMARY KEY (`article_id`, `author_id`, `role_id`),
  INDEX `fk_article_author_t_1_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_article_author_t_3_idx` (`role_id` ASC) VISIBLE,
  CONSTRAINT `fk_article_author_t_1`
    FOREIGN KEY (`author_id`)
    REFERENCES `dbm_project_db`.`authors_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_article_author_t_2`
    FOREIGN KEY (`article_id`)
    REFERENCES `dbm_project_db`.`articles_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_article_author_t_3`
    FOREIGN KEY (`role_id`)
    REFERENCES `dbm_project_db`.`roles_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`keywords_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`keywords_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`keywords_t` (
  `id` INT NOT NULL,
  `keyword` VARCHAR(240) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`article_keyword_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`article_keyword_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`article_keyword_t` (
  `article_id` INT NOT NULL,
  `keyword_id` INT NOT NULL,
  PRIMARY KEY (`article_id`, `keyword_id`),
  INDEX `fk_article_keyword_t_2_idx` (`keyword_id` ASC) VISIBLE,
  CONSTRAINT `fk_article_keyword_t_1`
    FOREIGN KEY (`article_id`)
    REFERENCES `dbm_project_db`.`articles_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_article_keyword_t_2`
    FOREIGN KEY (`keyword_id`)
    REFERENCES `dbm_project_db`.`keywords_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`categories_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`categories_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`categories_t` (
  `id` INT NOT NULL,
  `category` VARCHAR(240) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dbm_project_db`.`article_category_t`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dbm_project_db`.`article_category_t` ;

CREATE TABLE IF NOT EXISTS `dbm_project_db`.`article_category_t` (
  `article_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`article_id`, `category_id`),
  INDEX `fk_article_category_t_2_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_article_category_t_1`
    FOREIGN KEY (`article_id`)
    REFERENCES `dbm_project_db`.`articles_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_article_category_t_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `dbm_project_db`.`categories_t` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

