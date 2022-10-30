def template(FRAME,SLOT,PORT,ID,NAME,OLT,PROVIDER,PLAN,temp,pwr,SPID,REASON=""):
  return f"""\n
{NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} {PROVIDER.upper()} {PLAN[3:]}
TEMPERATURA:{temp}
POTENCIA:{pwr}
SPID :{SPID}
""" if REASON == "" else f"""\n
{NAME} {FRAME}/{SLOT}/{PORT}/{ID} OLT {OLT} {PROVIDER.upper()} {PLAN[3:]}
TEMPERATURA:{temp}
POTENCIA:{pwr}
SPID :{SPID}
- {REASON} -
"""