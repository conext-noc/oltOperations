def template(SLOT,PORT,ID,NAME,OLT,PROVIDER,PLAN,temp,pwr,SPID,REASON=""):
  return f"""
{NAME} 0/{SLOT}/{PORT}/{ID} OLT {OLT} {PROVIDER.upper()} {PLAN[3:]}
TEMPERATURA:{temp}
POTENCIA:{pwr}
SPID :{SPID}
""" if REASON == "" else """
{NAME} 0/{SLOT}/{PORT}/{ID} OLT {OLT} {PROVIDER.upper()} {PLAN[3:]}
TEMPERATURA:{temp}
POTENCIA:{pwr}
SPID :{SPID}
- {REASON} -
"""