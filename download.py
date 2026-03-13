import urllib.request
import os

url = "https://marceneiropro.site/?fbclid=IwY2xjawQeUMdleHRuA2FlbQIxMABicmlkETFXdHFSVTYzZUVHb1ZiZkFyc3J0YwZhcHBfaWQPNTQxNjM5NDkzODg5MDI1AAEepR7KvPRGrwmG_C6J8iJ74p5DztRISlbrq5wQ4KzSpnOZ10R5iNP0e2qAOg0_aem_JpW3RvVKtpKouD75E8WLOQ"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
        with open("index.html", "wb") as f:
            f.write(html)
    print("Downloaded index.html")
except Exception as e:
    print("Error:", e)
