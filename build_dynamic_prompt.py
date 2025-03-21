import random
import re
from csv_reader import *
from random_functions import *



#Builds a prompt dynanically
# insanity level controls randomness 0-10
# forcesubject can be used to force a certain type of subject
# Set artistmode to none to exclude artists.
def build_dynamic_prompt(insanitylevel = 5, forcesubject = "all", artistmode = "all", imagetype = "all"):
    completeprompt = " "

    isphoto = 0
    othertype = 0
    humanspecial = 0
    #wereanimaladded = 0
    isweighted = 0
    hybridorswap = ""

    if(insanitylevel==0):
        insanitylevel = random.randint(1, 10) # 10 = add everything, 1 is add almost nothing
    insanitylevel3 = int(insanitylevel/3) + 1
    print("Setting insanity level to " + str(insanitylevel))

    #main chooser: 0 object, 1 humanoid, 2 landscape, 3 event/concept
    mainchooserlist = ["object","humanoid","landscape","concept"]
    mainchooser = mainchooserlist[random.randint(0, 3)]

    if(forcesubject != "" and forcesubject != "all"):
        mainchooser = forcesubject
    # 0 object, 1 ManWoman, 2 Job, 3 fictional, 4 non-fictional, 5 humanoid, 6 landscape, 7 concept
    if(mainchooser == "object"):
        subjectchooser = "object"
    #if(mainchooser == "animal"):
        # sometimes interpret animal as human
        #if(random.randint(0,5) < 5):
            #subjectchooser = "animal"
        #else:
            #subjectchooser = "animal as human"
    if(mainchooser == "humanoid"):
        subjectchooserlist = ["human", "job", "fictional", "non fictional", "humanoid"]
        subjectchooser = subjectchooserlist[random.randint(0, 4)]
    if(mainchooser == "landscape"):
        subjectchooser = "landscape"
    if(mainchooser == "concept"):
        subjectchooserlist = ["event", "concept"]
        subjectchooser = subjectchooserlist[random.randint(0, 1)]

    hybridlist = [ "-object-", "-fictional-", "-nonfictional-", "-building-", "-vehicle-"]
    hybridhumanlist = ["-fictional-", "-nonfictional-"]

    # possible?: think about curated artist list?

    if(artistmode == "all"):
        # take 1-3 artists, weighted to 1-2
        step = random.randint(0, 1)
        end = random.randint(1, insanitylevel3)




        # determine artist mode:
        # normal
        # hybrid |
        # switching A:B:X
        # adding at step x a:X
        # stopping at step x ::X
        # enhancing from step  x

        artistmode = "normal"
        modeselector = random.randint(0, 10)
        if modeselector < 5 and end - step >= 2:
            artistmodelist = ["hybrid", "stopping", "adding", "switching", "enhancing"]
            artistmode = artistmodelist[modeselector]
            if artistmode in ["hybrid","switching"] and end - step == 1:
                artistmode = "normal"

        if artistmode in ["hybrid", "stopping", "adding", "switching"]:
            completeprompt += " ["

        while step < end:
            if(normal_dist(insanitylevel)):
                isweighted = 1

            if isweighted == 1:
                completeprompt += " ("

            completeprompt = add_from_csv(completeprompt, "artists", 0, "art by ", "")

            if isweighted == 1:
                completeprompt += ":" + str(1 + (random.randint(-3,3)/10)) + ")"

            if artistmode in ["hybrid"] and not end - step == 1:
                completeprompt += "|"
            if artistmode in ["switching"] and not end - step == 1:
                completeprompt += ":"
        
            if artistmode not in ["hybrid", "switching"]and not end - step == 1:
                completeprompt += ","
            
            isweighted = 0
            
            step = step + 1

        if artistmode in ["stopping"]:
            completeprompt += "::"
            completeprompt += str(random.randint(1,19))
        
        if artistmode in ["switching","adding"]:
            completeprompt += ":" + str(random.randint(1,18))
        if artistmode in ["hybrid", "stopping","adding", "switching"]:
            completeprompt += "]"


        completeprompt = completeprompt + ", "

        if artistmode in ["enhancing"]:
            completeprompt += " ["
    
    if(imagetype != "all"):
            completeprompt += " " + imagetype + " "
    elif(normal_dist(insanitylevel)):
    # one in 6 images is a complex/other type
        if(random.randint(0,5) < 5):
            completeprompt = add_from_csv(completeprompt, "imagetypes", 1, "",",")
        else:
            othertype = 1
            completeprompt = add_from_csv(completeprompt, "othertypes", 1, ""," of a ")


    if(mainchooser in ["object", "humanoid", "concept"] and othertype == 0 and "portait" not in completeprompt):
        completeprompt = add_from_csv(completeprompt, "shotsizes", 0, ""," of a ")
    elif("portait" in completeprompt):
        completeprompt += " ,close up of a "
   # Multiple subjects doesnt really work, need to think of other way to do multiple subjects. Maybe AND in the prompt?
   # if(subjectchooser in ["object", "animal", "humanoid"] and rare_dist(insanitylevel)):
   #     completeprompt = completeprompt[:-2] # remove a from 
   #     completeprompt = add_from_csv(completeprompt, "amounts", 0, "","")      

    if(common_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "descriptors", 0, "","")

    if(uncommon_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "descriptors", 0, "","")

    if(subjectchooser in ["animal as human,","human", "job", "fictional", "non fictional", "humanoid"] and normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "body_types", 0, "","")

    #if(subjectchooser in ["object","animal as human,","human", "job", "fictional", "humanoid"] and normal_dist(insanitylevel)):
    #    completeprompt = add_from_csv(completeprompt, "ethnicity", 0, "","")

    if(mainchooser == "object"):
        objecttypelist = ["objects", "buildings"]
        
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["

        completeprompt = add_from_csv(completeprompt, random.choice(objecttypelist), 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + random.choice(hybridlist) + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + random.choice(hybridlist) + ":" + str(random.randint(1,5)) +  "]"
        hybridorswap = ""

    """ if(mainchooser == "animal"):
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["
            
        if unique_dist(insanitylevel):
            wereanimaladded = 1
            completeprompt += "were-animal-"
        if(wereanimaladded != 1):
            completeprompt = add_from_csv(completeprompt, "animals", 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + random.choice(hybridlist) + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + random.choice(hybridlist) + ":" + str(random.randint(1,5)) +  "]"
        hybridorswap = "" """
    
    if(subjectchooser == "human"):
        completeprompt = add_from_csv(completeprompt, "manwoman", 0, "","")

    if(subjectchooser == "job"):
        completeprompt = add_from_csv(completeprompt, "malefemale", 0, "","")
        completeprompt = add_from_csv(completeprompt, "jobs", 0, "","")

    if(subjectchooser == "fictional"):
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["
        
        completeprompt = add_from_csv(completeprompt, "fictional characters", 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + random.choice(hybridhumanlist) + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + random.choice(hybridhumanlist) + ":" + str(random.randint(1,5)) +  "]"
        hybridorswap = ""

    if(subjectchooser == "non fictional"):
       if rare_dist(insanitylevel):
           hybridorswaplist = ["hybrid", "swap"]
           hybridorswap = random.choice(hybridorswaplist)
           completeprompt += "["

       completeprompt = add_from_csv(completeprompt, "nonfictional characters", 0, "","")

       if(hybridorswap == "hybrid"):
           completeprompt += "|" + random.choice(hybridhumanlist) + "]"
       if(hybridorswap == "swap"):
           completeprompt += ":" + random.choice(hybridhumanlist) + ":" + str(random.randint(1,5)) +  "]"
       hybridorswap = ""

    if(subjectchooser == "humanoid"):
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["
        
        completeprompt = add_from_csv(completeprompt, "humanoids", 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + random.choice(hybridhumanlist) + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + random.choice(hybridhumanlist) + ":" + str(random.randint(1,5)) +  "]"
        hybridorswap = ""

    if(subjectchooser == "landscape"):
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["
        
        completeprompt = add_from_csv(completeprompt, "locations", 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + "-location-"  + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + "-location-" + ":" + str(random.randint(1,5)) +  "]"        
        hybridorswap = ""

        if(normal_dist(insanitylevel)):
            addontolocation = ["locations","buildings"]
            completeprompt = add_from_csv(completeprompt, random.choice(addontolocation), 0, "and ","")
    
    if(subjectchooser == "event"):
        completeprompt = add_from_csv(completeprompt, "events", 0, "\"","\"")
    
    if(subjectchooser == "concept"):
        completeprompt = add_from_csv(completeprompt, "concept_prefix", 0, "\" The "," of ")
        completeprompt = add_from_csv(completeprompt, "concept_suffix", 0, "","\"")

    # object with a face
    if(mainchooser == "object" and legendary_dist(insanitylevel)):
        completeprompt += " with a face "

    # object materials
    if(mainchooser == "object" and normal_dist(insanitylevel)):
        completeprompt += "made from -material- "
    
    # riding an animal, holding an object or driving a vehicle, rare
    if(subjectchooser in ["animal as human,","human","fictional", "non fictional", "humanoid"] and rare_dist(insanitylevel)):
        humanspecial = 1
        speciallist = [ " holding a -object- ", " visiting a -building-"]
        completeprompt += random.choice(speciallist)

    # SD understands emoji's. Can be used to manipulate facial expressions.
    # emoji, legendary
    if(subjectchooser in ["animal as human,","human","fictional", "non fictional", "humanoid"] and legendary_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "emojis", 1, "","")
        completeprompt += " ,"

    # cosplaying
    if(subjectchooser in ["animal as human", "non fictional", "humanoid"] and rare_dist(insanitylevel) and humanspecial != 1):
        completeprompt = add_from_csv(completeprompt, "fictional characters", 0, "cosplaying as ","")

    # Job 
    if(subjectchooser in ["animal as human","human","fictional", "non fictional", "humanoid"]  and normal_dist(insanitylevel) and humanspecial != 1):
        completeprompt = add_from_csv(completeprompt, "jobs", 1, "","")

    if(subjectchooser in ["animal as human","human","job", "fictional", "non fictional", "humanoid"] and normal_dist(insanitylevel) and humanspecial != 1):
        completeprompt = add_from_csv(completeprompt, "human_activities", 1, "","")

    if(subjectchooser in ["animal as human","human","job", "fictional", "non fictional", "humanoid"] and legendary_dist(insanitylevel)):
        completeprompt += ", with -color- skin, "

    # outfit builder
    if(subjectchooser in ["animal as human","human","fictional", "non fictional", "humanoid"]  and normal_dist(insanitylevel)):
        completeprompt = " ".join([completeprompt, ", wearing"])
        if(normal_dist(insanitylevel)):
            completeprompt = add_from_csv(completeprompt, "descriptors", 0, "","")
        if(normal_dist(insanitylevel)):
            completeprompt += " -color- "
        if(rare_dist(insanitylevel)):
            completeprompt += " -material- "
        
        if rare_dist(insanitylevel):
            hybridorswaplist = ["hybrid", "swap"]
            hybridorswap = random.choice(hybridorswaplist)
            completeprompt += "["
        
        completeprompt = add_from_csv(completeprompt, "outfits", 0, "","")

        if(hybridorswap == "hybrid"):
            completeprompt += "|" + "-outfit-" + "]"
        if(hybridorswap == "swap"):
            completeprompt += ":" + "-outfit-" + ":" + str(random.randint(1,5)) +  "]"  
        hybridorswap = ""      

    if(subjectchooser in ["human","job","fictional", "non fictional", "humanoid"]  and normal_dist(insanitylevel)):
            completeprompt = completeprompt + ", "
            completeprompt = add_from_csv(completeprompt, "haircolors", 0, "","")
    #        completeprompt = add_from_csv(completeprompt, "hairstyles", 0, " hair styled as ","")

    if(subjectchooser in ["animal as human,","human","fictional", "non fictional", "humanoid"]  and normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "accessories", 1, "","")

    
    if(subjectchooser not in ["landscape", "concept"]  and normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "locations", 1, " background is ","")

    if(subjectchooser not in ["landscape", "concept"] and humanspecial != 1 and normal_dist(insanitylevel)):
        backgroundtype = ["landscape", "buildingbackground", "insidebuilding"]
        match random.choice(backgroundtype):
            case "landscape":
                completeprompt = add_from_csv(completeprompt, "locaitons", 1, " background is ", "")
            case "buildingbackground":
                completeprompt = ",background is "
                if(uncommon_dist(insanitylevel)):
                    completeprompt = add_from_csv(completeprompt, "descriptors", 0, "", "")
                completeprompt = add_from_csv(completeprompt, "buildings", 0, "", "")
            case "insidebuilding":
                completeprompt = ",inside a "
                if(uncommon_dist(insanitylevel)):
                    completeprompt = add_from_csv(completeprompt, "descriptors", 0, "","")
                completeprompt = add_from_csv(completeprompt, "buildings", 0, "","")

    if(normal_dist(insanitylevel) or subjectchooser=="landscape"):
        completeprompt = add_from_csv(completeprompt, "timeperiods", 1, "","")

    if(mainchooser not in ["landscape"]  and normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "focus", 1, "","")
        
    # others
    if(normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "directions", 1, "","")   

    if(normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "moods", 1, "","")    

    #if(normal_dist(insanitylevel)):
    #    completeprompt = add_from_csv(completeprompt, "artmovements", 1, "","")     
    
    if(normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "lighting", 1, "","")    

    if("photo" in completeprompt):
        isphoto = 1
        if(common_dist(insanitylevel)):
            completeprompt = ", film grain"
            
    if(isphoto == 1):
        completeprompt = add_from_csv(completeprompt, "cameras", 1, "","")

    if(normal_dist(insanitylevel) or isphoto == 1):
        completeprompt = add_from_csv(completeprompt, "lenses", 1, "","")   

    if(normal_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "colorscheme", 1, "","")

    # vomit some cool/wierd things into the prompt
    if(uncommon_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "vomit", 1, "","")

    # everyone loves the adding quality. The better models don't need this, but lets add it anyway
    if(uncommon_dist(insanitylevel)):
        completeprompt = add_from_csv(completeprompt, "quality", 1, "","")


    if artistmode in ["enhancing"]:
        completeprompt += "::" + str(random.randint(1,17)) + "]"

    #replace any values
    colorlist = csv_to_list("colors")
    #animallist = csv_to_list("animals")    
    materiallist = csv_to_list("materials")
    objectlist = csv_to_list("objects")
    fictionallist = csv_to_list("fictional characters")
    nonfictionallist = csv_to_list("nonfictional characters")
    conceptsuffixlist = csv_to_list("concept_suffix")
    buildinglist = csv_to_list("buildings")
    #vehiclelist = csv_to_list("vehicles")
    outfitlist = csv_to_list("outfits")
    locationlist = csv_to_list("locations")
    
    # lol, this needs a rewrite :D 
    # ommited "-animal-",  "-vehicle-", "-outfit-"; "-nonfictional-" and "-outfit-" have alternative logic"
    while "-color-" in completeprompt or "-material-" in completeprompt or "-object-" in completeprompt or "-fictional-" in completeprompt or "-nonfictional-" in completeprompt or "-conceptsuffix-" in completeprompt or "-outfit-" in completeprompt or "-building-" in completeprompt or "-location-" in completeprompt:
        while "-object-" in completeprompt:
            completeprompt = completeprompt.replace('-object-', random.choice(objectlist),1)

        while "-location-" in completeprompt:
            completeprompt = completeprompt.replace('-location-', random.choice(locationlist),1)

        while "-outfit-" in completeprompt:
            completeprompt = completeprompt.replace('-outfit-', random.choice(outfitlist),1)
        
        while "-building-" in completeprompt:
            completeprompt = completeprompt.replace('-building-', random.choice(buildinglist),1)

        # while "-vehicle-" in completeprompt:
        #     completeprompt = completeprompt.replace('-vehicle-', random.choice(vehiclelist),1)
        
        while "-conceptsuffix-" in completeprompt:
            completeprompt = completeprompt.replace('-conceptsuffix-', random.choice(conceptsuffixlist),1)
        
        while "-color-" in completeprompt:
            completeprompt = completeprompt.replace('-color-', random.choice(colorlist),1)

        while "-material-" in completeprompt:
            completeprompt = completeprompt.replace('-material-', random.choice(materiallist),1)
        
        while "-fictional-" in completeprompt:
            completeprompt = completeprompt.replace('-fictional-', random.choice(fictionallist),1)
        
        while "-nonfictional-" in completeprompt:
            completeprompt = completeprompt.replace('-nonfictional-', random.choice(nonfictionallist),1)

        # while "-animal-" in completeprompt:
        #     completeprompt = completeprompt.replace('-animal-', random.choice(animallist),1)

    completeprompt = re.sub('\[ ', '[', completeprompt)
    completeprompt = re.sub(' \]', ']', completeprompt)
    completeprompt = re.sub(' \|', '|', completeprompt)
    completeprompt = re.sub(' \"', '\"', completeprompt)
    completeprompt = re.sub('\" ', '\"', completeprompt)
    completeprompt = re.sub('\( ', '(', completeprompt)
    completeprompt = re.sub(' \(', '(', completeprompt)
    completeprompt = re.sub('\) ', ')', completeprompt)
    completeprompt = re.sub(' \)', ')', completeprompt)
    
    completeprompt = re.sub(',,', ',', completeprompt)    
    completeprompt = re.sub(', ,', ',', completeprompt)
    completeprompt = re.sub(' , ', ',', completeprompt)
    completeprompt = re.sub(' +', ' ', completeprompt[2:]) # remove first character, that is always a comma. Remove any excess spaces
    
    print(completeprompt)
    return completeprompt
