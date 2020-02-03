PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE teams (
    teamId integer primary key not null,
    name varchar default ''
);
INSERT INTO teams VALUES(1456,'');
INSERT INTO teams VALUES(2132,'');
INSERT INTO teams VALUES(2342,'');
INSERT INTO teams VALUES(3135,'');
INSERT INTO teams VALUES(3575,'');
INSERT INTO teams VALUES(4367,'');
INSERT INTO teams VALUES(4567,'');
INSERT INTO teams VALUES(5648,'');
INSERT INTO teams VALUES(5668,'');
INSERT INTO teams VALUES(5788,'');
INSERT INTO teams VALUES(6666,'');
INSERT INTO teams VALUES(6794,'');
INSERT INTO teams VALUES(8305,'');
INSERT INTO teams VALUES(8487,'');
CREATE TABLE raw_scores (
    scoreId integer primary key autoincrement not null,
    teamId integer not null,
    round integer not null,
    low_balls integer default 0,
    high_balls integer default 0,
    autonomous integer not null check (autonomous in (0,1)) default 0,
    climb integer not null check (climb in (0,1)) default 0,
    spin_by_colour integer not null check (spin_by_colour in (0,1)) default 0,
    spin_by_rotate integer not null check (spin_by_rotate in (0,1)) default 0,
    rating varchar default '',
    foreign key (teamId) references teams(teamId) on delete no action on update no action
);
INSERT INTO raw_scores VALUES(107,3135,1,6,15,1,1,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(108,5788,1,10,10,1,1,0,0,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(109,4567,1,5,12,1,1,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(110,8305,1,3,13,1,1,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(111,4367,1,4,8,1,1,0,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(112,5668,1,2,5,1,1,0,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(113,8487,1,1,4,0,0,0,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(114,1456,1,0,13,1,0,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(115,6794,1,0,12,0,1,0,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(116,6666,1,0,3,0,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(117,2342,1,0,0,0,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(118,3575,1,1,0,0,0,0,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(119,2132,1,0,10,1,0,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(120,3135,2,8,13,1,1,0,0,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(121,5788,2,2,17,1,1,0,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(122,4567,2,10,8,1,0,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(123,8305,2,5,3,1,1,1,0,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(124,4367,2,2,10,1,0,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(125,5668,2,2,6,0,1,0,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(126,8487,2,1,5,0,1,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(127,1456,2,9,4,0,0,1,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(128,6794,2,0,7,1,0,0,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(129,6666,2,0,1,0,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(130,2342,2,0,3,0,1,0,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(131,3575,2,0,3,0,0,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(132,2132,2,0,2,0,0,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(133,3135,3,10,7,0,1,0,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(134,5788,3,3,8,1,1,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(135,4567,3,11,3,1,1,0,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(136,8305,3,5,5,1,1,1,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(137,4367,3,6,6,0,0,1,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(138,5668,3,3,6,1,1,0,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(139,8487,3,2,2,1,1,0,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(140,1456,3,5,3,1,0,0,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(141,6794,3,2,1,0,1,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(142,6666,3,3,0,0,1,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(143,2342,3,4,0,0,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(144,3575,3,1,1,1,0,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(145,2132,3,0,0,0,1,1,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(146,3135,4,5,1,1,1,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(147,5788,4,3,9,1,1,0,0,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(148,4567,4,6,5,1,0,1,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(149,8305,4,10,7,1,1,0,1,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(150,4367,4,9,3,0,1,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(151,5668,4,7,4,0,1,0,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(152,8487,4,8,7,0,0,1,0,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(153,1456,4,9,3,1,0,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(154,6794,4,5,2,1,0,1,1,'MEDIOCRE TEAM');
INSERT INTO raw_scores VALUES(155,6666,4,3,1,1,1,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(156,2342,4,5,0,0,1,0,1,'BAD TEAM');
INSERT INTO raw_scores VALUES(157,3575,4,2,0,1,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(158,2132,4,1,0,0,0,1,0,'BAD TEAM');
INSERT INTO raw_scores VALUES(165,5648,0,1,0,0,0,0,0,'');
INSERT INTO raw_scores VALUES(166,5648,0,2,0,0,0,0,0,'');
INSERT INTO raw_scores VALUES(167,5648,0,3,0,0,0,0,0,'GOOD TEAM ');
INSERT INTO raw_scores VALUES(168,5648,0,4,0,0,0,0,0,'');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('raw_scores',168);
COMMIT;
