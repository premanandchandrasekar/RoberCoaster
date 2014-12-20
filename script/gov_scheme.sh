curl -XDELETE 'http://localhost:9200/gov' && echo 
curl -XPOST 'http://localhost:9200/gov' && echo

curl -XPUT 'http://localhost:9200/gov/scheme/1' -d '
{
"sid": 1,
"name": "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA)",
"funding":"Central",
"dept":"Department of Rural Development, GoI",
"target":"Rural employment guarantee",
"coverage":"(a) 2005 (b) All rural areas are covered under NREGA.",
"objectives":"To ensure livelihood and food security by providing unskilled work to people through creation of sustainable assets in rural areas.",
"eligibility":"(a)  Open to all rural households in the areas notified by the Central government.(b) Only adult members belonging to rural households and willing to do unskilled manual work are eligible. (c) A person current status of work in no bar to demand employment under NREGA.(d) Women are encouraged to register and work under NREGA.",
"documents":"(a) Job Card (b) Bank/Post Office Account",
"benefits":"(a) Benefit of guaranteed wage employment for 100 days in rural areas (b) NREGA workers are paid the statutory minimum wage applicable to agricultural workers in the State. Payment of wages in cash on a daily basis If working on a piece-rate basis, ie for 7 hours, payment of minimum wages is applicable.(c) Injury or hospitalization of any labourer during the course of employment at work site is entitled to free medical treatment, medicines, hospital accomdation and also for daily allowance not less than 50% of the wage rate.(d) Safe drinking water, shade for children, periods of rest and first-aid box with adequate material for emergency treatment for minor injuries and other health  hazards connected with the work.",
"refurl":"www.nrega.nic.in"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/2' -d '
{
"sid": 2,
"name": "Yeshasvini Cooperative Farmers Health Care Scheme",
"funding":"State",
"dept":"Karnataka State Co-operative Department",
"target":"Health Insurance to farmers",
"coverage":"1st June 2003 Covers entire state of Karnataka particularly rural areas excluding corporation and urban cities.",
"objectives":"To provide quality health care to rural co-operators through a ‘Self Funded’ scheme in Karnataka.",
"eligibility":"(a) Any member of a Rural Cooperative Society for a minimum period of 6 months is eligible.(b) All family members of the main member are eligible to avail the benefit.(c) Open to all Rural Cooperative Society members, Fisheries Cooperative Societies, Beedi Workers Cooperative Societies and Weavers Cooperative Societies situated in urban and rural areas, Cultural Development Cooperative Societies of Film actors, Stage artists, Folk artists of rural areas, Plantation labourers, representatives of the farmers, elected in State APMC, Rural Journalists of the State, Rural Self Help Groups and Stree Shakti Groups in rural areas, Transgender minorities,  who are members of rural Cooperative Societies having transactions with Cooperative Societies Banks. (d) Ages of insured are from newborn upto 75 years.",
"documents":"(a) UHID (Unique Health Identification) card (b) Each enrolment form contains particulars of the main member and his family members name, age, relationship, society membership number, date and members photo etc.",
"benefits":"(a) Free surgery costing upto Rs.1.25 lakh and Rs.2.00 lakhs for multiple surgeries in one year.(b) Insurance limit is 2 lakh per annum per individual. 1 lakh per surgery per annum. (c) During surgeries, the beneficiaries are given cost of medicines, consumables during hospital stay, cost of Operation Theater, Anesthesia, surgeons fee, professional charge, consultation fee, nursing fee, general ward bed charges etc. (d) Free out patient consultation. (e) Discounted tariffs for lab investigations and tests.",
"refurl":"http://www.yeshasvini.kar.nic.in/Home.html, http://sahakara.kar.gov.in/Yashasivini.html"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/3' -d '
{
"sid": 3,
"name": "Janani Suraksha Yojana (JSY)",
"funding":"Central",
"dept":"Ministry of Health and Family Welfare",
"target":"Conditional cash transfer for institutional births/ Pregnant women in BPL families",
"coverage":"12th April, 2005",
"objectives":"To provide financial assistance to the poor pregnant women during delivery.To increase institutional deliveries in BPL families.",
"eligibility":"(a) All pregnant women who ordinarily reside in Low Peforming State are eligible. The scheme covers all births delivered in a health centre in Low performing states.(b) In High Performing States-BPL pregnant women, aged 19 years and above and upto 2 live births only are eligible. Benefits would be extended to a woman belonging to a BPL family even after a third live birth if the mother of her own accord chooses to undergo sterilisation immediately after the delivery.(c) She should be above 19 years of age and must have got ANC check up atleast 3 times.(d)Must have taken Iron and Folic acid tablets and TT injection.Karnataka falls under High Performing State category.",
"documents":"1. BPL or a SC/ST certificate or certification of poor and needy status of the expectant mother’s family by the gram pradhan or ward member in High Performing States (HPS) 2. Age Certificate in HPS 3. Referral slip from the ASHA/ANM/MO where the pregnant woman generally resides 4. Maternal and Child Health Card 5. Janani Suraksha Yojana (JSY) card ",
"benefits":"Cash Assistance In Karnataka, which belongs to High Performing State Category- Rural areas- To the Mother-1400Rs as Cash incentive Urban areas- To the Mother-600Rs as Cash incentive Compensation amount under JSY for sterilization-Rs.1500/.",
"refurl":"http://karhfw.gov.in, http://mohfw.nic.in/WriteReadData/l892s/file28-99526408.pdf, http://mohfw.nic.in/dofw%20website/JSY_features_FAQ_Nov_2006.htm"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/4' -d '
{
"sid": 4,
"name": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
"funding":"Central and State",
"dept":"The Directorate of Social Security and Pensions (DSSP), Revenue Department",
"target":"Pension for elderly",
"coverage":"15th August, 1995",
"objectives":"To provide pension to old people above the age of 60 who cannot fend for themselves and do not have any means of subsistence.",
"eligibility":"(a) Age of the applicant (male or female) should be 60 years or above (b) The applicant should belong to a BPL household (c) Low income group and handicapped are eligible",
"documents":"(a) Medical Certificate : A certificate from a Medical Officer as a proof of age for the destitute person (b) Photograph: Two recent photographs with signature of the applicant duly attested by a Gazetted Officer. (c) Income Certificate: A certificate showing the annual income in prescribed format from DC/SDO/SDC or an employer in case of an employed Applicant/ Husband/ Wife/Son(s)/Daughter(s)/Grand Sons/grand Daughters",
"benefits":"(a)  Rs 200 per month is provided to persons of 60 years or higher and belonging to a BPL family (b) BPL persons post 80 years of age are eligible to receive Rs.500/month. (c) Additional pension in case of disability, loss of adult children and concomitant responsibility for grand children and women.",
"refurl":"http://dssp.kar.nic.in/indira.html"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/5' -d '
{
"sid": 5,
"name": "Bhagyalakshmi Scheme",
"funding":"State",
"dept":"Department of Women and Child Development",
"target":"Promotion of girl child",
"coverage":"1st April, 2006",
"objectives":"To promote the birth of girl children in BPL families and to raise the status of the girl child in society.",
"eligibility":"(a) All girl children born in BPL families after 31.3.06 are eligible. (b) Those families with the BPL card or families with their annual income within Rs 17000 in urban areas and in within Rs 12000 in rural areas are eligible.  (c) The benefits are restricted to 2 girl children of a BPL family. (d)The father, mother or guardian should have undergone terminal family planning methods and the total number of children should not exceed 3. Additional conditions that the girl child should fulfil to be eligible to receive the maturity amount are: a.  be immunized as per the programme of the Health Department b.  be enrolled in the Anganwadi centre until she attains 6 years.c.  take admission in a school recognized by  Education Department. d.  not to be engaged a child labourer e.  complete Standard VIII f.   not to marry until the age of 18 years.",
"documents":"(a) Birth Certificate (b) Income certificate (c) Photograph of the child with parents (d) BPL card/ Ration Card (e) Immunization card if the girl child has received immunization (f) Marriage Certificate of parents",
"benefits":"(a) The girl child gets health insurance cover up to a maximum of Rs. 25000 a year, an annual scholarship of Rs 300 to Rs 1000 till X Standard. The annual scholarship slab for each class is as given below 1st standard to 3rd standard Rs.300/- 4th standard     Rs.500/- 5th standard     Rs.600/- 6th standard to 7th standard  Rs.700/- 8th standard     Rs.800/- 9th standard to 10th standard  Rs.1000/- (b) Parents would get Rs. 1 lakh in case of an accident and Rs 42500 in case of natural death of the beneficiary. (c) On attainment of 18 years of age, the first girl beneficiary who fulfills the conditions of the scheme will get a maturity amount of Rs 1, 00,097 and the second girl beneficiary will receive Rs 1,00,052. The annual scholarships and insurance benefits will be made available to the beneficiary on fulfilment of the eligibility criteria mentioned in the scheme.(d) The beneficiaries willing to continue higher education after passing Standard X are eligible to pledge the bond and avail a loan, up to a maximum of Rs 50,000 from recognized banks.",
"refurl":"http://dwcdkar.gov.in/index.php"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/6' -d '
{
"sid": 6,
"name": "Arivu (Education Loan) Scheme",
"funding":"State",
"dept":"Karnataka Minorities Development Corporation Ltd",
"target":"Financial assistance for education of minority students",
"coverage":"Karnataka",
"objectives":"To provide financial assistance to minority students for completion of professional courses.",
"eligibility":"(a) Annual income of the family should be within Rs. 22,000. (b) All professional courses. (c ) Applicant should belong to religious minority",
"documents":"Documents to be submitted with application form:(a) Photograph of applicant 4-Passport size  (b) Income Certificate  (c) Caste Certificate (d ) PUC / Degree Marks card (e) Transfer Certificate (f)New Ration card or any other document for address proof(g) CET Admission order /College Admission order/CAC order (h) SSLC marks card for proof of Date of Birth (i)Study Certificate (Present course)Documents to be submitted at the time of release of loan:(a) Agreement I - Surety affidavit on Rs. 50% paper along with 2 passport size photograph of Parents / Husband / Guardian. (b)Agreement II - Indemnity Bond on Rs. 100/- paper (to be signed before the notary) ",
"benefits":"Financial loan upto Rs 75000 per year to minority students till the completion of professional courses.",
"refurl":"http://www.kmdc.kar.nic.in/Arivu.html"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/7' -d '
{
"sid": 7,
"name": "Shramashakthi Scheme",
"funding":"State",
"dept":"Karnataka Minorities Development Corporation Ltd",
"target":"Training of Minority rural artisans",
"coverage":"",
"objectives":"The loan will be sanctioned to the poor religious minority rural artisans to improve their economics status and to overcome BPL.",
"eligibility":"(a) Resident of Karnataka by birth or domicile (b) Belong to the religious minority community (c) Family annual income should within Rs.22,000/- to apply for loan",
"documents":"(a) Attested copy of address proff (b) Caste Certificate (c ) Income Certificate (d) Documentary proof for estimated cost for start up (e ) Bank account details ",
"benefits":"(a) Training to minority artisans to upgrade their artistic and technical skills (b) Loan of upto Rs.25000/- will be provided at a low rate of interest i.e., 4% to set up and improve their business. 75% will be considered as a loan and 25% will be considered as back end subsidy.  ",
"refurl":"http://kmdc.kar.nic.in/PDF/shramashakthi-scheme.pdf"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/8' -d '
{
"sid": 8,
"name": "Thayi Bhagya",
"funding":"State",
"dept":"Ministry of Health and Family Welfare",
"target":"Pregnant women in BPL families",
"coverage":"C category districts of Gulbarga, Bidar, Raichur, Koppal, Bijapur and Bagalkot and the backward district Chamarajanagar.",
"objectives":"The scheme provides totally free service for the pregnant women belonging to BPL families in registered private hospitals.",
"eligibility":"(a) Pregnant women in BPL families",
"documents":"(a) BPL card (b) ANC Card",
"benefits":"Pregnant woman belonging to BPL family can avail delivery services free of cost in the registered private hospital near her house",
"refurl":"http://karhfw.gov.in/NRHM/PrTHAYIBHAGYAScheme.aspx"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/9' -d '
{
"sid": 9,
"name": "Indira Awaas Yojana (IAY)",
"funding":"Central and State",
"dept":"Ministry of Rural Development, GoI",
"target":"BPL families",
"coverage":"",
"objectives":"To help construction/upgradation of dwelling units of members of SC/ST, freed bonded labourers, minorities in the BPL families and BPL non-SC/ST rural households.",
"eligibility":"(a) BPL households living in the rural areas (b) Applicable to Scheduled Castes/Scheduled tribes, freed bonded labourees, minorities in the BPL category and non-SC/ST BPL rural households, widows and next-of-kin to defence personnel/paramilitary forces killed in action residing in rural areas (irrespective of their income criteria), ex-servicemen and retired members of paramilitary forces. (c) Women in difficult circumstance-widows, divorced, deserted  (d) Mentally challenged persons with atleast 40% disability (e) Transgender persons ",
"documents":"(a) BPL card (b) ANC Card",
"benefits":"(a) Lumpsum financial assistance to the eligible BPL and non-BPL families (i) Financial assistance for construction of a new house is Rs 70000- in plain areas and Rs 75000 in hilly/difficult/IAP areas. (ii) Financial assistance for upgradation of Kutcha or dilapidated house is Rs15000 (iii) Financial assistance for acquiring house site is Rs 20000. (b)  An amount of Rs 20000 is provided for acquiring plot to an IAY beneficiary ",
"refurl":"http://ashraya.kar.nic.in/"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/10' -d '
{
"sid": 10,
"name": "Santhwana",
"funding":"State",
"dept":"Department of Women and Child Development",
"target":"Assistance to distress women",
"coverage":"",
"objectives":"To provide assistance to distressed women so as to help them to be self-reliant and achieve social and economic empowerment. ",
"eligibility":"Women who are victims of domestic violence, rape, sexual abuse and dowry harassment.",
"documents":"",
"benefits":"(a) Legal assistance, temporary shelter, financial relief and training to distressed women. (b) If the woman is in immediate need of financial help an amount ranging from Rs. 2000/- to a maximum of Rs. 10000/- is sanctioned as financial relief.",
"refurl":"http://dwcdkar.gov.in/index.php?option=com_content&view=article&id=70&Itemid=115&lang=en"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/11' -d '
{
"sid": 11,
"name": "Attendance Scholarship for girls from rural areas",
"funding":"State",
"dept":"Department of Women and Child Development",
"target":"Education of girl children in rural areas",
"coverage":"Implemented in 18 educationally backward districts  through Zilla Panchayaths.  ",
"objectives":"Scholarship is provided to girls from rural areas to reduce the dropout rate in primary and secondary school levels to encourage education of girl children.",
"eligibility":"(a) Only those girl children who have a  minimum of 80% attendance and successfully completion  examinations are eligible. (b) Family income of the girl must be below Rs. 10,000/- per  annum (c ) Girl child must be a resident of the village with a population less than 20,000.(d) A girl child who hails from educationally backward districts like Chamarajanagar, Bijapur, Bagalkot,  Raichur, Bidar, Koppal, Gulbarga  and Bellary is eligible for the scheme.",
"documents":"(a) Caste/Community Certificate (b) BPL Certificate (c ) Income Certificate",
"benefits":"(a) An amount of Rs. 25/ per month for10 months is given to girls studying in 5th to 7th  standard (b) Rs. 50/-  per month is given to girls studying in 8th to 10th standard.  ",
"refurl":"http://dwcdkar.gov.in/index.php?option=com_content&view=article&id=66%3Aattendance-scholarship-for-girls-from-rural-areasfor-&catid=108%3Awomen-welfare&Itemid=114&lang=en"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/12' -d '
{
"sid": 12,
"name": "Anna Bhagya Yojana",
"funding":"State",
"dept":"Food, Civil Supplies and Consumer Affairs Department",
"target":"Food security for BPL families",
"coverage":"10th July 2013",
"objectives":"To ensure food security among BPL households",
"eligibility":"(a) BPL families",
"documents":"",
"benefits":"(a) Subsidized rice to BPL families-  Supply 30 kg foodgrains at Rs 1 per kg to BPL families   1.1 Single member cardholders would get 10 kg per month       1.2 Two-member ones 20 kg       1.3 Three and above would get a maximum of 30 kg",
"refurl":"http://ahara.kar.nic.in/annabhagyyojana.html"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/13' -d '
{
"sid": 13,
"name": "Navachetana",
"funding":"State",
"dept":"Department of social Welfare",
"target":"Livelihoods promotion for SC unemployed youth",
"coverage":"1996",
"objectives":"To provide training to unemployed Scheduled Castes youths in various trades",
"eligibility":"(a) must be a Scheduled Caste unemployed youth.(b) must have registered his name in the local employment exchange (c) must be within the age group 18 to 35 years (d) should not have already under gone training in any other government agencies. (e) must not be a student.",
"documents":"",
"benefits":"(a) Training to SC unemployed youth to make them self-reliant.(b) Various trades- crafts like Carpentry, Smithing, Fitters, Turners, Welders, Gear Cutting, Flute milling, Lathe, Automobile, Garments, hotel industry, Leather industry, IT sector, Hardware sector, TV repairs, Home appliances repairs, screen printing etc., depending upon the qualification of the candidate, his aptitude and skill.(c) Training is imparted through Govt, semi Govt, Public sector and reputed private sector organisations.",
"refurl":"http://sw.kar.nic.in/emptrng_files/empNtrng-navachetana.htm"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/14' -d '
{
"sid": 14,
"name": "National Programme for Health Care of the Elderly (NPCHE)",
"funding":"Central",
"dept":"Ministry of Health and Family Welfare",
"target":"Health care of elderly",
"coverage":"1996",
"objectives":"To address various health related problems of elderly people.",
"eligibility":"All elderly People (above 60 Years) in the country. ",
"documents":"",
"benefits":"Free, Specialized health care facilities exclusively for the elderly people through the State health delivery system.",
"refurl":"http://mohfw.nic.in/index1.php?lang=1&level=2&sublinkid=2183&lid=1879"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/15' -d '
{
"sid": 15,
"name": "Rashtriya Arogya Nidhi (RAN)",
"funding":"Central",
"dept":"Ministry of Health and Family Welfare",
"target":"Financial assistance to Poor patients",
"coverage":"1996",
"objectives":"To provide financial assistance to patients belonging to BPL families",
"eligibility":"(a) Only for BPL persons suffering from specified life threatening disease. (b)  Central Government/State Government/PSU employees are not eligible. (c) Assistance admissible for treatment in Government Hospital only.(d) Re-imbursement of medical expenditure already incurred not permissible. (e) Diseases of common nature and disease for which treatment is available free of cost under other health schemes are not eligible for grant.",
"documents":"(a) Below Poverty Line ration card (b) Income certificate from Govt revenue authorities",
"benefits":"Financial assistance to poor patients for healthcare",
"refurl":"http://mohfw.nic.in/index1.php?lang=1&level=1&sublinkid=1988&lid=1817"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/16' -d '
{
"sid": 16,
"name": "Sandhya Surakshay Yojana (Ssy)",
"funding":"State",
"dept":"The Directorate of Social Security and Pensions (DSSP), Revenue Department",
"target":"Elderly pension",
"coverage":"",
"objectives":"To help eligible elderly citizens by providing them with direct cash pensions.",
"eligibility":"(a) Beneficiaries are selected from among small farmers, marginal farmers, Agricultural farmers, weavers and unorganized workers. (b) Elderly persons between 60-79 years of age (c) Annual income of the elderly person must not exceed Rs. 20,000 per annum (d) Persons availing old age pension, destitute widow pension, physically handicapped pension or any form of pension from public / private sources are not eligible for this scheme.",
"documents":"(a) Below Poverty Line ration card (b) Income certificate from Govt revenue authorities",
"benefits":"Elderly pension",
"refurl":"http://www.graam.org.in/completed-projects"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/17' -d '
{
"sid": 17,
"name": "Annapoorna Yojana",
"funding":"Central",
"dept":"Food Supply and Commerce Department",
"target":"Old destitutes",
"coverage":"1st April, 2004",
"objectives":"To ensure food security for old desitutes",
"eligibility":"Under this scheme old destitutes are above 65 years of age and not covered in state or central social security pension scheme;  who are not getting the National old age pension (NOAPS) but have its eligibility, are being provided 10 kg food-grain (6 kg wheat + 4 kg rice) per month free of cost as Food Security. They are issued special green ration cards.",
"documents":"(a) Below Poverty Line ration card (b) Income certificate from Govt revenue authorities",
"benefits":"Old destitutes",
"refurl":"http://dssp.kar.nic.in/Annapoorna.html"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/18' -d '
{
"sid": 18,
"name": "National Family Benefit Scheme (NFBS)",
"funding":"State",
"dept":"Community and rural department",
"target":"BPL families",
"coverage":"To provide assistance to the poor and to ensure minimum national standard for social assistance.",
"objectives":"To ensure food security for old desitutes",
"eligibility":"(a) Age of the deceased person should have been between 18 and 65 at the time of death. (b) Primarily for BPL families. ",
"documents":"",
"benefits":"The NFBS provides a lump sum family benefit of Rs. 10000 to the bereaved household in case of death of the primary bread winner irrespective of the cause of death. ",
"refurl":"http://nsap.nic.in"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/19' -d '
{
"sid": 19,
"name": "MADILU",
"funding":"State",
"dept":"Ministry of Health and Family Welfare",
"target":"Mother and child",
"coverage":"To provide assistance to the poor and to ensure minimum national standard for social assistance.",
"objectives":"To encourage poor pregnant women to deliver in health centres and hospitals in order to considerably reduce maternal and infant mortality.",
"eligibility":"(a) BPL and SC/ST families (b) Scheme is applicable only for 1st and 2nd deliveries. (c)  Applicable to only to those who undergo delivery in government hospitals or primary health centres through registered midwives in rural areas.",
"documents":"",
"benefits":"Kids containing 19 items essential to Mother & Baby in the post-delivery period are given to women in BPL category who have delivered in institutions.Each kit is worth Rs.825/ will be distributed free of cost to parents of each newborn child. It consists of 19 essential items for the benefit of mother and child. ",
"refurl":"http://karhfw.gov.in"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/20' -d '
{
"sid": 20,
"name": "Prasooti Araike",
"funding":"State",
"dept":"Ministry of Health and Family Welfare",
"target":"Pregnant women in BPL families",
"coverage":"All districts in Karnataka",
"objectives":"To provide assistance to pregnant women belonging to BPL families.",
"eligibility":"(a) Pregnant women belonging to BPL families (b) Limited to the first two deliveries.",
"documents":"",
"benefits":"(a) Incentives to BPL women who belong to SC/ST category to help them during prenatal and postnatal period.(b) Rs.1500/-is given in cash and Rs.500/-in kind to compensate wage loss.",
"refurl":"http://karhfw.gov.in"
}'

curl -XPUT 'http://localhost:9200/gov/scheme/21' -d '
{
"sid": 21,
"name": "Rashtriya Swasthya Bhima Yojana (RSBY)",
"funding":"Central",
"dept":"Department of Labour",
"target":"Health care of BPL households",
"coverage":"15th August 2007",
"objectives":"To provide protection to BPL households from financial liabilities arising out of health shocks that involve hospitalization",
"eligibility":"(a) Coverage extends to the head of household, spouse and up to three dependents. (b) Pre-existing medical  conditions are covered (c) No age limit. ",
"documents":"(a) BPL card (b) Smart card",
"benefits":"(a) Access to BPL families to quality medical care for treatment involving hospitalization and surgery among health care providers. Insurance limit is Rs 30000 per annum for a family of 5 members. (b) Transportation cost of Rs. 100/‐ per visit with an overall limit of Rs. 1,000/‐ per annum is also admissible under the scheme. ",
"refurl":"http://www.rsby.gov.in/about_rsby.aspx"
}'


