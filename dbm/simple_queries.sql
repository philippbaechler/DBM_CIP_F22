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


## In how many articles is Obama mentioned, grouped by month?
SELECT YEAR(articles.datetime), MONTH(articles.datetime), COUNT(articles.id)
FROM articles_t articles
WHERE articles.text LIKE "%Obama%"
GROUP BY YEAR(articles.datetime), MONTH(articles.datetime);


## Calculate the percentage of articles in which Obama was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_obama_v as (
	SELECT 
		concat(a.year, "-", a.month) as date, (a.obama_count / b.total_count) as percent_articles 
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as obama_count
		FROM articles_t articles 
		WHERE articles.text LIKE "%Obama%" 
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count 
		FROM articles_t articles 
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_obama_v;


## Calculate the percentage of articles in which Trump was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_trump_v as (
	SELECT 
		concat(a.year, "-", a.month) as date, (a.trump_count / b.total_count) as percent_articles 
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as trump_count
		FROM articles_t articles 
		WHERE articles.text LIKE "%Trump%" 
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count 
		FROM articles_t articles 
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_trump_v;


## Calculate the percentage of articles in which Biden was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_biden_v as (
	SELECT
		concat(a.year, "-", a.month) as date, (a.biden_count / b.total_count) as percent_articles
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as biden_count
		FROM articles_t articles
		WHERE articles.text LIKE "%Biden%"
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count
		FROM articles_t articles
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_biden_v;


## Calculate the percentage of articles in which Putin was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_putin_v as (
	SELECT
		concat(a.year, "-", a.month) as date, (a.putin_count / b.total_count) as percent_articles
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as putin_count
		FROM articles_t articles
		WHERE articles.text LIKE "%Putin%"
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count
		FROM articles_t articles
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_putin_v;


## Calculate the percentage of articles in which war was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_war_v as (
	SELECT
		concat(a.year, "-", a.month) as date, (a.war_count / b.total_count) as percent_articles
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as war_count
		FROM articles_t articles
		WHERE articles.text LIKE "%war%"
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count
		FROM articles_t articles
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_war_v;


## Calculate the percentage of articles in which climate was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_climate_v as (
	SELECT
		concat(a.year, "-", a.month) as date, (a.climate_count / b.total_count) as percent_articles
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as climate_count
		FROM articles_t articles
		WHERE articles.text LIKE "%climate%"
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count
		FROM articles_t articles
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_climate_v;


## Calculate the percentage of articles in which virus was mentioned.
CREATE OR REPLACE VIEW percentage_articles_mention_virus_v as (
	SELECT
		concat(a.year, "-", a.month) as date, (a.virus_count / b.total_count) as percent_articles
	FROM (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as virus_count
		FROM articles_t articles
		WHERE articles.text LIKE "%virus%"
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS a, (
		SELECT YEAR(articles.datetime) as year, MONTH(articles.datetime) as month, COUNT(articles.id) as total_count
		FROM articles_t articles
		GROUP BY YEAR(articles.datetime), MONTH(articles.datetime)
	) AS b
	WHERE a.year = b.year AND a.month = b.month
);

SELECT * FROM percentage_articles_mention_virus_v;



