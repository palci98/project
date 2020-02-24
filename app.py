#!/usr/bin/python3

import argparse  
import hashlib
from src.parse import *
from src.errors import *
from src.storage import *

def argument_parse():


    parser = argparse.ArgumentParser()

    parser.add_argument("source", nargs='?', default="Brno hl.n.",
                        help="From where you going?")
    parser.add_argument("destination", nargs='?', default="Handlová",
                        help="Where you going?")
    parser.add_argument("date", nargs='?', default=datetime.now().strftime("%d.%m.%Y"),
                        help="Date: DD.MM.YEAR")
    parser.add_argument("time", nargs='?', default=datetime.now().strftime("%H:%M"),
                        help="time: HH:MM")
    args = parser.parse_args()
    
    validate_date_time(args.date, args.time)
    
    return args

def main():


    args = argument_parse()
    redis_hash = hashlib.sha1(str.encode(args.source
                                         + args.destination 
                                         + args.date 
                                         + args.time)).hexdigest()

    if not redis_load(redis_hash):
        print("searching for connection online")
        page = get_connection(args.source, args.destination, args.date, args.time)
        
        if not page:
            raise ValueError("Not supported city name")
        
        json_data = get_data(page)
        redis_save(json_data, redis_hash)        
        data_frame=pandas.DataFrame(json_data)
        print(data_frame.transpose())
        
if __name__ == "__main__":
    main()
