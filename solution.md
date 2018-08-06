Nexus Edge Coding Challenge
--------------------------------------
First of all  I really appreciate that everything in the readme file was pretty clear and crisp which really helped me while coding.

Why I coded the way I coded:
-
1. Most of my code has been encapsulated into functions to improvise the code reusability.
2. Few more functions have been added to improvise the code readability.
3. I honestly thought it would be clumsy to write all database related code in create_user function so I sub divided the 
tasks(creating table, inserting values) and created separate functions for those respective functionality.
4. There is one more function "pull_user_from_api" to pull the data from the API and assign the needed data to variables which is frequently used function to achieve the 6th point the problem description.
5. <b>I was unsure if usage of regular expressions is acceptable or not. So, I decided to use it only once to check if the complexity level is 4. It improves time complexity of search rather than checking every character of the string using a loop.</b>
6. Added a formatting library for color coding to highlight the result when the password complexity has been overridden.
7. Made sure the newly inserted values are stored in database permanantly and closed the connection after usage. I believe it is a good coding practice.

