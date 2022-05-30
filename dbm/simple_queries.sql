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


## In how many articles is Obama mentioned, grouped by month?
SELECT YEAR(articles.datetime), MONTH(articles.datetime), COUNT(articles.id)
FROM articles_t articles
WHERE articles.text LIKE "%Obama%"
GROUP BY YEAR(articles.datetime), MONTH(articles.datetime);


## Calculate the percentage of articles in which Obama was mentioned.
SELECT 
	(a.obama_count / b.total_count) as final_count 
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
WHERE a.year = b.year AND a.month = b.month;


## Calculate the percentage of articles in which Trump was mentioned.
SELECT 
	(a.trump_count / b.total_count) as final_count 
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
WHERE a.year = b.year AND a.month = b.month;


## Calculate the percentage of articles in which Biden was mentioned.
SELECT 
	concat(a.year, "-", a.month), (a.biden_count / b.total_count) as final_count 
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
WHERE a.year = b.year AND a.month = b.month;



