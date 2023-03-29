import requests
import json
from datetime import datetime, timedelta
import itertools


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def getFlight(departure, destination, dateFrom, dateTo):
    url = f'https://api.tequila.kiwi.com/v2/search?fly_from={departure}&fly_to={destination}&dateFrom={dateFrom.strftime("%d/%m/%Y")}&dateTo={dateFrom.strftime("%d/%m/%Y")}&returnFrom={dateTo.strftime("%d/%m/%Y")}&returnTo={dateTo.strftime("%d/%m/%Y")}'
    payload = ""
    headers = {
        'apikey': '1zUNabKAXrUrstGBchcZpcuqVKWAqmST',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if len(response.json()['data']) > 0:
        return {
            "details": response.json()['data'][0],
            "price": float(response.json()['data'][0]['price'])
        }
    else:
        print(f"No flights")
        return None


def sendTelegramMessage(message):
    url = f"https://api.telegram.org/bot5745144237:AAHmVv6UHoqCK5ejmp_jA3XVkcZd9BdOraw/sendMessage"
    data = {"chat_id": "469506949", "text": message}
    response = requests.post(url, json=data)
    return response.json()


hotelIds = {
    "PRG": ['deminka_palace', 'union_hotel_prague'],
    "OPO": ['eurostars_heroismo', 'quality_inn_praca_da_batalha_porto', 'hotel_internacional_5',
            'best_western_hotel_inca', 'cliphotel', 'tryp_porto_centro', 'hotel_pao_de_acucar', 'hf_fenix_porto',
            'hf_tuela_porto_2', 'pedra_iberica', 'hotel_spot_family_suites', 'holiday_inn_express_porto_santa_catarina',
            'acta_the_avenue', 'neya_porto_hotel', 'ibis_porto_centro_mercado_do_bolhao'],
    "LIS": ['hotel_as_lisboa_lisbon', 'turim_suisso_atlantico_hotel', 'botanico_hotel', 'lisbon_sao_bento_hotel',
            'the_lift_boutique_hotel', 'rossio_boutique_hotel', 'exe_saldanha', 'omid_saldanha_hotel'],
    "CAG": ['il_giardino_segreto', 'il_carignano', 'le_dimore_del_sole', 'blulassu_', 'sa_babbaiola',
            'brezza_marina_7'],
    "PAR": ['hotel_aix_europe', 'republique_hotel_2', 'staycity_serviced_apartments__gare_de_lest_2',
            'saint_louis_bastille', 'hotel_viator_2'],
    "LON": ['zedwell_piccadilly', 'ibis_london_blackfriars', 'citizenm_london_bankside', 'the_z_hotel_city',
            'yotel_london_clerkenwell'],
    "NAP": ['bb_cupole_e_campanili', 'savoy_riviera', 'iris_4', 'the_fresh_glamour_accommodation', 'cerasiello'],
    "FLR": ['hotel_ferrucci_firenze', 'loggia_fiorentina', 'ridolfi_guest_house_3', 'popartment',
            'dei_mori_bedbreakfast', 'cosy_house_6'],
    "IST": ['sah_hotel_pension', 'beyazithan_suites', 'pembe_apart_hotel', 'istanbul_terrace_hotel', 'biter_hotel',
            'arven_butique_hotel', 'rhythm_hotel'],
    "CFU": ['telesilla_hotel_corfu', 'folies_corfu_hotel_apartments', 'sunset_9', 'aquis_mon_repos_palace'],
    "BDS": ['antiche_volte', 'i_4_balconi', 'il_tacco_dello_stivale_', 'bb_imbriani_24', 'la_corte_bed__breakfast',
            'piazza_argento_'],
    "DUB": ['best_western_plus_academy_plaza_hotel', 'hotel_st_george', 'point_a_hotel_dublin_parnell_street',
            'the_hendrick_smithfield', 'jurys_inn_dublin_parnell_street', 'holiday_inn_express_dublin_city_centre'],
    "TGD": ['jp_apartments_kotor', 'royal_house_8', 'hotel_cattaro', 'hotel_monte_cristo_2', 'almare_apartments_budva',
            'martinovic_rooms', 'dd_apartments_budva_3', 'apartments_villa_m_palace'],
    "AMS": ['ibis_styles_amsterdam_amstel', 'amadi_park_hotel', 'hotel_iron_horse', 'hotel_v_frederiksplein',
            'quentin_zoo_hotel', 'hampshire_hotel__theatre_district_amsterdam'],
    "ROM": ['napoleon_hotel', 'maryelen__giovi_2', 'hotel_giolli_nazionale', 'medici', 'hotel_elite',
            'augusta_lucilla_palace', 'hotel_morgana'],
    "BER": ['best_western_hotel_am_spittelmarkt', 'winters_hotel_berlin_mitte_am_gendarmenmarkt',
            'derag_livinghotel_henriette', 'derag_livinghotel_grosser_kurfurst_2', 'moevenpick_hotel_berlin',
            'winters_hotel_berlin_mitte_the_wall_at_checkpoint_charlie'],
    "ATH": ['athensredcom', 'athens_panorama_project', 'hydria_boutique_suites_by_athens_stay', 'ariston_2',
            'pame_paradiso', 'hotel_katerina_4'],
    "BCN": ['mercure_alberta_barcelona_2', 'bcn_urban_gran_rosellon', 'evenia_rossello',
            'umma_barcelona_bedbreakfast_boutique', 'catalonia_hotel_barcelona_golf', 'onix_fira'],
    "MAD": ['hotel_principe_pio', 'ibis_budget_madrid_centro_lavapies', 'hotel_acta_madfor', 'gran_hotel_conde_duque',
            'lh_la_latina', 'hotel_gran_versalles'],
    "SVQ": ['ribera_de_triana_hotel_2', 'nh_viapol', 'sevilla_center', 'confortel_puerta_de_triana',
            'nh_plaza_de_armas_2', 'fontecruz_sevilla_2'],
    "BRU": ['hotel_beverly_hills', 'bb_hotel_brussels_centre_gare_du_midi', 'ibis_styles_brussels_centre_stephanie',
            'the_pantone_hotel', 'mercure_brussels_centre_midi', 'hotel_retro'],

}

country_codes = {
    "ES": ["BCN", "SVQ"],
    "IT": ["ROM", "NAP"],
    "FR": ["PAR"],
    "DE": ["BER"],
    "GR": ["ATH"],
    "PT": ["LIS", "OPO"],
    "GB": ["LON"],
    "NL": ["AMS"],
    "BE": ["BRU"],
    "CZ": ["PRG"]
}


def calculateCheapestRoute(departure, dateFrom, dateTo, countries, adults):
    url = f'https://tequila-api.kiwi.com/v2/nomad?adults={adults}&conn_on_diff_airport=0&sort=quality&limit=20&date_from={dateFrom.strftime("%d/%m/%Y")}&date_to={dateFrom.strftime("%d/%m/%Y")}&fly_from={departure}&fly_to={departure}&return_from={dateTo.strftime("%d/%m/%Y")}&return_to={dateTo.strftime("%d/%m/%Y")}'

    via = []
    for country in countries:
        via.append({
            "locations": [country],
            "nights_range": [
                2,
                3
            ]
        })

    payload = json.dumps({
        "via": via
    })
    headers = {
        'accept': 'application/json',
        'apikey': 'OWV4CI2G2vXy3KyqVRxcFrmxqT_V0g9h',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)

    if len(response.json()['data']) > 0:
        cheapest_route = response.json()['data'][0]
        kiwi_uRL = f"https://www.kiwi.com/es/booking?activeStep=0&currency=eur&locale=es&passengers=1&searchType=return&token={cheapest_route['booking_token']}"
        print(kiwi_uRL)
        return cheapest_route
    else:
        return None


def calculateHotelPricePerJump(dateFrom, dateTo, destination, adults):
    url = "https://api.worldota.net/api/b2b/v3/search/serp/hotels/"

    payload = json.dumps({
        "checkin": dateFrom.strftime("%Y-%m-%d"),
        "checkout": dateTo.strftime("%Y-%m-%d"),
        "residency": "es",
        "language": "en",
        "guests": [
            {
                "adults": adults,
                "children": []
            }
        ],
        "currency": "EUR",
        "ids": hotelIds[destination]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MjYyNDphYWMzODllMC1jODg1LTQ0ZjMtOTM5Ni1mOTc4OTYwOTM1YmY=',
        'Cookie': 'uid=TfTb8GPuK15QnBS4CMYZAg=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if len(response.json()['data']['hotels']) > 0:
        return {
            "details": response.json()['data']['hotels'][0],
            "price": float(
                response.json()['data']['hotels'][0]['rates'][0]['payment_options']['payment_types'][0]['amount'])
        }
    else:
        print(f"No hotels")
        return None


def getCheapestRoute(departure, dateFrom, dateTo, countries, adults):

    city_lists = [country_codes[country] for country in countries]
    city_combinations = list(itertools.product(*city_lists))
    cheapest_route = None
    for combination in city_combinations:
        route = calculateCheapestRoute(departure, dateFrom, dateTo, combination, adults)
        if route is not None:
            if cheapest_route is None:
                cheapest_route = route
            elif cheapest_route['price'] > route['price']:
                cheapest_route = route
    return cheapest_route


if __name__ == '__main__':
    departure = "BCN"
    countries = ["IT", "PT"]
    dateFrom = datetime.strptime("17/07/2023", '%d/%m/%Y')
    dateTo = datetime.strptime("23/07/2023", '%d/%m/%Y')
    adults = 2

    cheapest_route = getCheapestRoute(departure, dateFrom, dateTo, countries, adults)
    cost_price = 0
    if cheapest_route is None:
        print("No routes found")
        exit(0)
    print("flights:", cheapest_route['price'])
    cost_price += cheapest_route['price']
    jumps = cheapest_route['route']
    for i in range(len(jumps) - 1):
        arrival_datetime = datetime.strptime(jumps[i]['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ')
        departure_datetime = datetime.strptime(jumps[i + 1]['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ')
        destination = jumps[i]['cityCodeTo']
        selected_hotel = calculateHotelPricePerJump(arrival_datetime, departure_datetime, destination, adults)
        print(destination)
        print(selected_hotel['price'])
        print(selected_hotel['details']['id'])
        print(selected_hotel['details']['rates'][0]['room_name'])
        cost_price += selected_hotel['price']

    cost_price = cost_price / adults
    print("Cost price (pp):", cost_price)
    final_price = cost_price * 1.2
    print("Final price (pp):", final_price)
