#######################################

Introduction:
	This is a reporting analysis application written in python and used to extract informations from the postgresql database, 
	information could be extracted from the database are:
		The top 3 popular articles based on the number of views the articles got
		The rank of the authors based on the number of views their articles got
		The dates on which more than 1% of the request leads to an error

	Library used: psycopg2
	Python version: 2.7



######################################

Contents:
	logsAnalysis.py
	README.md


######################################

How to run the application?
	First create views (listed at the end of the file) in the database
	Then in the command line of Linuc or Mac run: python logsAnalysis.py



######################################
views created in the database:

create view top_articles as 
	select title, count(*) as num 
	from articles 
	join log on ('/article/' || articles.slug = log.path) 
	group by title 
	order by num DESC;

create view top_authors as 
	select authors.name, SUM(top_articles.num) as nums 
	from articles 
	join top_articles on articles.title = top_articles.title 
	join authors on authors.id = articles.author 
	group by authors.name 
	order by nums DESC;



create view status_ok as
	select time::date, count(*) as num 
	from log where status = '200 OK' 
	group by time::date;


create view status_error as
	select time::date, count(*) as num 
	from log where status != '200 OK' 
	group by time::date;

