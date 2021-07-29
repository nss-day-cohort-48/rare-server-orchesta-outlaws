-- if you ran "rare-init.sql" then "steve-subs.sql",
--	this will return two posts
SELECT s.author_id,
	p.*,
	c.label category_label
FROM Subscriptions s
	JOIN Posts p ON p.user_id = s.author_id
	JOIN Categories c ON p.category_id = c.id
WHERE s.follower_id = 1;