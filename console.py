descriptions = {
    "/menu": "ወደ ዋናው ዝርዝር መልሰኝ",
    "/categories": "ከእኔ ፍላጎት አንጻር አሳየኝ",
    "/stop": "አገልግሎቱን አቋርጥ",

    "/all_ads": "ሁሉንም ቦርድ ላይ የተለተፉ ማስታዎቂያዎች አሳየኝ",
    "/new_ads": "ዛሬ ቦርድ ላይ የተለጠፉ ማስታዎቂያዎች አሳየኝ",
    
    "/products": "የድርጅት የምርት ማስታወቂያ",
    "/exhibition": "የእግዚብሽን ማስታወቂያ",
    "/bid": "የጨረታ ማስታወቂያ",
    "/lottery": "የሎተሪ ማስታወቂያ",
    "/brochure": "የብሮሸሮች ማስታወቂያ",
    "/education": "የትምህርት ማስታወቂያ",
    "/art": "የኪነ-ጥበብ ማስታወቂያ",
    "/vacancy": "የሥራ ቅጥር ማስታወቂያ",
    "/call": "የጥሪ ማስታወቂያ",
    "/social": "የተለያዩ ዐብይ ማኅንራዊ መልክቶች ማስታወቂያ",
    "/meetings": "የጥሪ ማስታወቂያ",
    "/vital_event": "የልደት፣ የሞት፣ የመታሰቢያ፣ የሠርግ ማስታወቂያ",
    "/assistance": "የርዳታ ማስታዎቂያ",
    "/missing": "የአፋልጉኝ ማስታዎቂያ",
}



def start(user_name, all_posts, new_posts):
    return f"ውድ { user_name } እንኳን በሰላም መጡ፡፡ ዛሬ { new_posts }"\
        + f" አዳዲስ ማስታዎቂያ(ዎች) ቦርድ ላይ ተለጥፈዋል፡፡ በተጨማሪም { all_posts }"\
        + f" ማስታዎቂያ(ዎች) በአሁኑ ሰአት ቦርድ ላይ ተለጥፈው ይገኛሉ፡፡ እባክዎ በምን መልኩ ማየት እንደሚፈልጉ ይምረጡ?\n"\
        + menu()


def stop(contact=""):
    return "በአገልግሎቱ እንደተደሰቱ ተስፋ እናደርጋልን፡፡ እባክዎ ሃሳብ ወይም አስተያየት ካልዎት"\
        + f" በ {contact} ያግኙን፡፡\n\nመልካም ቀን፡፡\n\nእንደገና አገልግሎቱን ለማግኘት /start ይጫኑ፡፡"


def categories(end_prompt=False):
    if end_prompt:
        return "ወደ ማስታዎቂያ አይነቶች ዝርዝር መልሰኝ"
    else:
        return f"""
/products - {descriptions["/products"]}
/exhibition - {descriptions["/exhibition"]}
/bid - {descriptions["/bid"]}
/lottery - {descriptions["/lottery"]}
/brochure - {descriptions["/brochure"]}
/education - {descriptions["/education"]}
/art - {descriptions["/art"]}
/vacancy - {descriptions["/vacancy"]}
/call - {descriptions["/call"]}
/social - {descriptions["/social"]}
/meetings - {descriptions["/meetings"]}
/assistance - {descriptions["/assistance"]}
/missing - {descriptions["/missing"]};
"""


def menu():
    return f"""
/all_ads - {descriptions["/all_ads"]}
/new_ads - {descriptions["/new_ads"]}
/categories - {descriptions["/categories"]}
"""


def prompt_after_img(category=False):
    if category:
        return f"""
/categories - {categories(end_prompt=True)}
/menu - {descriptions["/menu"]}
/stop - {descriptions["/stop"]}
        """
    return f"""
/menu - {descriptions["/menu"]}
/stop - {descriptions["/stop"]}
"""

# Commands
cmds = {
    "/categories": categories,
    "/menu": menu,
}


categories_list = list(descriptions.keys())[5:]