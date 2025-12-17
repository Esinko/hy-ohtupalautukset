*** Settings ***
Documentation     Tests for Kivi-Paperi-Sakset Web UI
Library           SeleniumLibrary
Library           Process
Suite Setup       Start Flask App
Suite Teardown    Stop Flask App
Test Setup        Go To    http://localhost:5000

*** Variables ***
${BROWSER}        headlessfirefox
${SERVER_URL}     http://localhost:5000

*** Test Cases ***
Home Page Loads Successfully
    [Documentation]    Verify that the home page loads and displays game options
    Page Should Contain    Kivi-Paperi-Sakset
    Page Should Contain    Valitse pelityyppi
    Page Should Contain    Ihmistä vastaan
    Page Should Contain    Tekoälyä vastaan
    Page Should Contain    Parannettua tekoälyä vastaan

Start Game Against AI
    [Documentation]    Start a game against simple AI
    Select Radio Button    game_type    tekoaly
    Click Button    Aloita peli
    Wait Until Page Contains    Tekoälyä vastaan
    Page Should Contain    Kierros: 1 / 5
    Page Should Contain    Pelitilanne

Play One Round Against AI
    [Documentation]    Play a single round against AI
    Select Radio Button    game_type    tekoaly
    Click Button    Aloita peli
    Wait Until Page Contains    Valitse siirtosi
    Click Button    K (Kivi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    Wait Until Page Contains    Kierros: 2 / 5
    Page Should Contain    Edellinen kierros

Play Complete Game And See Game Over
    [Documentation]    Play 5 rounds and verify game over screen appears
    Select Radio Button    game_type    tekoaly
    Click Button    Aloita peli
    
    # Play 5 rounds
    FOR    ${round}    IN RANGE    5
        Wait Until Page Contains    Valitse siirtosi
        Click Button    K (Kivi)
        Wait Until Element Is Enabled    id:submit-btn    timeout=5s
        Click Element    id:submit-btn
        Sleep    0.5s
    END
    
    # Verify game over page
    Wait Until Page Contains    Peli päättyi!    timeout=10s
    Page Should Contain    Lopputulos
    Page Should Contain    Pelatut kierrokset: 5
    Page Should Contain    Lopullinen tilanne

Two Player Mode Hides Player 1 Selection
    [Documentation]    Verify that player 1's choice is hidden from player 2
    Select Radio Button    game_type    pelaaja_vs_pelaaja
    Click Button    Aloita peli
    Wait Until Page Contains    Pelaaja 1: Valitse siirtosi
    
    # Player 1 makes a selection
    Click Button    K (Kivi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    
    # Verify player 1's selection is hidden
    Wait Until Page Contains    Pelaaja 1 on tehnyt valintansa
    Page Should Contain    Nyt on Pelaaja 2:n vuoro
    Page Should Not Contain    Pelaaja 1 valitsi: K
    
    # Player 2 makes a selection
    Click Button    P (Paperi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    
    # Now both moves should be revealed
    Wait Until Page Contains    Edellinen kierros
    Page Should Contain    Pelaaja 1 valitsi: K
    Page Should Contain    Pelaaja 2 valitsi: P

Game Shows Round Progress
    [Documentation]    Verify that round counter is displayed correctly
    Select Radio Button    game_type    tekoaly
    Click Button    Aloita peli
    Page Should Contain    Kierros: 1 / 5
    
    # Play one round
    Click Button    K (Kivi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    Wait Until Page Contains    Kierros: 2 / 5
    
    # Play another round
    Click Button    K (Kivi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    Wait Until Page Contains    Kierros: 3 / 5

Improved AI Mode Works
    [Documentation]    Verify improved AI mode can be started and played
    Select Radio Button    game_type    parempi_tekoaly
    Click Button    Aloita peli
    Wait Until Page Contains    Parannettua tekoälyä vastaan
    Page Should Contain    Kierros: 1 / 5
    
    # Play one round
    Click Button    P (Paperi)
    Wait Until Element Is Enabled    id:submit-btn
    Click Element    id:submit-btn
    Wait Until Page Contains    Kierros: 2 / 5

Reset Button Returns To Home
    [Documentation]    Verify that reset button returns to home page
    Select Radio Button    game_type    tekoaly
    Click Button    Aloita peli
    Wait Until Page Contains    Valitse siirtosi
    Click Button    Lopeta peli
    Wait Until Page Contains    Valitse pelityyppi
    Page Should Contain    Ihmistä vastaan

*** Keywords ***
Start Flask App
    [Documentation]    Start the Flask development server
    Start Process    poetry    run    python    src/web_app.py
    ...    alias=flask_server
    Sleep    3s    # Wait for server to start
    Open Browser    ${SERVER_URL}    ${BROWSER}

Stop Flask App
    [Documentation]    Stop the Flask development server
    Close Browser
    Terminate Process    flask_server
