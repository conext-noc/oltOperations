import gspread

cellMap = {
    'SN': 1,
    'NAME': 2,
    'CI': 3,
    'OLT': 4,
    'FRAME': 5,
    'SLOT': 6,
    'PORT': 7,
    'ID': 8,
    'ONT': 9,
    'STATUS': 10,
    'PROVIDER': 11,
    'PLAN': 12,
    'SPID': 13,
    'STATE': 14,
}


def modifier(column, searchedValue, value):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    
    cell = wks.find(searchedValue)
    wks.update_cell(cell.row, cellMap[column], value)
