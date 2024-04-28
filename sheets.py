from googleapiclient.discovery import build

# Function to update the Google Spreadsheet
def update_spreadsheet(data, token):
    # Create a service object for the Google Sheets API
    service = build('sheets', 'v4', credentials=token)
    spreadsheet_id = get_or_create_sheet('FluentMind', service)

    # Set the range for the update
    range_ = "Sheet1"

    # Create the value range object
    value_range_body = {
        "values": [data]
    }

    # Call the Sheets API
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_, 
        valueInputOption='RAW', 
        body=value_range_body
    )

    # Execute the request
    response = request.execute()
    return response

def get_or_create_sheet(sheet_name, service):
    # Get a list of all spreadsheets
    spreadsheet_list = service.spreadsheets().get().execute().get('files', [])

    # Check if the desired sheet exists
    for sheet in spreadsheet_list:
        if sheet.get('name') == sheet_name:
            return sheet.get('id')
    
    # If the sheet doesn't exist, create it
    spreadsheet = {
        'properties': {
            'title': sheet_name
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
    return spreadsheet.get('spreadsheetId')
