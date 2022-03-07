-- USE AT TOP OF SCRIPT
DROP SCHEMA pokemon_tcg_api;
CREATE SCHEMA pokemon_tcg_api;
USE pokemon_tcg_api;


-- USE AFTER TABLE DDL, BUT BEFORE FOREIGN KEYS
ALTER TABLE `card_attack` ADD INDEX (`name`);


