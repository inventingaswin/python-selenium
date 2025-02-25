import pyautogui
import pytest
from time import sleep, time
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.usefixtures('initialize_driver')
class GetLink:
    """Class to automate browser"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://demoqa.com/")
    cate = driver.find_element(By.XPATH, "//div[@Class='category-cards']")
    driver.execute_script('arguments[0].scrollIntoView();', cate)

    def test_an_element_cate(self):
        driver = self.driver
        ele = driver.find_element(By.XPATH,
                                  "//div[@class='card mt-4 top-card' and contains(., 'Interactions')]")
        ele.click()
        assert "DEMOQA" == driver.title, "Failed to click elements"

    def test_check_box(self):
        driver = self.driver
        # Below is the example to scroll until element ntg to do with above example.
        # str = driver.find_element(By.XPATH, "//div[contains(text(), 'Book Store Application')]")
        # driver.execute_script('arguments[0].scrollIntoView();', str)
        check_box = driver.find_element(By.XPATH, "//span[@class='text' and contains(text(), 'Check Box')]")
        driver.execute_script('arguments[0].scrollIntoView();', check_box)
        check_box.click()
        assert driver.find_element(By.XPATH,
                                   "//h1[@class='text-center' and contains(text(), 'Check Box')]").is_displayed()
        driver.find_element(By.CSS_SELECTOR, "span.rct-checkbox").click()
        assert driver.find_element(By.CSS_SELECTOR, "div#result").is_displayed()
        ele1 = driver.find_element(By.XPATH, "//span[@class='rct-checkbox']/*[name()='svg']")
        assert 'check' in ele1.get_attribute("class")
        driver.find_element(By.XPATH, '//button[@aria-label="Expand all"]').click()
        ele = driver.find_element(By.XPATH,
                                  "//span[contains(text(), 'Downloads')]/preceding-sibling::span[@class='rct-checkbox']")
        txt = ele.get_attribute('class')
        assert 'uncheck' not in txt
        driver.execute_script('arguments[0].scrollIntoView();', ele)
        ele.click()
        assert 'uncheck' in driver.find_element(By.XPATH,
                                                "//span[contains(text(), 'Downloads')]/preceding-sibling::span["
                                                "@class='rct-checkbox']/*[name()='svg']").get_attribute('class')
        self.test_web_tabel()

    def test_web_tabel(self):
        """method to check tabel"""
        driver = self.driver
        driver.find_element(By.XPATH, "//li[@class='btn btn-light ']/span[contains(., 'Web Tables')]").click()
        heading = driver.find_element(By.XPATH, "//h1[@class='text-center' and text()='Web Tables']")
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        assert heading.is_displayed()
        rows = driver.find_elements(By.XPATH, "//div[@class='rt-tbody']/div")
        i = 0
        for row in rows:
            if 'padRow' in row.find_element(By.CSS_SELECTOR, 'div').get_attribute('class'):
                break
            i += 1
        print("Total rows in the table is: ", i)
        driver.find_element(By.CSS_SELECTOR, 'button#addNewRecordButton').click()
        assert driver.find_element(By.CLASS_NAME, 'modal-content').is_displayed()
        ac = ActionChains(driver)
        f_name = driver.find_element(By.ID, 'firstName-wrapper')
        ac.click(f_name).send_keys('Aswin').perform()
        l_name = driver.find_element(By.CSS_SELECTOR, "div#lastName-wrapper")
        ac.click(l_name).send_keys('S').perform()
        email = driver.find_element(By.ID, 'userEmail-wrapper')
        ac.click(email).send_keys('aswin@gmail.com').perform()
        age = driver.find_element(By.ID, 'age-wrapper')
        ac.click(age).send_keys('26').perform()
        salary = driver.find_element(By.ID, 'salary-wrapper')
        ac.click(salary).send_keys('2200000').perform()
        dept = driver.find_element(By.ID, 'department-wrapper')
        ac.click(dept).send_keys('Software').perform()
        submit_button = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].click();", submit_button)
        assert driver.find_element(By.XPATH, "//div[text()='Aswin']").is_displayed()
        self.test_buttons()

    def test_buttons(self):
        """"""
        driver = self.driver
        button = driver.find_element(By.XPATH, "//span[@class='text' and text()='Buttons']")
        driver.execute_script('arguments[0].scrollIntoView();', button)
        button.click()
        assert driver.find_element(By.XPATH, "//h1[@class='text-center' and text()='Buttons']").is_displayed()
        ac = ActionChains(driver)
        double = driver.find_element(By.ID, "doubleClickBtn")
        driver.execute_script('arguments[0].scrollIntoView();', double)
        ac.double_click(double).perform()
        assert driver.find_element(By.ID, 'doubleClickMessage').is_displayed()
        right = driver.find_element(By.ID, "rightClickBtn")
        ac.context_click(right).perform()
        assert driver.find_element(By.ID, 'rightClickMessage').is_displayed()
        click = driver.find_element(By.XPATH, "//button[text()='Click Me']")
        ac.click(click).perform()
        assert driver.find_element(By.ID, 'dynamicClickMessage').is_displayed()

    def test_links(self):
        """"""
        driver = self.driver
        link = driver.find_element(By.XPATH, '//li[@class="btn btn-light "]/span[text()="Links"]')
        driver.execute_script('arguments[0].scrollIntoView();', link)
        link.click()
        assert driver.find_element(By.CSS_SELECTOR, 'h1.text-center').is_displayed()
        parent = driver.current_window_handle
        driver.find_element(By.LINK_TEXT, "Home").click()
        windows = driver.window_handles
        for window in windows:
            if parent != window:
                driver.switch_to.window(window)
                break
        else:
            print("No new window to switch")
        assert driver.find_element(By.XPATH,
                                   "//div[@class='card mt-4 top-card' and contains(., 'Elements')]").is_displayed(), \
            'failed to switch to new window.'
        driver.switch_to.window(parent)
        driver.switch_to.window(window)
        driver.close()
        driver.switch_to.window(parent)
        driver.find_element(By.ID, "dynamicLink").click()
        windows = driver.window_handles
        for window in windows:
            if parent != window:
                driver.switch_to.window(window)
        else:
            print("No new window to switch")
        assert driver.find_element(By.XPATH,
                                   "//div[@class='card mt-4 top-card' and contains(., 'Elements')]").is_displayed(), \
            'failed to switch to new window.'
        driver.switch_to.window(parent)
        driver.switch_to.window(window)
        driver.close()
        driver.switch_to.window(parent)
        assert driver.find_element(By.ID, "dynamicLink").is_displayed(), 'failed to switch to new window.'

    def test_scroll_and_click(self):
        """"""
        driver = self.driver
        up_down = driver.find_element(By.XPATH, '//li/span[text()="Upload and Download"]')
        driver.execute_script("arguments[0].scrollIntoView();", up_down)
        up_down.click()
        down_button = driver.find_element(By.LINK_TEXT, "Download")
        driver.execute_script("arguments[0].scrollIntoView();", down_button)
        # driver.find_element(By.XPATH, '//div[@class="form-file"]/input[@id="uploadFile"]')
        upload = driver.find_element(By.CSS_SELECTOR, "div.form-file input#uploadFile")
        # upload.send_keys(r"C:\Users\7000033203\Downloads\Aswin resume.pdf")
        upload.is_displayed()
        pyautogui.write(r"C:\Users\7000033203\Downloads\Aswin resume.pdf")
        pyautogui.press("enter")

    def test_dynamic(self):
        """"""
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(5):
            try:
                dynamic = driver.find_element(By.XPATH, "//li/span[text()='Dynamic Properties']")
                driver.execute_script("arguments[0].scrollIntoView();", dynamic)
                dynamic.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
                sleep(0.5)
        head = driver.find_element(By.CSS_SELECTOR, "h1.text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        wait = WebDriverWait(driver, 7)
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button#enableAfter")))
        assert driver.find_element(By.CSS_SELECTOR, "button#visibleAfter").is_displayed()
        sleep(10)

    def test_form(self):
        driver = self.driver
        form_ele = driver.find_element(By.XPATH, "//span[text()='Practice Form']")
        driver.execute_script("arguments[0].scrollIntoView();", form_ele)
        form_ele.click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH,
                                                                                    "//h1[text()='Practice Form']"))
        assert driver.find_element(By.XPATH, "//h1[text()='Practice Form']").is_displayed()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID, "state"))
        city = driver.find_element(By.ID, "city")
        opacity = city.value_of_css_property("opacity")  # Check if it's faded
        pointer_events = city.value_of_css_property("pointer-events")  # Check if it's
        if opacity == "0.5" or pointer_events == "none":
            print("City dropdown is disabled!")
        else:
            print("City dropdown is active!")
        driver.find_element(By.ID, "state").click()
        wait = WebDriverWait(driver, 5)
        wait.until(ec.presence_of_element_located((By.XPATH, '//div[@class=" css-26l3qy-menu"]')))
        haryana_option = driver.find_element(By.XPATH,
                                             "//div[contains(@class, 'css-26l3qy-menu')]//div[text()='Haryana']")
        driver.execute_script("arguments[0].scrollIntoView();", haryana_option)
        haryana_option.click()
        assert city.value_of_css_property("opacity") == "1"
        assert "Haryana" in driver.find_element(By.ID, "state").text
        driver.find_element(By.ID, "city").click()
        driver.find_element(By.XPATH, "//div[contains(@class, 'css-26l3qy-menu')]//div[text()='Panipat']").click()
        assert "Panipat" in driver.find_element(By.ID, "city").text
        print('success')

    def test_browser_window(self):
        driver = self.driver
        alert = driver.find_element(By.XPATH, '//div[@class="header-text" and text()="Alerts, Frame & Windows"]')
        driver.execute_script("arguments[0].scrollIntoView();", alert)
        driver.find_element(By.XPATH, '//span[@class="text" and text()="Browser Windows"]').click()
        heading = driver.find_element(By.CSS_SELECTOR, 'div#browserWindows h1.text-center')
        driver.execute_script("arguments[0].scrollIntoView();", heading)
        assert heading.is_displayed()
        parent = driver.current_window_handle
        driver.find_element(By.CSS_SELECTOR, 'button#tabButton').click()
        windows = driver.window_handles
        for window in windows:
            if window != parent:
                driver.switch_to.window(window)
                break
        assert "This is a sample page" == driver.find_element(By.ID, "sampleHeading").text
        driver.switch_to.window(parent)
        driver.switch_to.window(window)
        driver.close()
        print("new tab success")
        driver.switch_to.window(parent)
        wait = WebDriverWait(driver, 15)
        new = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button#windowButton')))
        driver.execute_script('arguments[0].scrollIntoView();', new)
        new.click()
        windows = driver.window_handles
        for window in windows:
            if parent != window:
                driver.switch_to.window(window)
                break
        assert "This is a sample page" == driver.find_element(By.ID, "sampleHeading").text
        driver.switch_to.window(parent)
        driver.switch_to.window(window)
        driver.close()
        driver.switch_to.window(parent)
        print(driver.find_element(By.CSS_SELECTOR, 'div#browserWindows h1.text-center').text)
        print("new window success")
        parent = driver.current_window_handle
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button#messageWindowButton')))
        new_win = driver.find_element(By.CSS_SELECTOR, 'button#messageWindowButton')
        driver.execute_script("arguments[0].scrollIntoView();", new_win)
        new_win.click()
        windows = driver.window_handles
        for window in windows:
            if parent != window:
                driver.switch_to.window(window)
                print("switched to new message windiow")
                break
        html = driver.page_source  # Get the entire HTML source instantly
        soup = BeautifulSoup(html, "html.parser")
        text = soup.body.get_text(strip=True)  # Extract body text efficiently
        print(text)
        assert "Knowledge increases by sharing" in text
        driver.switch_to.window(parent)
        driver.switch_to.window(window)
        driver.close()
        driver.switch_to.window(parent)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div#browserWindows h1.text-center')))
        print(driver.find_element(By.CSS_SELECTOR, 'div#browserWindows h1.text-center').text)
        print("New message success")
        driver.quit()
        print("completely done")

    def test_alert(self):
        driver = self.driver
        alert = driver.find_element(By.XPATH, '//div[@class="header-text" and text()="Alerts, Frame & Windows"]')
        driver.execute_script('arguments[0].scrollIntoView();', alert)
        driver.find_element(By.XPATH, '//span[@class="text" and text()="Alerts"]').click()
        heading = driver.find_element(By.XPATH, '//h1[@class="text-center" and text()="Alerts"]')
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        driver.find_element(By.ID, 'alertButton').click()
        alear = Alert(driver)
        alear.accept()
        assert driver.find_element(By.ID, 'alertButton').is_displayed()
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        driver.find_element(By.ID, 'timerAlertButton').click()
        wait = WebDriverWait(driver, 7)
        alert = wait.until(ec.alert_is_present())
        alert.accept()
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        assert driver.find_element(By.ID, 'alertButton').is_displayed()
        driver.find_element(By.ID, 'confirmButton').click()
        alear = Alert(driver)
        alear.accept()
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        driver.find_element(By.ID, 'confirmResult').is_displayed()
        driver.find_element(By.ID, 'promtButton').click()
        alert = Alert(driver)
        alert.send_keys("Aswin")
        alert.accept()
        driver.execute_script('arguments[0].scrollIntoView();', heading)
        driver.find_element(By.ID, 'promptResult').is_displayed()
        print("Success")

    def test_frames(self):
        driver = self.driver
        driver.execute_script('arguments[0].scrollIntoView();',
                              driver.find_element(By.XPATH, '//span[@class="text" and text()="Alerts"]'))
        driver.find_element(By.XPATH, '//span[@class="text" and text()="Frames"]').click()
        head = driver.find_element(By.CLASS_NAME, "text-center")
        assert head.is_displayed()
        driver.execute_script('arguments[0].scrollIntoView();', head)
        driver.switch_to.frame("frame1")
        assert "This is a sample page" in driver.find_element(By.ID, "sampleHeading").text
        driver.switch_to.default_content()
        print(driver.find_element(By.CLASS_NAME, "text-center").text)
        driver.switch_to.frame("frame2")
        assert "This is a sample page" in driver.find_element(By.ID, "sampleHeading").text
        driver.quit()
        print("Success")

    def test_widgets(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(5):
            try:
                wid = driver.find_element(By.CSS_SELECTOR, "div span.pr-1")
                driver.execute_script('arguments[0].scrollIntoView();', wid)
            except:
                body.send_keys(Keys.PAGE_DOWN)
                sleep(3)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.XPATH, "//span[@class='text' and text()='Auto Complete']")))
        body.send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.XPATH, "//span[@class='text' and text()='Auto Complete']").click()
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        auto1 = driver.find_element(By.ID, 'autoCompleteMultipleContainer')
        ac = ActionChains(driver)
        ac.click(auto1).send_keys('B').perform()
        wait = WebDriverWait(driver, 5)
        wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="auto-complete__menu css-26l3qy-menu"]')))
        black = driver.find_element(By.XPATH,
                                    '//div[@class="auto-complete__menu css-26l3qy-menu"]//div[text()="Black"]')
        black.click()
        vals = driver.find_elements(By.XPATH,
                                    '//div[@id="autoCompleteMultipleContainer"]//div[@class="css-1rhbuit-multiValue auto-complete__multi-value"]')
        assert len(vals) > 0
        driver.quit()
        print('Success')

    def test_date_picker(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(5):
            try:
                wid = driver.find_element(By.CSS_SELECTOR, "div span.pr-1")
                driver.execute_script('arguments[0].scrollIntoView();', wid)
            except:
                body.send_keys(Keys.PAGE_DOWN)
                sleep(3)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.XPATH, "//span[@class='text' and text()='Date Picker']")))
        body.send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.XPATH, "//span[@class='text' and text()='Date Picker']").click()
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        driver.find_element(By.ID, "datePickerMonthYearInput").click()
        mon = Select(driver.find_element(By.XPATH,
                                         '//div[@class="react-datepicker-popper"]//div['
                                         '@class="react-datepicker"]//div['
                                         '@class="react-datepicker__month-container"]//select['
                                         '@class="react-datepicker__month-select"]'))
        mon.select_by_visible_text("August")
        year = Select(driver.find_element(By.XPATH,
                                          '//div[@class="react-datepicker-popper"]//div['
                                          '@class="react-datepicker"]//div['
                                          '@class="react-datepicker__month-container"]//select['
                                          '@class="react-datepicker__year-select"]'))
        year.select_by_value('1998')
        driver.find_element(By.XPATH, '//div[@class="react-datepicker-popper"]//div[@class="react-datepicker"]//div['
                                      '@class="react-datepicker__month-container"]//div['
                                      '@class="react-datepicker__month"]//div[@class="react-datepicker__day '
                                      'react-datepicker__day--024"]').click()
        driver.find_element(By.ID, 'dateAndTimePickerInput').click()
        target_time = "11.45"
        time_list = driver.find_element(By.XPATH, '//div[@id="dateAndTimePicker"]//div['
                                                  '@class="react-datepicker-popper"]//div['
                                                  '@class="react-datepicker__time-container "]//ul['
                                                  '@class="react-datepicker__time-list"]')
        while True:
            try:
                target_element = driver.find_element(By.XPATH, "//li[text()='11.45']")
                target_element.click()
                print("Time selected:", target_time)
                break
            except:
                driver.execute_script("arguments[0].scrollTop += 50;", time_list)
                sleep(0.5)

    def test_slider(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(6):
            try:
                slider = driver.find_element(By.XPATH, '//ul[@class="menu-list"]//li/span[text()="Slider"]')
                driver.execute_script("arguments[0].scrollIntoView();", slider)
                slider.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
                sleep(0.5)
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        slider = driver.find_element(By.XPATH, '//div[@id="sliderContainer"]//span[@class="range-slider__wrap"]')
        ac = ActionChains(driver)
        ac.drag_and_drop_by_offset(slider, 70, 0).perform()  # OR
        ac.click_and_hold(slider).pause(1).move_by_offset(-70, 0).release().perform()
        sleep(5)
        print("Success")

    def test_tooltip(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(7):
            try:
                tip = driver.find_element(By.XPATH, '//ul[@class="menu-list"]//span[text()="Tool Tips"]')
                driver.execute_script('arguments[0].scrollIntoView();', tip)
                tip.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        but1 = driver.find_element(By.ID, 'toolTipButton')
        ActionChains(driver).move_to_element(but1).perform()
        but2 = driver.find_element(By.ID, 'toolTipTextField')
        ActionChains(driver).move_to_element(but2).perform()
        print('Success')

    def test_menu(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(7):
            try:
                menu = driver.find_element(By.XPATH, '//ul[@class="menu-list"]//span[text()="Menu"]')
                driver.execute_script('arguments[0].scrollIntoView();', menu)
                menu.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        menu2 = driver.find_element(By.LINK_TEXT, 'Main Item 2')
        ActionChains(driver).move_to_element(menu2).perform()
        but2 = driver.find_element(By.PARTIAL_LINK_TEXT, 'SUB SUB LIST')
        ActionChains(driver).move_to_element(but2).perform()
        sub2 = driver.find_element(By.PARTIAL_LINK_TEXT, "Sub Sub Item 2")
        ActionChains(driver).move_to_element(sub2).perform()
        print('Success')

    def test_resize(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(7):
            try:
                menu = driver.find_element(By.XPATH, '//ul[@class="menu-list"]//span[text()="Resizable"]')
                driver.execute_script('arguments[0].scrollIntoView();', menu)
                menu.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        previous_size = driver.find_element(By.CSS_SELECTOR, 'div#resizableBoxWithRestriction').get_attribute('style')
        print(previous_size)
        arrow = driver.find_element(By.CSS_SELECTOR, 'div#resizableBoxWithRestriction '
                                                     'span.react-resizable-handle.react-resizable-handle-se')
        ActionChains(driver).click_and_hold(arrow).move_by_offset(389, 230).release().perform()
        current_size = driver.find_element(By.CSS_SELECTOR, 'div#resizableBoxWithRestriction').get_attribute('style')
        print(current_size)
        print('Success')

    # below method is not working
    def test_drag_drop(self):
        driver = self.driver
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(7):
            try:
                menu = driver.find_element(By.XPATH, '//ul[@class="menu-list"]//span[text()="Droppable"]')
                driver.execute_script('arguments[0].scrollIntoView();', menu)
                menu.click()
                break
            except:
                body.send_keys(Keys.PAGE_DOWN)
        head = driver.find_element(By.CLASS_NAME, "text-center")
        driver.execute_script('arguments[0].scrollIntoView();', head)
        some = driver.find_element(By.ID, 'droppableExample-tab-accept')
        some.click()
        driver.execute_script('arguments[0].scrollIntoView();', some)
        body = driver.find_element(By.TAG_NAME, "body")
        ActionChains(driver).move_to_element(body).click().perform()
        not_ac = driver.find_element(By.ID, 'notAcceptable')
        acc = driver.find_element(By.ID, 'acceptable')
        wait = WebDriverWait(driver, 10)
        drop_able = wait.until(ec.presence_of_element_located((By.ID, "droppable")))
        drop_able = driver.find_element(By.ID, 'droppable')
        ac = ActionChains(driver)
        # ac.drag_and_drop(not_ac, drop_able).perform()
        ac.click_and_hold(acc).drag_and_drop(acc, drop_able).release().perform()
        assert drop_able.text == 'Dropped!', "failed to drop"
        sleep(10)

if __name__ == "__main__":
    g = GetLink()
    g.test_an_element_cate()
    g.test_drag_drop()
