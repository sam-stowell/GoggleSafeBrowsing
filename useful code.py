# # search bar
# self.searchBar = QLineEdit()
# self.searchBar.returnPressed.connect(self.load_url)
# nav_bar.addWidget(self.searchBar)
# self.browser.urlChanged.connect(self.update_url)

# # loads url for search bar
# def load_url(self):
#     url = self.searchBar.text()
#     self.browser.setUrl(QUrl(url))
#
# # updates url for search bar
# def update_url(self, url):
#   self.searchBar.setText(url.toString())

# print("i am dumb")

# # tab bar
# tab_bar = QToolBar()
# self.addToolBar(tab_bar)
#
# tab_button = QAction(QIcon(stopimage), "Stop", self)
# tab_button.setStatusTip("Stop loading current page")
# tab_button.triggered.connect(self.browser.stop)
# tab_bar.addAction(tab_button)

# # tabs
# self.tabs = QTabWidget()
# self.tabs.setDocumentMode(True)
# self.tabs.setTabsClosable(True)
#
# self.setCentralWidget(self.tabs)
#
# self.add_new_tab(QUrl('http://google.com'), 'Homepage')
#
# self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

# file_menu = self.menuBar().addMenu("&File")
# new_tab_action = QAction(QIcon(stopimage), "New Tab")
# new_tab_action.setStatusTip("Open a new tab")
# file_menu.addAction(new_tab_action)

#AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U

# from gglsbl3 import SafeBrowsingList
# sbl = SafeBrowsingList('AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U')
# sbl.lookup_url('http://github.com/')

# from pysafebrowsing import SafeBrowsing
# s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
# r = s.lookup_urls(['http://malware.testing.google.test/testing/malware/'])
# print(r)
#
# e = s.lookup_urls(['http://bing.com'])
# print(e)

# from safesearch import safe_search
# tested_url_results = safe_search()
# if tested_url_results == True:
#     print("oke")


# searchbar_url = "http://malware.testing.google.test/testing/malware/"
# print("The site you are trying to access",searchbar_url,"has been flagged as potentially malicious.")


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Hello World')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


# tabs
    self.tabs = QTabWidget()
    self.tabs.setDocumentMode(True)
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.close_current_tab)
    self.setCentralWidget(self.tabs)

    self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

    self.showMaximized()

    self.add_new_tab(QUrl('http://google.com'), 'Homepage')