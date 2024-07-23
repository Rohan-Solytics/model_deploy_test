# model_deploy_test
Test to remove Kubernetes and Docker dependency

In POSTMAN:

########################################
  Create models:
  Method: POST
  URL: {{Localurl}}/models
  Headers: Add a header with Key: "Content-Type" and Value: "application/json"
  Body: 
  {
    "name": "model1",
    "requirements_file": "requirements1.txt"
  }

########################################
  List all models:
  Method: GET
  URL: {{url}}/models/

########################################
  Get details of a specific model:
  
  Method: GET
  URL: {{url}}/models/model1

########################################
  Run a model:
  
  Method: POST
  URL: {{url}}/models/model1/run

#########################################
  Check model status:
  
  Method: GET
  URL: {{url}}/models/model1/status
