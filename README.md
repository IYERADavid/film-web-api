# film-web-backend
film web API created with python flask (development)

Domain name : https://vendor-videos-api.herokuapp.com/

current created routes :
  -("/home") : methods ['GET']
  -("/signup") : methods ['POST]
  -("/signin") : methods ['POST']
  
  
  # every_where you see (varialbe_name ==> contains:) those are explanation on what varilable,property,etc contains as its value
  
 current routes functionality :
 
  - signup : 
            * inputs:
               - POST request with request.body equal to { html_form }
               html_form ==> contains:
                  - html_input with name attribute equal to 'first_name' and value equal to user first_name
                    and also must less than 26 characters
                  - html_input with name attribute equal to 'last_name' and value equal to user last_name
                    and also must less than 26 characters
                  - html_input with name attribute equal to 'middle_name' and value equal to user middle_name
                    and also must less than 16 characters
                  - html_input with name attribute equal to 'email' and value equal to user email
                    and also must less than 322 characters
                  - html_input with name attribute equal to 'password' and value equal to user password
                    and also must less than 81 characters
           * outputs:
              
              - if one of html input value not less than specified value above:
                    output > { "status" : "input_errors", "body" : 
                             "Inputs not validating (invalid values that database can't except)"}
                             
              - if the email you send already have an account:
                    output > { "status" : "email_exist_error",
                             "body" : "The email you entered already exist"}
                             
              - if the user is created:
                    output > { "status" : "success", "body" : user}
                    user ==> contains: - used data object
                    
  - signin:
           * inputs:
              - POST request with request.body equal to { html_form }
              html_form ==> contains:
                  - html_input with name attribute equal to 'email' and value equal to user email
                    and also must less than 322 characters
                  - html_input with name attribute equal to 'password' and value equal to user password
                    and also must less than 81 characters
           * outputs:
              
               - if one of html input value not less than specified value above:
                    output > { "status" : "input_errors", "body" : 
                             "Inputs not validating (invalid values that database can't except)"}
                             
              - if the email and password you send is not found in database:
                    output > { "status" : "invalid_credentials", "body" :
                             "The email or password you entered is invalid"}
                             
              - if the email and password you send is found in database:
                    output > { "status" : "success", "body" : {"user" : user , "access_token" : token} }
                    user ==> contains: - used data object
                    token ==> contains: - created login token for the user (in string format)
               
  - home :
           * inputs:
              - GET request with request.headers equal to { 'Authorization': pass your login token here }
           * outputs:
           
               - if you make get request wthiout passing request.headers as shown above or
                or your token is expired:
                    output > { "status" : "login_required", "body" : "You must login to continue" }
                  
               - if your token is valid:
                    output > { "status" : "success", "body" : user }
                    user ==> contains: - used data object
               
                
    
