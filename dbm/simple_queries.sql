SHOW databases;
USE dbm_project_db;
SHOW tables;

SELECT * FROM article_author_role_t;
SELECT * FROM article_category_t;
SELECT * FROM article_keyword_t;
SELECT * FROM articles_t;
SELECT * FROM authors_t;
SELECT * FROM categories_t;
SELECT * FROM companies_t;
SELECT * FROM keywords_t;
SELECT * FROM roles_t;


## How many articles are published every month?
SELECT YEAR(articles.datetime), MONTH(articles.datetime), COUNT(articles.id)
FROM articles_t articles
GROUP BY YEAR(articles.datetime), MONTH(articles.datetime);


## How many articles are published every month by Reuters?
CREATE OR REPLACE VIEW amount_articles_published_by_reuters_per_month_v as (
	SELECT concat(a.year, "-", a.month) as date, a.article_count
	FROM(
		SELECT YEAR(art.datetime) as year, MONTH(art.datetime) as month, COUNT(art.id) as article_count
		FROM articles_t art
		LEFT JOIN companies_t comp
			ON art.company_id = comp.id
		WHERE comp.name LIKE "Thompson and Reuters"
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
		ORDER BY YEAR(art.datetime) ASC, MONTH(art.datetime) ASC
	) AS a
);

SELECT * FROM amount_articles_published_by_reuters_per_month_v;
## Create table from view
DROP TABLE if exists amount_articles_published_by_reuters_per_month_t;
CREATE TABLE amount_articles_published_by_reuters_per_month_t as SELECT * FROM amount_articles_published_by_reuters_per_month_v;


## How many articles are published every month by Kyodo?
CREATE OR REPLACE VIEW amount_articles_published_by_kyodo_per_month_v as (
	SELECT concat(a.year, "-", a.month) as date, a.article_count
	FROM(
		SELECT YEAR(art.datetime) as year, MONTH(art.datetime) as month, COUNT(art.id) as article_count
		FROM articles_t art
		LEFT JOIN companies_t comp
			ON art.company_id = comp.id
		WHERE comp.name LIKE "Kyodo News"
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
		ORDER BY YEAR(art.datetime) ASC, MONTH(art.datetime) ASC
	) AS a
);

SELECT * FROM amount_articles_published_by_kyodo_per_month_v;
## Create table from view
DROP TABLE if exists amount_articles_published_by_kyodo_per_month_t;
CREATE TABLE amount_articles_published_by_kyodo_per_month_t as SELECT * FROM amount_articles_published_by_kyodo_per_month_v;


## In how many articles is Obama mentioned, grouped by month?
SELECT YEAR(articles.datetime), MONTH(articles.datetime), COUNT(articles.id)
FROM articles_t articles
WHERE articles.text LIKE "%Obama%"
GROUP BY YEAR(articles.datetime), MONTH(articles.datetime);


## Calculate the percentage of articles in which Obama was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_obama_v as (
	SELECT
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("% obama%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_obama_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_obama_t;
CREATE TABLE percentage_articles_mention_obama_t as SELECT * FROM percentage_articles_mention_obama_v;


## Calculate the percentage of articles in which Trump was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_trump_v as (
	SELECT
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("% trump%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_trump_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_trump_t;
CREATE TABLE percentage_articles_mention_trump_t as SELECT * FROM percentage_articles_mention_trump_v;


## Calculate the percentage of articles in which Biden was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_biden_v as (
	SELECT
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("% biden%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_biden_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_biden_t;
CREATE TABLE percentage_articles_mention_biden_t as SELECT * FROM percentage_articles_mention_biden_v;



## Calculate the percentage of articles in which Putin was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_putin_v as (
	SELECT
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("%putin%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_putin_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_putin_t;
CREATE TABLE percentage_articles_mention_putin_t as SELECT * FROM percentage_articles_mention_putin_v;



## Calculate the percentage of articles in which war was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_war_v as (
	SELECT
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("% war%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_war_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_war_t;
CREATE TABLE percentage_articles_mention_war_t as SELECT * FROM percentage_articles_mention_war_v;


## Calculate the percentage of articles in which climate was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_climate_v as (
	SELECT 
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("%climate%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_climate_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_climate_t;
CREATE TABLE percentage_articles_mention_climate_t as SELECT * FROM percentage_articles_mention_climate_v;


## Calculate the percentage of articles in which virus was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_virus_v as (
	SELECT 
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE ("%virus%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_virus_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_virus_t;
CREATE TABLE percentage_articles_mention_virus_t as SELECT * FROM percentage_articles_mention_virus_v;


## Calculate the percentage of articles in which bitcoin was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_bitcoin_v as (
	SELECT 
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE "%bitcoin%"
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_bitcoin_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_bitcoin_t;
CREATE TABLE percentage_articles_mention_bitcoin_t as SELECT * FROM percentage_articles_mention_bitcoin_v;


## Calculate the percentage of articles in which ether was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_ether_v as (
	SELECT 
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE "% ether%"
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_ether_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_ether_t;
CREATE TABLE percentage_articles_mention_ether_t as SELECT * FROM percentage_articles_mention_ether_v;


## Calculate the percentage of articles in which crypto was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_crypto_v as (
	SELECT 
		a.date, IFNULL(b.count, "0") / c.total_count as percent_articles
	FROM (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as a
	LEFT JOIN (
		SELECT art.id as id, concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as count
		FROM articles_t art
		WHERE LOWER(art.text) LIKE LOWER("%Crypto%")
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as b
	ON (a.date = b.date), (
		SELECT concat(YEAR(art.datetime), "-", MONTH(art.datetime)) as date, COUNT(art.id) as total_count
		FROM articles_t art
		GROUP BY YEAR(art.datetime), MONTH(art.datetime)
	) as c
	WHERE a.date=c.date
);

SELECT * FROM percentage_articles_mention_crypto_v;

## Create table from view
DROP TABLE if exists percentage_articles_mention_crypto_t;
CREATE TABLE percentage_articles_mention_crypto_t as SELECT * FROM percentage_articles_mention_crypto_v;









