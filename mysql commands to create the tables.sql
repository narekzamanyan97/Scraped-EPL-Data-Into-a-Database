-- !!! Change the schema

create table stadium(
	stadium_id int(2) not null auto_increment,

	stadium_name varchar(50),
	city varchar(25),
	capacity int(6),
	record_pl_attendance varchar(100),
	address varchar(100),
	pitch_size varchar(15),
	built int(4),
	phone varchar(25),

	constraint STADIUM_ID_PK PRIMARY KEY (stadium_id)
);

create table club(
	club_id int(2) not null auto_increment,

	club_name varchar(50) not null,
	stadium_id int(2),

	website varchar(50) not null,

	constraint CLUB_ID_PK PRIMARY KEY (club_id),
	constraint CLUB_STADIUM_ID_FK FOREIGN KEY (stadium_id)
		references stadium(stadium_id) on delete set null
			on update cascade	
);



create table manager(
	manager_id int(3) not null auto_increment,

	manager_name varchar(40),
	country varchar(40),
	active boolean,
	joined_club date,
	date_of_birth date,
	epl_seasons int(2),
	epl_debut_match varchar(100),

	constraint MANAGER_ID_PK PRIMARY KEY(manager_id),
);

create table player(
	player_id varchar(8) not null,

	player_name varchar(50),
	player_number int(2),
	position varchar(12),
	country varchar(50),
	date_of_birth date,
	height int(3),

	constraint PLAYER_ID_PK PRIMARY KEY(player_id)
);

create table match_(
	match_id int(5) not null,
	

	home_team_id int(2) not null,
	away_team_id int(2) not null,

	home_team_goals int(2),
	away_team_goals int(2),
	match_date date,
	matchweek int(2),
	referee varchar(50),

	stadium_id int(2),

	season varchar(7) default '2020/21',

	attendance varchar(7),

	constraint MATCH_ID_PK PRIMARY KEY (match_id),
	constraint MATCH_HOME_TEAM_ID FOREIGN KEY (home_team_id)
		references club(club_id) on delete cascade
			on update cascade,
	constraint MATCH_AWAY_TEAM_ID FOREIGN KEY (away_team_id)
		references club(club_id) on delete cascade
			on update cascade,
	constraint MATCH_STADIUM_ID FOREIGN KEY (stadium_id)
		references stadium(stadium_id) on delete set null
			on update cascade
);



create table player_stats(
	player_id varchar(8) not null,
	match_id int(5) not null,

	is_in_starting_11 boolean,

	substitution_on varchar(7),
	substitution_off varchar(7),
	yellow_card varchar(7),
	red_card varchar(7),

	constraint PLAYER_STATS_PK primary key (player_id, match_id),
	constraint PLAYER_STATS_PLAYER_ID foreign key (player_id)
		references player(player_id) on delete cascade
			on update cascade,
	constraint PLAYER_STATS_MATCH_ID foreign key (match_id)
		references match_(match_id) on delete cascade
			on update cascade

);

create table player_performance(
	player_performance_id int not null auto_increment,
	player_id varchar(8) not null,
	match_id int(5) not null,

	type_of_stat int(2),
	minute varchar(7),

	constraint PLAYER_PERFORMANCE_ID primary key (player_performance_id),
	constraint PLAYER_PERFORMANCE_PLAYER_ID foreign key (player_id)
		references player(player_id) on delete cascade
			on update cascade,
	constraint PLAYER_PERFORMANCE_MATCH_ID foreign key (match_id)
		references match_(match_id) on delete cascade
			on update cascade
);

create table club_stats(
	match_id int(5) not null,
	club_id int(2) not null,

	possession dec(3, 1),
	shots int(2),
	shots_on_target int(2),
	touches int(4),
	passes int(4),
	tackles int(3),
	clearances int(3),
	corners int(2),
	offsides int(2),
	fouls_conceded int(2),
	yellow_cards int(2),
	red_cards int(1),

	constraint CLUB_STATS_MATCH_ID_FK foreign key (match_id)
		references match_(match_id) on delete cascade
			on update cascade,
	constraint CLUB_STATS_CLUB_ID_FK foreign key (club_id)
		references club(club_id) on delete cascade
			on update cascade
);

create table manager_club(
	manager_id int(3) not null,
	club_id int(2) not null,

	season varchar(7) default '2020/21',

	constraint MANAGER_CLUB_PK primary key (manager_id, club_id, season),
	constraint MANAGER_CLUB_MANAGER_ID_FK foreign key (manager_id)
		references manager(manager_id) on delete cascade
			on update cascade,
	constraint MANAGER_CLUB_CLUB_ID_FK foreign key (club_id)
		references club(club_id) on delete cascade
			on update cascade
);

create table player_club(
	player_id varchar(8) not null,
	club_id int(2) not null,

	season varchar(7) default '2020/21',

	constraint PLAYER_CLUB_PK primary key (player_id, club_id, season),
	constraint PLAYER_CLUB_PLAYER_ID_FK foreign key (player_id)
		references player(player_id) on delete cascade
			on update cascade,
	constraint PLAYER_CLUB_CLUB_ID_FK foreign key (club_id)
		references club(club_id) on delete cascade
			on update cascade
);

create table fixture(
	fixture_id varchar(8) not null,
	
	home_team_id int(2) not null,
	away_team_id int(2) not null,
	stadium_id int(2),
	season varchar(7) default '2021/22',
	time_ Time default Null,
	date_ Date default Null,
	weekday varchar(9),



	constraint FIXTURE_PK primary key (fixture_id),
	constraint FIXTURE_HOME_TEAM_ID_FK foreign key (home_team_id)
		references club(club_id) on delete cascade
			on update cascade,
	constraint FIXTURE_AWAY_TEAM_ID_FK foreign key (away_team_id)
		references club(club_id) on delete cascade
			on update cascade,

	constraint FIXTURE_STADIUM_ID_FK FOREIGN KEY (stadium_id)
		references stadium(stadium_id) on delete set null
			on update cascade	
);