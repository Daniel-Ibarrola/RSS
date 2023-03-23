CITIES = {
    40: 'CDMX',
    41: 'Guerrero',
    42: 'Oaxaca',
    43: 'Michoacán',
    44: 'Colima',
    45: 'Jalisco',
    46: 'Puebla',
    47: 'Morelos',
    48: 'Veracruz',
    49: 'Chiapas',
}


def get_region(region_code: int) -> str:
    # TODO: convert this code into a hash table
    if region_code > 49200:
        return "Chiapas"
    elif region_code > 48200:
        return "Veracruz"
    elif region_code > 47200:
        return 'Morelos'
    elif region_code > 46200:
        return 'Puebla'
    elif region_code > 45200:
        return 'Costa Jal'
    elif region_code > 44200:
        return 'Costa Col'
    elif region_code > 43200:
        n1 = region_code - 43200
        if n1 == 1:
            return "Costa Mich-Gro"
        elif n1 in [2, 3]:
            return "Playa Azul Mich"
        elif n1 == 7:
            return "Costa Mich-Col"
        else:
            return "Costa Mich"
    elif region_code > 42200:
        n1 = region_code - 42200
        if n1 in [1, 3]:
            return 'Costa Oax-Gro'
        if n1 in [4, 5]:
            return 'Pinotepa Oax'
        if n1 in [6, 8]:
            return 'PtoEscondido Oax'
        if n1 in [9, 11]:
            return 'Huatulco Oax'
        if n1 in [12, 14]:
            return 'SalinaCruz Oax'
        if n1 in [15, 18]:
            return 'Oax Centro'
        if n1 in [19]:
            return 'Huatulco Oax'
        if n1 in [20, 21]:
            return 'Huajuapan Oax'
        if n1 in [22]:
            return 'Lim Oax-Pue'
        if n1 in [23, 24]:
            return 'Oax Centro'
        if n1 in [25, 26]:
            return 'Tuxtepec Oax'
        if n1 in [27]:
            return 'Lim Oax-Pue'
        if n1 in [28, 29]:
            return 'Oax Centro'
        if n1 in [30]:
            return 'Lim Oax-Pue'
        if n1 in [31, 32]:
            return 'Oax Centro'
        if n1 in [33]:
            return 'Lim Ver-Oax'
        if n1 in [34, 36]:
            return 'Istmo Oax-Chis'
        if n1 in [37]:
            return 'Oax Centro'
        else:
            return 'Oaxaca'
    elif region_code > 41200:
        n1 = region_code - 41200
        if n1 in [1, 2]:
            return 'Petatlan Gro'
        if n1 in [3, 5]:
            return 'Atoyac Gro'
        if n1 in [6, 7]:
            return 'Acapulco Gro'
        if n1 in [8, 11]:
            return 'SanMarcos Gro'
        if n1 in [12]:
            return 'Costa Gro-Oax'
        if n1 in [13, 14]:
            return 'Petatlan Gro'
        if n1 in [15, 17]:
            return 'Zihuatanejo Gro'
        if n1 in [18]:
            return 'Costa Gro-Mich'
        else:
            return 'Guerrero'
    return ""
