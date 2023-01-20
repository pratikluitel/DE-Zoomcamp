
## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```
Now run the command to get help on the "docker build" command
Which tag has the following text? - *Write the image ID to the file* 

**Ans:**
- `--iidfile string`

**Command:**
```sh
docker build --help
```

## Question 2. Understanding docker first run 
Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

**Ans:**
- 3

**Command:**
```sh
docker run -it python:3.9 /bin/bash
``` 
and
```sh
pip list
```

## Question 3. Count records 
How many taxi trips were totally made on January 15?
Tip: started and finished on 2019-01-15. 
Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

**Ans:**
- 20689

**Query:**
```sql
select count(*) from green_taxi_2019_01 
where lpep_pickup_datetime::date == '2019-01-15';
```

## Question 4. Largest trip for each day
Which was the day with the largest trip distance
Use the pick up time for your calculations.

**Ans:**
- 2019-01-15

**Query:**
```sql
select lpep_pickup_datetime, sum(trip_distance) 
    from green_taxi_2019_01 
    group by lpep_pickup_datetime 
    order by sum(trip_distance) desc
    limit 1
```

## Question 5. The number of passengers
In 2019-01-01 how many trips had 2 and 3 passengers?

**Ans:**
- 2: 1282 ; 3: 254

**Query:**
```sql
select passenger_count, count(*) 
    from green_taxi_2019_01
    where lpep_pickup_datetime::date = '2019-01-01' 
        and passenger_count in (2,3) 
    group by passenger_count;
```

## Question 6. Largest tip
For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.
Note: it's not a typo, it's `tip` , not `trip`

**Ans:**

- Long Island City/Queens Plaza

**Query:**

```sql
with t1 as (
        select "DOLocationID", "PULocationID", tip_amount 
        from green_taxi_2019_01 gt
    ), 
    t2 as (
        select "Zone" as puzone, "DOLocationID", tip_amount 
        from t1 join taxi_zone_lookup 
            on t1."PULocationID" = taxi_zone_lookup."LocationID" 
        where "Zone" ilike '%Astoria%'
    ), 
    t3 as (
        select "DOLocationID", tip_amount 
        from t2 
        order by tip_amount desc 
        limit 1
    ) 
select "Zone", tip_amount 
from t3 join taxi_zone_lookup 
    on t3."DOLocationID" = taxi_zone_lookup."LocationID";
```