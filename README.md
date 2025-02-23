# Assignment5
The code will now run via going into src directory and typing python api.py and node index.js which will start up the api and then boot up the application project in https://localhost:3000
# Backend testing
Run via going into directory src and running pytest test_api.py.
This will run 20 tests for the backend api in api.py. 

![image](https://github.com/user-attachments/assets/e4c71fdf-4385-40c3-8437-46b738cef3b5)\
This test will test to see if the api can correctly add a new monster to the database

![image](https://github.com/user-attachments/assets/25f624a0-e889-4cc0-9be2-d4642bca0052)\
This test will try to create a new monster with no name declared which should lead to a 400 error

![image](https://github.com/user-attachments/assets/7ea490bc-4ac8-4c11-9baf-4e7928915b41)\
This test will try to create a monster with no description which should lead to a 400 error

![image](https://github.com/user-attachments/assets/31b2258b-75aa-4a32-aaa2-523c27df21cb)\
This test will try to input a monster with invalid data so the json is blank this should return a 400 error

![image](https://github.com/user-attachments/assets/3f41ecda-b921-447c-bf50-0b87b8acf131)\
This test will try to create a duplicate monster. So if the name is found already in the database it will send a 400 error

![image](https://github.com/user-attachments/assets/aabb8516-fe82-4863-8ec8-984c6151bf7f)\
This test will attempt to retrieve all monsters in the databaase which should return 200

![image](https://github.com/user-attachments/assets/dd68a7dd-8bc8-4530-b221-7a4e4792bcc3)\
This test will retrieve 1 monster given an id number which should succeed

![image](https://github.com/user-attachments/assets/16242b36-8424-40d2-901a-c521bcceea99)\
attempt to get monster with incorrect id number to recieve monster not found

![image](https://github.com/user-attachments/assets/13917750-09e4-47b5-91fd-57e39c1e561a)\
retreive no monster when there isnt any monsters in database causing a 200 response

![image](https://github.com/user-attachments/assets/e90d63d7-c842-412b-b5ae-e437bc4790e0)\
attempt to use a non integer as input for retrieving a monster which gives 404 error

![image](https://github.com/user-attachments/assets/cd21e2b1-49da-4241-86dd-3baf88b2d916)\
test getting monsters via a filter which should succeed and give a 200 response

![image](https://github.com/user-attachments/assets/ed4561f4-3d60-4685-8e8c-59deb983dd47)\
test out the updating of a monster in the database which should give 200

![image](https://github.com/user-attachments/assets/93909d69-beeb-424d-a0f1-90c954f1c972)\
update a monster that doesnt exist which should return 404 monster not found

![image](https://github.com/user-attachments/assets/713e3cd2-7513-4221-bea5-3b99590219eb)\
attempt to update with missing field which will throw a 400 error saying name and description are required fields

![image](https://github.com/user-attachments/assets/4e8667cf-687c-4f64-b1da-adfa5ff13d1c)\
update a monster given a non integer id which will give 404 error

![image](https://github.com/user-attachments/assets/f30c0f9d-01fd-4a37-a039-698e56709abe)\
delete a monster given id which should give 200 monster deleted successfully

![image](https://github.com/user-attachments/assets/42a87ce2-57ec-4e54-8dba-c42c7f6f1860)\
delete a monster with undeclared id so that the monster isnt found giving 404 error

![image](https://github.com/user-attachments/assets/ae1ab532-dde9-4ce6-8920-ad1c80aa3fb6)\
delete a monster with an invalid id giving a 404 error

![image](https://github.com/user-attachments/assets/6b12c97d-fda0-41e2-98ed-0366bddce540)\
delete a monster with a non integer id which gives 404 error

![image](https://github.com/user-attachments/assets/ba3ec65b-141e-4d3e-92dd-982c276067ef)\
Test to see if the api will run without errors

# Frontend Testing
Run via going into directory mosnterhunter-app and running karma start karma.conf.js.
This will run 5 tests for the frontend connection in app.js.

![image](https://github.com/user-attachments/assets/e9877565-6c19-43b6-ad2f-2d1828bea3db)\
this will test to see if the monster list is initialized on startup

![image](https://github.com/user-attachments/assets/f94e2ae3-7c5b-4a56-a577-93e267b7bcd8)\
this will test when user tries to submit a new monster that it will post to the database

![image](https://github.com/user-attachments/assets/a0a63ca4-43a7-4f73-a9c4-95d8cb73c7fd)\
tests if the user is able to find a monster by the id function

![image](https://github.com/user-attachments/assets/a3f81036-a15c-4b2f-9eea-555a2343974e)\
will test if when the user goes to delete by id it will delete from database




