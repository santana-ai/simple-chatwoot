# Simple Chatwoot

Simple-Chatwoot is a Python library for connecting to Chatwoot REST API.

## Usage

```python
import os
from dotenv import load_dotenv

from simple_chatwoot import ChatWoot

load_dotenv()

DOMAIN = os.getenv("DOMAIN") #https://chatwoot.example.com
API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN") #rkoo0op2PPsihsv8JW3IjfiF
ACCOUNT_ID = os.getenv("ACCOUNT_ID") #1
INBOX_ID = os.getenv("INBOX_ID") #1

chatwoot_client = ChatWoot(DOMAIN, API_ACCESS_TOKEN, ACCOUNT_ID, INBOX_ID)

contacts = chatwoot_client.search_contacts("henrique")
print(contacts)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

