from selenium import webdriver
import json, time
import webbrowser

#get_video_results HEAVILY uses this tutorial on youtube web scraping (changed so it just returns top link, no longer in JSON format)
#had to edit as code was slightly outdated with new release of selenium
#https://medium.com/geekculture/scrape-youtube-search-with-python-part-1-7521a0f40315 
def get_video_results(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    youtube_data = []
    num_of_results = 0
    # scrolling to the end of the page
    # https://stackoverflow.com/a/57076690/15164646

    while True:
        # end_result = "No more results" string at the bottom of the page
        # this will be used to break out of the while loop
        end_result = driver.find_element("css selector", '#message').is_displayed()
        driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")

        # once element is located, break out of the loop
        if end_result == True:
            break
        else:
            num_of_results += 1
        if num_of_results == 1:
            break
    num_of_results = 0
    for result in driver.find_elements("css selector", '.text-wrapper.style-scope.ytd-video-renderer'):
        if num_of_results >= 1:
            break
        link = result.find_element("css selector", '.title-and-badge.style-scope.ytd-video-renderer a').get_attribute('href')
        youtube_data = link
        num_of_results+=1
    
    driver.quit()
    return youtube_data

#Takes in a string query like "How to saute onions" and returns a youtube url query
def youtube_url_fixer(query):
    youtube_base_link = 'https://www.youtube.com/results?search_query='
    query = query.lower()
    query_words = query.split(' ')
    youtube_query = ""
    for i in range(len(query_words)):
        word = query_words[i]
        if i < len(query_words) - 1:
            youtube_query = youtube_query + word + "+"
        else:
            youtube_query = youtube_query + word
    return youtube_base_link + youtube_query

def open_youtube_video(query):
    url = youtube_url_fixer(query)
    link = get_video_results(url)
    webbrowser.open(link)



#print(youtube_url_fixer("How to saute onions"))
#get_video_results('https://www.youtube.com/results?search_query=how+to+saute+onions')

