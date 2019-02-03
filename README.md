# Chatbot API

## Installation steps:
Under Construction


### Dummy API for chatting
dummy api hosted at http://13.233.158.98:8888/chat/  

usage:  
send a post request to http://13.233.158.98:8888/chat/ containing data as  
question="user query"

[sample usage using ajax in js](demo_ui/testAPI_Javascript.php)  

[sample usage using ajax in jquery](demo_ui/testApiJQuery.php) 


### Dummy API for paragraph
hosted at http://13.233.158.98:8888/para/  

send a GET request to get the paragraph from the database  
Response ⇒ "paragraph_text"

To update the paragraph, send a POST request with data as:  
"paragraph=paragraph_text"
Response ⇒ "updated_paragraph_text"
 

### Dummy API hosted for Key, Value CRUD operations  
1. Insert key-value = http://13.233.158.98:8888/values/insert/  
   Request ⇒ “key=”+key+”&value=”+value  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

2. Update key-value = http://13.233.158.98:8888/values/update/  
   KEY WILL NOT BE UPDATED  
   Request ⇒ “key=”+key+”&value=”+value  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

3. Delete key = http://13.233.158.98:8888/values/delete/  
   Request ⇒ “key=”+key  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

4. Read table = http://13.233.158.98:8888/values/read/  
   Request ⇒ None  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

[sample usage using ajax](demo_ui/substitute.php)  
