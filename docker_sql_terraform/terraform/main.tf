terraform {
  required_version = ">= 1.0"
  backend "local" {} # this can be a google cloud storage location or s3 bucket location in actual prod
  required_providers {
    google = {
      source = "hashicorp/google" # this is where we declare the provider, 
    }                             # each provider has different resource definitions, data sources (e.g. google's bucket is GCS vs aws is s3),
  }                               # this provides access to underlying resources and their functions
}                                 # kind of like importing a library in programming languages

# var - are values coming from the variables.tf fi,e
provider "google" {
  project = var.project
  region  = var.region
  // credentials = file(var.credentials) we can pass credientials explicitly here as a file param, but since we have the env var for credentials implemented, that's not needed 
}

# google cloud storage bucket definition, the params are inside the curly braces
# this definition has been yanked from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

# a resource is a physical component - a server, bucket, warehouse etc
# the arguments in these blocks configure the resource
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}"
  location = var.region

  storage_class = var.storage_class

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }

  force_destroy = true
}

# data warehouse
# yanked from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}
