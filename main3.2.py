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


# creates window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # connection to parent class
        super(MainWindow, self).__init__(*args, **kwargs)
        # sets the browser to the web engine view
        self.browser = QWebEngineView()
        # sets the default page from config for startup
        self.browser.setUrl(QUrl(default_browser))
        # sets the central widget of the UI to the browser and in web engine view
        self.setCentralWidget(self.browser)
        # sets the colour scheme of the browser using CSS
        self.setStyleSheet("background-color: #5c5c5c;")
        # maximises the window
        self.showMaximized()

        # navigation bar set up as a toolbar
        nav_bar = QToolBar()
        # adds the navigation toolbar to the top of the screen
        self.addToolBar(nav_bar)

        # back button action being set up with an icon now from the config file path
        back_button = QAction(QIcon(previmage), 'Prev', self)
        # back button hover over tip
        back_button.setStatusTip("Back to the previous page")
        # back button connecting the the actual function sending the browser back
        back_button.triggered.connect(self.browser.back)
        # adding the back button to the navigation toolbar
        nav_bar.addAction(back_button)

        # forward button action being set up with an icon now from the config file path
        forward_button = QAction(QIcon(nextimage), 'Next', self)
        # forward button hover over tip
        forward_button.setStatusTip("Forward to the next page")
        # forward button connecting the the actual function sending the browser forward
        forward_button.triggered.connect(self.browser.forward)
        # adding the forward button to the navigation toolbar
        nav_bar.addAction(forward_button)

        # refresh button action being set up with an icon now from the config file path
        refresh_button = QAction(QIcon(refreshimage), 'Refresh', self)
        # refresh button connecting the the actual function getting the browser to refresh
        refresh_button.triggered.connect(self.browser.reload)
        # adding the refresh button to the navigation toolbar
        nav_bar.addAction(refresh_button)

        # home button action being set up with an icon now from the config file path
        home_button = QAction(QIcon(homeimage), 'Home', self)
        # home button connecting the the actual function getting the browser to return home
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
        stop_button.triggered.connect(self.browser.stop)
        # adding the stop button to the navigation toolbar
        nav_bar.addAction(stop_button)

    def home(self):
        self.browser.setUrl(QUrl(default_browser))

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

            # defaults back to default browser page
            self.browser.setUrl(QUrl(default_browser))
            self.browser.urlChanged.connect(self.update_urlbar)
            self.browser.loadFinished.connect(self.update_title)

        elif lookup_malicious_results == False:
            # if malware is not there then the site is loaded
            self.browser.setUrl(QUrl("http://google.com"))
            print(searchbar_url)
            ########################################################################################################################################################################### above - 156 broken
            self.browser.urlChanged.connect(self.update_urlbar)
            self.browser.loadFinished.connect(self.update_title)
            self.setCentralWidget(self.browser)
        else:
            # if it breaks
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
    def update_urlbar(self, q):
        if q.scheme() == 'https':
            # secure
            self.httpsicon.setPixmap(QPixmap(lockimage))

        else:
            # not secure
            self.httpsicon.setPixmap(QPixmap(unlockimage))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

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


# executes app set up
app = QApplication(sys.argv)
# sets the application display name at the top of the screen to test
app.setApplicationName("test")
# sets app icon
app.setWindowIcon(QIcon(iconimage))
# sets the main window
window = MainWindow()
# shows the main window
window.show()
# executes app
app.exec()
