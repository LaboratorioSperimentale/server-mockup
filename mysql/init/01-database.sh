#!/bin/sh
# Eseguito da MySQL solo alla prima creazione del volume dati.
# Crea un database e un utente per ogni servizio.
# Le password arrivano dalle variabili d'ambiente di docker-compose.yml.

mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<SQL
CREATE DATABASE IF NOT EXISTS forgejo   CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS inception CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS sito_a    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'forgejo'@'%'   IDENTIFIED BY '${FORGEJO_DB_PASSWORD}';
CREATE USER IF NOT EXISTS 'inception'@'%' IDENTIFIED BY '${INCEPTION_DB_PASSWORD}';
CREATE USER IF NOT EXISTS 'sito_a'@'%'    IDENTIFIED BY '${SITO_A_DB_PASSWORD}';

GRANT ALL PRIVILEGES ON forgejo.*   TO 'forgejo'@'%';
GRANT ALL PRIVILEGES ON inception.* TO 'inception'@'%';
GRANT ALL PRIVILEGES ON sito_a.*    TO 'sito_a'@'%';
FLUSH PRIVILEGES;
SQL
