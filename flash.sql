DROP DATABASE IF EXISTS flashscore;
CREATE DATABASE flashscore;
USE flashscore;

DROP TABLE IF EXISTS `matches`;
CREATE TABLE `matches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_date` DATE default NULL,
  `team1_id` int(11) default NULL,
  `goals_scored_team1` int(11) default NULL,
  `team2_id` int(11) default NULL,
  `goals_scored_team2` int(11) default NULL,
  PRIMARY KEY  (`id`),
  FOREIGN KEY (`team1_id`) REFERENCES `teams` (`id`),
  FOREIGN KEY (`team2_id`) REFERENCES `teams` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(200) default NULL,
   PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `standings_five_seasons`;
CREATE TABLE `standings_five_seasons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table_position` int(11) default NULL,
  `team_id` int(11) default NULL,
  `matches_played` int(11) default NULL,
  `wins` int(11) default NULL,
  `losses` int(11) default NULL,
  `draws` int(11) default NULL,
  `goals_scored` int(11) default NULL,
  `goals_suffered` int(11) default NULL,
  `year` varchar(200) default NULL,
   PRIMARY KEY  (`id`),
   FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `form_last_five_matches`;
CREATE TABLE `form_last_five_matches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) default NULL,
  `matches_played` int(11) default NULL,
  `wins` int(11) default NULL,
  `losses` int(11) default NULL,
  `draws` int(11) default NULL,
  `goals_scored` int(11) default NULL,
  `goals_suffered` int(11) default NULL,
   PRIMARY KEY  (`id`),
   FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `players`;
CREATE TABLE `players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) default NULL,
  `player_name` varchar(200) default NULL,
  `injury` int(11) default NULL,
  `age` int(11) default NULL,
  `field_position` varchar(200) default NULL,
  `goals_scored` int(11) default NULL,
  `yellow_cards` int(11) default NULL,
  `red_cards` int(11) default NULL,
   PRIMARY KEY  (`id`),
   FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


INSERT INTO `teams` (`team_name`) VALUES
('Team A'),
('Team B'),
('Team C');


INSERT INTO `standings_five_seasons` (`team_id`,`table_position`, `matches_played`, `wins`, `losses`, `draws`, `goals_scored`, `goals_suffered`, `year`) VALUES
(1, 3, 5, 3, 1, 1, 10, 5, '1967-11-17'),
(2, 4, 5, 2, 2, 1, 8, 6, '1967-11-17'),
(3, 5, 5, 1, 3, 1, 6, 9, '1967-11-17');


INSERT INTO `form_last_five_matches` (`team_id`, `matches_played`, `wins`, `losses`, `draws`, `goals_scored`, `goals_suffered`) VALUES
(1, 5, 3, 1, 1, 10, 5),
(2, 5, 2, 2, 1, 8, 6),
(3, 5, 1, 3, 1, 6, 9);


INSERT INTO `players` (`team_id`, `player_name`, `injury`, `age`, `field_position`, `goals_scored`, `yellow_cards`, `red_cards`) VALUES
(1, 'Player 1', 0, 25, 'Forward', 5, 2, 0),
(2, 'Player 2', 1, 28, 'Midfielder', 3, 1, 0),
(3, 'Player 3', 0, 23, 'Defender', 1, 0, 0);

