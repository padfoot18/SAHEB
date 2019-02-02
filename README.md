# Chatbot API

### Dummy API
dummy api hosted at http://13.233.158.98/chat/

usage:

send a post request to http://13.233.158.98:8888/chat/ containing data as
question="user query"

[sample usage using ajax in js](testAPI_Javascript.php)

[sample usage using ajax in jquery](testApiJQuery.php)

### Dummy API hosted for Key, Value CRUD operations
1. Insert key-value = http://13.233.158.98:8888/api/v1/insert  
   Request ⇒ “key=”+key+”&value=”+value  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

2. Update key-value = http://13.233.158.98:8888/api/v1/update  
   KEY WILL NOT BE UPDATED  
   Request ⇒ “key=”+key+”&value=”+value  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

3. Delete key = http://13.233.158.98:8888/api/v1/delete  
   Request ⇒ “key=”+key  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

4. Read table = http://13.233.158.98:8888/api/v1/read  
   Request ⇒ None  
   Response ⇒ [ {‘key’:’abc’, ‘value’:100000 } , {‘key’: ‘def’, ‘value’: 100 } ]  

[sample usage using ajax](substitute.php)  
