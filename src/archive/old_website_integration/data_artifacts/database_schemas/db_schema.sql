-- USE AT TOP OF SCRIPT
DROP SCHEMA pokemon_tcg_api;
CREATE SCHEMA pokemon_tcg_api;
USE pokemon_tcg_api;

CREATE TABLE `series` (
  `name` varchar(50) PRIMARY KEY
);

CREATE TABLE `language` (
  `code` varchar(20) PRIMARY KEY,
  `name` varchar(50)
);

CREATE TABLE `set` (
  `id` varchar(20) PRIMARY KEY,
  `series` varchar(20),
  `printedTotal` int,
  `total` int,
  `ptcgoCode` varchar(255),
  `releaseDate` date,
  `updatedAt` datetime
);

CREATE TABLE `set_name` (
  `language` varchar(20),
  `set` varchar(20),
  `name` varchar(100),
  PRIMARY KEY (`language`, `set`)
);

CREATE TABLE `set_hpcode` (
  `language` varchar(20),
  `set` varchar(20),
  `hp_code` varchar(100),
  PRIMARY KEY (`language`, `set`)
);

CREATE TABLE `legality` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `set_legality` (
  `set` varchar(20),
  `legality` varchar(255),
  PRIMARY KEY (`set`, `legality`)
);

CREATE TABLE `set_images` (
  `set` varchar(20),
  `type` varchar(255),
  `url` varchar(255),
  PRIMARY KEY (`set`, `type`)
);

CREATE TABLE `energy_type` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `rarity` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `card` (
  `id` varchar(255) PRIMARY KEY COMMENT 'generated field from "{set}-{number}"',
  `set` varchar(20),
  `number` varchar(255),
  `name` varchar(255),
  `hp` varchar(255),
  `supertype` varchar(255),
  `artist` varchar(255),
  `rarity` varchar(255)
);

CREATE TABLE `card_nationalPokedexNumber` (
  `card` varchar(20) PRIMARY KEY,
  `nationalPokedexNumber` int
);

CREATE TABLE `supertype` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `type` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `card_type` (
  `name` varchar(255),
  `card` varchar(20),
  PRIMARY KEY (`name`, `card`)
);

CREATE TABLE `subtype` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `card_subtype` (
  `name` varchar(255),
  `card` varchar(20),
  PRIMARY KEY (`name`, `card`)
);

CREATE TABLE `evolution` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `card_evolution` (
  `card` varchar(20),
  `evolution` varchar(255),
  PRIMARY KEY (`card`, `evolution`)
);

CREATE TABLE `card_ability` (
  `card` varchar(20),
  `name` varchar(20),
  `language` varchar(20),
  `convertedEnergyCost` varchar(255),
  PRIMARY KEY (`card`, `name`, `language`)
);

CREATE TABLE `card_attack` (
  `card` varchar(20),
  `name` varchar(255),
  `convertedEnergyCost` int,
  `damage` varchar(255),
  PRIMARY KEY (`card`, `name`)
);

CREATE TABLE `cards_attack_text` (
  `card` varchar(20),
  `language` varchar(20),
  `text` varchar(200),
  PRIMARY KEY (`card`, `language`)
);

CREATE TABLE `card_attack_cost` (
  `card` varchar(20),
  `name` varchar(255),
  `energy_type` varchar(255),
  `amount` int,
  PRIMARY KEY (`card`, `name`, `energy_type`)
);

CREATE TABLE `card_retreat_cost` (
  `card` varchar(20),
  `energy_type` varchar(255),
  `amount` int,
  PRIMARY KEY (`card`, `energy_type`)
);

CREATE TABLE `artist` (
  `name` varchar(255) PRIMARY KEY
);

CREATE TABLE `deck` (
  `id` varchar(255) PRIMARY KEY,
  `set` varchar(255),
  `name` varchar(255)
);

CREATE TABLE `deck_type` (
  `deck` varchar(255),
  `energy_type` varchar(255),
  `amount` int,
  PRIMARY KEY (`deck`, `energy_type`)
);

CREATE TABLE `deck_card` (
  `deck` varchar(255),
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255),
  `rarity` varchar(255),
  `count` int
);

CREATE TABLE `card_flavortext` (
  `language` varchar(20),
  `card` varchar(20),
  `flavortext` varchar(255),
  PRIMARY KEY (`language`, `card`)
);

CREATE TABLE `card_name` (
  `language` varchar(20),
  `card` varchar(20),
  `name` varchar(255),
  PRIMARY KEY (`language`, `card`)
);

ALTER TABLE `card_attack` ADD INDEX (`name`);

ALTER TABLE `set` ADD FOREIGN KEY (`series`) REFERENCES `series` (`name`);

ALTER TABLE `set_name` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `set_name` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `set_hpcode` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `set_hpcode` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `set_legality` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `set_legality` ADD FOREIGN KEY (`legality`) REFERENCES `legality` (`name`);

ALTER TABLE `set_images` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `card` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `card` ADD FOREIGN KEY (`supertype`) REFERENCES `supertype` (`name`);

ALTER TABLE `card` ADD FOREIGN KEY (`artist`) REFERENCES `artist` (`name`);

ALTER TABLE `card` ADD FOREIGN KEY (`rarity`) REFERENCES `rarity` (`name`);

ALTER TABLE `card_nationalPokedexNumber` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_type` ADD FOREIGN KEY (`name`) REFERENCES `type` (`name`);

ALTER TABLE `card_type` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_subtype` ADD FOREIGN KEY (`name`) REFERENCES `subtype` (`name`);

ALTER TABLE `card_subtype` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_evolution` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_evolution` ADD FOREIGN KEY (`evolution`) REFERENCES `evolution` (`name`);

ALTER TABLE `card_ability` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_ability` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `card_attack` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `cards_attack_text` ADD FOREIGN KEY (`card`) REFERENCES `card_attack` (`card`);

ALTER TABLE `cards_attack_text` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `card_attack_cost` ADD FOREIGN KEY (`card`) REFERENCES `card_attack` (`card`);

ALTER TABLE `card_attack_cost` ADD FOREIGN KEY (`name`) REFERENCES `card_attack` (`name`);

ALTER TABLE `card_attack_cost` ADD FOREIGN KEY (`energy_type`) REFERENCES `energy_type` (`name`);

ALTER TABLE `card_retreat_cost` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_retreat_cost` ADD FOREIGN KEY (`energy_type`) REFERENCES `energy_type` (`name`);

ALTER TABLE `deck` ADD FOREIGN KEY (`set`) REFERENCES `set` (`id`);

ALTER TABLE `deck_type` ADD FOREIGN KEY (`deck`) REFERENCES `deck` (`id`);

ALTER TABLE `deck_type` ADD FOREIGN KEY (`energy_type`) REFERENCES `energy_type` (`name`);

ALTER TABLE `deck_card` ADD FOREIGN KEY (`deck`) REFERENCES `deck` (`id`);

ALTER TABLE `deck_card` ADD FOREIGN KEY (`rarity`) REFERENCES `rarity` (`name`);

ALTER TABLE `card_flavortext` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `card_flavortext` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

ALTER TABLE `card_name` ADD FOREIGN KEY (`language`) REFERENCES `language` (`code`);

ALTER TABLE `card_name` ADD FOREIGN KEY (`card`) REFERENCES `card` (`id`);

