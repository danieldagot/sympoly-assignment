Feature: File upload
  Scenario: Successfully upload a file
    Given I have a file named "H33BRlMmwZV3.exrf"
    When I upload the file
    Then I receive a successful upload response