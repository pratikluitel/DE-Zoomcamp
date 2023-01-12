## Assignment

## Question 1. Google Cloud SDK

Install Google Cloud SDK. What's the version you have? 

To get the version, run `gcloud --version`

> v 410.0.0

## Google Cloud account 

Create an account in Google Cloud and create a project.

> Done


## Question 2. Terraform 

Now install terraform and go to the terraform directory (`week_1_basics_n_setup/1_terraform_gcp/terraform`)

After that, run

* `terraform init`
* `terraform plan`
* `terraform apply` 

Apply the plan and copy the output (after running `apply`) to the form.

It should be the entire output - from the moment you typed `terraform init` to the very end.

> Done

## Prepare Postgres 

Run Postgres and load data as shown in the videos

We'll use the yellow taxi trips from January 2021:

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

You will also need the dataset with zones:

```bash 
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it to Postgres

> Done

## Question 3. Count records 

How many taxi trips were there on January 15?

Consider only trips that started on January 15.

> 53024
> Query: `
```sql
select count(*) from yellow_taxi_trips 
    where extract(month from tpep_pickup_datetime)=1 
    and extract(day from tpep_pickup_datetime)=15;
```

## Question 4. Largest tip for each day

Find the largest tip for each day. 
On which day it was the largest tip in January?

Use the pick up time for your calculations.

(note: it's not a typo, it's "tip", not "trip")

> Largest tip for each day:
```sql
with t as (
    select extract(year from tpep_pickup_datetime) as year, 
        extract(month from tpep_pickup_datetime) as month, 
        extract(day from tpep_pickup_datetime) as day, 
        tip_amount 
    from yellow_taxi_trips
) 
select year, month, day, max(tip_amount) 
from t 
group by year, month, day 
order by 4 desc;
```
> Max Jan tip: 1140.44, day: 1-20


## Question 5. Most popular destination

What was the most popular destination for passengers picked up 
in central park on January 14?

Use the pick up time for your calculations.

Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown" 

> Query to list all places with count in descending order
```sql
with t as (
    select "DOLocationID", count(*) 
    from yellow_taxi_trips 
    where extract(month from tpep_pickup_datetime) = 1 
        and extract(day from tpep_pickup_datetime)=14 
        and "PULocationID" =43
    group by "DOLocationID"
) 
select * from t 
order by count desc;
```
> Zone ID = 237,
> Zone Name: Upper East Side South

## Question 6. Most expensive locations

What's the pickup-dropoff pair with the largest 
average price for a ride (calculated based on `total_amount`)?

Enter two zone names separated by a slash

For example:

"Jamaica Bay / Clinton East"

If any of the zone names are unknown (missing), write "Unknown". For example, "Unknown / Clinton East". 

> Alphabet City / Unknown, amount: 2292.4


## Submitting the solutions

* Form for submitting: https://forms.gle/yGQrkgRdVbiFs8Vd7
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Wednesday), 22:00 CET


## Solution

Here is the solution to questions 3-6: [video](https://www.youtube.com/watch?v=HxHqH2ARfxM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)