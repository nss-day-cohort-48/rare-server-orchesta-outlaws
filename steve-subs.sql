-- create some users with posts for Steve to sub to
-- using https://picsum.photos/ for the avatars
-- user johnny has 1 post
INSERT INTO Users
VALUES (
		100,
		'Johnny',
		'John',
		'johnny@john.com',
		'I ALSO love to talk about crafting code!',
		'johnny',
		'john',
		'https://picsum.photos/200',
		"20210729",
		1
	);
INSERT INTO Posts
VALUES(
		null,
		100,
		1,
		"Call me John: the Johnny John Story",
		"20210729",
		"https://picsum.photos/400",
		"It all started with a bang... the big bang.",
		1
	);
-- user patricia has 1 post
INSERT INTO Users 
VALUES (
		101,
		'Patricia',
		'Pattinson',
		'patricia@pattinson.com',
		"I SOMETIMES love to talk about crafting code!",
		'patricia',
		'pattinson',
		'https://picsum.photos/200',
		"20210729",
		1
	);
INSERT INTO Posts
VALUES(
		null,
		101,
		1,
		"My thoughts...",
		20210729,
		"https://picsum.photos/400",
		"The industrial revolution and its consequences have been a disaster for the human race.",
		1
	);
-- user marty has 1 post
VALUES (
		102,
		'Marty',
		'McBye',
		'marty@mcbye.com',
		"I NEVER love to talk about crafting code!",
		'marty',
		'mcbye',
		'https://picsum.photos/200',
		"20210729",
		1
	);
INSERT INTO Posts
VALUES(
		null,
		102,
		1,
		"Bah Humbug",
		"20210729",
		"https://picsum.photos/400",
		"I hate the new Facebook layout!!!!",
		1
	);
-- make steve follow johhny
INSERT INTO Subscriptions VALUES(null, 1, 101, "20210729");
-- make steve follow patricia
INSERT INTO Subscriptions VALUES(null, 1, 100, "20210729");