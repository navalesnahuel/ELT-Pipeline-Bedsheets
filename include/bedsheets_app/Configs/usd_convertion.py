import requests

def usd_to_ars():

    #Matrix Format
        # Categories:
            #Materials
                #Sizes

    #Matrix of values in USD
    price_matrix = {
        1: {
            1: {1: 12, 2: 15, 3: 17, 4: 16, 5: 14, 6: 11},
            2: {1: 11, 2: 13, 3: 15, 4: 14, 5: 12, 6: 9},
            3: {1: 12, 2: 15, 3: 17, 4: 16, 5: 14, 6: 11},
            4: {1: 11, 2: 14, 3: 16, 4: 15, 5: 13, 6: 10},
            5: {1: 13, 2: 16, 3: 18, 4: 17, 5: 15, 6: 12},
            6: {1: 14, 2: 17, 3: 19, 4: 18, 5: 16, 6: 13}
        },
        2: {
            1: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17},
            2: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17},
            3: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17},
            4: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17},
            5: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17},
            6: {1: 23, 2: 30, 3: 32, 4: 30, 5: 27, 6: 17}
        },
        3: {
            1: {1: 6, 2: 7, 3: 8, 4: 8, 5: 7, 6: 5},
            2: {1: 5, 2: 6, 3: 7, 4: 7, 5: 6, 6: 4},
            3: {1: 6, 2: 7, 3: 8, 4: 8, 5: 7, 6: 5},
            4: {1: 5, 2: 7, 3: 8, 4: 7, 5: 6, 6: 5},
            5: {1: 6, 2: 8, 3: 9, 4: 9, 5: 8, 6: 6},
            6: {1: 7, 2: 8, 3: 9, 4: 9, 5: 8, 6: 6}
        }
    }


    # USD Blue Today:
    url = "https://dolarapi.com/v1/dolares/blue"
    response = requests.get(url)
    data = response.json()
    dolar_blue = data.get("venta")

    for category, materials in price_matrix.items():
        for material, sizes in materials.items():
            for size, price in sizes.items():
                price_matrix[category][material][size] *= dolar_blue

    return price_matrix
