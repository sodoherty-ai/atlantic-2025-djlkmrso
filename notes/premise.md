[list of major hospitals across Ireland, based on the Health Service Executive (HSE) website.csv](https://github.com/user-attachments/files/19937618/list.of.major.hospitals.across.Ireland.based.on.the.Health.Service.Executive.HSE.website.csv)# Elder Connect (need better name?)

## Elevator pitch
This is a web app aimed at promoting well-being for older people by 
shining a light on social isolation in our communities.

## Notes

- Feature to see who are over 65 and are living in isolation in the general area.
- Presents a short narrative on why it matters.
- Highlight local volunteer groups or charities
- Services that are available to help them.
- Compelling story telling.
  - Stir emotions to action.
- Actionable ideas.
- Focusing on single metric provides depth.
  - Less likely to be part of other teams submissions.
  - Can be a disruptor
- Personalises the issue.
- Not a personal tracker. Not a health tool.
### Functional notes
- Needs to be AI agnostic. 
- Non-technical team members can contribute through prompts.

## Data sources
- https://data.gov.ie/en_GB/dataset/fy010a-population-aged-65-years-and-over-living-alone#:~:text=CSV
- [UploadiHospital,Google Map Plus code,County
"Beaumont Hospital, Dublin",9QRG+4C Dublin,Dublin
"Bon Secours Hospital, Cork","51.89143489209615, -8.497916531513708 Cork",Cork
"Crumlin Children's Hospital, Dublin","53.32656654282114, -6.317526573768919 Dublin",Dublin
"Mater Misericordiae University Hospital, Dublin","53.360160794617734, -6.265203087260223 Dublin",Dublin
"Our Lady of Lourdes Hospital, Drogheda","53.722290851445855, -6.354374917926618 Drogheda",Louth
"St. James’s Hospital, Dublin","53.34073372367383, -6.294950431439477 Dublin",Dublin
"St. Vincent's University Hospital, Dublin","53.316913374567385, -6.212324290881905 Dublin",Dublin
"Tallaght University Hospital, Dublin","53.29128265620214, -6.3786160314420375 Dublin",Dublin
University Hospital Galway,"53.27694220163123, -9.066133460278417 Galway",Galway
Waterford University Hospital,"52.24865038095744, -7.078474444988629 Waterford",Waterford
University Hospital Limerick,"52.63531910709857, -8.653859702640148 Limerick",Limerick
"Mercy University Hospital, Cork","51.89889767560388, -8.482824571992479 Cork",Cork
Sligo University Hospital,"54.274333800531274, -8.46272218721255 Sligo",Sligo
"South Tipperary General Hospital, Clonmel","52.355435630129904, -7.71456887169621 South Tipperary",Tipperary
Wexford General Hospital,"52.34321157277536, -6.482768073819433 Wexford",Wexford
University Hospital Waterford,"52.248663518112544, -7.078506631495586 Waterford",Waterford
"St. Colum's Hospital, Limerick (now part of University Hospital Limerick)","52.635312595917604, -8.653881160311458 Limerick",Limerick
Sligo Regional Hospital (now part of Saolta University Health Care Group),"54.27437138823524, -8.462765102555156 Sligo",Sligo
"Letterkenny University Hospital, Donegal (now part of Saolta University Health Care Group)","54.96011039137302, -7.7341514871763986 Donegal",Galway
"Portiuncula Hospital, Ballinasloe, Galway (now part of Saolta University Health Care Group)","53.326814475297475, -8.234625473768865 Galway",Mayo
"Mayo University Hospital, Castlebar","53.8518497887274, -9.30427291791985 Sligo",Sligo
Sligo University Maternity Hospital (now part of Saolta University Health Care Group),"54.27438391746228, -8.462765102555156 Sligo",Sligo
"University Hospital Kerry, Tralee","52.26541445858766, -9.688675389166018 Kerry",Kerry
"Donegal Acute Services Site, Letterkenny","54.96013636093509, -7.73415145794009 Donegal",Donegal
"Ennis General Hospital, Clare (now part of Saolta University Health Care Group)","52.85120387341983, -8.983316502629087 Clare",Clare
"Nenagh Hospital, Tipperary (now part of Saolta University Health Care Group)","52.85851084237447, -8.191352702628715 Tipperary",Tipperaryng list of major hospitals across Ireland, based on the Health Service Executive (HSE) website.csv…]()

- Needs other datasets.
- **Invalid datasets**
-   https://www.medicalcouncil.ie/public-information/check-the-register/ - **not possible to search by location, only surname, firstname, registration number**
-   https://abbeycare.ie/
-   https://www.homeinstead.ie/
-   https://www.caringtimes.ie/
-   https://www.hse.ie/eng/services/list/l/homecare/
- **Valid datasets**
-   ** https://dovida.ie/contact/** - can search by city or postcode or region (32), search on example Donegal points to https://dovida.ie/local-office/donegal/ and home care 
    services available from Dovida Donegal office
- **https://www.hse.ie/eng/services/list/4/olderpeople/**
- To extract data from the HSE (Health Service Executive) Older People Services webpage (<https://www.hse.ie/eng/services/list/4/olderpeople/>), you would need to use web scraping techniques or APIs if available. Since the HSE website does not provide an official API for data extraction, 

  **   >>> what irish data sets exist in csv format for "Highlighting local volunteer groups or charities or services" to people aged 65 and over?**
To find CSV datasets that highlight local volunteer groups, charities, or services tailored for individuals aged 65 and over in Ireland, you can explore the following resources:

1. **Data.gov.ie**:
   - Source: https://data.gov.ie/dataset/
   - Search for datasets related to older people, volunteering, or community services. Some potential datasets include:
     - "Community Games" (https://data.gov.ie/dataset/community-games)
     - "Older People's Services" (https://data.gov.ie/dataset/older-peoples-services)

DJ comment on above -> https://data.gov.ie/dataset/?q=over+65&sort=score+desc%2C+metadata_created+desc
**124 datasets returned. None specific to services available to 65+
**
2. **CSO (Central Statistics Office)**:
   - Source: https://appsso.cis.gov.ie/pages/surveys/1850_Social_Survey/2019_SS_Report.pdf
   - Although not in CSV format, the CSO's Social Survey provides insights into community participation and volunteering among different age groups.

3. **Irish Statistic Office (CSO) Data on Social Participation and Community Activities**:
   - Source: https://appsso.cis.gov.ie/pages/surveys/1850_Social_Survey/2019_SS_Report.pdf
   - This report contains data on social participation and community activities, which can help identify areas with high senior volunteer engagement.

4. **Age Friendly Ireland Network**:
   - Source: https://www.agefriendlyireland.ie/network/
   - The Age Friendly Ireland network features local authorities committed to making their communities age-friendly, often providing CSV or downloadable files with service and activity information for older adults.

5. **Irish Senior Timebank**:
   - Source: http://www.seniorstimebank.ie/
   - A volunteer exchange platform that connects seniors with opportunities to engage in meaningful activities, which can also be used as a resource for identifying active volunteer groups.

6. **Local Authority Websites**:
   - Many local authorities in Ireland maintain their own databases of community groups and services. These can usually be accessed through their official websites and may provide downloadable CSV files or data feeds.
