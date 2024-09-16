# Usage
1. Run the setup_bigquery.sh script to setup the bigquery dataset and tables. Make sure to enter the variables at the top of the script.
2. Create a new service account and give it the "BigQuery Data Editor" role.
3. Deploy the cloud function using the deploy_function.sh script. Make sure to enter the variables at the top of the script.
4. Copy the webhook url from the cloud function console and paste it into the Vero webhook settings.


