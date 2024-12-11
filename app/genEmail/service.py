from app.config import get_settings
import json, re
import openai
import requests
import logging
import requests
from msal import ConfidentialClientApplication
import pandas as pd
from .extract_content import extract_email_content

logger = logging.getLogger()
config = get_settings()


class EmailService:
    @staticmethod
    async def email_response(clientid, emailid):

        clientid = str(clientid)
        # Replace with your API key
        openai.api_key = config.gpt_api_key
        # Load the JSON file
        with open('app/data/message_list.json', 'r') as file:
            email_data = json.load(file)

        # Extract sender name
        sender_name = email_data['sender'][clientid]
        if sender_name == "Unknown Sender":
            sender_name = ""  # Leave blank if unknown

        prompt = f"""
        You are highly skilled in crafting professional and polite email responses. Based on the provided email, draft a clear and concise reply.Start the response with a polite salutation such as 'Dear [Name],' or 'Hello,' followed by the main content paragraph. Ensure the response is professional and excludes any signature or closing phrase or additional niceties such as best regeads ETC, as these are typically pre-added in most email systems. .

        Email Subject: {email_data['subject'][clientid]}
        Email Body: {email_data['body'][clientid]}
        Sender Name: {sender_name}

        Draft a reply:
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in drafting professional email responses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        generated_response = response['choices'][0]['message']['content']


        # Prepare the response data to save
        response_data = {
            "subject": email_data['subject'][clientid],
            "body": email_data['body'][clientid],
            "response": generated_response,
            "sender": sender_name,
        }

        df = pd.DataFrame(response_data, index=[0])
        # Save the email details to a JSON file
        df.to_json('app/data/response_email.json', index=False)

        # Extract the AI-generated response
        

        return generated_response


    @staticmethod
    async def specific_email(clientid):

        clientid = clientid - 1
        # Initialize MSAL app
        subject_list = []
        body_list = []
        sender_list = []
        message_dict = {}

        # Initialize MSAL app
        app = ConfidentialClientApplication(
            client_id=config.client_id,
            authority=f"https://login.microsoftonline.com/{config.tenant_id}",
            client_credential=config.client_secret,
        )

        # Acquire token
        token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        if "access_token" in token_response:
            access_token = token_response["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            user_email = config.user_email  # Replace with the user's email
            # Use $top=1 and $skip=2 to fetch only the 3rd email
            messages_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages?$top=1&$skip={clientid}"

            # Fetch the specific email
            messages_response = requests.get(messages_url, headers=headers)

            if messages_response.status_code == 200:
                response_data = messages_response.json()
                messages = response_data.get("value", [])

                # Extract and store details of the specific email
                if messages:
                    message = messages[0]
                    subject = message.get("subject", "No Subject")
                    subject_list.append(subject)
                    body = message.get("body", {}).get("content", "No Body")
                    body_content = extract_email_content(body)  # Extract plain text from HTML
                    body_list.append(body_content)
                    sender = message.get("from", {}).get("emailAddress", {}).get("address", "Unknown Sender")
                    sender_list.append(sender)

                    # Create a DataFrame for the single email
                    message_dict['subject'] = subject_list
                    message_dict['body'] = body_list
                    message_dict['sender'] = sender_list
                    df = pd.DataFrame(message_dict)

                    # Save the email details to a JSON file
                    df.to_json('app/data/specific_email.json', index=False)

                    print("Specific email JSON file has been created successfully.")
                    return (df)
                else:
                    return("No email found at the specified position.")
            else:
                return(f"Failed to fetch the email: {messages_response.json()}")

        else:
            print(f"Error acquiring token: {token_response.get('error_description')}")



    @staticmethod
    async def email_list():

        subject_list = []
        body_list = []
        sender_list = []
        message_dict = {}

        # Initialize MSAL app
        app = ConfidentialClientApplication(
            client_id = config.client_id,
            authority = f"https://login.microsoftonline.com/{config.tenant_id}",
            client_credential = config.client_secret,
        )

        # Acquire token
        token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        if "access_token" in token_response:
            access_token = token_response["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            user_email = config.user_email  # Replace with the user's email
            messages_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages?$top=50"

            all_subjects = []  # List to store all message subjects

            while messages_url:
                messages_response = requests.get(messages_url, headers=headers)

                if messages_response.status_code == 200:
                    response_data = messages_response.json()
                    messages = response_data.get("value", [])

                    # Extract and store subjects
                    for message in messages:
                        subject = message.get("subject", "No Subject")
                        subject_list.append(subject)
                        body = message.get("body", "No Body")
                        body_content = extract_email_content(body['content'])
                        body_list.append(body_content)
                        sender = message.get("from", {}).get("emailAddress", {}).get("address", "Unknown Sender")
                        sender_list.append(sender)

                    # Get the nextLink if present
                    messages_url = response_data.get("@odata.nextLink", None)
                else:
                    print(f"Failed to fetch messages: {messages_response.json()}")
                    break

        else:
            print(f"Error acquiring token: {token_response.get('error_description')}")

        # print(message_list)

        # df = pd.DataFrame([subject_list, body_list], columns=['Subject', 'Body'])
        message_dict['subject'] = subject_list
        message_dict['body'] = body_list
        message_dict['sender'] = sender_list
        df = pd.DataFrame(message_dict)
        # df = pd.DataFrame(response_data, index=[0])
        df.index = df.index + 1 
        df.to_json('app/data/message_list.json', index=True)

        print("JSON file has been created successfully.")

        return df


