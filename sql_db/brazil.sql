
CREATE DATABASE  IF NOT EXISTS Brazil_ceaf;
use Brazil_ceaf;

CREATE TABLE Brazil_demo (
    Name varchar(255),
    CPF varchar(20),
    MAT varchar(20),
    ORG varchar(20),
    State varchar(10),
    charge varchar(100),
    CFC varchar(100),
    NPP  varchar(50),
    charge_date date,
    pages int,
    sessions int,
    types varchar(50),
    Num_pro varchar(100),
    law text,
    date_dump varchar(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE  INDEX nameidx on Brazil_demo(name);
CREATE  INDEX datedumpidx on Brazil_demo(date_dump);
