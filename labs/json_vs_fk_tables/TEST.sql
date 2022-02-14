DROP TABLE
    IF EXISTS tests.hashtags;

CREATE TABLE
    tests.hashtags (
        id INT(10) NOT NULL auto_increment,
        datalist json NULL,
        PRIMARY key (id),
        key hashtags_datalist_IDX (datalist(768)) USING btree
    ) ENGINE = InnoDB AUTO_INCREMENT = 55 DEFAULT CHARSET = utf8mb4;

INSERT INTO tests.hashtags (datalist) values
()