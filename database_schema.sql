CREATE TABLE IF NOT EXISTS ASSIGNMENTS (
	id				integer		primary key,
	course			text,
	assignment_name	text,
	due_date		text,
	submitted		integer,
	in_trello		integer		DEFAULT 0,
	trello_card_id	text,
	sync_needed		integer		DEFAULT 1,
	assignment_link text		DEFAULT ''
	);
