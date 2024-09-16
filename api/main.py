import functions_framework
from google.cloud import bigquery
import os
from datetime import datetime, timezone

@functions_framework.http
def vero_webhook_handler(request):
    # Get environment variables
    project_id = os.environ.get('PROJECT_ID')
    dataset = os.environ.get('DATASET')
    table = os.environ.get('TABLE')

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Get the JSON data from the request
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return 'No JSON data received', 400

    # Map the request to the BigQuery schema
    row_to_insert = {
        'event_timestamp': get_event_timestamp(request_json),
        'type': request_json.get('type'),
        'user_id': str(request_json.get('user', {}).get('id')),
        'user_email': request_json.get('user', {}).get('email'),
        'bounce_type': request_json.get('bounce_type'),
        'message_id': request_json.get('message_id'),
        'user_agent': request_json.get('user_agent'),
        'created_at': datetime.now(timezone.utc).isoformat()
    }

    # Add flattened campaign data
    campaign_data = get_campaign_data(request_json)
    row_to_insert.update({
        'campaign_id': campaign_data.get('id'),
        'campaign_type': campaign_data.get('campaign_type'),
        'campaign_name': campaign_data.get('name'),
        'campaign_group': campaign_data.get('group'),
        'campaign_channel': campaign_data.get('channel'),
        'campaign_subject': campaign_data.get('subject'),
        'campaign_trigger_event': campaign_data.get('trigger_event'),
        'campaign_permalink': campaign_data.get('permalink'),
        'campaign_sent_to': campaign_data.get('sent_to'),
        'campaign_variation': campaign_data.get('variation'),
        'campaign_locale': campaign_data.get('locale'),
        'campaign_series_title': campaign_data.get('series_title'),
        'campaign_template': campaign_data.get('template'),
        'campaign_tags': campaign_data.get('tags')
    })

    # Insert the data into BigQuery
    table_ref = client.dataset(dataset).table(table)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if errors:
        return f'Error inserting rows: {errors}', 500
    else:
        return 'Data inserted successfully', 200

def get_event_timestamp(data):
    timestamp_fields = ['sent_at', 'delivered_at', 'opened_at', 'clicked_at', 'bounced_at', 'unsubscribed_at']
    for field in timestamp_fields:
        if field in data:
            return datetime.fromtimestamp(data[field], tz=timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()

def get_campaign_data(data):
    campaign = data.get('campaign', {})
    return {
        'id': campaign.get('id'),
        'campaign_type': campaign.get('type'),
        'name': campaign.get('name') or campaign.get('campaign_title'),
        'group': campaign.get('group'),
        'channel': campaign.get('channel'),
        'subject': campaign.get('subject') or campaign.get('email_subject'),
        'trigger_event': campaign.get('trigger-event'),
        'permalink': campaign.get('permalink'),
        'sent_to': campaign.get('sent_to'),
        'variation': campaign.get('variation') or campaign.get('variation_name'),
        'locale': campaign.get('locale'),
        'series_title': campaign.get('series_title'),
        'template': campaign.get('template'),
        'tags': campaign.get('tags')
    }