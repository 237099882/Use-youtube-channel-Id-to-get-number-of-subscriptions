
import os
import csv
import googleapiclient.discovery

def get_youtube_subscriber_count(api_key, channel_id):
    # Create a YouTube Data API client
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    try:
        # Get the subscriber count using the channel ID
        subscriber_request = youtube.channels().list(
            part='statistics',
            id=channel_id
        )
        subscriber_response = subscriber_request.execute()

        if subscriber_response['items']:
            subscriber_count = int(subscriber_response['items'][0]['statistics']['subscriberCount'])
            return subscriber_count
        else:
            print(f"No subscriber data found for channel with ID '{channel_id}'.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def update_csv_with_subscribers(api_key, csv_file_path):
    try:
        # Open the CSV file and create a list to hold updated rows
        updated_rows = []

        with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            updated_header = header + ['Subscriber Count']  # Append 'Subscriber Count' to header

            for row in csv_reader:
                if len(row) > 0:
                    channel_id = row[3].strip()  # Assuming channel ID is in the first column
                    subscriber_count = get_youtube_subscriber_count(api_key, channel_id)

                    if subscriber_count is not None:
                        # Append subscriber count to the current row
                        updated_row = row + [str(subscriber_count)]
                        updated_rows.append(updated_row)
                    else:
                        # If subscriber count retrieval fails, append empty string
                        updated_row = row + ['']
                        updated_rows.append(updated_row)

        # Write updated rows back to the CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(updated_header)  # Write updated header
            csv_writer.writerows(updated_rows)  # Write updated rows

        print(f"CSV file '{csv_file_path}' updated successfully.")

    except FileNotFoundError:
        print(f"CSV file '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while updating the CSV file: {e}")
def main():
    # Set your YouTube Data API key
    api_key = 'AIzaSyDw_uy6LDxaNCD39UCBZbtLcWU0bXOjdXo'

    # Path to the CSV file containing channel IDs (user IDs)
    csv_file_path = 'US_youtube_trending_data.csv'

    update_csv_with_subscribers(api_key, csv_file_path)

if __name__ == "__main__":
    main()

