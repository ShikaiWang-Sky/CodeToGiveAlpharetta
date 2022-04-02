create table if not exists mentee
(
    id          integer primary key autoincrement not null,
    first_name  text                              not null,
    last_name   text                              not null,
    email       text                              not null,
    password    text                              not null,
    mentor_id   integer,
    language_id integer,
    interest_id integer
);

create table if not exists mentor
(
    id              integer primary key autoincrement not null,
    first_name      text                              not null,
    last_name       text                              not null,
    email           text                              not null,
    password        text                              not null,
    mentee_group_id integer,
    language_id     integer,
    interest_id     integer
);

create table if not exists meeting
(
    id        integer primary key autoincrement not null,
    mentor_id integer                           not null,
    mentee_id integer                           not null,
    time      integer                           not null
);

create table if not exists mentee_group
(
    id        integer primary key autoincrement not null,
    group_id  integer                           not null,
    mentee_id integer                           not null
);

create table if not exists language
(
    id       integer primary key autoincrement not null,
    language text                              not null
);

create table if not exists interest
(
    id       integer primary key autoincrement not null,
    interest text                            not null
)