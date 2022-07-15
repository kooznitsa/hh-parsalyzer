from helpers import *
from parser_id import get_ids
from parser_ads import get_listings


get_ids(area=cities['Москва'], metro=msk_metro, filename='data/jul-22/hh-id-msk')
get_ids(area=cities['Санкт-Петербург'], metro=spb_metro, filename='data/jul-22/hh-id-spb')
get_ids(area=areas, metro=None, filename='data/jul-22/hh-id-regions')

get_listings(id_list='data/jul-22/hh-id-msk.csv', filename='data/jul-22/hh-ads-msk')
get_listings(id_list='data/jul-22/hh-id-spb.csv', filename='data/jul-22/hh-ads-spb')
get_listings(id_list='data/jul-22/hh-id-regions.csv', filename='data/jul-22/hh-ads-regions')