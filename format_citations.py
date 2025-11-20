citations_text = """
South Los Angeles Historic Districts, Planning Districts and Multi-Property Resources - March 2012, accessed November 19, 2025, https://planning.lacity.gov/odocument/270bad25-1551-4272-9c9a-f37c63636ec4/SouthLosAngeles_HistoricDistrictsPlanningDistrictsandMulti-PropertyResources.pdf
West Adams Matters, accessed November 19, 2025, https://westadamsheritage.org/sites/default/files/WAHA_April-2015-News__.pdf
First African Methodist Episcopal Church Los Angeles - ArcGIS StoryMaps, accessed November 19, 2025, https://storymaps.arcgis.com/stories/9fc62ace418c4fd281089db90a3c5fc4
Hattie McDaniel - Wikipedia, accessed November 19, 2025, https://en.wikipedia.org/wiki/Hattie_McDaniel
Sugar Hill - SEGREGATION BY DESIGN, accessed November 19, 2025, https://www.segregationbydesign.com/los-angeles/sugar-hill
No. 117 - Beckett Residence - Big Orange Landmarks, accessed November 19, 2025, http://bigorangelandmarks.blogspot.com/2008/02/no-117-beckett-residence.html
LOS ANGELES CITYWIDE HISTORIC CONTEXT STATEMENT Context: African American History of Los Angeles, accessed November 19, 2025, https://planning.lacity.gov/odocument/7db8747f-87fb-4c6f-bb95-5482be050683/SurveyLA_AfricanAmericanHCS_05242019.pdf
Sugar Hill Historic District, West Adams | Los Angeles City Planning, accessed November 19, 2025, https://planning.lacity.gov/blog/sugar-hill-historic-district-west-adams
Sugar Hill Historic District - Historic Places Los Angeles - Resource Report, accessed November 19, 2025, https://hpla.lacity.org/reports/eb8e796c-927c-4b91-ba77-a5c6cc210c35
West Adams: 12 Facts to Know About the Neighborhood's Forgotten History - L.A. Taco, accessed November 19, 2025, https://lataco.com/west-adams-history
Homes and Highways: Rupture and Resistance in Los Angeles's West Adams Neighborhood - Environmental Inequality, accessed November 19, 2025, https://ejhistory.com/homes-and-highways/
JUL 2 3 2009 - LA City Clerk - City of Los Angeles, accessed November 19, 2025, https://cityclerk.lacity.org/onlinedocs/2009/09-1851_rpt_chc_7-23-09.pdf
Hattie McDaniel Residence - LA Conservancy, accessed November 19, 2025, https://www.laconservancy.org/learn/historic-places/hattie-mcdaniel-residence/
Black L.A. 1947: A Guide to the Homes of Famous Black Entertainers | - Larry Harnisch, accessed November 19, 2025, https://ladailymirror.com/2018/08/22/black-l-a-1947-a-guide-to-the-homes-of-famous-black-entertainers/
Search form - West Adams Heritage Association | in Historic West Adams, Los Angeles, California, accessed November 19, 2025, https://westadamsheritage.org/read/1290
accessed November 19, 2025, https://en.wikipedia.org/wiki/Ben_Carter_(actor)#:~:text=Carter%20was%20a%20member%20of,Angeles%2C%20California%2C%20in%201942.
Making a "black Beverly Hills": The struggle for housing equality in modern Los Angeles - UNH Scholars Repository, accessed November 19, 2025, https://scholars.unh.edu/context/dissertation/article/1538/viewcontent/3442534.pdf
Sugar Hill in West Adams, once home to Los Angeles' Black elite, before-and-after construction of the Santa Monica Freeway (I-10). "Before" photos colorized in photoshop. - Reddit, accessed November 19, 2025, https://www.reddit.com/r/LosAngeles/comments/17h46xs/sugar_hill_in_west_adams_once_home_to_los_angeles/
Hidden Gems of Los Angeles: West Adams District | FilmLA, accessed November 19, 2025, https://filmla.com/hidden-gems-of-los-angeles-west-adams-district/
A Storied Los Angeles Club for African American Women Looks to the Future, accessed November 19, 2025, https://savingplaces.org/stories/a-storied-los-angeles-club-for-african-american-women-looks-to-the-future
HfSTORIC-C1JLTURAL MONUMENT NOMINATION FORM - LA City Clerk - City of Los Angeles, accessed November 19, 2025, https://cityclerk.lacity.org/onlinedocs/2015/15-0326_misc_a_3-20-15.pdf
A History of Restrictive Covenants in California, accessed November 19, 2025, https://www.cschs.org/wp-content/uploads/2025/04/2025-CSCHS-Review-Spring-Restrictive-Covenants.pdf
CALIFORNIA: Victory on Sugar Hill - Time Magazine, accessed November 19, 2025, https://time.com/archive/6772901/california-victory-on-sugar-hill/
West Adams Matters, accessed November 19, 2025, https://westadamsheritage.org/sites/default/files/March2014_News_FINAL.pdf
Black Americans And The Racist Architecture Of Homeownership | KPBS Public Media, accessed November 19, 2025, https://www.kpbs.org/news/2021/05/08/black-americans-and-the-racist-architecture-of
Cordary Family Residence and Pacific Ready-Cut Cottage 1828-1830 South Gramercy Place - Los Angeles City Planning, accessed November 19, 2025, https://planning.lacity.gov/StaffRpt/CHC/2018/5-3-2018/CordaryFamilyResidence_PacificReadyCutCottage_1828Gramercy_FINAL.pdf
West Adams Heights, Los Angeles - Wikipedia, accessed November 19, 2025, https://en.wikipedia.org/wiki/West_Adams_Heights,_Los_Angeles
REBELLIOUS LAWYERS FOR FAIR HOUSING: THE LOST SCIENTIFIC MODEL OF THE EARLY NAACP - Wisconsin Law Review, accessed November 19, 2025, https://wlr.law.wisc.edu/wp-content/uploads/sites/1263/2021/12/14-Bliss-Camera-Ready.pdf
West Adams, Los Angeles - Wikipedia, accessed November 19, 2025, https://en.wikipedia.org/wiki/West_Adams,_Los_Angeles
West Adams, Los Angeles Facts for Kids, accessed November 19, 2025, https://kids.kiddle.co/West_Adams,_Los_Angeles
Highways destroyed hundreds of urban neighborhoods. What's the solution? | Allendale Strong, accessed November 19, 2025, https://allendalestrong.org/2021/05/28/105/
Berkeley Square, Los Angeles - Wikipedia, accessed November 19, 2025, https://en.wikipedia.org/wiki/Berkeley_Square,_Los_Angeles
accessed November 19, 2025, https://en.wikipedia.org/wiki/Berkeley_Square,_Los_Angeles#:~:text=The%20development%2C%20located%20several%20blocks,Gramercy%20Place%20on%20the%20west.
Stories of Sugar Hill - Architecture + Advocacy, accessed November 19, 2025, https://architectureandadvocacy.org/en/blog/stories-of-sugar-hill
"""

lines = citations_text.strip().split('\n')
html_output = "<p><strong>Works cited</strong></p>\n<ul>\n"

for line in lines:
    line = line.strip()
    if not line: continue
    
    # Find the URL
    url_start = line.find("http")
    if url_start == -1:
        print(f"Skipping line (no URL): {line}")
        continue
        
    url = line[url_start:].strip()
    text_part = line[:url_start].strip()
    
    # Remove trailing comma from text part if present
    if text_part.endswith(','):
        text_part = text_part[:-1].strip()
        
    # Extract "accessed Date" if present
    accessed_marker = ", accessed "
    title = text_part
    accessed_date = ""
    
    if accessed_marker in text_part:
        parts = text_part.split(accessed_marker)
        title = parts[0].strip()
        accessed_date = "accessed " + parts[1].strip()
    elif "accessed " in text_part:
         # Handle case where it starts with accessed
         if text_part.startswith("accessed "):
             title = "Source" # Fallback if no title
             accessed_date = text_part
         else:
             # Try splitting by last comma?
             pass

    # Construct list item
    # Format: Title, accessed Date, <a href="URL">Link</a>
    # Or: <a href="URL">Title</a>, accessed Date
    # Let's go with: <a href="URL" target="_blank">Title</a> (accessed Date)
    
    if not title or title == "Source":
        # Use domain or something as title? Or just the URL?
        title = url
        
    html_output += f'    <li><a href="{url}" target="_blank">{title}</a> ({accessed_date})</li>\n'

html_output += "</ul>"

print(html_output)
