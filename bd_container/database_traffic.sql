CREATE DATABASE traffic;
USE traffic;

CREATE TABLE traffic(
    RecordID int NOT NULL AUTO_INCREMENT,
    UnixTime DATETIME,
    SourceIp VARCHAR(255),
    DestinationIp VARCHAR(255),
    Protocol VARCHAR(50),
    ByteSize int,
    AnomalyMarker int DEFAULT NULL,
    PRIMARY KEY (RecordID)
);

SET @@session.time_zone="+03:00"; -- меняем часовой пояс в MYSQL

INSERT INTO traffic (UnixTime, SourceIp, DestinationIp, Protocol, ByteSize, AnomalyMarker)
VALUES ('2023-04-01 12:34:56', '192.168.1.1', '192.168.1.2', 'TCP', 1024, NULL);