import requests
import json
from datetime import datetime, timedelta

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    dateFrom = datetime.datetime.now()
    dateFrom = dateFrom + datetime.timedelta(days=65)
    dateTo = dateFrom + datetime.timedelta(days=3)
    #flightPrice = getFlightPrices("BCN", "MIL", "01/04/2023", "02/04/2023")
    cheaptestHotel = getHotel("BDS", dateFrom, dateTo)
    cheapestFlight = getFlight("BCN","BDS", dateFrom,dateTo)
    print(dateFrom.strftime("%d/%m/%Y"))
    print(dateTo.strftime("%d/%m/%Y"))
    print(cheaptestHotel['details']['id'])
    print('Hotel: ',cheaptestHotel['price'])
    print('Flight: ',cheapestFlight['price'])
    print(cheapestFlight['details']['booking_token'])


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
            "details":  response.json()['data'][0],
            "price": float(response.json()['data'][0]['price'])
        }
    else:
        print(f"No flights")
        return None

def getHotel(destination, dateFrom, dateTo):
    url = "https://api.worldota.net/api/b2b/v3/search/serp/hotels/"

    payload = json.dumps({
        "checkin": dateFrom.strftime("%Y-%m-%d"),
        "checkout": dateTo.strftime("%Y-%m-%d"),
        "residency": "es",
        "language": "en",
        "guests": [
            {
                "adults": 2,
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
            "price": float(response.json()['data']['hotels'][0]['rates'][0]['payment_options']['payment_types'][0]['amount']) / 2
        }
    else:
        print(f"No hotels")
        return None

def sendTelegramMessage(message):
    url = f"https://api.telegram.org/bot5745144237:AAHmVv6UHoqCK5ejmp_jA3XVkcZd9BdOraw/sendMessage"
    data = {"chat_id": "469506949", "text": message}
    response = requests.post(url, json=data)
    return response.json()


hotelIds = {
    "PRG": ['deminka_palace', 'union_hotel_prague'],
    "OPO": ['eurostars_heroismo', 'quality_inn_praca_da_batalha_porto', 'hotel_internacional_5','best_western_hotel_inca','cliphotel','tryp_porto_centro','hotel_pao_de_acucar','hf_fenix_porto','hf_tuela_porto_2','pedra_iberica','hotel_spot_family_suites','holiday_inn_express_porto_santa_catarina','acta_the_avenue','neya_porto_hotel','ibis_porto_centro_mercado_do_bolhao'],
    "LIS": ['hotel_as_lisboa_lisbon', 'turim_suisso_atlantico_hotel', 'botanico_hotel','lisbon_sao_bento_hotel','the_lift_boutique_hotel','rossio_boutique_hotel','exe_saldanha','omid_saldanha_hotel'],
    "CAG": ['il_giardino_segreto','il_carignano','le_dimore_del_sole','blulassu_','sa_babbaiola','brezza_marina_7'],
    "PAR": ['hotel_aix_europe','republique_hotel_2','staycity_serviced_apartments__gare_de_lest_2','saint_louis_bastille','hotel_viator_2'],
    "LON": ['zedwell_piccadilly','ibis_london_blackfriars','citizenm_london_bankside','the_z_hotel_city','yotel_london_clerkenwell'],
    "NAP": ['bb_cupole_e_campanili','savoy_riviera','iris_4','the_fresh_glamour_accommodation','cerasiello'],
    "FLR": ['hotel_ferrucci_firenze','loggia_fiorentina','ridolfi_guest_house_3','popartment','dei_mori_bedbreakfast','cosy_house_6'],
    "IST": ['sah_hotel_pension','beyazithan_suites','pembe_apart_hotel','istanbul_terrace_hotel','biter_hotel','arven_butique_hotel','rhythm_hotel'],
    "CFU": ['telesilla_hotel_corfu','folies_corfu_hotel_apartments','sunset_9','aquis_mon_repos_palace'],
    "BDS": ['antiche_volte','i_4_balconi','il_tacco_dello_stivale_','bb_imbriani_24','la_corte_bed__breakfast','piazza_argento_'],
    "DUB": ['best_western_plus_academy_plaza_hotel','hotel_st_george','point_a_hotel_dublin_parnell_street','the_hendrick_smithfield','jurys_inn_dublin_parnell_street','holiday_inn_express_dublin_city_centre'],
    "TGD": ['jp_apartments_kotor','royal_house_8','hotel_cattaro','hotel_monte_cristo_2','almare_apartments_budva','martinovic_rooms','dd_apartments_budva_3','apartments_villa_m_palace'],
    "AMS": ['ibis_styles_amsterdam_amstel','amadi_park_hotel','hotel_iron_horse','hotel_v_frederiksplein','quentin_zoo_hotel','hampshire_hotel__theatre_district_amsterdam'],
    "ROM": ['napoleon_hotel','maryelen__giovi_2','hotel_giolli_nazionale','medici','hotel_elite','augusta_lucilla_palace','hotel_morgana'],
    "BER": ['best_western_hotel_am_spittelmarkt','winters_hotel_berlin_mitte_am_gendarmenmarkt','derag_livinghotel_henriette','derag_livinghotel_grosser_kurfurst_2','moevenpick_hotel_berlin','winters_hotel_berlin_mitte_the_wall_at_checkpoint_charlie'],
    "ATH": ['athensredcom','athens_panorama_project','hydria_boutique_suites_by_athens_stay','ariston_2','pame_paradiso','hotel_katerina_4'],
    "BCN": ['mercure_alberta_barcelona_2','bcn_urban_gran_rosellon','evenia_rossello','umma_barcelona_bedbreakfast_boutique','catalonia_hotel_barcelona_golf','onix_fira'],
    "MAD": ['hotel_principe_pio','ibis_budget_madrid_centro_lavapies','hotel_acta_madfor','gran_hotel_conde_duque','lh_la_latina','hotel_gran_versalles'],
    "SVQ": ['ribera_de_triana_hotel_2','nh_viapol','sevilla_center','confortel_puerta_de_triana','nh_plaza_de_armas_2','fontecruz_sevilla_2'],

}


if __name__ == '__main__':


    departure = "VLC"  # Madrid airport code
    destinations = list(hotelIds.keys())

    budget = 200

    # Define the date ranges
    startingDate = datetime.today()
    startingDate = startingDate + timedelta(days=90)
    dateFrom = startingDate + timedelta(days=(4 - startingDate.weekday()) % 7)  # Get next Friday
    dateTo = dateFrom + timedelta(days=2)  # Stay for the weekend
    dateRange = [dateFrom + timedelta(days=7 * i) for i in range(10)]  # Get next 10 weekends


    # Loop through the date ranges
    for i, weekend in enumerate(dateRange):
        for destination in destinations:
            print(f"Checking {departure} to {destination} on {weekend.date().strftime('%d-%m')}")
            # Calculate the flight and hotel prices for the weekend
            flight = getFlight(departure, destination, weekend, weekend + timedelta(days=2))
            hotel = getHotel(destination, weekend, weekend + timedelta(days=2))
            if flight and hotel:
                flightPrice = flight['price']
                hotelPrice = hotel['price']
                totalPackagePrice = flightPrice + hotelPrice
                print(f"Total price: {totalPackagePrice}")

                # Check if the total package price is within budget
                if totalPackagePrice <= budget:
                    kiwiURL = f"https://www.kiwi.com/es/booking?activeStep=0&currency=eur&locale=es&passengers=1&searchType=return&token={flight['details']['booking_token']}"
                    telegramMessage = f"{departure} ✈ {destination}               {totalPackagePrice}€ \n{weekend.date().strftime('%d-%m')} to {(weekend + timedelta(days=2)).date().strftime('%d-%m')} \nFlights: {flightPrice}€ \n{kiwiURL} \nHotel: {hotelPrice}€ \n{hotel['details']['id']}";
                    sendTelegramMessage(telegramMessage)
                    print(f"{destination}: ({weekend.date()} - {weekend + timedelta(days=2)})  Flight: {flightPrice}€, Hotel: {hotelPrice}€, Total package: {totalPackagePrice}€")


