# Top goal scorers, assits, red cards, pendalty goals, own goals

select player_name as name, c.club_name as Club,count(*) as goals from player_performance as pp 
	INNER JOIN player as p ON pp.player_id=p.player_id
	INNER JOIN club as c on p.club_id=c.club_id
	where (type_of_stat=1 or type_of_stat=2)
	group by p.player_id
	order by goals desc
	limit 10;


# most appearances

# get goals per season:
select m.season, p_c.club_id, c.club_name, count(*)  as goals   from player_performance as p_p   inner join match_ as m on m.match_id=p_p.match_id inner join player_stats as p_s on p_s.match_id=m.match_id and p_s.player_id=p_p.player_id inner join player_club as p_c on p_c.player_id=p_p.player_id   and p_c.season=m.season   and if(p_s.is_home_side is True, p_c.club_id=m.home_team_id, p_c.club_id=m.away_team_id)   inner join club as c on c.club_id=p_c.club_id   where p_p.player_id="p57249"   and (type_of_stat=1 or type_of_stat=2)   group by season, p_c.club_id   order by m.season desc;

# goals for a given season:
select m.season, p_c.club_id, c.club_name, count(*)  as goals   from player_performance as p_p   inner join match_ as m on m.match_id=p_p.match_id inner join player_stats as p_s on p_s.match_id=m.match_id and p_s.player_id=p_p.player_id inner join player_club as p_c on p_c.player_id=p_p.player_id   and p_c.season=m.season   and if(p_s.is_home_side is True, p_c.club_id=m.home_team_id, p_c.club_id=m.away_team_id)   inner join club as c on c.club_id=p_c.club_id   where p_p.player_id="p57249"   and (type_of_stat=1 or type_of_stat=2)  and c.club_id=120 and m.season='2017/18' group by season, p_c.club_id   order by m.season desc;

# squad info with appearances and goals for each player for a given team in a given season
SELECT p.player_id, p.player_name, (select count(*) as appearances from player_stats as p_s2 inner join match_ as m2 on p_s2.match_id=m2.match_id where p_s2.player_id=p.player_id and (is_in_starting_11=1 or substitution_on!='Null') and m2.season='2007/08' and if(p_s2.is_home_side=True, m2.home_team_id=p_c.club_id, m2.away_team_id=p_c.club_id)) as appearances, (select count(*)  as goals   from player_performance as p_p3   inner join match_ as m3 on m3.match_id=p_p3.match_id inner join player_stats as p_s3 on p_s3.match_id=m3.match_id and p_s3.player_id=p_p3.player_id inner join player_club as p_c3 on p_c3.player_id=p_p3.player_id   and p_c3.season=m3.season  and if(p_s3.is_home_side is True, p_c3.club_id=m3.home_team_id, p_c3.club_id=m3.away_team_id)   inner join club as c3 on c3.club_id=p_c3.club_id   where p_p3.player_id=p.player_id and (type_of_stat=1 or type_of_stat=2)  and c3.club_id=134 and m3.season='2007/08' group by m3.season, p_c3.club_id) as goals FROM player AS p INNER JOIN player_club AS p_c on p.player_id=p_c.player_id WHERE p_c.season="2007/08" and p_c.club_id=134 order by field(position, 'Goalkeeper', 'Defender', 'Midfielder', 'Forward');