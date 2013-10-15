TestLink Python API
=============================

This project uses python to abstact the Testlink API into a resource driven querying API.

Basic usage is as follows:

Get the api:
```
from testlink import TestLinkClient

#Note that TestLinkClient will pull TESTLINK_URL and TESTLINK_KEY from the
#environment if they exist
client = TestLinkClient("http://localhost/lib/api/xmlrpc/v1/xmlrpc.php", "your-key")

#Get projects
for project in client.projects.cursor:
  print project.name 

#Get plans
project = client.projects.get("My Project")
for plan in project.plans.cursor:
    print plan.name

plans = client.get_plans(project_id=1)
print len(plans.cursor)

#Get suites
for suite in plan.suites.cursor:
  for second_tier_suite in suite.suites.cursor:
    print second_tier_suite.name

for first_level suite in project.suites.first_level:
  print first_level.name

#Get test cases
for case in plan.cases.cursor:
  print case.name

#Create case: Note this requires a suite
from testlink.resource.cases import make_step
from testlink.common import execution_types
steps = [make_step(1, 'Actions', 'Expected results', execution_type=execution_types.AUTOMATED)]
project.suites.get('test suite name').cases.create('test case one', 'author', 'summary', steps)

#Report on a test case
from testlink.common import status
case.report(status.SUCCESS, build_id=build.id, build_name="name",
	    platform_id=project.platforms.cursor.pop(), notes='something")

```