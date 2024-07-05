import requests
import json
from datetime import datetime

# Set your Azure DevOps organization, project, and PAT
organization = 'your_organization'
project = 'your_project'
pat = 'your_personal_access_token'

# Set the saved query ID
query_id = 'your_saved_query_id'

# Set the API version
api_version = '6.0'

# Create a session and set the authorization headers
session = requests.Session()
session.auth = ('', pat)

def get_work_items_from_query(query_id):
    query_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql/{query_id}?api-version={api_version}"
    response = session.get(query_url)
    response.raise_for_status()
    work_items = response.json()['workItems']
    return [item['id'] for item in work_items]

def get_work_item_details(work_item_ids):
    ids = ','.join(map(str, work_item_ids))
    work_items_url = f"https://dev.azure.com/{organization}/_apis/wit/workitems?ids={ids}&api-version={api_version}&$expand=all"
    response = session.get(work_items_url)
    response.raise_for_status()
    return response.json()['value']

def calculate_time_in_states(work_item):
    history_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{work_item['id']}/updates?api-version={api_version}"
    response = session.get(history_url)
    response.raise_for_status()
    updates = response.json()['value']

    state_times = {}
    current_state = None
    current_state_start = None

    for update in updates:
        fields = update.get('fields', {})
        state_change = fields.get('System.State')
        
        if state_change:
            new_state = state_change.get('newValue')
            changed_date = datetime.strptime(update['revisedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

            if current_state:
                if current_state not in state_times:
                    state_times[current_state] = 0
                time_in_state = (changed_date - current_state_start).total_seconds()
                state_times[current_state] += time_in_state

            current_state = new_state
            current_state_start = changed_date

    # Capture time in the last state
    if current_state and current_state_start:
        time_in_state = (datetime.utcnow() - current_state_start).total_seconds()
        if current_state not in state_times:
            state_times[current_state] = 0
        state_times[current_state] += time_in_state

    return state_times

def main():
    work_item_ids = get_work_items_from_query(query_id)
    work_items = get_work_item_details(work_item_ids)
    
    for work_item in work_items:
        print(f"Work Item ID: {work_item['id']}")
        state_times = calculate_time_in_states(work_item)
        for state, time in state_times.items():
            print(f" - {state}: {time / 3600:.2f} hours")

if __name__ == "__main__":
    main()