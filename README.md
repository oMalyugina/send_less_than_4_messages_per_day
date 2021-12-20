# 

There are 4 parts of my work in the repo:
1. jupyter notebooks for data analysis and model comparison
2. code to generate a csv file with sent messages
3. system to simulate generation and sending messages 
4. ideas to try, if I have more time

Repo doesn't contain datasets, so if you want to run it locally you need to download it.

## jupyter notebooks

#### Running locally

In order to run the python notebooks locally you need to install ```pandas``` and ```numpy```, and then run the notebook.
The following commands show how to do it:

```shell
python -m venv venv

. venv/bin/activate

pip install pandas numpy

TODO command to run notebook
```


#### visualization.ipynb

There is data visualization. 
I did it to understand data, not for demonstration purposes, so it isn't clean.

#### method_comparison.ipynb

I tried simple rule base approaches here.
There are statistics for train and test for different methods in the first cell
1. method1\
I collect all notifications for 6 hours and send them at 00:00, 6:00, 12:00, 18:00.
2. method2\
I compute quantiles for messages times and send notifications to users 4 times pro day at 00:00, 10:42, 14:21, 17:18
4. method4\
There is a lot of users who get less than 4 messages pro day.
I compute mean number of messages for every user. If this mean is less than 3 I send 3 first messages immediately.
If mean is more or equal than 3, I wait before I collect several messages for user and send them.
All unsent messages I send in the evening.

#### genarate_answer.ipynb
It is jupyter notebook to generate CSV file which contains all (bundled) notifications with method4. 

## code to generate a csv file with sent messages
It is python script ```generate_answer.py``` to generate CSV file which contains all (bundled) notifications with method4. 
You should install ```pandas``` and ```numpy``` to run script.

To execute a script you should run in terminal:
```shell
python generate_answer.py --source=path_to_your_csv_file --result=path_to_save_output
```
for example
```shell
python generate_answer.py --source="data/notifications.csv" --result="data/malyugina_output.csv"
```

## System to simulate generation and sending messages 

### Why I did it
After the implementation of a simple approach I started to think about a smarter solution.
There were some ideas I was not able to implement due to lack of time. They can be found at the end of this file.

This system simulates the process of sending, receiving, and delay computation.
It also demonstrates the possibility of creating services over the delay computation algorithms.

Unfortunately, this system took more time that I expected, so I had to stop with the current implementation
of time simulation and batches pulling.

### System overview
At the current moment it's implemented fo the method1 (send messages every 6 hours). 
But normally it can be extended for other methods by creating new Queue like classes 
(classes with the same public interface).

There are 3 services:
1. batcher\
this fastapi service gets all messages and should send them in batches depending on an approach
2. emmiter\
it is a simple python script which reads csv file and sends messages to batcher 
when simulation time is equal message's timestamp. 
3. collector\
it schedules task to send collected every 6 hours. 
Also, it prints delay stats for all sent messages.

The code of all 3 services is in ```src``` folder. `docker-compose.yml` and `Dockerfile` allow to run these service in docker.

To set up project define:
1. environment variable ```DATA``` for service `emitter` in ```docker-compose.yml```  - it is path to source csv file. 
It should be in ```data``` folder.
2. how many seconds of simulations time in one real second and when simulation time starts.
It is in ```src/emitter.py``` in lines 48-52. Line 51 says that there are 3 hours in one real second.
4. depending on the previous setting you can say how often you want to print all collected messages. 
It is in line 13 in ```src/collector.py```
It prints every 2 real seconds or every 6 hours of simulated time (by default).

### To run a simulation

```shell
docker-compose up --build
```
or
```shell
docker-compose up --build batcher
docker-compose up --build collector
docker-compose up --build emitter
```


### Ideas which I didn't implement
1. some users can send several messages during a small period of time
(for example user 014513DF37B10C0B1979C5B2A05E7B).
I think that it can be a good idea to wait a short time (20 min?) after generation first message and check, 
that there is only one message, not a batch.
2. It can be a good idea to predict, how many messages each user will send today.
With this information, we can get an estimation, how many messages should every follower get today
(it is just a sum of the estimated number for following by given user people).
Graph of followers could be reconstructed from given data.
3. We can create features for each day 
(day of the week, working/nonworking days, season, whether in particular day),
and train classifier to predict how many messages user will get today (or will send).
For example, if we know that user should get 10 messages today, we can batch every 3 messages together.
4. It can be a good idea to predict if a user will send messages on day and hour (using features in point 3).