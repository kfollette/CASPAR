#Converts RA and DEC from H:M:S to Degrees

import numpy as np

def degcon(rahr, ramin, rasec, dechr, decmin, decsec):

  ra = (rahr*15) + (ramin*15/60) + (rasec*15/3600)
  if ra > 360:
    ra = np.abs(ra-360)
  else:
    ra = (rahr*15) + (ramin*15/60) + (rasec*15/3600)

  dec = dechr - (decmin/60) - (decsec/3600)
  if dec < 0:
    dec = dechr - (decmin/60) - (decsec/3600)
  else:
    dec = dechr + (decmin/60) + (decsec/3600)

  return ra, dec
