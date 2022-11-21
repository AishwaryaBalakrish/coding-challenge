from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


class RyanAirWebAPIs:
    def __init__(self):
        self.web_site_url = "https://www.ryanair.com/"
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.web_site_url)  # Open Site in new chrome window

    def wait_for_home_page_to_load(self):
        accept_cookie_xpath = "//div[@id='cookie-popup-with-overlay']//button[contains(text(),'Yes, I agree')]"
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, accept_cookie_xpath)))
        except TimeoutException:
            print("Loading took too much time!, Refreshing web page again...")
            self.driver.refresh()

    def accept_cookie(self):
        try:
            accept_cookie_xpath = "//div[@id='cookie-popup-with-overlay']//button[contains(text(),'Yes, I agree')]"
            accept_cookie_button = self.driver.find_element(By.XPATH, accept_cookie_xpath)
            accept_cookie_button.click()
            return True, "success"
        except Exception as e:
            print("Got Exception %s", e)
            return False, "Failed to Accept cookies as - Got an Exception -%s" % e

    def subscribe_with_junk_email(self):
        try:
            email_input_xpath = "//hp-subscriber-widget-container//input[@type='email']"
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, email_input_xpath)))
            email_input_button = self.driver.find_element(By.XPATH, email_input_xpath)
            email_input_button.send_keys("test@gmail.com")
            self.driver.find_element(By.XPATH, "//hp-subscriber-widget-container//button[@type='submit']").click()
            self.driver.find_element(By.XPATH, "//hp-subscriber-widget-container//span").click()
        except ElementNotVisibleException:
            self.driver.find_element(By.XPATH, "//hp-subscriber-widget-container//span").click()
            email_input_button = self.driver.find_element(By.XPATH, email_input_xpath)
            email_input_button.send_keys("test@gmail.com")
            self.driver.find_element(By.XPATH, "//hp-subscriber-widget-container//button[@type='submit']").click()
            self.driver.find_element(By.XPATH, "//hp-subscriber-widget-container//span").click()

    def terminate_web_session(self):
        self.driver.close()
        self.driver.quit()

    def search_trip_flights(self, trip_type, departure_country, departure_city, destination_country, destination_city,
                        departure_date, num_of_adults, num_of_teens, num_of_children, num_of_infants, return_date=''):

        try:
            if trip_type.lower() == 'one way':
                button_label = "One way"
            else:
                button_label = "Return trip"
            trip_type_button_xpath = "//button[@aria-label='%s']" % button_label
            trip_type_button = self.driver.find_element(By.XPATH, trip_type_button_xpath)
            trip_type_button.click()

            departure_place_input_xpath = "//input[@id='input-button__departure']"
            departure_place_input = self.driver.find_element(By.XPATH, departure_place_input_xpath)
            departure_place_input.click()
            self.driver.implicitly_wait(5)

            departure_country_button = self.driver.find_element(By.XPATH,
                                                             "//div/span[contains(text(),'%s')]" % departure_country.capitalize())
            departure_country_button.click()

            departure_city_button = self.driver.find_element(By.XPATH, "//span[contains(text(),'%s')]" % departure_city.capitalize())
            departure_city_button.click()

            destination_place_input_xpath = "//input[@id='input-button__destination']"
            destination_place_input = self.driver.find_element(By.XPATH, destination_place_input_xpath)
            destination_place_input.clear()

            destination_country_button = self.driver.find_element(By.XPATH, "//div/span[contains(text(),'%s')]"% destination_country.capitalize())
            destination_country_button.click()

            destination_city_button = self.driver.find_element(By.XPATH, "//div//span[contains(text(),'%s')]"% destination_city.capitalize())
            destination_city_button.click()


            # if one way is selected then make sure the return date picker disappears
            if trip_type.lower() == 'one way':
                return_date_xpath = "//fsw-input-button[@uniqueid='dates-to']"
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, return_date_xpath)))

            departure_date_formatted = datetime.strptime(departure_date, '%d/%m/%Y')
            departure_date_reverse_format = departure_date_formatted.strftime('%Y-%m-%d')
            departure_date_formatted = departure_date_formatted.ctime().split(' ')
            departure_date_final_format = \
                departure_date_formatted[0] + ', ' + departure_date_formatted[2] + ' ' + departure_date_formatted[1]

            departure_date_xpath = "//fsw-input-button[@uniqueid='dates-from']"
            departure_date_picker = self.driver.find_element(By.XPATH, departure_date_xpath)
            self.driver.implicitly_wait(5)

            #select the month
            month_xpath = "//div[@data-id='%s']"%departure_date_formatted[1]
            month_button = self.driver.find_element(By.XPATH, month_xpath)
            month_button.click()

            #select the data
            month_xpath = "//div[@data-id='%s']" % departure_date_reverse_format
            month_button = self.driver.find_element(By.XPATH, month_xpath)
            month_button.click()

            if not trip_type.lower() == 'one way':
                return_date_formatted = datetime.strptime(return_date, '%d/%m/%Y')
                return_date_reverse_format = return_date_formatted.strftime('%Y-%m-%d')
                return_date_formatted = return_date_formatted.ctime().split(' ')
                return_date_final_format = \
                    return_date_formatted[0] + ', ' + return_date_formatted[2] + ' ' + return_date_formatted[1]

                # making sure return date picker is present
                return_date_xpath = "//fsw-input-button[@uniqueid='dates-to']"
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, return_date_xpath)))

                # select the month
                month_xpath = "//div[@data-id='%s']" % return_date_formatted[1]
                month_button = self.driver.find_element(By.XPATH, month_xpath)
                month_button.click()

                # select the data
                month_xpath = "//div[@data-id='%s']" % return_date_reverse_format
                month_button = self.driver.find_element(By.XPATH, month_xpath)
                month_button.click()

            num_passengers_xpath = "//fsw-input-button[@uniqueid='passengers']"
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, num_passengers_xpath)))

            if num_of_adults>1:
                adult_xpath = "//ry-counter-button[contains(@aria-label,'Adults+1')]/ancestor::div[contains(@data-ref,'counter__increment')]"
                adult_button = self.driver.find_element(By.XPATH, adult_xpath)
                for i in range(num_of_adults-1):
                    adult_button.click()
            if num_of_teens>0:
                teens_xpath = "//ry-counter-button[contains(@aria-label,'Teens+1')]/ancestor::div[contains(@data-ref,'counter__increment')]"
                teen_button = self.driver.find_element(By.XPATH, teens_xpath)
                for i in range(num_of_teens):
                    teen_button.click()
            if num_of_infants>0:
                infant_xpath = "//ry-counter-button[contains(@aria-label,'Infant+1')]/ancestor::div[contains(@data-ref,'counter__increment')]"
                infant_button = self.driver.find_element(By.XPATH, infant_xpath)
                for i in range(num_of_infants):
                    infant_button.click()
                    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'got it')]")))
                    infant_companion_agreement_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'got it')]")
                    infant_companion_agreement_button.click()

            if num_of_children>0:
                children_xpath = "//ry-counter-button[contains(@aria-label,'Children+1')]/ancestor::div[contains(@data-ref,'counter__increment')]"
                children_button = self.driver.find_element(By.XPATH, children_xpath)
                for i in range(num_of_children):
                    children_button.click()

            #submitting the number of passengers
            self.driver.find_element(By.XPATH, "//button[@aria-label='Done']").click()

            search_button_xpath = "//button[@aria-label='Search']"
            search_button = self.driver.find_element(By.XPATH, search_button_xpath)
            search_button.click()
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), ' Edit search')]")))
            return True, "success"
        except Exception as e:
            print("Got Exception %s", e)
            return False, "Failed to search flights as - Got an Exception - %s" % e

    def check_if_the_right_flights_are_displayed(self, departure_city, destination_city, departure_date, trip_type,
                                                 num_passengers, return_date=''):
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), ' Edit search')]")))
            departure_date_formatted = datetime.strptime(departure_date, '%d/%m/%Y')
            departure_date_formatted = departure_date_formatted.ctime().split(' ')
            departure_date_final_format = departure_date_formatted[2] + ' ' + departure_date_formatted[1]
            if return_date:
                return_date_formatted = datetime.strptime(return_date, '%d/%m/%Y')
                return_date_formatted = return_date_formatted.ctime().split(' ')
                return_date_final_format = return_date_formatted[2] + ' ' + return_date_formatted[1]
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(), '%s')]"%departure_city.capitalize())))
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), '%s')]" % destination_city.capitalize())))
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'fadeInOut') and contains(text(), '%s')]"
                                                %trip_type.capitalize())))
            trip_details = self.driver.find_element(By.XPATH, "//div[contains(@class,'fadeInOut') and contains(text(), '%s')]" %trip_type.capitalize()).text
            if not departure_date_final_format in trip_details:
                return False, "Departure date is not as expected in trip details-%s"%trip_details
            if return_date and not return_date_final_format in trip_details:
                return False, "Return date is not as expected in trip details-%s"%trip_details
            if not str(num_passengers) in trip_details:
                return False, "Number of passenger is not as expected in trip details-%s"%trip_details
            return True, "success"
        except Exception as e:
            print("Got Exception %s", e)
            return False, "Failed to validate flights as - Got an Exception -%s" % e


if __name__ == "__main__":
    try:
        session = RyanAirWebAPIs()
        session.wait_for_home_page_to_load()
        session.accept_cookie()
        print(session.search_trip_flights(trip_type="one way", departure_country='Ireland', departure_city='Dublin', destination_country='Spain',
                            destination_city = 'Barcelona',
                            departure_date='26/11/2022',
                            return_date = '30/11/2022',
                            num_of_adults=2, num_of_teens=1, num_of_children=1, num_of_infants=1))

        print(session.check_if_the_right_flights_are_displayed(departure_city='Dublin', destination_city='Barcelona',  trip_type='return',
                                                 departure_date='26/11/2022',
                                                 return_date='30/11/2022',
                                                num_passengers=5))

    except Exception as e:
        print("Got Exception %s", e)
