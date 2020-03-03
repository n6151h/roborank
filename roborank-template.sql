-- RoboRank sqlit3 schema

pragma foreign_keys=off;

create table teams (
    teamId integer primary key not null,
    name varchar default ''
);

create table raw_scores (
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
