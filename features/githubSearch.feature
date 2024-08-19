Feature:

  Scenario: Verify number of followers against API
    Given Browser: Navigate to gh-users-search website
    When UI: search for "<username>"
    And API: send GET request to <usersname>'s followers
    And API: verify status code is 200
    Then GitHub Integration API: verify fields values
