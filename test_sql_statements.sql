# Top goal scorers, assits, red cards, pendalty goals, own goals

select player_name as name, c.club_name as Club,count(*) as goals from player_performance as pp 
	INNER JOIN player as p ON pp.player_id=p.player_id
	INNER JOIN club as c on p.club_id=c.club_id
	where (type_of_stat=1 or type_of_stat=2)
	group by p.player_id
	order by goals desc
	limit 10;


# most appearances