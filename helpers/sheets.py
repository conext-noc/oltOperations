import gspread

cellMap = {
    'SN': 1,
    'NAME': 2,
    'OLT': 3,
    'FRAME': 4,
    'SLOT': 5,
    'PORT': 6,
    'ID': 7,
    'ONT': 8,
    'STATUS': 9,
    'PROVIDER': 10,
    'PLAN': 11,
    'SPID': 12,
    'STATE': 13,
}


def modifier(column, searchedValue, value):
    sa = gspread.service_account(
        filename="service_account_olt_operations.json")
    sh = sa.open("CPDC")
    wks = sh.worksheet("DATOS")
    
    cell = wks.find(searchedValue)
    wks.update_cell(cell.row, cellMap[column], value)
