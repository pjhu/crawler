# local
pip install pyspider
pip install --egg mysql-connector-python-rf
pip install redis

drop database projectdb;
drop database taskdb;
drop database resultdb;
curl -XDELETE 10.202.129.165:9200/cars

# setup swarm

## create machine
docker-machine create --driver virtualbox manager1
docker-machine create --driver virtualbox worker1
docker-machine create --driver virtualbox worker2

## create swarm
docker-machine ssh manager1


```
docker@manager1:~$ docker swarm init --advertise-addr 192.168.99.101
Swarm initialized: current node (wpf2jcvhhvfosv3c9ac6c50dh) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-69wvyxsrnjtm11z38eus20tm0z9cof2ks9khzyv7fdo8it0dln-drdoszuykjp1uvhmn2spaa8vj \
    192.168.99.101:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

Run docker info to view the current state of the swarm:

```
$ docker info

Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 0
Server Version: 17.05.0-ce
Storage Driver: aufs
 Root Dir: /mnt/sda1/var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 0
 Dirperm1 Supported: true
 ...snip...
```

Run the docker node ls command to view information about nodes:
```
docker@manager1:~$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
wpf2jcvhhvfosv3c9ac6c50dh *   manager1            Ready               Active              Leader
```

# add nodes to swarm
Open a terminal and ssh into the machine where you want to run a worker node

```
docker@worker1:~$ docker swarm join \
>     --token SWMTKN-1-69wvyxsrnjtm11z38eus20tm0z9cof2ks9khzyv7fdo8it0dln-drdoszuykjp1uvhmn2spaa8vj \
>     192.168.99.101:2377
This node joined a swarm as a worker.


docker@worker2:~$ docker swarm join \
>     --token SWMTKN-1-69wvyxsrnjtm11z38eus20tm0z9cof2ks9khzyv7fdo8it0dln-drdoszuykjp1uvhmn2spaa8vj \
>     192.168.99.101:2377
This node joined a swarm as a worker.


docker@manager1:~$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
k926754fhudg5tu51rnlp2fdj     worker2             Ready               Active
q1seyrwugtdceqd515tmp8ph3     worker1             Ready               Active
wpf2jcvhhvfosv3c9ac6c50dh *   manager1            Ready               Active              Leader
```

# create network
docker network create --driver overlay

## scheduler
--taskdb "mysql+taskdb://root:root@mysql:3306/taskdb" --resultdb "mysql+resultdb://root:root@mysql:3306/resultdb" --projectdb "mysql+projectdb://root:root@mysql:3306/projectdb" --message-queue "redis://redis:6379/1"  scheduler --inqueue-limit 5000 --delete-time 43200

## fetch
--message-queue "redis://redis:6379/1" --phantomjs-proxy "phantomjs:80" fetcher --xmlrpc

## processor
--projectdb "mysql+projectdb://root:root@mysql:3306/projectdb" --message-queue "rredis://redis:6379/1" processor

## result-worker
--taskdb "mysql+taskdb://root:root@mysql:3306/taskdb" --resultdb "mysql+resultdb://root:root@mysql:3306/resultdb" --projectdb "mysql+projectdb://root:root@mysql:3306/projectdb" --message-queue "redis://redis:6379/1" result-worker


## webui
--taskdb "mysql+taskdb://root:root@mysql:3306/taskdb" --resultdb "mysql+resultdb://root:root@mysql:3306/resultdb" --projectdb "mysql+projectdb://root:root@mysql:3306/projectdb" --message-queue "redis://redis:6379/1" webui --max-rate 0.2 --max-burst 3 --scheduler-rpc "http://o4.i.binux.me:23333/" --fetcher-rpc "http://fetcher/"

# 部署
登陆manager1, 执行如下命令:
```
docker@manager1:~$ docker stack deploy -c docker-compose.yml myspider
```
