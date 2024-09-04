import scrapy

# Define spider class
class Senate_Description_Spider(scrapy.Spider):
  name = "senate"
  # start_requests method
  def start_requests(self):
    yield scrapy.Request(url = "https://www.senado.gov.co/index.php/el-senado/senadores",
                         callback = self.parse_first_page)
  # First parsing method
  def parse_first_page(self, response):

    sen_blocks = response.css('blockquote')
    senator_links = sen_blocks.xpath('./p/a/@href').extract()
    
    for url in senator_links:
      print(url)
      yield response.follow(url = url,
                            callback = self.parse_pages)
  # Second parsing method
  def parse_pages(self, response):
    # Extract senator name
    name = response.css('h3.sppb-addon-title::text').get()
    info = response.css("tbody > tr > td::text").extract()

    if len(info) > 0:

      f_nac = info[0]
      l_nac = info[1]
      partido = info[2]
      ubicacion = info[3]
      tel = info[4]

      info2 = response.css("tbody > tr > td > a::text").extract()

      comisiones = ", ".join([x for x in info2 if "Comisión" in x])
      email = [x for x in info2 if "@senado" in x]

      if len(email) > 0:
        email = email[0]
      else:
        email = None

      web = [x for x in info2 if (("www" in x) or ("http" in x))]

      if len(web) > 0:
        web = web[0]
      else:
        web = None

      red_social = response.xpath("//tbody/tr/td/a/@href").extract()

      facebook = [link for link in red_social if "facebook" in link]
      twitter = [link for link in red_social if "twitter" in link]
      instagram = [link for link in red_social if "instagram" in link]
      youtube = [link for link in red_social if "youtube" in link]
      tiktok = [link for link in red_social if "tiktok" in link]

      if len(facebook) > 0:
        facebook = facebook[0]
      else:
        facebook = None

      if len(twitter) > 0:
        twitter = twitter[0]
      else:
        twitter = None

      if len(instagram) > 0:
        instagram = instagram[0]
      else:
        instagram = None

      if len(youtube) > 0:
        youtube = youtube[0]
      else:
        youtube = None

      if len(tiktok) > 0:
        tiktok = tiktok[0]
      else:
        tiktok = None
    else:
      f_nac = None
      l_nac = None
      partido = None
      ubicacion = None
      tel = None
      comisiones = None
      email = None
      web = None
      facebook = None
      twitter = None
      instagram = None
      youtube = None
      tiktok = None

    yield {
      "Nombre": name,
      "Fecha de nacimiento": f_nac,
      "Lugar de nacimiento": l_nac,
      "Partido": partido,
      "Ubicación": ubicacion,
      "Teléfono": tel,
      "Comisiones": comisiones,
      "Email": email,
      "Página web": web,
      "Facebook": facebook,
      "Twitter": twitter,
      "Instagram": instagram,
      "Youtube": youtube,
      "Tiktok": tiktok
    }
   

