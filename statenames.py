def abbreviations(region):
    if region =="ne":
        output = northEast()
    elif region == "s":
        output = south()
    elif region == "mw":
        output = midWest()
    elif region == "w":
        output = west()
    else:
        output = "NONE"
    return output
        

def northEast():
    output = """
        CT - Connecticut
        DE - Delaware
        ME - Maine
        MD - Maryland
        MA - Massachusetts
        NH - New Hampshire
        NJ - New Jersey
        NY - New York
        PA - Pennsylvania
        RI - Rhode Island
        VT - Vermont
    """
    return output

def south():
    output = """
        AL - Alabama
        AR - Arkansas
        FL - Florida
        GA - Georgia
        KY - Kentucky
        LA - Louisiana
        MS - Mississippi
        NC - North Carolina
        OK - Oklahoma
        SC - South Carolina
        TN - Tennessee
        TX - Texas
        VA - Virginia
        WV - West Virginia
    """
    return output

def midWest():
    output = """
        IA - Iowa
        IL - Illinois
        IN - Indiana
        KS - Kansas
        MI - Michigan
        MN - Minnesota
        MO - Missouri
        ND - North Dakota
        NE - Nebraska
        OH - Ohio
        SD - South Dakota
        WI - Wisconsin
    """
    return output

def west():
    output ="""
        AK - Alaska
        AZ - Arizona
        CA - California
        CO - Colorado
        HI - Hawaii
        ID - Idaho
        MT - Montana
        NV - Nevada
        NM - New Mexico
        OR - Oregon
        UT - Utah
        WA - Washington
        WY - Wyoming
    """
    return output