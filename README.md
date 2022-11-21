Automation Script for Ryan Air Flight Booking

Test suite contains the following test cases:
-----
1. Got https://www.ryanair.com/ -&gt; Home Ryanair page is loaded
2. Search for flights -&gt; the page with suggested flights is loaded with correct dates and number of
persons
E.g. (you can choose any valid values)
from Dublin to Basel
Departure date Thu, 26 Nov
Return date Tue, 31 Dec
2 adults

****I was not able to add other test cases from the coding chanllenge to the test suite***

Python Version:
-------
Latest

OS Supported:
------
Windows, Linux

ChromeDriver Version
-----
Latest version

Setup Steps:
--------
The chromedriver is automatically installed by the python module - chromedriver_autoinstaller.
> pip install -r requirements.txt
> RUN: pytest test_cases.py --html=report.html

The Dockerfile contains all the details to convert this project into a docker image a run:
To run from docker desktop:
> docker build -t <tag-name> <the repo path, either local path or remote path>
> docker run <tag-name>
Image uploaded to docker hub and can be identified using the following tag- aishwaryabalakrish/latest
>docker run aishwaryabalakrish/ryanair-latest

Test case parameter details:
------
The test cases are written in test_case.py file. The arguments for the test case is parametrized.
This way the flow could be validated with different set of parameter or arguments. The parameters or
arguments are specified in the test_cases.py file itself. Feel free to test the flow by adding different
 set of parameters.