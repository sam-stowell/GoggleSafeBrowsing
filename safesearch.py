from pysafebrowsing import SafeBrowsing
def safe_search():
    # url being checked
    url_test = 'http://malware.testing.google.test/testing/malware/'
    # api key
    s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
    # looking up the url
    lookup_test = s.lookup_urls([url_test])
    # printing the dictionary
    print(lookup_test)
    # printing the dictionary inside the dictionary
    lookup_results_test = lookup_test[url_test]
    print(lookup_results_test)
    # printing the 'malicious' value in the dictionary
    lookup_malicious_results_test = lookup_results_test['malicious']
    print(lookup_malicious_results_test)
    return lookup_malicious_results_test

    # url being checked
    url = 'http://malware.testing.google.test/testing/malware/'
    # api key
    s = SafeBrowsing("AIzaSyCqKZBZwjuflLwmlNSu3EucvxZjJJdp86U")
    # looking up the url
    lookup = s.lookup_urls([url])
    # printing the dictionary
    print(lookup)
    # printing the dictionary inside the dictionary
    lookup_results = lookup[url]
    print(lookup_results)
    # printing the 'malicious' value in the dictionary
    lookup_malicious_results = lookup_results['malicious']
    print(lookup_malicious_results)
    return lookup_malicious_results

    # e = s.lookup_urls(['http://bing.com'])
    # print("e", e)
    # return e
safe_search()