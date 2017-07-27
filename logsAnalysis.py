#! /usr/bin/env/ python2.7

import psycopg2

DBNAME = 'news'


# this function will return a list of top 3 popular articles
# with number of views they got
def top3_articles():
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()

    # get the top 3 articles
    query = "select * from top_articles limit 3"
    cur.execute(query)
    res = cur.fetchall()

    # reconstruct the output
    s = ' -- '
    re = [s.join((a, str(n) + " views")) for a, n in res]
    conn.close()
    return re


# this function will return a list of the popular authors with number
# of views their articles got ordered in a descending way
def top_authors():
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    query = "select * from top_authors"
    cur.execute(query)
    res = cur.fetchall()

    # reconstruct the output and store it in a list
    s = ' -- '
    re = [s.join((a, str(n) + " views")) for a, n in res]

    conn.close()
    return re


# this function will return a list of dates on which more than
# 1% request leads to errors
def dates_with_error():
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    query = """\
        select status_ok.time as date,
        (status_error.num::float / (status_error.num + status_ok.num)) as rate
        from status_ok left join status_error
        on status_error.time = status_ok.time
        where (status_error.num::float / (status_error.num + status_ok.num))
        > 0.01;
        """
    cur.execute(query)
    res = cur.fetchall()

    # reconstruct the output and sotre it in a list
    s = ' -- '
    re = [s.join((str(a), str(round(n * 100, 2)) + '% error')) for a, n in res]
    conn.close()
    return re


def main():
    print "\n"
    print "######################################################"
    print "Here list the top 3 popular articles from the database: "

    articles = top3_articles()
    for item in articles:
        print item

    print"\n"
    print "#####################################################"
    print "Here list the author rank from the database: "
    authors = top_authors()
    for item in authors:
        print item

    print "\n"
    print "#####################################################"
    print "Here list the dates with error more than 1% from the database: "
    error = dates_with_error()
    for item in error:
        print item


if __name__ == '__main__':
    main()
