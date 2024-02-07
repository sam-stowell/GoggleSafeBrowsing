import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from pysafebrowsing import SafeBrowsing
from PyQt5.QtWidgets import QMessageBox

from config import lockimage, nextimage, stopimage, unlockimage, previmage, refreshimage, homeimage, iconimage, \
  searchimage, default_browser


# creates window
class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    #connection to parent class
    super(MainWindow, self).__init__(*args, **kwargs)
    # sets the browser to the web engine view
    self.browser = QWebEngineView()
    # sets the default page to google for startup
    self.browser.setUrl(QUrl("https://goggle.com"))
    # sets the central widget of the UI to the browser and in web engine view
    self.setCentralWidget(self.browser)
    # maximises the window
    self.showMaximized()

    # navigation bar set up as a toolbar
    nav_bar = QToolBar()
    # adds the navigation toolbar to the top of the screen
    self.addToolBar(nav_bar)

    # back button action being set up
    back_button = QAction('Prev', self)
    # back button hover over tip
    back_button.setStatusTip("Back to the previous page")
    # back button connecting the the actual function sending the browser back
    back_button.triggered.connect(self.browser.back)
    # adding the back button to the navigation toolbar
    nav_bar.addAction(back_button)

    # forward button action being set up
    forward_button = QAction('Next', self)
    # forward button hover over tip
    forward_button.setStatusTip("Forward to the next page")
    # forward button connecting the the actual function sending the browser forward
    forward_button.triggered.connect(self.browser.forward)
    # adding the forward button to the navigation toolbar
    nav_bar.addAction(forward_button)

    # refresh button action being set up
    refresh_button = QAction('Refresh', self)
    # refresh button connecting the the actual function getting the browser to refresh
    refresh_button.triggered.connect(self.browser.reload)
    # adding the refresh button to the navigation toolbar
    nav_bar.addAction(refresh_button)

    # home button action being set up
    home_button = QAction('Home', self)
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
    # adding the search bar to the navigation toolbar
    nav_bar.addWidget(self.urlbar)

    # search button action being set up
    search_button = QAction('Search', self)
    # search button connecting the the actual function getting the browser to search
    search_button.triggered.connect(self.navigate_to_url)
    # adding the search button to the navigation toolbar
    nav_bar.addAction(search_button)

    # stop button action being set up
    stop_button = QAction("Stop", self)
    # stop button hover over tip
    stop_button.setStatusTip("Stop loading current page")
    # stop button connecting the the actual function getting the browser to stop
    stop_button.triggered.connect(self.browser.stop)
    # adding the stop button to the navigation toolbar
    nav_bar.addAction(stop_button)

  def home(self):
    # sets the home button to the url google
    self.browser.setUrl(QUrl("https://goggle.com"))

  def navigate_to_url(self):
    # sets q to the url the user will type into the search bar
    q = QUrl(self.urlbar.text())
    # the url being searched is checked if it starts with http
    if q.scheme() == "":
      # the url is changed to include http at the start
      q.setScheme("http")

      # sets the url being searched to what the user has typed into the search bar
      self.browser.setUrl(QUrl(q))
      # updates the urlbar
      self.browser.urlChanged.connect(self.update_urlbar)
      # when the load finishes the title is updated
      self.browser.loadFinished.connect(self.update_title)

  def update_urlbar(self, q):
    # if the url starts with https
    if q.scheme() == 'https':
      # sets the https icon to the secure image from the config file path
      self.httpsicon.setPixmap(QPixmap(lockimage))

    # if the url doesnt start with https
    else:
      # sets the https icon to the not secure image from the config file path
      self.httpsicon.setPixmap(QPixmap(unlockimage))

    # sets the url bar text to the users url searched
    self.urlbar.setText(q.toString())
    # sets the url bar cursors position to the start
    self.urlbar.setCursorPosition(0)

  def update_title(self):
    # sets the title to the browsers page title
    title = self.browser.page().title()
    # sets the window to "title - test"
    self.setWindowTitle("%s - test" % title)


# executes app
app = QApplication(sys.argv)
# sets the application display name at the top of the screen to test
app.setApplicationName("test")
# sets the main window
window = MainWindow()
# shows the main window
window.show()
app.exec()

