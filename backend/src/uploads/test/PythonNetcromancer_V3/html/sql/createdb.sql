CREATE DATABASE sqlinthesky;
USE sqlinthesky;
-- DROP TABLE tblHosts,tblPacket,tblThroughput;
-- TRUNCATE TABLE tblHosts, tblPacket, tblThroughput;
CREATE TABLE tblHosts (
    idHost INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    dtHostname VARCHAR(255),
    dtIP VARCHAR(15),
    dtMAC VARCHAR(17),
    dtStatus VARCHAR(50)
);

CREATE TABLE tblPacket (
    idPacket INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    dtSrcIP VARCHAR(15),
    dtDestIP VARCHAR(15)
);

CREATE TABLE tblThroughput (
    idData INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    dtIncoming DECIMAL (65,10),
    dtOutgoing DECIMAL (65,10),
    dtTimestamp DATETIME
);