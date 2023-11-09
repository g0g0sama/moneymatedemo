import requests

url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx"


headers = {
  'Content-Type': 'text/xml; charset=utf-8',
  'Host': 'tckimlik.nvi.gov.tr',
  'SOAPAction': 'http://tckimlik.nvi.gov.tr/WS/TCKimlikNoDogrula',
  'POST': '/Service/KPSPublic.asmx HTTP/1.1'
}

def mernis_check(national_identity_number, firstname, lastname, birth_year):
    with requests.Session() as session:
        payload = f"""
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
      <TCKimlikNo>{national_identity_number}</TCKimlikNo>
      <Ad>{firstname}</Ad>
      <Soyad>{lastname}</Soyad>
      <DogumYili>{birth_year}</DogumYili>
    </TCKimlikNoDogrula>
  </soap12:Body>
</soap12:Envelope>

"""
        r = session.post(url, headers=headers, data=payload)
        r.raise_for_status()
        print(r.text[r.text.find("<TCKimlikNoDogrulaResult>")+25:r.text.find("</TCKimlikNoDogrulaResult>")])
        
        if r.text[r.text.find("<TCKimlikNoDogrulaResult>")+25:r.text.find("</TCKimlikNoDogrulaResult>")] == "true":
            return True 
        else:
            return False