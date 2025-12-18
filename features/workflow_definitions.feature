Feature: Workflow Definitions

  Scenario: Define and verify a simple workflow
    Given I create a new workflow named "Simple Approval"
    When I add a "Trigger" node with id "start" and label "Start Request"
    And I add a "Process" node with id "approve" and label "Manager Approval"
    And I add a "Completion" node with id "end" and label "End Process"
    And I connect "start" to "approve"
    And I connect "approve" to "end"
    Then the workflow should be valid
    And the workflow should have 3 nodes and 2 edges
    And the node "start" should be reachable from the start
    And the node "end" should be reachable from the start
