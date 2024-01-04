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


DROP TABLE IF EXISTS `future_fixtures_predictions_data`;
CREATE TABLE `future_fixtures_predictions_data` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `home_team_id` varchar(200) default NULL,
    `away_team_id` varchar(200) default NULL,
    `prediction_home_team_wins` FLOAT default NULL,
    `prediction_draw` FLOAT default NULL,
    `prediction_away_team_wind` FLOAT default NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`id`),
    FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


