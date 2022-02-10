"""
Core functionality for Simple-Chatwoot
"""

from typing import Dict
import json

import requests

from .utils import check_response

class ChatWoot:
    def __init__(self, 
                 domain:str, 
                 api_access_token:str, 
                 account_id:str, 
                 inbox_id:str,
                 ) -> None:

        """
        Initialize the instance with the given parameters.

        Arguments

        * api_access_token -- should be an administrators security token for the account
                              example: rkoo0op2PPsihsv8JW3IjfiF 
        * account_id -- numeric ID of the account
                        example: 1
        * inbox_id -- ID of the inbox
                      example: 1
        * domain -- domain to use for connecting to Chatwoot instance
                    example: https://chatwoot.example.com
        """

        self.domain = domain
        self.api_access_token = api_access_token
        self.account_id = account_id
        self.inbox_id = inbox_id
    
    def __repr__(self) -> str:
        return "ChatWoot Client for account {} & inbox {}".format(self.account_id, self.inbox_id)

    ### AGENT ###
    def create_agent(self):
        """
        Add a new Agent to Account
        """
        pass

    ### CONTACT ###
    def create_contact(self,
                    name:str, 
                    email:str, 
                    phone:str, 
                    identifier:str=None, 
                    custom_attributes:Dict={}
                    )->str:
        """
        Create a new Contact

        A Contact represents a Person in your chatwoot CRM. A contact can have conversations in multiple 
        inboxes via the Contact-Inbox relationship. The contact models helps to agregate 
        conversations from variaous inboxes belonging to a single identity.

        You need to have one contact in order to create conversations and messages, because conversation creation 
        uses source_id to tie the session and the messages together
        The output is the contact source_id. Example: 561f3286-a92e-4b59-ae1d-9301154313f1

        Arguments

        * name -- name of the contact
        * email -- email of the contact
        * phone -- phone number of the contact
        * identifier -- a unique identifier for the contact in external system
        * custom_attributes -- an object where you can store custom attributes for contact. 4
                               example: {"type":"customer", "age":30}
 
        """

        payload = {
            'inbox_id': self.inbox_id, 
            'name': name, 
            'email': email, 
            'phone_number': phone, 
            'identifier': identifier, 
            'custom_attributes':custom_attributes
        }
        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.post(self.domain+"/api/v1/accounts/"+self.account_id+"/contacts", 
                            data=json.dumps(payload),
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Contact Creation Failed")
        contact_source_id = str(json_response_dict['payload']['contact_inbox']['source_id'])

        return contact_source_id


    def search_contacts(self, search_key:str,page:str="1")->Dict:
        """
        Search the resolved contacts using a search key, currently supports email search (Page size = 15). 
        Resolved contacts are the ones with a value for identifier, email or phone number.

        Arguments

        * search_key -- can be contact name, identifier, email or phone number
        * page -- page number, default is 1
        """

        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/contacts/search?q="+search_key+"&page="+page, 
                            headers=headers)

        json_response_dict = check_response(response, 200, "Search Contact Failed")

        return json_response_dict

   
    ### CONVERSATION ###

    def create_conversation(self, 
                            contact_source_id:str,
                            contact_id:str=None,
                            assignee_id:str=None,
                            team_id:str=None,
                            additional_attributes:Dict={ },
                            status:str="open"
                            )->str:
        """
        Creating a conversation in chatwoot requires a source id.
        Learn more about source_id: https://github.com/chatwoot/chatwoot/wiki/Building-on-Top-of-Chatwoot:-Importing-Existing-Contacts-and-Creating-Conversations

        Arguments

        * contact_source_id -- source id could be the identifier hash in case of a webwidget, 
                               twitter_id in case of a twitter profile and email in case of email channel.
                               example: 561f3286-a92e-4b59-ae1d-9301154313f1
        * contact_id -- contact Id for which conversation is created
        * assignee_id -- agent Id for assigning a conversation to an agent
        * team_id -- team Id for assigning a conversation to a team
        * additional_attributes -- lets you specify attributes like browser information
        * status -- specify the conversation whether it's pending, open, closed
        """

        # Note: inbox_id is the Id of inbox in which the conversation is created
        # Allowed Inbox Types: Website, Phone, Api, Email

        payload = {
            'source_id': contact_source_id, 
            'inbox_id': self.inbox_id,
            'contact_id': contact_id,
            'additional_attributes': additional_attributes, 
            'status': status,
            'assignee_id':assignee_id,
            'team_id':team_id,
        }

        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.post(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations", 
                            data=json.dumps(payload),
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Message Creation Failed")
        conversation_id = str(json_response_dict['id'])

        return conversation_id

    def get_conversation_details(self, conversation_id:str)->Dict:
        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id, 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Get Conversation Details Failed")

        return json_response_dict
   
    ### MESSAGES ###

    def create_message(self,
                       conversation_id:str, 
                       message:str, 
                       message_type:str="incoming",
                       is_private:bool=False,
                      )->str:
        """
        Conversation is a numeric identification like 5670
        If using API inbox type, make sure your webhook server is up and running otherwise you'll get errors from it
        """

        payload = {
            'content': message, 
            'message_type': message_type, 
            'private': is_private, 
        }
        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.post(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id+"/messages", 
                            data=json.dumps(payload),
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Message Creation Failed")
        message_id = str(json_response_dict['id'])

        return message_id

    def list_messages(self, conversation_id:str)->Dict:
        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id+"/messages", 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "List Messages Failed")

        return json_response_dict


    ### INBOX ###

    def list_inboxes(self)->Dict:
        """
        List all inboxes available in the current account
        """
        headers = {'api_access_token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/inboxes", 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Message Creation Failed")

        return json_response_dict

