## Udacity - Full Stack Nanodegree
### Project 3 - Logs Analysis
### About this project
This project requires building an internal reporting tool that will use information from the sql database to discover what kind of articles the site's readers like. The user-facing newspaper site frontend itself, and the database behind it, are already built and running.

The database contains details about newspaper articles, authors as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The program will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

### How to run?
#### Software requirements
* [Python3](https://www.python.org/downloads/)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/)

#### Setup Project
##### 1. Check python3 is installed
```
$ python3
```
or
```
$ python -version
```

##### 2. check virtualbox and vagrant are installed
```
$ vagrant --version
```

```
$ virtualbox --version
```

##### 3. download VM configuration
You can download and unzip this file: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.
Unzip the folder and if necessary move it to the convenient location.

##### 4. Launch VM
cd to the FSND-Virtual-Machine folder where ever it is located. Then running following commands in sequence;
```
$ cd vagrant
```

```
$ vagrant up
```

```
$ vagrant ssh
```

```
vagrant@vagrant:~$ cd /vagrant
```

Running "ls" command will provide a mirror/virtual image of files located within vagrant folder located on the hard drive.

##### 5. download and link with log data
download [newspapers.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) file, unzip it and move it to the vagrant folder.

```
/vagrant$ psql -d news -f newsdata.sql
```

```
/vagrant$ psql news
```

Your command line will probably look like following

```
news=>
```
The database contains three tables
* authors - provides details about the authors of the articles.
* articles - provides details about articles and the author of each article.
* log - provides details of all the visits to each article page on the website.

##### 6. Create view tables

i. author details

```
CREATE VIEW author_details AS SELECT authors.id, authors.name, articles.title, articles.slug FROM authors JOIN articles ON authors.id = articles.author;
```
ii. log count
```
CREATE VIEW log_count AS SELECT log.path, count(*) AS count FROM log GROUP BY log.path ORDER BY (count(*)) DESC;
```

iii. top articles
```
CREATE VIEW top_articles AS SELECT a.name, a.title, b.count as total FROM author_details AS a JOIN log_count AS b ON b.path = CONCAT('/article/', a.slug);
```

iv. top authors
```
CREATE VIEW top_authors AS SELECT a.name, sum(b.count) as total FROM author_details AS a JOIN log_count AS b ON b.path = CONCAT('/article/', a.slug) GROUP BY a.name ORDER BY total desc;
```

v. daily log views
```
CREATE VIEW log_view_total AS SELECT date(time) AS date1, count(*) AS total_view FROM log GROUP BY date(time);
```

vi. daily error views
```
CREATE VIEW log_view_error AS SELECT date(time) AS date2, count(*) AS error_view FROM log WHERE status = '404 NOT FOUND' GROUP BY date(time);
```

vii. error rate
```
CREATE VIEW log_view_final AS SELECT date1 AS date, ROUND((100.0*error_view/total_view),3) AS error_percent FROM log_view_total JOIN log_view_error ON date1 = date2;
```
