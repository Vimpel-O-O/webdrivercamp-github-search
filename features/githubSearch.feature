Feature:

  Scenario Outline: Verify [Repos, Followers, Following, Gists] fields values against API
    Given Browser: Navigate to gh-users-search website
    When UI: search for <username> by <Button/RETURN>
    And API: send GET request to <username>'s <data>
    And API: verify status code is 200
    Then GitHub Integration API: verify user's <data> fields values
    Examples:
      | username     | data         | Button/RETURN |
      | nadvolod     | public_repos | Button        |
      | nadvolod     | followers    | RETURN        |
      | nadvolod     | following    | Button        |
      | nadvolod     | public_gists | RETURN        |
      | nadvolod     | name         | Button        |
      | nadvolod     | login        | RETURN        |
      | nadvolod     | bio          | Button        |
      | nadvolod     | blog         | RETURN        |
      | nadvolod     | company      | Button        |
      | nadvolod     | location     | RETURN        |