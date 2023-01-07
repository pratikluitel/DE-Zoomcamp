locals { #locals are basically like a constant
  data_lake_bucket = "dtc_data_lake"
}

# variables are passed at runtime, there will be a prompt while doing terraform plan

variable "project" {
  description = "GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources"
  default     = "asia-south2" # it is good practice to choose the same region for all resources, because $$$$ cost for inter region communication
  type        = string
}

variable "bucket_name" {
  description = "Name of the GCS bucket, globally unique"
  # if the default argument is present in a variable, the value is optional
  # if default is not present, the argument is mandatory (like the above 2 variables)
  default = ""
}

variable "storage_class" {
  description = "Storage class for bucket. See GCS docs for more"
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "trips_data_all" # because new york taxi trips data
}

variable "TABLE_NAME" {
  description = "BigQuery Table"
  type        = string
  default     = "ny_trips"
}


