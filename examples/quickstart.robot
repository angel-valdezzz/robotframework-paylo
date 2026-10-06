*** Settings ***
Library    Paylo
Library    Collections

*** Test Cases ***
Render A Payload
    VAR    &{values}    name=Ana    email=ana@example.com    quantity=${3}    id=QA-001
    ${body}=    Render JSON File    ${CURDIR}/template.json    ${values}
    Should Be Equal    ${body}[customer][name]    Ana
    Should Be Equal As Integers    ${body}[quantity]    3
    Write JSON File    ${body}    ${OUTPUT DIR}/payload.json
