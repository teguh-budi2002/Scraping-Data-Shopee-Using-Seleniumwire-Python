import sys
sys.path.append('./module')
from module_scraping import WebScrape
from module_mysql import MySQL

url_shopee="https://shopee.co.id/search?keyword=ssd"
next_page = "&page="
do_scrape = WebScrape(url_shopee, next_page)
data_scrape = do_scrape.execute_scrape_shopee()
# data_frame = do_scrape.convert_to_dataframe(data_scrape)
# to_excel = do_scrape.convert_to_excel("DATA_SHOPEE.xlsx", data_scrape)
print(data_scrape)


# mysql = MySQL()
# conn = mysql.connection()
# # data = mysql.get_all_data_from_table(conn, "users")
# data_list = [{
#   "test_column" : "Testing 1",
#   "test_column_2" : "Test 1"
# }, {"test_column" : "Testing 2",
#   "test_column_2" : "Test 2"}]
# is_added  = mysql.add_data(conn, "testings", data_list)
# print(is_added)
