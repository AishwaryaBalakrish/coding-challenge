"""
Testsuite contains the following test cases:
1. Got https://www.ryanair.com/ -&gt; Home Ryanair page is loaded
2. Search for flights -&gt; the page with suggested flights is loaded with correct dates and number of
persons
E.g. (you can choose any valid values)
from Dublin to Basel
Departure date Thu, 26 Nov
Return date Tue, 31 Dec
2 adults
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest
from .web_apis.ryanair_web_apis import RyanAirWebAPIs


@pytest.fixture(scope='function')
def session():
    web_session = RyanAirWebAPIs()
    web_session.wait_for_home_page_to_load()
    return web_session


@pytest.fixture(scope='function', autouse=True)
def setup(request, session):
    accept_cookie_status, message = session.accept_cookie()
    assert accept_cookie_status, message
    session.subscribe_with_junk_email()
    def teardown():
        session.terminate_web_session()
    request.addfinalizer(teardown)


@pytest.mark.FLIGHT_BOOKING
class TestFlightBooking:
    @pytest.mark.parametrize('trip_type, departure_country, departure_city, destination_country, destination_city, '
                             'departure_date, num_of_adults, num_of_teens, num_of_children, num_of_infants, '
                             'return_date', [
        ('return', 'ireland', 'dublin', 'switzerland', 'basel', '26/11/2022', 2, 1, 1, 1, '31/12/2022'),
        ('one way', 'ireland', 'dublin', 'switzerland', 'basel', '26/11/2022', 1, 0, 1, 1, '')
                                                ])
    def test_validate_flight_booking_flow(self, session, trip_type, departure_country, departure_city,
                                          destination_country, destination_city, departure_date, num_of_adults,
                                          num_of_teens, num_of_children, num_of_infants, return_date):
        search_flight_status, message = session.search_trip_flights(trip_type=trip_type,
                                        departure_country=departure_country, departure_city=departure_city,
                                        destination_country=destination_country, destination_city=destination_city,
                                        departure_date=departure_date,  return_date = return_date,
                                        num_of_adults=num_of_adults, num_of_teens=num_of_teens,
                                        num_of_children=num_of_children, num_of_infants=num_of_infants)
        assert search_flight_status, "Searching for flight with the given details failed as %s" % message
        total_num_passengers = num_of_infants+num_of_children+num_of_teens+num_of_adults
        search_validation_status, message = session.check_if_the_right_flights_are_displayed(departure_city=departure_city,
                                                    destination_city=destination_city,  trip_type=trip_type,
                                                    departure_date=departure_date, return_date=return_date,
                                                   num_passengers=total_num_passengers)
        assert search_validation_status, "The flight search validation to confirm the trip/flight details failed as %s" \
                                         % message

