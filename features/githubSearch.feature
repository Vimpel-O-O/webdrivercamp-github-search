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
      | Vimpel-O-O   | location     | RETURN        |


  Scenario Outline: Verify follow button functionality
    Given Browser: Navigate to gh-users-search website
    When UI: search for <username> by <Button/RETURN>
    Then Sleep 1
    And UI: Press follow button
    Then Verify transfer to <username> github page
     Examples:
      | username       | Button/RETURN |
      | Vimpel-O-O     | RETURN        |

  Scenario Outline: Verify followers field against API
    Given Browser: Navigate to gh-users-search website
    When UI: search for <username> by <Button/RETURN>
    Then Sleep 1
    And API: send GET request for <username>'s followers list
    Then GitHub Integration API: verify user's followers field values
     Examples:
      | username       | Button/RETURN |
      | nadvolod       | Button        |
      | Vimpel-O-O     | RETURN        |

    