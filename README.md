### Bet Maker

You've made it to the second app, congrats! 🎉

### Description
Bet maker allows users to place bets on events.
When placing a bet it considers things like deadline and event completeness.
Once an event changes status, the related bets also change their status.
Data is stored in Postgres database.

Bet Maker consumes events from the Line Provider via RabbitMQ.

### Requirements
Create .env and copy the contents of .env.example to it.

In the root directory, run:
```
make start
```
WARNING:
The command may ask for password to set perms to data directory.
This is required for the database and I've setup permission setting for linux systems.
Hope, you are fellow linux users cos idk how to do that stuff on Mac.

You can access swagger here, I've set the examples so that it would be easier to test.
http://127.0.0.1:8081/docs

### Considerations
There's some stuff I really wanted to do, but since it's a time-limited task,
I've decided to focus on the most important things.

Important notice:
I've worked with both FastAPI and Django, but I've always
made DB operations on Django ORM because we had only one DB in our setup
with plans to make separate DBs for each service later. So,
for this demo I had to learn a couple of things on the fly, which consumed
like 80% of the time. 

Just for you to make sure I'm aware of the limitations:
- I really wanted to set alembic for efficient DB migrations, but I've spent too much 
time on the mock db, so I decided to skip it. Hope you will let it slide this time 
(I haven't brought you croissants for no reason you know)
- When deleting an event, effects on bets are not handled. I know, I know.
I've decided to just leave it as is because there are plenty of other examples of 
event processing in Bet Maker.
- Haven't added pagination. Since it's tiny little app, I've decided to let it be
(Please, just don't use it in pord until it's fixed)
- Haven't tidied up logic. The project has good structure as is, but in 
a real setting it would have had an even better structure, I guess such things just don't
come out perfect in a 3-hour coding session.

### Tests
```
make test
```

I'm really proud of how I've handled mock DB. It's still a crude implementation,
but it does what @django_db does and I'm really happy with it.

### Shutdown
```
make stop
```

### Line provider
https://github.com/anatoly-rozhkov/anatoly-rozhkov-demo

### Finishing note
Looking forward to working with you. I've used to work in 3-backend-dev setup, 
so I'm really exited to see what tens of devs can do together.

Cheers,
Anatoly Rozhkov