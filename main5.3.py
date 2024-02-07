import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from pysafebrowsing import SafeBrowsing
from PyQt5.QtWidgets import QMessageBox

# imports images used for the browser as well as the user's settings such as default browser
from config import lockimage, nextimage, stopimage, unlockimage, previmage, refreshimage, homeimage, iconimage, \
    searchimage, default_browser

from datetime import datetime
import pytz


# creates window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # connection to parent class
        super(MainWindow, self).__init__(*args, **kwargs)

        # setup for the browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(default_browser))
        self.setCentralWidget(self.browser)
        self.setStyleSheet("background-color: #5c5c5c;")
        self.showMaximized()

        # navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        # back button action being set up
        back_button = QAction(QIcon(previmage), 'Prev', self)
        # back button hover over tip
        back_button.setStatusTip("Back to the previous page")
        # back button connecting the the actual function sending the tab back
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        # adding the back button to the navigation toolbar
        nav_bar.addAction(back_button)

        # forward button action being set up
        forward_button = QAction(QIcon(nextimage), 'Next', self)
        # forward button hover over tip
        forward_button.setStatusTip("Forward to the next page")
        # forward button connecting the the actual function sending the tab forward
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        # adding the forward button to the navigation toolbar
        nav_bar.addAction(forward_button)

        # refresh button action being set up
        refresh_button = QAction(QIcon(refreshimage), 'Refresh', self)
        # refresh button connecting the the actual function getting the tab to refresh
        refresh_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        # adding the refresh button to the navigation toolbar
        nav_bar.addAction(refresh_button)

        # home button action being set up
        home_button = QAction(QIcon(homeimage), 'Home', self)
        # home button connecting the the actual function getting the tab to return home
        home_button.triggered.connect(self.home)
        # adding the home button to the navigation toolbar
        nav_bar.addAction(home_button)

        # https secure being set to a label rather than action button
        self.httpsicon = QLabel()
        # setting the https icons actual image being lockimage path from the config file
        self.httpsicon.setPixmap(QPixmap(lockimage))
        # adding the https secure image to the navigation toolbar
        nav_bar.addWidget(self.httpsicon)

        # search bar being set up as an editable box
        self.urlbar = QLineEdit()
        # search bar connecting the the actual function getting the browser search (navigate to url)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # url bar white border changed to black
        self.urlbar.setStyleSheet("border :1px solid ;")
        # adding the search bar to the navigation toolbar
        nav_bar.addWidget(self.urlbar)

        # search button action being set up with an icon now from the config file path
        search_button = QAction(QIcon(searchimage), 'Search', self)
        # search button connecting the the actual function getting the browser to search
        search_button.triggered.connect(self.navigate_to_url)
        # adding the search button to the navigation toolbar
        nav_bar.addAction(search_button)

        # stop button action being set up with an icon now from the config file path
        stop_button = QAction(QIcon(stopimage), "Stop", self)
        # stop button hover over tip
        stop_button.setStatusTip("Stop loading current page")
        # stop button connecting the the actual function getting the browser to stop
        stop_button.triggered.connect(lambda: self.tabs.currentWidget().stop())
        # adding the stop button to the navigation toolbar
        nav_bar.addAction(stop_button)

        # tabs setup adding a tab widget
        self.tabs = QTabWidget()
        # sets the tabs to document mode to render the page
        self.tabs.setDocumentMode(True)
        # sets the tabs to be able to be closed
        self.tabs.setTabsClosable(True)
        # the functionality for the rab close request when the user presses the x
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # sets the tab to central widget
        self.setCentralWidget(self.tabs)

        # when tab bar is double clicked another tab is created
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # maximise window
        self.showMaximized()

        # adds a tab with the default browser home page from the config and names the tab homepage
        self.add_new_tab(QUrl(default_browser), 'Homepage')

    def home(self):
        self.tabs.currentWidget().setUrl(QUrl(default_browser))

    def navigate_to_url(self):
        # sets q to the url the user will type into the search bar
        q = QUrl(self.urlbar.text())
        # the url being searched is taken
        searchbar_url = (self.urlbar.text())
        print(searchbar_url)

        # the url being searched is checked if it starts with http
        if q.scheme() == "":
            # the url is changed to include http at the start
            q.setScheme("http")

            # if the url has no http then it is added
            searchbar_url = "http://" + searchbar_url

        # using pysafebrowsing to search the url to check with the google api and send back a result True or False
        print(searchbar_url)
        # sets s to the safe browsing api key
        s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
        # looking up the url with the api
        lookup = s.lookup_urls([searchbar_url])
        # printing the dictionary
        print(lookup)
        # printing the dictionary inside the dictionary
        lookup_results = lookup[searchbar_url]
        print(lookup_results)
        # printing the 'malicious' value in the dictionary
        lookup_malicious_results = lookup_results['malicious']
        # should print true or false
        print(lookup_malicious_results)

        if lookup_malicious_results == True:
            # if malware is there then the site is not loaded
            print("malware detected")
            # shows the user malware is detected in a popup box
            msg = QMessageBox()
            # msg.setsetStyleSheet("background-color: grey;")
            # sets the popupbox title to alert
            msg.setWindowTitle("ALERT!")
            # sets the popup box sub text to malware detected
            msg.setText("MALWARE DETECTED")
            # sets the popup box icon to the critical icon from the library
            msg.setIcon(QMessageBox.Critical)
            # sets the text description in the popup box
            msg.setInformativeText("What would you like to do?")

            # creates message for the extra details on the popup
            detailedtext = ("The site you are trying to access ") + (searchbar_url) + (
                " has been flagged as potentially malicious.")
            print(detailedtext)
            # sets the detailed text to the message
            msg.setDetailedText(detailedtext)
            # sets the other options of the popup box
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # sets the default selected button in the popup box
            msg.setDefaultButton(QMessageBox.Ok)
            # sets the action of the popup box to the button the user clicks
            msg.buttonClicked.connect(self.popup_clicked)
            # executest the popup box
            x = msg.exec_()

            # sets the malware detected to the searchbar url
            malwaredetect = searchbar_url

            # sets tz_london to the timezone for the current time for Europe/London
            tz_london = pytz.timezone('Europe/London')
            # gets the time for the current timezone (london)
            datetime_london = datetime.now(tz_london)
            # print statement for testing
            print("London time:", datetime_london.strftime("%H:%M:%S"))

            # opens the malware report and appends or if there is none then creates the file
            f = open("malware_report.txt", "a")
            # writes the first section of the report so the title
            f.write("\n" + "\n" + "Malicious site detected" + "\n")
            f.write(" - - - - - - - " + "\n")
            # writes the content of the report which is the url of the site
            f.write("Malicious site: " + malwaredetect + "\n")
            # writes the time the attemted accessed to the site with the timezone
            f.write("Time of search request (London time): " + datetime_london.strftime("%H:%M:%S") + "\n")
            f.close()

            # open and read the file after the appending:
            f = open("malware_report.txt", "r")
            # prints statement to test if the contents of the file were written
            print(f.read())

            # defaults back to default browser page
            self.tabs.currentWidget().setUrl(QUrl(default_browser))
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)


        elif lookup_malicious_results == False:
            # if malware is not there then the site is loaded with the site being the variable q
            self.tabs.currentWidget().setUrl(q)
            print(searchbar_url)

            # # used to connect to url
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)
        else:
            # if the program breaks
            print("error with url")

    def popup_clicked(self, i):
        # print the popup text
        print(i.text())

    # asks the user if they want to quit or not
    def closeEvent(self, event):
        # sets the popup box options with the details too
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        # if yes is clicked the popup box closes the app
        if reply == QMessageBox.Yes:
            event.accept()
        # if not then the app stays on
        else:
            event.ignore()

    # updates the url bar and adds a lock or unlock depending on how secure the site is
    def update_urlbar(self, q, browser=None):

        # obtains the url of the current page and converts to string
        currenturl = browser.url().toString()
        print(currenturl)

        # the url being searched is checked if it starts with http
        if q.scheme() == "":
            # the url is changed to include http at the start
            q.setScheme("http")

            # if the url has no http then it is added
            currenturl = "http://" + currenturl

        # using pysafebrowsing to search the url to check with the google api and send back a result True or False
        print(currenturl)
        # sets s to the safe browsing api key
        s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
        # looking up the url with the api
        lookup = s.lookup_urls([currenturl])
        # printing the dictionary
        print(lookup)
        # printing the dictionary inside the dictionary
        lookup_results = lookup[currenturl]
        print(lookup_results)
        # printing the 'malicious' value in the dictionary
        lookup_malicious_results = lookup_results['malicious']
        # should print true or false
        print(lookup_malicious_results)

        if lookup_malicious_results == True:
            # if malware is there then the site is not loaded
            print("malware detected")
            # defaults back to default browser page
            self.tabs.currentWidget().setUrl(QUrl(default_browser))
            # shows the user malware is detected in a popup box
            msg = QMessageBox()
            # msg.setsetStyleSheet("background-color: grey;")
            # sets the popupbox title to alert
            msg.setWindowTitle("ALERT!")
            # sets the popup box sub text to malware detected
            msg.setText("MALWARE DETECTED")
            # sets the popup box icon to the critical icon from the library
            msg.setIcon(QMessageBox.Critical)
            # sets the text description in the popup box
            msg.setInformativeText("What would you like to do?")

            # creates message for the extra details on the popup
            detailedtext = ("The site you are trying to access ") + (currenturl) + (
                " has been flagged as potentially malicious.")
            print(detailedtext)
            # sets the detailed text to the message
            msg.setDetailedText(detailedtext)
            # sets the other options of the popup box
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # sets the default selected button in the popup box
            msg.setDefaultButton(QMessageBox.Ok)
            # sets the action of the popup box to the button the user clicks
            msg.buttonClicked.connect(self.popup_clicked)
            # executest the popup box
            x = msg.exec_()

            # sets the malware detected to the searchbar url
            malwaredetect = currenturl

            # sets tz_london to the timezone for the current time for Europe/London
            tz_london = pytz.timezone('Europe/London')
            # gets the time for the current timezone (london)
            datetime_london = datetime.now(tz_london)
            # print statement for testing
            print("London time:", datetime_london.strftime("%H:%M:%S"))

            # opens the malware report and appends or if there is none then creates the file
            f = open("malware_report.txt", "a")
            # writes the first section of the report so the title
            f.write("\n" + "\n" + "Malicious site detected" + "\n")
            f.write(" - - - - - - - " + "\n")
            # writes the content of the report which is the url of the site
            f.write("Malicious site: " + malwaredetect + "\n")
            # writes the time the attemted accessed to the site with the timezone
            f.write("Time of search request (London time): " + datetime_london.strftime("%H:%M:%S") + "\n")
            f.close()

            # open and read the file after the appending:
            f = open("malware_report.txt", "r")
            # prints statement to test if the contents of the file were written
            print(f.read())


            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)


        elif lookup_malicious_results == False:
            # if malware is not there then the site is loaded with the site being the variable q
            self.tabs.currentWidget().setUrl(q)
            print(currenturl)

            # # used to connect to url
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)
        else:
            # if the program breaks
            print("error with url")




        # if the browser is not the tab current widget
        if browser != self.tabs.currentWidget():
            return

        # if the url starts with https
        if q.scheme() == 'https':
            # sets the https icon to the secure image from the config file path
            self.httpsicon.setPixmap(QPixmap(lockimage))

        # if the url doesnt start with https
        else:
            # sets the https icon to the not secure image from the config file path
            self.httpsicon.setPixmap(QPixmap(unlockimage))

        #self.urlbar.setText(q.toString())
        #self.urlbar.setCursorPosition(0)

    # updates the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - test" % title)

    # adds a new tab for the browser
    def add_new_tab(self, qurl=None, label="Blank"):
        # check url
        if qurl is None:
            # sets the url to the default browser
            qurl = QUrl(default_browser)

        # sets the browser to be web engine view
        browser = QWebEngineView()
        # sets the browser url to the url from above
        browser.setUrl(qurl)

        # adds a new tab and labels it
        i = self.tabs.addTab(browser, label)
        # sets the tab in the right place
        self.tabs.setCurrentIndex(i)

        # when url is changed te tab url and urlbar will be changed
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        # when the load finisbes tbe tab text will be set to the browser page title
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    # if the tabs are greater than one then the extra tabs can be closed
    def close_current_tab(self, i):

        # checks the tab amount
        if self.tabs.count() < 2:
            # print statements for testing
            print("tab count is 2")
            return
        else:
            # print statements for testing
            print("tab can be removed")

        # functionality for removing the tab
        self.tabs.removeTab(i)

    # used to open a tab when the bar is double clicked
    def tab_open_doubleclick(self, i):
        if i == -1:
            # functionality for adding the tab
            self.add_new_tab()

    # updates title and url bar when a tab is changed
    def current_tab_changed(self, i):
        # sets qurl to the tab current url
        qurl = self.tabs.currentWidget().url()
        # updates url bar to the current url
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # updates title to the current title
        self.update_title(self.tabs.currentWidget())



# executes app
app = QApplication(sys.argv)

# sets app name
app.setApplicationName("Google - test")

# sets app icon
app.setWindowIcon(QIcon(iconimage))

# makes app fullscreen
window = MainWindow()
window.show()
app.exec()
