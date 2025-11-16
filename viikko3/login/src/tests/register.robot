*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      ReSet Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  foo
    Set Password  bar12345
    Set Password-Confirmation  bar12345
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  f
    Set Password  bar12345
    Set Password-Confirmation  bar12345
    Click Button  Register
    Register Should Fail With Message  Username too short

Register With Valid Username And Too Short Password
    Set Username  foo2
    Set Password  bar
    Set Password-Confirmation  bar
    Click Button  Register
    Register Should Fail With Message  Password too short

Register With Valid Username And Invalid Password
    Set Username  foo
    Set Password  bargfgfdgfddfg
    Set Password-Confirmation  bargfgfdgfddfg
    Click Button  Register
    Register Should Fail With Message  Password too weak

Register With Nonmatching Password And Password Confirmation
    Set Username  foo88
    Set Password  bar12345
    Set Password-Confirmation  bar12345gfdg
    Click Button  Register
    Register Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  bar12345
    Set Password-Confirmation  bar12345
    Click Button  Register
    Register Should Fail With Message  Username taken

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password-Confirmation
    [Arguments]  ${password}
    Input Password  name:password_confirmation  ${password}

*** Keywords ***
ReSet Application Create User And Go To Register Page
    ReSet Application
    Create User  kalle  kalle123
    Go To Register Page