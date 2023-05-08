"""
Core functionality for Simple-Chatwoot
"""

from typing import Dict
import json

import requests

from .utils import check_response

class ChatWoot:
    """
        Initialize the instance with the given parameters.

        Arguments

        * param api_access_token -- should be an administrators security token for the account, example: rkoo0op2PPsihsv8JW3IjfiF
        * param account_id -- numeric ID of the account, example: 1
        * param inbox_id -- ID of the inbox, example: 1
        * param domain -- domain to use for connecting to Chatwoot instance, example: https://chatwoot.example.com
    
    """

    def __init__(self, 
                 domain:str, 
                 api_access_token:str, 
                 account_id:str, 
                 inbox_id:str,
                 ) -> None:

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

        # Not implemented yet. Here for documentation purposes.
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
        * custom_attributes -- an object where you can store custom attributes for contact, example: {"type":"customer", "age":30}
 
        """

        payload = {
            'inbox_id': self.inbox_id, 
            'name': name, 
            'email': email, 
            'phone_number': phone, 
            'identifier': identifier, 
            'custom_attributes':custom_attributes
        }
        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
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

        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
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
                            status:str="open",
                            **kargs
                            )->str:
        """
        Creating a conversation in chatwoot requires a source id.
        Learn more about source_id: https://github.com/chatwoot/chatwoot/wiki/Building-on-Top-of-Chatwoot:-Importing-Existing-Contacts-and-Creating-Conversations

        Arguments

        * contact_source_id -- source id could be the identifier hash in case of a webwidget, twitter_id in case of a twitter profile and email in case of email channel, example: 561f3286-a92e-4b59-ae1d-9301154313f1
        * contact_id -- contact Id for which conversation is created
        * assignee_id -- agent Id for assigning a conversation to an agent
        * team_id -- team Id for assigning a conversation to a team
        * additional_attributes -- lets you specify attributes like browser information
        * status -- specify the conversation whether it's pending, open, closed
        * kargs -- additional named arguments
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

        # If user sends other arguments, update payload
        payload.update(dict(kargs))

        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.post(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations", 
                            data=json.dumps(payload),
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Conversation Creation Failed")
        conversation_id = str(json_response_dict['id'])

        return conversation_id

    def get_conversation_details(self, conversation_id:str)->Dict:
        """
        Get all details regarding a conversation with all messages in the conversation
        
        Arguments

        * conversation_id -- numeric ID of the conversation
        """
        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id, 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Get Conversation Details Failed")

        return json_response_dict
   
    ### MESSAGES ###

    def create_message(self,
                       conversation_id:str, 
                       content:str, 
                       message_type:str="incoming",
                       is_private:bool=False,
                      )->str:
        """
        Conversation is a numeric identification like 5670
        If using API inbox type, make sure your webhook server is up and running otherwise you'll get errors from it
        
        Arguments

        * conversation_id -- numeric ID of the conversation
        * content -- content of the message
        * message_type -- weather it's "outgoing" or "incoming"
        * is_private -- flag to identify if it is a private note        
        """

        payload = {
            'content': content, 
            'message_type': message_type, 
            'private': is_private, 
        }
        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.post(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id+"/messages", 
                            data=json.dumps(payload),
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Message Creation Failed")
        message_id = str(json_response_dict['id'])

        return message_id

    def list_messages(self, conversation_id:str)->Dict:
        """
        List all messages of a conversation
        
        Arguments

        * conversation_id -- numeric ID of the conversation
        """
        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/conversations/"+conversation_id+"/messages", 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "List Messages Failed")

        return json_response_dict


    ### INBOX ###

    def list_inboxes(self)->Dict:
        """
        List all inboxes available in the current account
        """
        headers = {'api-access-token': self.api_access_token, 'Content-type': 'application/json'}
        response = requests.get(self.domain+"/api/v1/accounts/"+self.account_id+"/inboxes", 
                            headers=headers)
        
        json_response_dict = check_response(response, 200, "Message Creation Failed")

        return json_response_dict
