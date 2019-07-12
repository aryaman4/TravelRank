from src.backend.Rank import Rank
from src.backend.Request import Request
from src.backend.filter import Filter
import pandas as pd
from src.backend.utils import *
import time
count = 0
st_date = '2019-03-15'
end_date = '2019-03-25'

main_dict = {}
main_dict['total_time'] = list()
main_dict['flight_price'] = list()
main_dict['hotel_price'] = list()

while count < 10:
    print(count)
    #req = Request(current_city=Request.get_all_cities()[count], st_date=st_date, end_date=end_date, max_hbudget='1000', max_fbudget=1000)
    fil = Filter(current_city=Request.get_all_cities()[count], locations=Request.get_all_cities(), start=st_date, end=end_date, num_people='1')
    rank = Rank(fil.request, fil)
    start = time.time()
    rank.create_location_dict()
    end = time.time()
    print(end - start)
    c = 0
    for hotel, flight in rank.location_dict.values():
        hname, hprice = hotel
        f, info = flight
        price, ftime = info
        main_dict['hotel_price'].append(hprice)
        main_dict['flight_price'].append(price)
        arr, dep = ftime
        main_dict['total_time'].append(arr+dep)
        if c == 10:
            break
        c+=1
    count += 1

df = pd.DataFrame.from_dict(main_dict)

print(df)

df.to_csv("data.csv")



