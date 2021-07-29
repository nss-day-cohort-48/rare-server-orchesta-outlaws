-- if you ran "rare-init.sql" then "steve-subs.sql",
--	this will return two posts
SELECT s.author_id,
	p.*
FROM Subscriptions s
	JOIN Posts p ON p.user_id = s.author_id
WHERE s.follower_id = 1;