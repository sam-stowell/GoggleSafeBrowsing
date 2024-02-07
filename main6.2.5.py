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

        # back button
        back_button = QAction(QIcon(previmage), 'Prev', self)
        back_button.setStatusTip("Back to the previous page")
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_bar.addAction(back_button)

        # forward button
        forward_button = QAction(QIcon(nextimage), 'Next', self)
        forward_button.setStatusTip("Forward to the next page")
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav_bar.addAction(forward_button)

        # refresh button
        refresh_button = QAction(QIcon(refreshimage), 'Refresh', self)
        refresh_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        nav_bar.addAction(refresh_button)

        # home button
        home_button = QAction(QIcon(homeimage), 'Home', self)
        home_button.triggered.connect(self.home)
        nav_bar.addAction(home_button)

        # https secure
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(lockimage))
        nav_bar.addWidget(self.httpsicon)

        # # https secure
        # httpsicon = QAction(QIcon(lockimage), "stop", self)
        # httpsicon.triggered.connect(self.browser.stop)
        # nav_bar.addAction(httpsicon)

        # search bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # white border changed to black
        self.urlbar.setStyleSheet("border :1px solid ;")
        nav_bar.addWidget(self.urlbar)

        # search button
        search_button = QAction(QIcon(searchimage), 'Search', self)
        search_button.triggered.connect(self.navigate_to_url)
        nav_bar.addAction(search_button)

        # stop button
        stop_button = QAction(QIcon(stopimage), "Stop", self)
        stop_button.setStatusTip("Stop loading current page")
        stop_button.triggered.connect(self.browser.stop)
        nav_bar.addAction(stop_button)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # when tab bar is double clicked another tab is created
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # maximise window
        self.showMaximized()

        # adds a tab
        self.add_new_tab(QUrl(default_browser), 'Homepage')

    def home(self):
        self.tabs.currentWidget().setUrl(QUrl(default_browser))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        # the url being searched is taken
        searchbar_url = (self.urlbar.text())
        print(searchbar_url)

        if q.scheme() == "":
            q.setScheme("http")

            # if the url has no http then it is added
            searchbar_url = "http://" + searchbar_url

        # using pysafebrowsing to search the url to check with the google api and send back a result True or False
        print(searchbar_url)
        s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
        # looking up the url
        lookup = s.lookup_urls([searchbar_url])
        # printing the dictionary
        print(lookup)
        # printing the dictionary inside the dictionary
        lookup_results = lookup[searchbar_url]
        print(lookup_results)
        # printing the 'malicious' value in the dictionary
        lookup_malicious_results = lookup_results['malicious']
        print(lookup_malicious_results)

        if lookup_malicious_results == True:
            # if malware is there then the site is not loaded
            print("malware detected")
            # shows the user malware is detected
            msg = QMessageBox()
            # msg.setsetStyleSheet("background-color: grey;")
            msg.setWindowTitle("ALERT!")
            msg.setText("MALWARE DETECTED")
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText("What would you like to do?")

            # creates message for the extra details on the popup
            detailedtext = ("The site you are trying to access ") + (searchbar_url) + (
                " has been flagged as potentially malicious.")
            print(detailedtext)
            msg.setDetailedText(detailedtext)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(self.popup_clicked)

            x = msg.exec_()

            malwaredetect = searchbar_url

            tz_london = pytz.timezone('Europe/London')
            datetime_london = datetime.now(tz_london)
            print("London time:", datetime_london.strftime("%H:%M:%S"))

            f = open("malware_report.txt", "a")
            f.write("\n" + "\n" + "Malicious site detected" + "\n")
            f.write(" - - - - - - - " + "\n")
            f.write("Malicious site: " + malwaredetect + "\n")
            f.write("Time of search request (London time): " + datetime_london.strftime("%H:%M:%S") + "\n")
            f.close()

            # open and read the file after the appending:
            f = open("malware_report.txt", "r")
            print(f.read())

            # defaults back to default browser page
            self.tabs.currentWidget().setUrl(QUrl(default_browser))
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)


        elif lookup_malicious_results == False:
            # if malware is not there then the site is loaded
            self.tabs.currentWidget().setUrl(q)
            print(searchbar_url)

            # # used to connect to url
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)
        else:
            # if the program breaks
            print("error with url")

    def popup_clicked(self, i):
        print(i.text())

    # asks the user if they want to quit or not
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # updates the url bar and adds a lock or unlock depending on how secure the site is
    def update_urlbar(self, q, browser=None):

        # obtains the url of the current page and converts to string
        currenturl = browser.url().toString()

        # checks the current url for malicious site
        print(currenturl)
        s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
        # looking up the url
        lookup = s.lookup_urls([currenturl])
        # printing the dictionary
        print(lookup)
        # printing the dictionary inside the dictionary
        lookup_results = lookup[currenturl]
        print(lookup_results)
        # printing the 'malicious' value in the dictionary
        lookup_malicious_results = lookup_results['malicious']
        print(lookup_malicious_results)

        if lookup_malicious_results == True:
            # if malware is there then the site is not loaded
            print("malware detected")

            # defaults back to default browser page
            self.tabs.currentWidget().setUrl(QUrl(default_browser))

            # shows the user malware is detected
            msg = QMessageBox()
            # msg.setsetStyleSheet("background-color: grey;")
            msg.setWindowTitle("ALERT!")
            msg.setText("MALWARE DETECTED")
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText("What would you like to do?")

            # creates message for the extra details on the popup
            detailedtext = ("The site you are trying to access ") + (currenturl) + (
                " has been flagged as potentially malicious.")
            print(detailedtext)
            msg.setDetailedText(detailedtext)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(self.popup_clicked)

            x = msg.exec_()

            malwaredetect = currenturl

            tz_london = pytz.timezone('Europe/London')
            datetime_london = datetime.now(tz_london)
            print("London time:", datetime_london.strftime("%H:%M:%S"))

            f = open("malware_report.txt", "a")
            f.write("\n" + "\n" + "Malicious site detected" + "\n")
            f.write(" - - - - - - - " + "\n")
            f.write("Malicious site: " + malwaredetect + "\n")
            f.write("Time of search request (London time): " + datetime_london.strftime("%H:%M:%S") + "\n")
            f.close()

            # open and read the file after the appending:
            f = open("malware_report.txt", "r")
            print(f.read())





        elif lookup_malicious_results == False:
            # if malware is not there then the site is loaded
            self.tabs.currentWidget().setUrl(q)
            print(currenturl)

            # # used to connect to url
            # self.browser.urlChanged.connect(self.update_urlbar)
            # self.browser.loadFinished.connect(self.update_title)
        else:
            # if the program breaks
            print("error with url")

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            # secure
            self.httpsicon.setPixmap(QPixmap(lockimage))

        else:
            # not secure
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
            qurl = QUrl(default_browser)

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    # if the tabs are greater than one then the extra tabs can be closed
    def close_current_tab(self, i):

        # checks the tab amount
        if self.tabs.count() < 2:
            print("tab count is 2")
            return
        else:
            print("tab can be removed")

        # removes a tab
        self.tabs.removeTab(i)

    # used to open a tab when the bar is double clicked
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    # updates title and url bar when a tab is changed
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
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
