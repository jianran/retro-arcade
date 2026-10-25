"""
Clue Hunt — all static game data: families, locations, puzzles, shop items.
"""

FAMILIES = {
    "python": {
        "name": "Python",
        "motto": "Logic conquers all.",
        "color": "\033[32m",
        "bonus": "Starts with one random weapon in inventory.",
        "trait": "Masters of lethal inventory — begin the race already armed.",
    },
    "rally": {
        "name": "Rally",
        "motto": "Strike first, strike true.",
        "color": "\033[31m",
        "bonus": "Starts with 20 Health Points instead of 10.",
        "trait": "High endurance — double the health of any other family.",
    },
    "cyber": {
        "name": "Cyber",
        "motto": "Information is the ultimate weapon.",
        "color": "\033[36m",
        "bonus": "One free decryption / code-breaking hint per clue location.",
        "trait": "Tech geniuses — type 'decrypt' at any location for a free puzzle hint.",
    },
    "encyclopedia": {
        "name": "Encyclopedia",
        "motto": "Knowledge never fails.",
        "color": "\033[33m",
        "bonus": "One free historical trivia / lore hint per clue location.",
        "trait": "Infinite knowledge — type 'lore' at any location for deep historical context.",
    },
}

# ── Locations & Puzzles ──────────────────────────────────────────────

LOCATIONS = [
    {
        "id": "franklin_institute",
        "name": "Franklin Institute",
        "city": "Philadelphia, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 1,
        "mystery": "The marble halls of the Franklin Institute lie silent after hours. A janitor's\nreport mentions a strange blue spark arcing across the massive Tesla coil in the\nelectricity exhibit at exactly 10:04 PM — the moment of Ben Franklin's legendary\nkite experiment. Security footage shows a shadow pressing something into the base\nof the Lightning Rod obelisk in the courtyard.",
        "stages": [{
            "desc": "You stand beneath the giant Tesla coil. The air smells of ozone. A loose floor tile\nhas faint scorch marks. Something glints beneath it.",
            "triggers": ["examine tesla coil", "search floor", "check loose tile", "lift tile", "examine obelisk", "look under coil", "inspect tile", "search courtyard", "examine lightning rod"],
            "success": "Beneath the loose tile: a brass plaque with Franklin's words. Below, a second\nengraving glows faintly: 'What force did I capture from the heavens in 1752?'",
            "hint": "Look near the Tesla coil. There's something under the loose floor tile."
        }],
        "final_answer": "LIGHTNING",
        "answer_hint": "What Franklin famously captured from the sky in 1752 (9 letters).",
        "points": 5,
        "lore": "Founded in 1824, the Franklin Institute is a hands-on science museum. Ben Franklin's 1752 kite experiment proved lightning is electrical."
    },
    {
        "id": "smithsonian_castle",
        "name": "Smithsonian Castle",
        "city": "Washington D.C., USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 2,
        "mystery": "The red sandstone towers loom over the National Mall. An intercepted curator email\nmentions a hidden safe behind the portrait of James Smithson — the British founder\nwho never set foot in America. The safe's combination is tied to his name.",
        "stages": [{
            "desc": "James Smithson's portrait hangs above a fireplace in the Castle's west wing. The\ngilded frame is slightly crooked, with a rectangular outline on the wallpaper.",
            "triggers": ["examine portrait", "look behind painting", "check smithson", "move painting", "search frame", "examine fireplace", "look behind frame", "check wall", "check portrait"],
            "success": "Behind the portrait, a wall safe bears a golden plate: 'Who am I? I gave my fortune\nto a nation I never saw. My legacy became the world's largest museum complex.'",
            "hint": "Behind the portrait of James Smithson. The curators' hiding spot."
        }],
        "final_answer": "SMITHSON",
        "answer_hint": "The British scientist whose fortune founded the Smithsonian (8 letters).",
        "points": 5,
        "lore": "James Smithson (1765-1829) left $500,000 to the US to found the Smithsonian. He never visited America in his lifetime."
    },
    {
        "id": "statue_of_liberty",
        "name": "Statue of Liberty Pedestal",
        "city": "New York, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 3,
        "mystery": "Lady Liberty's torch burns bright over New York Harbor. A French diplomat's journal\nreveals sculptor Bartholdi hid a time capsule in the pedestal during construction.\nThe capsule bears the name of the gift France gave to America.",
        "stages": [{
            "desc": "Inside the pedestal museum, you find the 1886 cornerstone. A copper plate shaped\nlike a flame bears an inscription asking what this monument represents.",
            "triggers": ["examine cornerstone", "read inscription", "search pedestal", "look at copper plate", "check museum", "examine flame plate", "read cornerstone"],
            "success": "The copper flame plate reads: 'I am the gift of one republic to another — a symbol\nrecognized across every ocean. My name is the promise of welcome to every weary\ntraveler. What am I called?'",
            "hint": "The cornerstone in the pedestal museum. Look for a flame-shaped copper plate."
        }],
        "final_answer": "LIBERTY",
        "answer_hint": "The name of the statue — the ideal she represents (7 letters).",
        "points": 5,
        "lore": "A gift from France in 1886, the Statue of Liberty was engineered by Gustave Eiffel and stands 305 feet tall."
    },
    {
        "id": "harvard_old_yard",
        "name": "Harvard Old Yard",
        "city": "Boston, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 4,
        "mystery": "Crimson leaves carpet Harvard Yard. The John Harvard statue — the 'Statue of Three\nLies' — sits at its center. A graduate donor's will mentions a hidden compartment\nin the statue's base containing a clue from the university's namesake himself.",
        "stages": [{
            "desc": "The John Harvard statue gleams with polished bronze. The inscription reads 'JOHN\nHARVARD, FOUNDER, 1638' — though students know none of those three facts are true.\nA loose bronze plate at the base catches your eye.",
            "triggers": ["examine statue", "check statue base", "examine john harvard", "look at bronze plate", "search base", "examine inscription", "touch loose plate", "inspect statue"],
            "success": "The bronze plate shifts. Behind it, a parchment asks: 'I am the man whose name this\nuniversity bears. Though I was not its founder, my library of 400 books began it all.'",
            "hint": "The John Harvard statue. The base has a loose bronze plate."
        }],
        "final_answer": "HARVARD",
        "answer_hint": "The clergyman whose name graces America's oldest university (7 letters).",
        "points": 5,
        "lore": "Founded in 1636, Harvard is America's oldest university. John Harvard donated his library and half his estate to the fledgling college."
    },
    {
        "id": "alamo_mission",
        "name": "Alamo Mission Chapel",
        "city": "San Antonio, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 5,
        "mystery": "The limestone walls of the Alamo still bear musket-fire scars from 1836. A classified\nTexas Ranger report describes a message carved into the back of the chapel altar by a\ndefender during the siege — a single word that became a revolution's battle cry.",
        "stages": [{
            "desc": "Inside the dim chapel, the altar stands worn and solemn. Behind it, the limestone wall\nbears faint scratches — letters carved in haste by a desperate hand.",
            "triggers": ["examine altar", "look behind altar", "read scratches", "check limestone wall", "search behind altar", "examine carving", "inspect wall", "study carving"],
            "success": "The crude carving reads: 'For Texas and for freedom. Shout the word that echoed\nthrough these walls on that final morning.'",
            "hint": "Behind the chapel altar. The defenders left messages on these walls."
        }],
        "final_answer": "REMEMBER",
        "answer_hint": "The battle cry of the Alamo — '_______ the Alamo!' (8 letters).",
        "points": 5,
        "lore": "The 1836 Battle of the Alamo saw 200 defenders hold out for 13 days against Santa Anna's army. 'Remember the Alamo!' became the rallying cry."
    },
    {
        "id": "golden_gate",
        "name": "Golden Gate Fort Point",
        "city": "San Francisco, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 6,
        "mystery": "Beneath the Golden Gate Bridge, Fort Point stands sentinel over churning waters. A\n1937 engineer's notebook describes a rivet in the south tower stamped with a coded\nmessage naming what the bridge spans.",
        "stages": [{
            "desc": "You descend into Fort Point beneath the south tower. A massive riveted steel beam\nrises overhead. One rivet is larger than the rest, stamped with letters.",
            "triggers": ["examine rivet", "look at beam", "read stamp", "inspect south tower", "check steel beam", "search fort point", "examine stamped rivet", "look at large rivet"],
            "success": "The rivet reads: 'I am the narrow passage this bridge crosses — the mile-wide\nentrance to the greatest bay on the Pacific. What am I called?'",
            "hint": "Beneath the south tower at Fort Point. Look for an unusual rivet in the steel."
        }],
        "final_answer": "STRAIT",
        "answer_hint": "The Golden Gate is this type of narrow water passage (6 letters).",
        "points": 5,
        "lore": "The Golden Gate Bridge (1937) spans the Golden Gate strait. At 4,200 feet it was the world's longest suspension bridge."
    },
    {
        "id": "space_needle",
        "name": "Space Needle Mechanics Deck",
        "city": "Seattle, USA",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 7,
        "mystery": "The Space Needle's saucer-top hovers 605 feet above Seattle. A maintenance logbook\nmentions an engraving on the main drive gear — a message from the 1962 World's Fair\nbuilders naming the era this tower was built to celebrate.",
        "stages": [{
            "desc": "The mechanical room hums. The massive drive gear is as tall as a person. Shining a\nlight on its inner face reveals etched text beneath decades of grease.",
            "triggers": ["examine gear", "look at drive gear", "read engraving", "clean gear", "search mechanical room", "inspect motor", "examine etching", "check inner face"],
            "success": "The etching reveals: 'Built for the World's Fair of 1962 — the fair that looked\nto tomorrow. We called it the _____ 21 Exposition. What era did we usher in?'",
            "hint": "The mechanical room. Check the giant drive gear that turns the restaurant."
        }],
        "final_answer": "CENTURY",
        "answer_hint": "The 1962 World's Fair was the '_______ 21 Exposition' (7 letters).",
        "points": 5,
        "lore": "The Space Needle was built for the 1962 Century 21 Exposition. It can withstand 200 mph winds and 9.1 magnitude earthquakes."
    },
    {
        "id": "cn_tower",
        "name": "CN Tower Sub-structure",
        "city": "Toronto, Canada",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 8,
        "mystery": "The CN Tower pierces the Toronto skyline. In the sub-basement, an engineer's blueprint\nshows a sealed capsule embedded in the foundation. The seal reads: 'Open with the one\nthing this tower lets you see through.'",
        "stages": [{
            "desc": "The sub-basement is cavernous. A metal access panel near the central pillar has a glass\nviewing port revealing a capsule inside.",
            "triggers": ["examine capsule", "look through glass", "open panel", "search foundation", "check access panel", "look at glass port", "examine pillar", "inspect base", "check viewing port"],
            "success": "The capsule reads: 'I rise 1,815 feet above this city. My most famous feature lets\nvisitors walk on air, looking down through what transparent material?'",
            "hint": "The sub-basement foundation. An access panel has a glass viewing port."
        }],
        "final_answer": "GLASS",
        "answer_hint": "The transparent material of the CN Tower's famous Glass Floor (5 letters).",
        "points": 5,
        "lore": "The CN Tower held the record for world's tallest freestanding structure for 34 years (1976-2010). Its Glass Floor can hold 14 hippos."
    },
    {
        "id": "chateau_frontenac",
        "name": "Chateau Frontenac Cellars",
        "city": "Quebec City, Canada",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 9,
        "mystery": "The castle-like Chateau Frontenac dominates Old Quebec. In its deepest cellar, behind\nracks of vintage wine, a 17th-century stone wall bears the mark of the explorer who\nfounded this city in 1608. His name is carved into the foundation itself.",
        "stages": [{
            "desc": "The cellar stairs descend into centuries of history. Behind wine racks, a section of\noriginal foundation wall bears a fleur-de-lis and a barely legible carved name.",
            "triggers": ["examine cellar", "look behind wine racks", "read carving", "move wine racks", "search stone wall", "examine foundation", "inspect fleur-de-lis", "check wall"],
            "success": "The carved stone reveals: 'Je me souviens. The founder of this city planted the French\nflag on this rock in 1608. My name is the beginning of Quebec's story. Who am I?'",
            "hint": "The deepest cellar, behind the wine racks. Old foundation stones hide the secret."
        }],
        "final_answer": "CHAMPLAIN",
        "answer_hint": "The French explorer who founded Quebec City in 1608 (9 letters).",
        "points": 5,
        "lore": "Samuel de Champlain founded Quebec City in 1608. The Chateau Frontenac (1893) is said to be the most photographed hotel in the world."
    },
    {
        "id": "banff_springs",
        "name": "Banff Springs Hotel Crypt",
        "city": "Alberta, Canada",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 10,
        "mystery": "The 'Castle in the Rockies' hides a sealed lower level. A bellhop's 1928 diary describes\na thermal spring bursting through the basement floor — the natural wonder that first\ndrew settlers to this valley and created Canada's first national park.",
        "stages": [{
            "desc": "The hotel's lowest level is warm and humid. A natural spring bubbles through the stone\nfloor into a basin. Around the rim, stones are arranged to spell a question.",
            "triggers": ["examine spring", "look at basin", "read stones", "search basement", "check thermal spring", "inspect stones", "look at pool", "examine water", "check arranged stones"],
            "success": "The arranged stones read: 'This valley was unknown until three railway workers stumbled\nupon me in 1883. My warm, mineral-rich waters gave birth to Canada's first national park.'",
            "hint": "The lowest basement level. Follow the steam to find the thermal waters."
        }],
        "final_answer": "HOTSPRING",
        "answer_hint": "The natural warm water source that put Banff on the map (9 letters).",
        "points": 5,
        "lore": "Banff National Park (est. 1885) is Canada's oldest national park. The hot springs were discovered by Canadian Pacific Railway workers in 1883."
    },
    {
        "id": "chichen_itza",
        "name": "Chichen Itza Serpent Pyramid",
        "city": "Yucatan, Mexico",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 11,
        "mystery": "El Castillo pyramid rises from the Yucatan jungle like a stone calendar. During the\nequinox, a serpent of shadow slithers down its steps. Mayan priests left a coded message\nin the inner chamber naming the feathered serpent god of this temple.",
        "stages": [{
            "desc": "You climb the steep steps to the summit temple. Inside, a chacmool statue reclines before\na jaguar throne. Carved into the ceiling are glyphs — a divine name.",
            "triggers": ["enter inner chamber", "examine jaguar throne", "read glyphs", "look at ceiling", "examine chacmool", "search temple", "study carving", "inspect chamber", "check ceiling"],
            "success": "The ceiling glyphs read: 'I am the Feathered Serpent, god of wind and wisdom. Maya and\nToltecs both worshipped me. My shadow crawls down these steps at every equinox.'",
            "hint": "Inside the pyramid's summit temple. Look up — the ceiling holds the answer."
        }],
        "final_answer": "KUKULKAN",
        "answer_hint": "The Mayan name for the Feathered Serpent god (8 letters).",
        "points": 5,
        "lore": "Chichen Itza was a major Mayan city (600-1200 AD). El Castillo has 365 steps matching the solar year. Kukulkan is the Mayan feathered serpent deity."
    },
    {
        "id": "teotihuacan",
        "name": "Teotihuacan Temple of the Sun",
        "city": "Mexico City, Mexico",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 12,
        "mystery": "The Pyramid of the Sun towers 216 feet above the Avenue of the Dead. A 2018 scan\nrevealed a sealed chamber beneath the pyramid containing an obsidian mirror etched\nwith the name of the plumed serpent deity who created humanity.",
        "stages": [{
            "desc": "You descend into the tunnel beneath the pyramid. The obsidian mirror sits on a stone\npedestal. Glyphs etched into the black glass spell out a divine name.",
            "triggers": ["examine mirror", "read mirror glyphs", "look at obsidian", "descend tunnel", "search chamber", "examine pedestal", "study obsidian", "inspect mirror", "check glyphs"],
            "success": "The mirror's glyphs read: 'I am the Plumed Serpent — creator and destroyer. The Aztecs\ncalled me by a name the Spanish could barely pronounce. I gave maize to humanity.'",
            "hint": "Beneath the Pyramid of the Sun. A tunnel leads to a chamber with a dark mirror."
        }],
        "final_answer": "QUETZALCOATL",
        "answer_hint": "The Aztec Plumed Serpent god — creator of humanity (12 letters).",
        "points": 5,
        "lore": "Teotihuacan (100 AD) was the largest city in pre-Columbian Americas with 125,000 people. The Pyramid of the Sun is Earth's third-largest pyramid."
    },
    {
        "id": "palenque",
        "name": "Palenque Mayan Ruins",
        "city": "Chiapas, Mexico",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 13,
        "mystery": "The Temple of the Inscriptions rises above the Lacandon jungle. A secret staircase leads\nto the tomb of a great Mayan king whose jade death mask became legendary. His name is\ncarved at the head of his sarcophagus.",
        "stages": [{
            "desc": "The tomb chamber is cold and narrow. The colossal carved sarcophagus lid depicts a man\ndescending into the underworld. At its head, Mayan glyphs spell the king's name.",
            "triggers": ["examine sarcophagus", "read glyphs on lid", "look at carving", "study lid", "search tomb", "examine head glyphs", "inspect sarcophagus", "check carving"],
            "success": "The sarcophagus glyphs name: 'I ruled Palenque for 68 years — the longest Mayan reign.\nMy tomb lay hidden for 1,200 years. My jade mask is the finest ever found.'",
            "hint": "Inside the Temple of Inscriptions. Descend to the hidden tomb chamber."
        }],
        "final_answer": "PAKAL",
        "answer_hint": "The great Mayan king buried at Palenque — K'inich Janaab' _____ (5 letters).",
        "points": 5,
        "lore": "Palenque flourished in the 7th century. King Pakal the Great ruled 615-683 AD. His tomb was discovered in 1952 by Alberto Ruz Lhuillier."
    },
    {
        "id": "tikal",
        "name": "Tikal Jungle Temples",
        "city": "Peten, Guatemala",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 14,
        "mystery": "Temple IV rises above the jungle canopy. Howler monkeys scream in the distance. A game\ncamera captured infrared images of glyphs glowing on Temple I's roof comb at night,\nnaming the sacred animal of Mayan kings.",
        "stages": [{
            "desc": "Temple I — the Temple of the Great Jaguar — towers before you. Under infrared light,\nits roof comb reveals hidden glyphs painted in a substance that glows only in darkness.",
            "triggers": ["climb temple", "examine roof comb", "use infrared light", "look at darkness", "search temple top", "inspect glyphs", "check roof", "study glowing glyphs", "examine temple one"],
            "success": "The glowing glyphs depict: 'I am the sacred beast of Mayan kings — lord of the jungle\nnight. My image adorns the thrones of Tikal's greatest rulers. This temple bears my name.'",
            "hint": "Temple I at night. The roof comb hides secrets visible only in darkness."
        }],
        "final_answer": "JAGUAR",
        "answer_hint": "Temple I at Tikal is the Temple of the Great _____ (6 letters).",
        "points": 5,
        "lore": "Tikal peaked around 700 AD with 90,000 inhabitants. Temple I (the Jaguar) was built around 732 AD and stands 154 feet tall."
    },
    {
        "id": "san_juan",
        "name": "San Juan Historic Citadels",
        "city": "San Juan, Puerto Rico",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 15,
        "mystery": "Castillo San Felipe del Morro guards San Juan Bay with 18-foot walls. A 1595 Spanish\nnaval logbook describes a hidden niche containing a silver medallion that bears the\nname of the fortress itself — El ______.",
        "stages": [{
            "desc": "The lowest bastion faces the Atlantic. Cannon ports gape at the sea. In the corner\nof the gun deck, a loose brick reveals a niche with a tarnished silver medallion.",
            "triggers": ["examine bastion", "search gun deck", "look at loose brick", "find niche", "check corner", "examine medallion", "read engraving", "inspect silver", "check brick"],
            "success": "The medallion reads: 'I am the great fortress guarding San Juan Bay. Drake failed\nto take me. My name — El _____ — means headland in Spanish.'",
            "hint": "The lowest bastion gun deck. A loose brick hides a silver secret."
        }],
        "final_answer": "MORRO",
        "answer_hint": "The fortress guarding San Juan Bay — El _____ (5 letters).",
        "points": 5,
        "lore": "El Morro, built starting 1539, withstood attacks by Sir Francis Drake (1595) and the Dutch (1625). Its walls are 18 feet thick in places."
    },
    {
        "id": "havana_castle",
        "name": "Havana Castillo de la Real Fuerza",
        "city": "Havana, Cuba",
        "region": "NORTH AMERICA & CARIBBEAN",
        "number": 16,
        "mystery": "Cuba's oldest stone fortress watches over Havana harbor. Atop its bell tower spins La\nGiraldilla — a bronze weathervane that is Havana's symbol. A captain's sea chest beneath\nthe tower contains a codebook tied to Spain's greatest naval fleet.",
        "stages": [{
            "desc": "The bell tower base holds Captain de Soto's sea chest. Inside, a codebook bears the seal\nof Spain's most powerful naval force — the fleet that ruled the seas for three centuries.",
            "triggers": ["examine bell tower", "look at weathervane", "search sea chest", "open chest", "check tower base", "examine codebook", "read seal", "inspect giraldilla", "check sea chest"],
            "success": "The codebook's seal reads: 'The Great Spanish _____ — the fleet that ruled these waters\nfor three centuries. In 1588, it sailed against England and changed history forever.'",
            "hint": "The bell tower base. Captain de Soto's sea chest and its codebook."
        }],
        "final_answer": "ARMADA",
        "answer_hint": "The Spanish naval fleet that ruled the seas — the Spanish _____ (6 letters).",
        "points": 5,
        "lore": "Castillo de la Real Fuerza (1577) is the oldest stone fortress in the Americas. The Spanish Armada's 1588 defeat marked the rise of English naval power."
    },
    {
        "id": "machu_picchu",
        "name": "Machu Picchu Intihuatana Stone",
        "city": "Cusco, Peru",
        "region": "SOUTH AMERICA",
        "number": 17,
        "mystery": "The Intihuatana stone sits at Machu Picchu's summit — a carved granite pillar the Inca\nused as an astronomical calendar. At solstice sunrise, glyphs emerge on its base naming\nthe sun god this 'hitching post of the sun' was dedicated to.",
        "stages": [{
            "desc": "The Intihuatana angles skyward. Dawn's first rays strike its face. Glyphs emerge from\nthe granite, revealing a divine name etched by Inca priests five centuries ago.",
            "triggers": ["examine intihuatana", "look at stone pillar", "watch sunrise", "read glyphs", "check stone base", "study carving", "examine hitching post", "inspect granite", "check sunlit glyphs"],
            "success": "The sunlit glyphs reveal: 'I am the sun — supreme god of the Inca. They built temples\nto me across an empire of 2,500 miles. My golden disc adorned the holiest shrine in Cusco.'",
            "hint": "The Intihuatana stone at sunrise. The sun reveals what shadows hide."
        }],
        "final_answer": "INTI",
        "answer_hint": "The Incan sun god — this stone was his 'hitching post' (4 letters).",
        "points": 5,
        "lore": "Machu Picchu was built around 1450 at the height of the Inca Empire. The Intihuatana stone is one of the few such stones the conquistadors never found and destroyed."
    },
    {
        "id": "nazca_lines",
        "name": "Nazca Lines Observation Tower",
        "city": "Nazca, Peru",
        "region": "SOUTH AMERICA",
        "number": 18,
        "mystery": "From the observation tower, the desert floor stretches in all directions, etched with\ncolossal figures visible only from above. A 1939 pilot's log describes seeing a creature\nwith a long curved beak that had a hidden marker at its throat.",
        "stages": [{
            "desc": "You climb the observation tower. Below, the desert reveals a famous geoglyph — a creature\nwith an impossibly long, needle-like beak stretching 300 feet across the pampa.",
            "triggers": ["examine geoglyph", "look at desert figure", "search beak", "climb tower", "check stone marker", "examine bird figure", "look through binoculars", "inspect pampa", "check throat"],
            "success": "The stone marker at the figure's throat reads: 'I hover above desert flowers, my needle\nbeak probing for nectar. The Nazca carved me 300 feet long into the earth.'",
            "hint": "The observation tower. Use binoculars to examine the geoglyphs closely."
        }],
        "final_answer": "HUMMINGBIRD",
        "answer_hint": "The long-beaked bird geoglyph — 300 feet across (11 letters).",
        "points": 5,
        "lore": "The Nazca Lines (500 BCE-500 CE) include 70+ animal and plant figures. The hummingbird geoglyph stretches 310 feet across the desert pampa."
    },
    {
        "id": "amazon_station",
        "name": "Amazon Rainforest Research Station",
        "city": "Amazonas, Brazil",
        "region": "SOUTH AMERICA",
        "number": 19,
        "mystery": "Deep in the Amazon, a research station stands on stilts above the flooded forest. An\nabandoned laptop contains a password-protected file. The hint: 'The word that describes\nwhat this forest has — more life than anywhere else on Earth.'",
        "stages": [{
            "desc": "The research station hums with solar-powered equipment. The abandoned laptop displays a\npassword prompt. A sticky note reads: 'Password = what makes this place so special.'",
            "triggers": ["examine laptop", "look at sticky note", "access computer", "check file", "search desk", "read password hint", "examine monitor", "open vault file", "check sticky note"],
            "success": "The sticky note reveals: 'The Amazon contains 10% of all known species — more than any\nother ecosystem on Earth. Scientists use one word to describe this variety of life.'",
            "hint": "The abandoned laptop. The password describes the Amazon's variety of life."
        }],
        "final_answer": "BIODIVERSITY",
        "answer_hint": "The scientific term for the variety of life in an ecosystem (12 letters).",
        "points": 5,
        "lore": "The Amazon Rainforest covers 2.1 million square miles and produces 20% of Earth's oxygen. It's home to 10% of all known species on the planet."
    },
    {
        "id": "christ_redeemer",
        "name": "Christ the Redeemer Base Vault",
        "city": "Rio de Janeiro, Brazil",
        "region": "SOUTH AMERICA",
        "number": 20,
        "mystery": "Christ the Redeemer's outstretched arms embrace Rio from 2,300 feet above the sea.\nInside the statue's base, a vault holds the 1931 dedication plaque naming the mountain\nthis monument crowns — the 'hunchback' peak visible from every corner of the city.",
        "stages": [{
            "desc": "Inside the statue's concrete pedestal, the original 1931 dedication plaque is bolted\nto the wall. The French inscription names the mountain that hosts this iconic monument.",
            "triggers": ["examine plaque", "read inscription", "search base", "look at brass plaque", "check chapel", "examine dedication", "read french", "inspect wall plaque"],
            "success": "The plaque's inscription reads: 'This monument to Christ the Redeemer stands atop the\npeak known as _____ — the Hunchback. This mountain inspired the statue itself.'",
            "hint": "Inside the statue's base. Read the original 1931 dedication plaque."
        }],
        "final_answer": "CORCOVADO",
        "answer_hint": "The mountain Christ the Redeemer crowns (9 letters).",
        "points": 5,
        "lore": "Christ the Redeemer (1931) is 98 feet tall with a 92-foot arm span. It stands on the 2,300-foot Corcovado (hunchback) mountain in Tijuca Forest."
    },
    {
        "id": "iguazu_falls",
        "name": "Iguazu Falls Hidden Cave",
        "city": "Argentina/Brazil",
        "region": "SOUTH AMERICA",
        "number": 21,
        "mystery": "The thundering cascade of Iguazu — 275 waterfalls stretching nearly two miles — drowns\nout all sound. Behind the largest curtain of water, a hidden cave used by Guarani shamans\nbears the name they gave this place: 'the waters that devour.'",
        "stages": [{
            "desc": "You navigate behind the Devil's Throat — Iguazu's largest cascade. Behind the roaring\nwater curtain, a cave opens in the basalt. The walls are painted with Guarani symbols.",
            "triggers": ["enter cave", "examine cave paintings", "read guarani symbols", "look at walls", "search behind waterfall", "check rock paintings", "study symbols", "inspect art", "examine paintings"],
            "success": "The Guarani paintings show a great serpent whose thrashing body created the falls. The\ntext reads: 'We call this place the _____ — the Throat of the Devil.'",
            "hint": "Behind the Devil's Throat waterfall. A hidden cave with Guarani art."
        }],
        "final_answer": "DEVILSTHROAT",
        "answer_hint": "The largest cataract at Iguazu — the _____'s Throat (12 letters, no apostrophe).",
        "points": 5,
        "lore": "Iguazu Falls spans 1.7 miles across Argentina-Brazil. The Devil's Throat (Garganta del Diablo) drops 269 feet and is the most powerful section of the falls."
    },
    {
        "id": "teatro_colon",
        "name": "Teatro Colon Underground Archives",
        "city": "Buenos Aires, Argentina",
        "region": "SOUTH AMERICA",
        "number": 22,
        "mystery": "Teatro Colon's horseshoe auditorium is famed for near-perfect acoustics. In the\nunderground archives, a locked cabinet from 1908 bears a riddle about the opening\nnight's opera — and the ghost said to haunt the theater's rafters to this day.",
        "stages": [{
            "desc": "The archives are a labyrinth of sheet music. A cabinet marked '1908 — OPENING SEASON'\nhas no key, just a riddle painted on its glass about a disfigured musical genius.",
            "triggers": ["examine cabinet", "read riddle on glass", "search archives", "look at program", "check locked cabinet", "examine 1908 label", "study glass riddle", "inspect riddle"],
            "success": "The glass riddle reads: 'I premiered here in 1908 — the story of a disfigured genius\nwho haunted a Paris opera house. What opera am I?'",
            "hint": "The underground archives. Find the locked 1908 opening season cabinet."
        }],
        "final_answer": "PHANTOM",
        "answer_hint": "The opera that haunts the theater — 'The _____ of the Opera' (7 letters).",
        "points": 5,
        "lore": "Teatro Colon (1908) is considered one of the top opera houses in the world for acoustics. The Phantom of the Opera premiered in Paris in 1910."
    },
    {
        "id": "torres_del_paine",
        "name": "Torres del Paine Outpost",
        "city": "Patagonia, Chile",
        "region": "SOUTH AMERICA",
        "number": 23,
        "mystery": "Three granite towers rise from the Patagonian steppe like broken teeth. A frozen\nmountaineer's journal describes a cache at the Central Tower's base containing the\nTehuelche word for the color that gives these peaks their name.",
        "stages": [{
            "desc": "You trek across glacial moraine to the Central Tower's base. A rusted box in the scree\nbears a faded label: 'The name of this place means: Towers of _____.'",
            "triggers": ["examine box", "look at rusted cache", "search scree", "read spanish label", "dig at tower base", "check cache", "examine label", "search base camp", "check rusted box"],
            "success": "The label asks: ''Paine' comes from the Tehuelche word for a specific color — the shade\nof these granite peaks at twilight. What color is it?'",
            "hint": "Base of the Central Tower. A rusted mountaineer's cache in the scree."
        }],
        "final_answer": "PAINE",
        "answer_hint": "The Tehuelche word for 'blue' that names these peaks (5 letters).",
        "points": 5,
        "lore": "Torres del Paine National Park covers 700 square miles of Patagonia. 'Paine' comes from the Tehuelche word for the blue color of the granite towers at twilight."
    },
    {
        "id": "easter_island",
        "name": "Easter Island Ahu Tongariki",
        "city": "Rapa Nui, Chile",
        "region": "SOUTH AMERICA",
        "number": 24,
        "mystery": "Fifteen stone giants stand at Ahu Tongariki, their eyeless faces watching the sunrise.\nA transcribed Rapa Nui oral tradition tells of a hidden petroglyph on the back of one\nstatue — the name of these stone figures themselves, carved for eternity.",
        "stages": [{
            "desc": "The fifteen statues are massive — some weigh 86 tons. You squeeze behind the largest\none. On its back, a petroglyph depicts a human figure being carved from volcanic rock.",
            "triggers": ["examine statue back", "look at largest moai", "check petroglyph", "search behind statue", "read carving", "examine behind moai", "inspect largest figure", "search stone back"],
            "success": "The petroglyph asks: 'We are the _____ — the living faces of our ancestors. We walked\nhere from Rano Raraku quarry, six miles distant. The world knows us by this name.'",
            "hint": "Behind the largest statue. Check the back for ancient carvings."
        }],
        "final_answer": "MOAI",
        "answer_hint": "The Rapa Nui name for Easter Island's monolithic statues (4 letters).",
        "points": 5,
        "lore": "Easter Island has 887 moai statues carved between 1250-1500 CE. The average moai stands 13 feet tall and weighs 14 tons. How they were transported is still debated."
    },
    {
        "id": "atacama",
        "name": "San Pedro de Atacama Observatory",
        "city": "Atacama, Chile",
        "region": "SOUTH AMERICA",
        "number": 25,
        "mystery": "The Atacama Desert has the clearest skies on Earth — 330 cloudless nights a year. At\nthe ALMA observatory, a technician's notes describe a signal from a distant star system.\nThe decoding key is the ancient Greek word for the ordered universe.",
        "stages": [{
            "desc": "The receiver room is bathed in red light. A technician's notebook lies open. The last\npage has a note: 'Key = the Greek word for the order we find in the heavens.'",
            "triggers": ["examine notebook", "read notes", "search receiver room", "look at data", "check technician notes", "study last page", "examine signal log", "read scribble", "check notebook"],
            "success": "The note reads: 'The ancient Greeks had a word for the ordered universe — the beautiful\narrangement of stars and planets above. Without it, there is only chaos.'",
            "hint": "The receiver room. Check the technician's notebook on the desk."
        }],
        "final_answer": "COSMOS",
        "answer_hint": "The Greek word for the ordered universe — opposite of chaos (6 letters).",
        "points": 5,
        "lore": "ALMA is the world's most powerful radio telescope at 16,000 feet elevation. The Atacama Desert's skies are the clearest and driest on Earth."
    },
    {
        "id": "salar_uyuni",
        "name": "Salar de Uyuni Salt Hotel Vault",
        "city": "Uyuni, Bolivia",
        "region": "SOUTH AMERICA",
        "number": 26,
        "mystery": "The world's largest salt flat — 4,086 square miles of white hexagons — becomes a giant\nmirror when it rains. Beneath the crust lies half the world's reserves of a metal so\nvaluable it's called 'white gold.' A miner's map marks a deposit with that very name.",
        "stages": [{
            "desc": "An old salt hotel — walls, tables, beds all made of salt. Behind the counter, a miner's\nmap marks a spot with an X and a single word: the element that makes the Salar priceless.",
            "triggers": ["examine map", "look behind counter", "check salt hotel", "read miner map", "search hotel desk", "examine marked spot", "study x mark", "inspect counter", "check map"],
            "success": "The miner's note reads: 'Beneath these ancient salt crusts lies the world's largest deposit\nof _____ — the lightest metal on Earth, essential for every phone battery on the planet.'",
            "hint": "The salt hotel counter. A miner's map marks the treasure's name."
        }],
        "final_answer": "LITHIUM",
        "answer_hint": "The 'white gold' metal beneath the salt — used in every battery (7 letters).",
        "points": 5,
        "lore": "Salar de Uyuni contains 10 billion tons of salt and an estimated 5.4 million tons of lithium — about 50-70% of the world's known lithium reserves."
    },
    {
        "id": "ciudad_perdida",
        "name": "Ciudad Perdida Lost City Ruins",
        "city": "Sierra Nevada, Colombia",
        "region": "SOUTH AMERICA",
        "number": 27,
        "mystery": "High in the Sierra Nevada jungle lies a city older than Machu Picchu with 169 stone\nterraces. Looters found golden figurines here in the 1970s. The name of the indigenous\npeople who built it is carved into the entrance terrace.",
        "stages": [{
            "desc": "Terrace 1 marks the entrance — 1,200 stone steps rise through the jungle. The first\nterrace stone is carved with the symbol of the civilization that built this lost city.",
            "triggers": ["climb steps", "examine terrace stone", "read carving", "look at terrace", "search first terrace", "check stone symbol", "examine step carving", "inspect entrance", "check terrace"],
            "success": "The Terrace 1 stone reads: 'We are the _____ — people of the Sierra Nevada. Our ancestors\nbuilt this city 1,200 years ago. Our descendants still live in these mountains today.'",
            "hint": "Terrace 1 at the city entrance. Read the carving on the first stone step."
        }],
        "final_answer": "TAIRONA",
        "answer_hint": "The indigenous people who built Ciudad Perdida (7 letters).",
        "points": 5,
        "lore": "Ciudad Perdida (Lost City) was built by the Tairona around 800 AD — 650 years before Machu Picchu. It was rediscovered by treasure looters in 1972."
    },
    {
        "id": "galapagos",
        "name": "Galapagos Tortoise Research Center",
        "city": "Santa Cruz, Ecuador",
        "region": "SOUTH AMERICA",
        "number": 28,
        "mystery": "Giant tortoises lumber through the research station. A biologist's field notebook in the\nincubation lab describes how studying these islands' finches led to a theory that changed\nthe world. The final page names the man whose ideas were born here in 1835.",
        "stages": [{
            "desc": "The incubation lab is warm and humid. Tiny tortoises scuttle in enclosures. A worn field\nnotebook filled with sketches of finch beaks sits on the counter.",
            "triggers": ["examine notebook", "read field notes", "look at sketches", "check lab counter", "search incubation lab", "study finch sketches", "examine last page", "read biologist notes"],
            "success": "The final page reads: 'September 1835. HMS Beagle. A young naturalist spent five weeks\nhere studying finches and tortoises. What he observed became the foundation of modern biology.'",
            "hint": "The incubation lab. Look for the biologist's notebook with finch sketches."
        }],
        "final_answer": "DARWIN",
        "answer_hint": "The naturalist whose Galapagos observations sparked evolutionary theory (6 letters).",
        "points": 5,
        "lore": "Charles Darwin visited the Galapagos in 1835 during the HMS Beagle voyage. His observations of finches and tortoises were pivotal to his theory of natural selection."
    },
    {
        "id": "tower_of_london",
        "name": "Tower of London Jewel House",
        "city": "London, UK",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 29,
        "mystery": "The White Tower has guarded the Crown Jewels for centuries. A Yeoman Warder's note\nmentions a loose stone in the Jewel House wall hiding a clue tied to the Tower's most\nfamous residents — the black birds whose departure would doom the kingdom.",
        "stages": [{
            "desc": "The Jewel House gleams. Near the Imperial State Crown display, a loose stone in the\ninner wall has a feather carved into its surface.",
            "triggers": ["examine loose stone", "check jewel house wall", "look at feather carving", "search near crown", "examine carving", "inspect wall", "check loose stone", "look behind display"],
            "success": "Behind the stone, a Tudor-era note reads: 'We guard this Tower as we guard the Crown.\nLegend says if we six ever leave, the kingdom itself will fall. What are we?'",
            "hint": "The Jewel House inner wall. Look for a loose stone with a feather carving."
        }],
        "final_answer": "RAVEN",
        "answer_hint": "The birds that must never leave the Tower — or the kingdom falls (5 letters).",
        "points": 5,
        "lore": "At least six ravens are kept at the Tower at all times. Legend says if they leave, both the Tower and the kingdom will fall."
    },
    {
        "id": "stonehenge",
        "name": "Stonehenge Inner Circle",
        "city": "Wiltshire, UK",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 30,
        "mystery": "The standing stones are silhouettes against Salisbury Plain. The altar stone at the\ncenter was brought from Wales — 150 miles away. A bronze plaque describes the celestial\nevent these 5,000-year-old stones were built to mark.",
        "stages": [{
            "desc": "You stand at the altar stone. The Heel Stone is visible through the trilithon arch. A\nbronze plaque embedded in the altar describes the turning point of the year.",
            "triggers": ["examine altar stone", "look at heel stone", "read bronze plaque", "check trilithon", "search altar", "examine plaque", "study alignment", "look through arch"],
            "success": "The plaque reads: 'Built to mark the _____ — when the sun stands still. The longest day\nand the shortest night. For 5,000 years, people have gathered here to witness it.'",
            "hint": "The altar stone at the center. A bronze plaque describes the celestial event."
        }],
        "final_answer": "SOLSTICE",
        "answer_hint": "The astronomical event Stonehenge was built to mark — summer _____ (8 letters).",
        "points": 5,
        "lore": "Stonehenge (3000-1500 BCE) aligns with the summer solstice sunrise. The massive sarsen stones weigh up to 25 tons each and were transported from Marlborough Downs."
    },
    {
        "id": "edinburgh_castle",
        "name": "Edinburgh Castle Vaults",
        "city": "Edinburgh, Scotland",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 31,
        "mystery": "Edinburgh Castle broods atop an extinct volcano. In a sealed vault beneath the Great\nHall, a Jacobite rebel's letter mentions a silver casket holding the name of the palace\nwhere Scotland's crown jewels were hidden for over a century.",
        "stages": [{
            "desc": "The vault is cold and dark. Among old weapon racks, a silver casket sits on a stone\nshelf. Its lid is engraved with a crown and thistle, and a question in Latin and Gaelic.",
            "triggers": ["examine silver casket", "open casket", "read engraving", "search vault", "check stone shelf", "examine lid", "inspect engraving", "look at crown thistle"],
            "success": "The casket reads: 'The Crown of Scotland lay hidden in _____ Palace — the royal residence\nat the bottom of the Royal Mile — for 111 years. Name this palace.'",
            "hint": "The sealed vault beneath the Great Hall. Find the silver casket."
        }],
        "final_answer": "HOLYROOD",
        "answer_hint": "The Edinburgh palace where Scotland's crown jewels lay hidden (8 letters).",
        "points": 5,
        "lore": "Edinburgh Castle sits atop a 350-million-year-old volcanic plug. Scotland's crown jewels were hidden at Holyrood Palace from 1707 to 1818."
    },
    {
        "id": "trinity_college",
        "name": "Trinity College Old Library",
        "city": "Dublin, Ireland",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 32,
        "mystery": "The Long Room stretches 213 feet beneath a barrel-vaulted ceiling, holding 200,000\nancient books. A locked display case holds Ireland's greatest national treasure — an\nilluminated manuscript that draws 500,000 visitors a year.",
        "stages": [{
            "desc": "The Long Room smells of aged vellum and oak. A display case glows softly, showcasing a\nmanuscript of breathtaking intricacy. A brass plate on the case names this priceless book.",
            "triggers": ["examine display case", "look at manuscript", "read brass plate", "search long room", "check illuminated book", "examine case", "study manuscript", "inspect plate"],
            "success": "The brass plate reads: 'Created by Irish monks around 800 AD, I contain the four Gospels\nin Latin. My intricate knotwork is the pinnacle of Insular art. What book am I?'",
            "hint": "The display case in the Long Room. Read the brass nameplate."
        }],
        "final_answer": "BOOKOFKELLS",
        "answer_hint": "Ireland's greatest illuminated manuscript — the _____ of _____ (11 letters, no spaces).",
        "points": 5,
        "lore": "Trinity College's Long Room holds 200,000 books. The Book of Kells (c. 800 AD) is Ireland's finest national treasure and a masterpiece of medieval illumination."
    },
    {
        "id": "catacombs_paris",
        "name": "Catacombs of Paris",
        "city": "Paris, France",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 33,
        "mystery": "Beneath Paris streets, the Catacombs hold the bones of six million Parisians arranged\nin macabre walls. A spelunker's map marks a skull in the deepest chamber carved with\nthe name of what these tunnels are called — the Empire of the Dead.",
        "stages": [{
            "desc": "The Empire of Death stretches into darkness. In the deepest ossuary, a skull sits on\na stone pedestal. Letters are carved into its frontal bone in French.",
            "triggers": ["examine skull", "read carving on forehead", "check pedestal", "look at marked skull", "search deepest chamber", "examine carved skull", "inspect bone", "study forehead"],
            "success": "The skull's carving reads: 'L'Empire de la Mort — the _____ of Death. Six million souls\nrest in these tunnels beneath the City of Light.'",
            "hint": "The deepest ossuary chamber. A skull on a pedestal is marked in French."
        }],
        "final_answer": "EMPIRE",
        "answer_hint": "The Catacombs are known as l'Empire de la Mort — the '_____ of Death' (6 letters).",
        "points": 5,
        "lore": "The Catacombs of Paris hold the bones of 6 million people, moved from overflowing cemeteries between 1786-1860. There are over 200 miles of tunnels beneath Paris."
    },
    {
        "id": "versailles",
        "name": "Palace of Versailles Hall of Mirrors",
        "city": "Versailles, France",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 34,
        "mystery": "The Hall of Mirrors stretches 240 feet — 357 mirrors reflecting 17 arched windows. Here,\nthe Treaty of Versailles ended World War I. A courtier's diary describes a hidden panel\nbehind one mirror frame naming the king who built this palace as a monument to himself.",
        "stages": [{
            "desc": "The Hall of Mirrors is dazzling. Behind a mirror near the central window arch, a gilded\npanel bears the emblem of the monarch who called himself the center of Europe.",
            "triggers": ["examine mirror frame", "look behind mirror", "check recessed panel", "search hall", "examine gilded panel", "check behind mirror frame", "inspect emblem", "look at sun king symbol"],
            "success": "The hidden panel bears a golden sun emblem: 'I am the King who built this palace from a\nhunting lodge. I called myself the ____ King. What did they call me?'",
            "hint": "Behind a mirror frame in the Hall of Mirrors. Look for a panel with a sun emblem."
        }],
        "final_answer": "SUN",
        "answer_hint": "Louis XIV was known as the _____ King (3 letters).",
        "points": 5,
        "lore": "The Hall of Mirrors took 6 years to build. Louis XIV (the Sun King) moved the French court to Versailles in 1682, transforming a hunting lodge into Europe's grandest palace."
    },
    {
        "id": "mont_saint_michel",
        "name": "Mont Saint-Michel Abbey",
        "city": "Normandy, France",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 35,
        "mystery": "Mont Saint-Michel rises from tidal flats like a Gothic mirage — an abbey on a rocky\nisland cut off from land twice daily by Europe's fastest tides. The abbey's dedication\nplaque names the archangel who commanded it be built here in 708 AD.",
        "stages": [{
            "desc": "The abbey church crowns the mount. The dedication plaque depicts a winged figure\nbrandishing a sword and scales — the warrior archangel who battles a dragon.",
            "triggers": ["examine dedication plaque", "look at archangel image", "read altar plaque", "search abbey", "check church altar", "examine winged figure", "inspect plaque", "study archangel"],
            "success": "The plaque reads: 'I am the warrior _____ — the celestial being who appeared to Bishop\nAubert in 708 AD and commanded this sanctuary be built on this rock.'",
            "hint": "The abbey church altar. The dedication plaque shows an archangel."
        }],
        "final_answer": "ARCHANGEL",
        "answer_hint": "The celestial being who inspired Mont Saint-Michel — a warrior of heaven (9 letters).",
        "points": 5,
        "lore": "Mont Saint-Michel was built after Bishop Aubert reported visions of the Archangel Michael. The tides here rise 46 feet — among the fastest in Europe."
    },
    {
        "id": "atomium",
        "name": "Atomium Top Sphere",
        "city": "Brussels, Belgium",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 36,
        "mystery": "The Atomium's nine steel spheres connected by tubes represent an iron crystal magnified\n165 billion times — built for the 1958 World's Fair. In the top sphere, a physicist's\nnotebook describes the structure of matter itself.",
        "stages": [{
            "desc": "The top sphere offers panoramic views of Brussels. A 1958 exhibit panel glows, showing\nthe regular geometric arrangement of particles that gives a solid its shape and strength.",
            "triggers": ["examine exhibit panel", "look at crystal diagram", "read physicist notes", "search top sphere", "check 1958 panel", "study crystal structure", "inspect diagram"],
            "success": "The exhibit panel reads: 'We are the repeating arrangement of atoms that gives matter its\nstructure. Salt forms cubes; snowflakes form hexagons. In every solid, atoms lock into\na _____ lattice. What is this ordered structure called?'",
            "hint": "The top sphere exhibition. Look for the 1958 physics display panel."
        }],
        "final_answer": "CRYSTAL",
        "answer_hint": "The ordered repeating structure of atoms in a solid (7 letters).",
        "points": 5,
        "lore": "The Atomium was built for Expo 58 in Brussels. Its nine spheres form an iron crystal lattice magnified 165 billion times. Each sphere is 59 feet in diameter."
    },
    {
        "id": "rijksmuseum",
        "name": "Rijksmuseum Secret Annex",
        "city": "Amsterdam, Netherlands",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 37,
        "mystery": "The Rijksmuseum houses Rembrandt's colossal masterpiece — a militia company portrait\nthat seems to move with life and shadow. During WWII, a secret annex in the foundations\nhid this and thousands of other artworks from the Nazis.",
        "stages": [{
            "desc": "The secret basement annex is bare now, but a painted label on the concrete marks where\nthe most famous painting was stored. It names Rembrandt's greatest group portrait.",
            "triggers": ["examine label", "read painted text", "search annex", "look at storage marking", "check basement", "examine painted label", "inspect concrete mark", "study storage label"],
            "success": "The label reads: 'Here rested Rembrandt van Rijn's greatest work — a group portrait so\nvivid the figures seem to step from the canvas. Unlike other portraits of its era,\nthese militiamen are frozen in motion. What is this masterpiece called?'",
            "hint": "The secret basement annex. A painted label marks where the masterpiece was hidden."
        }],
        "final_answer": "NIGHTWATCH",
        "answer_hint": "Rembrandt's most famous group portrait — 'The _____ _____' (10 letters, no space).",
        "points": 5,
        "lore": "The Rijksmuseum houses 8,000 artworks. Rembrandt's 'The Night Watch' (1642) is its most famous — a colossal 11.9 x 14.3 feet and featuring a revolutionary use of light and shadow."
    },
    {
        "id": "cologne_cathedral",
        "name": "Cologne Cathedral Crypt",
        "city": "Cologne, Germany",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 38,
        "mystery": "Cologne Cathedral's twin spires took 632 years to complete. In the crypt beneath the\nhigh altar rests the Shrine of the Three Kings — a golden reliquary said to contain\nthe bones of the visitors who followed a star to Bethlehem.",
        "stages": [{
            "desc": "The crypt is shadowed and incense-heavy. The golden Shrine of the Three Kings gleams —\nthe largest reliquary in Europe. An inscription on its base names these famous visitors.",
            "triggers": ["examine shrine", "look at golden reliquary", "read inscription", "search crypt", "check shrine base", "examine three kings", "inspect reliquary", "study golden shrine"],
            "success": "The shrine's inscription reads: 'We came from the East, following a star. We brought\ngold, frankincense, and myrrh. The Bible calls us the Three _____.'",
            "hint": "The crypt beneath the high altar. The Shrine of the Three Kings glows gold."
        }],
        "final_answer": "MAGI",
        "answer_hint": "The Three Wise Men who visited baby Jesus — the Three _____ (4 letters).",
        "points": 5,
        "lore": "Cologne Cathedral took 632 years to build (1248-1880). The Shrine of the Three Kings is the largest reliquary in the Western world, attracting pilgrims for 800 years."
    },
    {
        "id": "neuschwanstein",
        "name": "Neuschwanstein Castle Throne Room",
        "city": "Bavaria, Germany",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 39,
        "mystery": "Neuschwanstein — the fairy-tale castle that inspired Disney — was built by King Ludwig\nII as a temple to Richard Wagner's operas. The Throne Room's mosaic floor depicts the\nknight of the Holy Grail, the hero of Wagner's final opera.",
        "stages": [{
            "desc": "The Throne Room shimmers with gold leaf and mosaics. The floor depicts a knight kneeling\nbefore the Holy Grail. An inscription circles the mosaic, naming Wagner's swan knight.",
            "triggers": ["examine mosaic floor", "look at grail knight", "read floor inscription", "search throne room", "check mosaic", "examine knight figure", "inspect inscription", "study floor"],
            "success": "The inscription reads: 'Richard Wagner's final opera tells of _____ — the pure knight\ndestined to find the Holy Grail. Mad King Ludwig dedicated this castle to Wagner.\nName this Swan Knight.'",
            "hint": "The Throne Room mosaic floor. It depicts Wagner's Grail-seeking knight."
        }],
        "final_answer": "LOHENGRIN",
        "answer_hint": "The Swan Knight of Wagner's opera — the pure Grail seeker (9 letters).",
        "points": 5,
        "lore": "Neuschwanstein was built 1869-1886 by 'Mad' King Ludwig II of Bavaria. The castle inspired Disney's Sleeping Beauty Castle and appears in countless films."
    },
    {
        "id": "brandenburg_gate",
        "name": "Brandenburg Gate Secret Vault",
        "city": "Berlin, Germany",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 40,
        "mystery": "The Brandenburg Gate's twelve Doric columns have witnessed Prussian triumphs, Nazi\nparades, and the fall of the Berlin Wall. Atop the gate, a chariot pulled by four\nhorses carries Victory herself. A secret compartment names this iconic sculpture.",
        "stages": [{
            "desc": "In the gate's attic, a dusty compartment opens beneath the chariot statue. A copper\nplaque names the four-horse chariot that has crowned this monument since 1793.",
            "triggers": ["examine attic compartment", "look beneath quadriga", "read copper plaque", "search gate attic", "check statue base", "examine chariot", "inspect plaque", "study quadriga"],
            "success": "The copper plaque reads: 'I crown this gate — a chariot of Victory pulled by four horses\nabreast. Greeks and Romans alike used my image to celebrate triumph.'",
            "hint": "The gate's attic passage. A compartment beneath the chariot statue."
        }],
        "final_answer": "QUADRIGA",
        "answer_hint": "The four-horse chariot that crowns the Brandenburg Gate (8 letters).",
        "points": 5,
        "lore": "The Brandenburg Gate (1791) is Berlin's most famous landmark. The Quadriga atop was briefly stolen by Napoleon in 1806 and taken to Paris as war booty."
    },
    {
        "id": "matterhorn",
        "name": "Matterhorn Alpine Ridge Lodge",
        "city": "Zermatt, Switzerland",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 41,
        "mystery": "The Matterhorn's jagged pyramid — 14,692 feet of rock and ice — straddles the Swiss-\nItalian border. In a high alpine hut, a climber's logbook mentions a name carved into\na wooden beam: the shape of the mountain, immortalized in a triangular Swiss chocolate.",
        "stages": [{
            "desc": "The ridge lodge is sparse — wooden benches and a climbing register. The main support beam\nhas a carving: a triangular shape, followed by a question in German and French.",
            "triggers": ["examine wooden beam", "read beam carving", "check climbing lodge", "search alpine hut", "look at carved beam", "examine triangle carving", "inspect register"],
            "success": "The carving reads: 'I share my shape with Switzerland's most famous export — the triangular\nchocolate bar from Bern. Millions taste my peak every day.'",
            "hint": "The alpine ridge lodge. Check the main support beam for carvings."
        }],
        "final_answer": "TOBLERONE",
        "answer_hint": "The triangular Swiss chocolate inspired by the Matterhorn's shape (9 letters).",
        "points": 5,
        "lore": "The Matterhorn (14,692 ft) was first climbed in 1865, ending tragically. Toblerone chocolate's distinctive triangular shape is based on the Matterhorn's silhouette."
    },
    {
        "id": "cern",
        "name": "CERN Large Hadron Collider Access Tunnel",
        "city": "Geneva, Switzerland",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 42,
        "mystery": "One hundred meters beneath the Franco-Swiss border, the LHC's 17-mile ring smashes\nparticles at nearly light speed. In an access tunnel, a physicist's whiteboard shows\nthe particle the LHC was built to find — the one that gives everything mass.",
        "stages": [{
            "desc": "The access tunnel is cold and lined with superconducting magnets. A whiteboard on the\nwall shows Feynman diagrams and a circled particle name — discovered here in 2012.",
            "triggers": ["examine whiteboard", "look at equation", "read circled name", "search access tunnel", "check physicist notes", "study feynman diagram", "inspect whiteboard", "check particle name"],
            "success": "The whiteboard reads: 'We built the LHC to find me — the particle that gives all other\nparticles their mass. Without me, the universe would be a soup of massless particles.\nIn 2012, we found me at last.'",
            "hint": "The LHC access tunnel. Read the physicist's whiteboard."
        }],
        "final_answer": "HIGGS",
        "answer_hint": "The particle that gives mass to everything — the 'God particle' (5 letters).",
        "points": 5,
        "lore": "CERN's Large Hadron Collider is the world's largest machine at 17 miles circumference. The Higgs boson discovery in 2012 confirmed the last missing piece of the Standard Model."
    },
    {
        "id": "viking_ship",
        "name": "Viking Ship Museum",
        "city": "Oslo, Norway",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 43,
        "mystery": "Three Viking burial ships — over 1,100 years old — rest in this Oslo museum. The finest,\na 9th-century oak longship, was discovered in a burial mound in 1904. Its name — carved\ninto the keel — identifies the Norwegian farm where it was unearthed.",
        "stages": [{
            "desc": "The massive oak longship dominates the hall. Its sweeping lines and 15 oar ports on each\nside speak of open-ocean voyages. A label near the keel names the ship after a farm.",
            "triggers": ["examine keel", "look at ship name", "read museum label", "search longship", "check oak vessel", "examine burial ship", "inspect keel carving", "study label"],
            "success": "The label reads: 'I am the finest Viking ship ever found — a 9th-century burial vessel\nunearthed from the _____ farm mound in 1904.'",
            "hint": "The largest longship's keel. Read the museum label near the hull."
        }],
        "final_answer": "OSEBERG",
        "answer_hint": "The Norwegian farm where the most famous Viking ship was discovered (7 letters).",
        "points": 5,
        "lore": "The Oseberg ship (c. 820 AD) is the finest preserved Viking longship. It was found in a burial mound on the Oseberg farm near Tonsberg, Norway, along with two female skeletons."
    },
    {
        "id": "svalbard_vault",
        "name": "Svalbard Global Seed Vault",
        "city": "Spitsbergen, Norway",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 44,
        "mystery": "Buried deep in an Arctic mountain, the Seed Vault stores over a million seed samples\nfrom every country on Earth — humanity's backup food supply. The vault's nickname is\ncarved into the concrete entrance: a two-word phrase describing its apocalyptic purpose.",
        "stages": [{
            "desc": "The concrete entrance juts from frozen mountainside. LEDs and mirrored panels create an\neerie glow. Above blast-proof doors, a sign bears the vault's unofficial name.",
            "triggers": ["examine vault entrance", "read entrance sign", "look at concrete", "search entrance", "check blast doors", "examine sign", "inspect vault", "study entrance"],
            "success": "The sign reads: 'We hold seeds from every nation — rice from Asia, wheat from Europe,\nmaize from the Americas. Should catastrophe strike, we are the backup. The press calls\nus the _____ Vault.'",
            "hint": "The concrete entrance. Read the sign above the blast-proof doors."
        }],
        "final_answer": "DOOMSDAY",
        "answer_hint": "The Seed Vault's nickname — the '_______ Vault' (8 letters).",
        "points": 5,
        "lore": "The Svalbard Global Seed Vault opened in 2008, buried 390 feet into a mountain. It stores over 1 million seed samples as a global food insurance policy against catastrophe."
    },
    {
        "id": "icehotel",
        "name": "Icehotel Frozen Archives",
        "city": "Jukkasjarvi, Sweden",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 45,
        "mystery": "The Icehotel is rebuilt every winter from blocks of ice harvested from the Torne River.\nIn a frozen archive room — walls of solid ice — a sculpted panel describes the celestial\nphenomenon that paints the Arctic sky with ribbons of green and purple light.",
        "stages": [{
            "desc": "The frozen archive glows with ethereal blue light. An ice panel carved by a master\nsculptor depicts swirling curtains of light in the night sky.",
            "triggers": ["examine ice panel", "look at frozen carving", "read sculpted panel", "search archive", "check ice sculpture", "examine light depiction", "inspect carving", "study frozen art"],
            "success": "The ice carving reads: 'When solar wind meets Earth's magnetic field, the polar sky dances\nwith light — green, purple, red, and blue curtains that shimmer and swirl. The Romans\nnamed me for the goddess of dawn.'",
            "hint": "The frozen archive room. Examine the sculpted ice panel depicting sky lights."
        }],
        "final_answer": "AURORA",
        "answer_hint": "The Northern Lights — the _____ Borealis (6 letters).",
        "points": 5,
        "lore": "The Icehotel is rebuilt each year using 1,000 tons of ice from the Torne River. It melts each spring. Aurora borealis is named for Aurora, Roman goddess of dawn."
    },
    {
        "id": "tivoli_gardens",
        "name": "Tivoli Gardens Clock Tower",
        "city": "Copenhagen, Denmark",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 46,
        "mystery": "Tivoli Gardens — Walt Disney's inspiration for Disneyland — has enchanted Copenhagen\nsince 1843. The clock tower at the main entrance hides a wooden box left by the founder.\nInside, a scroll names the Roman building that inspired Tivoli's original name.",
        "stages": [{
            "desc": "The clock tower chimes every quarter hour. Behind the clock face, a maintenance nook\nholds a dusty wooden box bearing the initials 'G.C.' — Georg Carstensen, Tivoli's creator.",
            "triggers": ["examine clock tower", "look behind clock face", "open wooden box", "search nook", "check maintenance space", "examine box", "read scroll", "inspect tower"],
            "success": "The scroll reads: 'I named this garden after a famous Roman temple district. The _____ in\nRome was a circular temple where all gods were honored.'",
            "hint": "The clock tower at the main entrance. Behind the clock face is a hidden box."
        }],
        "final_answer": "PANTHEON",
        "answer_hint": "The Roman temple whose name inspired Tivoli — the _____ (8 letters).",
        "points": 5,
        "lore": "Tivoli Gardens opened in 1843 and inspired Walt Disney to create Disneyland. It was named after the Jardin de Tivoli in Paris, itself named for the Roman Pantheon area."
    },
    {
        "id": "reykjavik_grid",
        "name": "Reykjavik Geothermal Power Grid",
        "city": "Reykjavik, Iceland",
        "region": "WESTERN & NORTHERN EUROPE",
        "number": 47,
        "mystery": "Iceland runs on volcanoes — 85% of its energy comes from the Earth's internal heat. At\nthe Hellisheidi Power Station, the world's largest geothermal plant, a monitoring station\ndisplays the one word that describes Iceland's entire energy philosophy.",
        "stages": [{
            "desc": "The control room glows with screens showing steam flow, turbine speeds, and output. A\nlarge sign above the main display summarizes Iceland's energy source in a single word.",
            "triggers": ["examine control room", "read display sign", "look at screens", "search station", "check main display", "examine sign", "inspect monitors", "study output"],
            "success": "The sign reads: 'Fire and ice — volcanoes and glaciers — give us power. The Earth's\ninternal heat provides 85% of all our energy. We harness what lies beneath our feet.'",
            "hint": "The control room. Read the sign above the main display."
        }],
        "final_answer": "GEOTHERMAL",
        "answer_hint": "Energy from the Earth's internal heat — what powers Iceland (10 letters).",
        "points": 5,
        "lore": "Iceland generates 85% of its energy from geothermal sources. Hellisheidi is the world's largest geothermal power station, harnessing volcanic heat."
    },
    {
        "id": "colosseum",
        "name": "Colosseum Underground Chambers",
        "city": "Rome, Italy",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 48,
        "mystery": "The hypogeum — the Colosseum's underground labyrinth — held gladiators and beasts before\nthey rose into the arena above. A gladiator's last message was carved into these stone\nwalls, naming the Emperor who began construction of this 'house of blood and sand.'",
        "stages": [{
            "desc": "The tunnels are damp and echoing. A carved message in rough Latin bears a gladiator's\nmark — a trident and shield. The text names the Emperor who raised these walls.",
            "triggers": ["enter hypogeum", "examine carving", "read latin", "search underground", "look at wall carving", "check tunnel walls", "examine gladiator mark", "study message"],
            "success": "The carving reads: 'The Emperor who raised these walls from the earth — his name opens\nthe gate. Seek the builder, not the inaugurator. Who began this Colosseum?'",
            "hint": "The underground hypogeum. Look for a gladiator's carved message on the tunnel walls."
        }],
        "final_answer": "VESPASIAN",
        "answer_hint": "The Roman Emperor who began construction of the Colosseum (9 letters).",
        "points": 5,
        "lore": "The Colosseum was inaugurated by Titus in 80 AD, but construction began under his father Vespasian. It held 50,000-80,000 spectators for gladiatorial contests and spectacles."
    },
    {
        "id": "vatican_archives",
        "name": "Vatican Secret Archives",
        "city": "Vatican City",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 49,
        "mystery": "The Vatican Secret Archives contain 53 miles of shelving — papal correspondence, papal\nbulls, and documents dating to the 8th century. A curator's codex mentions a hidden\nvault labeled with the name of the artist who painted the Sistine Chapel ceiling.",
        "stages": [{
            "desc": "Deep in the archives, a vault door bears no handle — only a keyhole and a single word\ncarved into the marble: the name of the Renaissance master who served Pope Julius II.",
            "triggers": ["examine vault door", "read marble carving", "search archives", "check hidden vault", "look at keyhole", "examine carving", "inspect marble", "study codex"],
            "success": "The marble reads: 'I painted the ceiling of the Sistine Chapel and sculpted the Pieta.\nPopes called me Il Divino — the Divine One. Who am I?'",
            "hint": "Deep in the archives. A vault door has a single name carved into marble."
        }],
        "final_answer": "MICHELANGELO",
        "answer_hint": "The Renaissance master who painted the Sistine Chapel ceiling (12 letters).",
        "points": 5,
        "lore": "The Vatican Secret Archives contain documents spanning 12 centuries. Michelangelo spent 4 years painting the Sistine Chapel ceiling (1508-1512) on scaffolding 60 feet above the floor."
    },
    {
        "id": "pisa_tower",
        "name": "Leaning Tower of Pisa Bell Chamber",
        "city": "Pisa, Italy",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 50,
        "mystery": "The Leaning Tower tilts at 3.97 degrees — a 12th-century engineering mistake that became\na world treasure. In the bell chamber at the top, a stonemason's mark hides the name of\nthe scientist who, legend says, dropped cannonballs from this very tower.",
        "stages": [{
            "desc": "The bell chamber houses seven bells, one for each musical note. A stonemason's chisel\nmark on the inner wall forms letters — a name famous in the history of science.",
            "triggers": ["examine bell chamber", "look at stonemason mark", "read chiseled name", "check inner wall", "search tower top", "examine chisel mark", "inspect bells", "study carving"],
            "success": "The chiseled name reads: 'I dropped two spheres of different masses from this tower to\nprove they fall at the same rate. My experiments changed physics forever.'",
            "hint": "The bell chamber at the top. Look for a stonemason's mark on the inner wall."
        }],
        "final_answer": "GALILEO",
        "answer_hint": "The scientist who legend says dropped cannonballs from the Leaning Tower (7 letters).",
        "points": 5,
        "lore": "Construction of the Leaning Tower began in 1173 and took 199 years. Galileo Galilei was born in Pisa in 1564, and legend holds he tested gravity from the famous tower."
    },
    {
        "id": "doges_palace",
        "name": "Venice Doge's Palace Dungeons",
        "city": "Venice, Italy",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 51,
        "mystery": "The Doge's Palace dungeons — the Piombi and Pozzi — held Venice's most notorious prisoners.\nA scratched message on a cell wall names the most famous escapee, who fled across the\nrooftops of Venice in 1756.",
        "stages": [{
            "desc": "The cell is damp and dark. On the stone wall, a prisoner scratched a name with a piece of\nbroken tile: the adventurer who made the most daring escape in Venice's history.",
            "triggers": ["examine cell wall", "read scratched name", "search dungeon", "check prison cell", "look at scratch marks", "examine prisoner message", "inspect dark cell"],
            "success": "The scratched message reads: 'I escaped these cells on November 1, 1756 — across the\nroof of the Doge's Palace, the only man ever to do so. Who am I?'",
            "hint": "The dungeon cells. A scratched name on the wall identifies the famous escapee."
        }],
        "final_answer": "CASANOVA",
        "answer_hint": "The Venetian adventurer who famously escaped the Doge's Palace prison (8 letters).",
        "points": 5,
        "lore": "Giacomo Casanova (1725-1798) was imprisoned in the Doge's Palace in 1755 for 'affront to religion and common decency.' His 1756 escape across the rooftop made him a legend."
    },
    {
        "id": "parthenon",
        "name": "Parthenon Acropolis Ruins",
        "city": "Athens, Greece",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 52,
        "mystery": "The Parthenon has crowned the Acropolis for 2,500 years — a temple to the goddess of\nwisdom. Among the fallen marble columns, a fragment of the original dedicatory frieze\nnames the goddess to whom this temple was consecrated.",
        "stages": [{
            "desc": "Among the scattered marble fragments, a piece of the original frieze shows a goddess\nspringing fully armed from the head of her father. The inscription names her.",
            "triggers": ["examine marble fragment", "read frieze inscription", "search acropolis", "check fallen columns", "look at dedicatory frieze", "examine goddess image", "inspect inscription"],
            "success": "The fragment reads: 'I sprang fully armed from the head of Zeus. I am the goddess of\nwisdom, war, and strategy. This city bears my name.'",
            "hint": "Among the ruins. A marble fragment of the original dedicatory frieze."
        }],
        "final_answer": "ATHENA",
        "answer_hint": "The Greek goddess of wisdom to whom the Parthenon was dedicated (6 letters).",
        "points": 5,
        "lore": "The Parthenon was built 447-432 BCE as a temple to Athena Parthenos (Athena the Virgin). It is considered the pinnacle of Doric architecture and a symbol of ancient Greece."
    },
    {
        "id": "santorini",
        "name": "Santorini Caldera Submerged Lab",
        "city": "Santorini, Greece",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 53,
        "mystery": "The volcanic caldera of Santorini — all that remains of a catastrophic eruption in 1600\nBCE. Some archaeologists believe this was the inspiration for the lost city of Atlantis.\nA submerged research station monitors the still-active volcano beneath the waves.",
        "stages": [{
            "desc": "A submerged glass dome on the caldera floor houses monitoring equipment. An underwater\nplaque names the legendary lost continent that many believe was inspired by this island.",
            "triggers": ["examine submerged dome", "look at underwater plaque", "read plaque name", "search caldera", "dive to station", "examine glass dome", "inspect monitoring station"],
            "success": "The plaque reads: 'Plato wrote of a great island civilization that sank beneath the waves\nin a single day and night. Many believe Santorini's eruption was the source of this myth.'",
            "hint": "The submerged research station. An underwater plaque names the legendary lost land."
        }],
        "final_answer": "ATLANTIS",
        "answer_hint": "The legendary lost continent said to have been inspired by Santorini (8 letters).",
        "points": 5,
        "lore": "Santorini (Thera) erupted around 1600 BCE in one of history's largest volcanic events. The Minoan civilization on nearby Crete may have been devastated by the resulting tsunami."
    },
    {
        "id": "alhambra",
        "name": "Alhambra Palace Gardens",
        "city": "Granada, Spain",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 54,
        "mystery": "The Alhambra — the 'Red Fortress' — is the pinnacle of Moorish architecture in Europe.\nIn the Court of the Lions, a hidden inscription in the fountain's basin names the palace\nitself, written in flowing Arabic calligraphy.",
        "stages": [{
            "desc": "The Court of the Lions is serene — 12 marble lions support a central fountain. A hidden\ninscription in the basin's interior is visible only when the water is still.",
            "triggers": ["examine fountain", "look at lion fountain", "read hidden inscription", "search court of lions", "check basin interior", "examine arabic calligraphy", "inspect marble lions"],
            "success": "The Arabic inscription reads: 'I am _____ — the Red One. The Nasrid dynasty built me as\ntheir palace-fortress, a paradise on Earth.'",
            "hint": "The Court of the Lions. A hidden Arabic inscription in the fountain basin."
        }],
        "final_answer": "ALHAMBRA",
        "answer_hint": "The Moorish palace whose name means 'The Red One' in Arabic (8 letters).",
        "points": 5,
        "lore": "The Alhambra was built by the Nasrid dynasty in the 13th-14th centuries. Its name comes from the Arabic 'al-hamra' (the red one), referring to the reddish stone of its walls."
    },
    {
        "id": "sagrada_familia",
        "name": "Sagrada Familia Spire",
        "city": "Barcelona, Spain",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 55,
        "mystery": "The Sagrada Familia — under construction since 1882 — is the world's largest unfinished\nCatholic church. Its architect, a devout Catalan, dedicated his final years to this\nproject and is buried in its crypt. His name is the key to understanding the design.",
        "stages": [{
            "desc": "Inside the Nativity Facade, scaffolding still climbs the interior. A construction worker's\nlocker from 1926 holds the architect's final sketch and his signed name.",
            "triggers": ["examine locker", "look at architect sketch", "read signed name", "search nativity facade", "check construction locker", "examine final sketch", "inspect signature", "study plans"],
            "success": "The sketch bears the signature: 'I gave my life to this temple. I am buried in its crypt.\nMy architectural style defines Barcelona. Who am I?'",
            "hint": "The Nativity Facade interior. A worker's locker holds the architect's final sketch."
        }],
        "final_answer": "GAUDI",
        "answer_hint": "The Catalan architect who dedicated his life to the Sagrada Familia (5 letters).",
        "points": 5,
        "lore": "Antoni Gaudi (1852-1926) worked on the Sagrada Familia for 43 years, the last 15 exclusively. It's expected to be completed in 2026, the centenary of his death."
    },
    {
        "id": "belem_tower",
        "name": "Belem Tower Gun Powder Room",
        "city": "Lisbon, Portugal",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 56,
        "mystery": "Belem Tower guarded Lisbon's harbor during the Age of Discovery. In the sub-basement gun\npowder room, a 16th-century sailor's sea chest contains a map naming the Portuguese\nexplorer who found the sea route to India.",
        "stages": [{
            "desc": "The gun powder room is cool and stone-vaulted. A sailor's sea chest, salt-crusted and\nancient, contains a faded map. The map names the captain who sailed to India in 1498.",
            "triggers": ["examine sea chest", "look at faded map", "read explorer name", "search gun powder room", "check sub-basement", "open sailor chest", "study old map", "inspect explorer route"],
            "success": "The map reads: 'In 1498, I became the first European to reach India by sea — sailing\naround the Cape of Good Hope. My voyage broke the Arab spice monopoly forever.'",
            "hint": "The sub-basement gun powder room. A sailor's sea chest holds an ancient map."
        }],
        "final_answer": "VASCODAGAMA",
        "answer_hint": "The Portuguese explorer who found the sea route to India (11 letters, no space).",
        "points": 5,
        "lore": "Belem Tower (1519) was built as a fortress and ceremonial gateway to Lisbon. Vasco da Gama's 1497-1499 voyage to India opened the European Age of Discovery in Asia."
    },
    {
        "id": "bran_castle",
        "name": "Bran Castle / Dracula's Castle",
        "city": "Transylvania, Romania",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 57,
        "mystery": "Bran Castle perches on a rocky Transylvanian cliff, its turrets silhouetted against the\nCarpathian sky. Bram Stoker's novel made this the lair of the world's most famous vampire.\nIn the crypt, a silver urn bears the name of the historical ruler who inspired the legend.",
        "stages": [{
            "desc": "The crypt is cold and gothic. A silver urn on an obsidian pedestal is engraved with a\nname: the Wallachian prince whose bloodthirsty reputation spawned a literary monster.",
            "triggers": ["examine crypt", "look at silver urn", "read engraved name", "search castle basement", "check obsidian pedestal", "examine urn inscription", "inspect silver urn"],
            "success": "The urn reads: 'I am Vlad III — Prince of Wallachia. I impaled my enemies in the\nthousands. History knows me as Vlad the Impaler — or by my father's name: Vlad _____.'",
            "hint": "The castle crypt. A silver urn bears the name of the historical Dracula."
        }],
        "final_answer": "DRACULA",
        "answer_hint": "Vlad the Impaler was also known as Vlad _____ (7 letters).",
        "points": 5,
        "lore": "Bran Castle, built 1377, is known as Dracula's Castle. Vlad III 'the Impaler' (1431-1476) ruled Wallachia and was nicknamed 'Dracula' — son of the Dragon (Dracul)."
    },
    {
        "id": "charles_bridge",
        "name": "Charles Bridge Watchtower",
        "city": "Prague, Czech Republic",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 58,
        "mystery": "Charles Bridge — 30 Baroque statues lining a 14th-century stone span across the Vltava.\nThe Old Town bridge tower houses a sealed chest containing a Jewish legend: the name of\nthe creature said to protect Prague's Jewish Quarter.",
        "stages": [{
            "desc": "The bridge tower's upper room holds an iron chest sealed with a Star of David. A Hebrew\ninscription names the legendary protector of the Prague ghetto.",
            "triggers": ["examine iron chest", "read hebrew inscription", "search bridge tower", "check sealed chest", "look at star of david", "examine hebrew text", "inspect protector legend"],
            "success": "The inscription reads: 'I am the _____ — a being of clay brought to life by Rabbi Loew\nto protect the Jews of Prague. My name means shapeless matter in Hebrew.'",
            "hint": "The Old Town bridge tower. An iron chest references Prague's legendary protector."
        }],
        "final_answer": "GOLEM",
        "answer_hint": "The clay creature of Jewish legend that protected Prague (5 letters).",
        "points": 5,
        "lore": "Charles Bridge was built 1357-1402 under Emperor Charles IV. According to legend, Rabbi Judah Loew created the Golem in the 16th century to defend Prague's Jewish ghetto."
    },
    {
        "id": "buda_castle",
        "name": "Buda Castle Labyrinth",
        "city": "Budapest, Hungary",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 59,
        "mystery": "Beneath Buda Castle, a natural cave system — the Buda Labyrinth — stretches for miles.\nMedieval prisoners, Ottoman soldiers, and Cold War spies all used these tunnels. A wall\ncarving in the deepest chamber names this underground world.",
        "stages": [{
            "desc": "The deepest chamber of the labyrinth is cold and wet. The cave walls are covered with\ncenturies of carvings. One particularly deep inscription names the maze itself.",
            "triggers": ["examine deepest chamber", "read wall carving", "search labyrinth", "check cave walls", "look at deep inscription", "examine maze name", "inspect cave carving"],
            "success": "The carving reads: 'I am the _____ beneath Buda Castle — a natural cave turned dungeon,\nturned wine cellar, turned Cold War bunker. I am the maze beneath the palace.'",
            "hint": "The deepest chamber of the Buda Labyrinth. Look for the oldest wall carving."
        }],
        "final_answer": "LABYRINTH",
        "answer_hint": "The maze of tunnels beneath Buda Castle (9 letters).",
        "points": 5,
        "lore": "The Buda Castle Labyrinth is a 1,200-meter cave system beneath Castle Hill. It has served as a prison, wine cellar, and Cold War bunker during its 800-year history."
    },
    {
        "id": "kremlin",
        "name": "Kremlin Secret Archives",
        "city": "Moscow, Russia",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 60,
        "mystery": "Behind the Kremlin's red walls lie state secrets spanning centuries. A declassified\nKGB document mentions a vault beneath the Terem Palace labeled with the name of the\nfirst Tsar of All Russia — the man who unified the Russian state through iron will.",
        "stages": [{
            "desc": "The Terem Palace basement holds a KGB-era vault. A brass label, now tarnished, names\nthe 16th-century ruler whose reign transformed Muscovy into the Russian Empire.",
            "triggers": ["examine vault", "read brass label", "search terem basement", "check kgb vault", "look at tarnished label", "examine tsar name", "inspect brass plate"],
            "success": "The label reads: 'I was the first Tsar of All Russia. My name means 'terrible' or\n'awesome' — a mistranslation that haunts my legacy. Who am I?'",
            "hint": "The Terem Palace basement. A KGB-era vault bears a 16th-century name."
        }],
        "final_answer": "IVAN",
        "answer_hint": "The first Tsar of All Russia — '_____ the Terrible' (4 letters).",
        "points": 5,
        "lore": "The Moscow Kremlin has been the seat of Russian power since the 14th century. Ivan IV 'the Terrible' (1530-1584) was the first ruler crowned Tsar of All Russia."
    },
    {
        "id": "hermitage",
        "name": "Hermitage Museum Amber Room Replica",
        "city": "St. Petersburg, Russia",
        "region": "SOUTHERN & EASTERN EUROPE",
        "number": 61,
        "mystery": "The Hermitage Museum — founded by Catherine the Great — houses 3 million artworks across\nsix buildings. The reconstructed Amber Room, whose original was looted by Nazis and\nvanished in 1945, holds a plaque naming the Empress who built this museum.",
        "stages": [{
            "desc": "In the restored Amber Room, panels of glowing Baltic amber surround you. A dedication\nplaque names the Empress who began the Hermitage collection in 1764.",
            "triggers": ["examine amber room", "read dedication plaque", "search hermitage", "check amber panels", "look at empress name", "examine plaque", "inspect amber walls"],
            "success": "The plaque reads: 'I was Empress of All Russia for 34 years. I acquired the first 225\npaintings that became this museum. My reign was the golden age of Imperial Russia.'",
            "hint": "The reconstructed Amber Room. A dedication plaque names the Hermitage's founder."
        }],
        "final_answer": "CATHERINE",
        "answer_hint": "The Empress who founded the Hermitage Museum — '_____ the Great' (9 letters).",
        "points": 5,
        "lore": "The Hermitage was founded in 1764 by Catherine the Great. The original Amber Room, gifted by Prussia to Peter the Great, was dismantled by Nazis in 1941 and its fate remains unknown."
    },
    {
        "id": "great_pyramid",
        "name": "Great Pyramid King's Chamber",
        "city": "Giza, Egypt",
        "region": "AFRICA & MIDDLE EAST",
        "number": 62,
        "mystery": "The Great Pyramid — the only surviving wonder of the ancient world — has guarded its\nsecrets for 4,500 years. The King's Chamber, deep within, is lined with granite blocks\nweighing 50 tons each. A cartouche on the north wall names the pharaoh entombed here.",
        "stages": [{
            "desc": "The King's Chamber is perfectly silent. The massive granite blocks fit so precisely that\na knife blade cannot slip between them. A faded cartouche on the north wall names the pharaoh.",
            "triggers": ["examine kings chamber", "look at cartouche", "read pharaoh name", "search north wall", "check granite blocks", "examine hieroglyphs", "inspect cartouche"],
            "success": "The cartouche reads: 'I built the Great Pyramid — the tallest structure on Earth for\n3,800 years. My name echoes through eternity as the greatest builder of ancient Egypt.'",
            "hint": "The King's Chamber. A cartouche on the north wall names the pyramid's builder."
        }],
        "final_answer": "KHUFU",
        "answer_hint": "The pharaoh who built the Great Pyramid of Giza (5 letters).",
        "points": 5,
        "lore": "The Great Pyramid was built around 2560 BCE for Pharaoh Khufu (Cheops). It stood 481 feet tall and contains 2.3 million blocks of stone totaling 6 million tons."
    },
    {
        "id": "library_alexandria",
        "name": "Library of Alexandria Underground Basement",
        "city": "Alexandria, Egypt",
        "region": "AFRICA & MIDDLE EAST",
        "number": 63,
        "mystery": "The modern Bibliotheca Alexandrina stands near the site of the ancient Library of\nAlexandria — the greatest repository of knowledge in the classical world. In its\nunderground basement, a holographic display names the last librarian of the ancient library.",
        "stages": [{
            "desc": "The underground basement houses archaeological remains of the original library. A holographic\ndisplay projects the name of the female mathematician who was the last head librarian.",
            "triggers": ["examine holographic display", "read projected name", "search basement", "check archaeological remains", "look at librarian display", "examine projection", "inspect ancient ruins"],
            "success": "The hologram reads: 'I was the last librarian of the Great Library of Alexandria — a\nmathematician, astronomer, and philosopher. A mob killed me in 415 AD. Who was I?'",
            "hint": "The underground basement. A holographic display names the last librarian."
        }],
        "final_answer": "HYPATIA",
        "answer_hint": "The female mathematician who was the last librarian of ancient Alexandria (7 letters).",
        "points": 5,
        "lore": "The Great Library of Alexandria was the largest library of the ancient world. Hypatia (c. 350-415 AD) was a renowned mathematician, astronomer, and Neoplatonist philosopher."
    },
    {
        "id": "valley_of_kings",
        "name": "Valley of the Kings KV62 Tomb",
        "city": "Luxor, Egypt",
        "region": "AFRICA & MIDDLE EAST",
        "number": 64,
        "mystery": "The Valley of the Kings holds 63 royal tombs. KV62 — the smallest — lay hidden for 3,200\nyears until Howard Carter's discovery in 1922. Inside, over 5,000 treasures surrounded\nthe sarcophagus of a pharaoh whose name became synonymous with ancient Egypt.",
        "stages": [{
            "desc": "You descend into the cramped tomb. The walls are painted with scenes from the Book of the\nDead. The sarcophagus lid bears the cartouche of the boy pharaoh buried within.",
            "triggers": ["examine sarcophagus", "read cartouche", "look at tomb paintings", "search kv62", "check burial chamber", "examine boy pharaoh", "inspect sarcophagus lid", "study wall art"],
            "success": "The cartouche reads: 'I became pharaoh at age 9 and died at 18. My tomb was discovered\nintact — the greatest archaeological find in history. Who am I?'",
            "hint": "The KV62 tomb. The sarcophagus bears the cartouche of the boy pharaoh."
        }],
        "final_answer": "TUTANKHAMUN",
        "answer_hint": "The boy pharaoh whose intact tomb was discovered in 1922 (11 letters).",
        "points": 5,
        "lore": "Tutankhamun ruled Egypt c. 1332-1323 BCE. Howard Carter discovered his tomb in 1922 — the only pharaoh's tomb found with its treasures intact. The golden death mask weighs 24 pounds."
    },
    {
        "id": "carthage",
        "name": "Carthage Roman Baths",
        "city": "Tunis, Tunisia",
        "region": "AFRICA & MIDDLE EAST",
        "number": 65,
        "mystery": "The ruins of Carthage lie along the Tunisian coast — the city that nearly defeated Rome.\nIn the Antonine Baths, the largest Roman baths outside Italy, a mosaic names the Carthaginian\ngeneral who crossed the Alps with elephants to invade Rome.",
        "stages": [{
            "desc": "The Antonine Baths sprawl across the coast. A remarkably preserved floor mosaic depicts\nan elephant crossing mountains. The inscription names Carthage's greatest military genius.",
            "triggers": ["examine mosaic", "read elephant mosaic", "search roman baths", "check floor mosaic", "look at general name", "examine carthaginian art", "inspect inscription"],
            "success": "The mosaic reads: 'I crossed the Alps with 37 elephants to attack Rome. I defeated legion\nafter legion but never took the city itself. I am Carthage's greatest son.'",
            "hint": "The Antonine Baths. A floor mosaic names Carthage's greatest general."
        }],
        "final_answer": "HANNIBAL",
        "answer_hint": "The Carthaginian general who crossed the Alps with elephants (8 letters).",
        "points": 5,
        "lore": "Carthage was Rome's greatest rival in the Punic Wars (264-146 BCE). Hannibal Barca crossed the Alps in 218 BCE and terrorized Italy for 15 years but never captured Rome itself."
    },
    {
        "id": "marrakesh",
        "name": "Marrakesh Medina Secret Riad",
        "city": "Marrakesh, Morocco",
        "region": "AFRICA & MIDDLE EAST",
        "number": 66,
        "mystery": "The Marrakesh Medina — a UNESCO World Heritage maze of 10,000 alleys — hides secret\nriads behind unmarked doors. A spice merchant's diary, left in a fountain courtyard,\ncontains a password: the name of the old walled city itself.",
        "stages": [{
            "desc": "A hidden riad opens into a jasmine-scented courtyard. A leather-bound diary floats in\nthe central fountain. Its waterlogged pages reveal a password written in Arabic and French.",
            "triggers": ["examine riad courtyard", "look at diary in fountain", "read waterlogged pages", "search hidden riad", "check fountain", "examine spice merchant diary", "inspect password"],
            "success": "The diary's password reads: 'The old city — the walled heart of Marrakesh — is called\nthe _____. Within these walls, 1,000 years of secrets are locked away.'",
            "hint": "A hidden riad in the Medina. A diary in the fountain holds the password."
        }],
        "final_answer": "MEDINA",
        "answer_hint": "The old walled city quarter of Marrakesh (6 letters).",
        "points": 5,
        "lore": "The Marrakesh Medina dates to the 11th century and is a UNESCO World Heritage site. Its labyrinth of souks, riads, and alleys has been the heart of the city for 1,000 years."
    },
    {
        "id": "timbuktu",
        "name": "Timbuktu Djinguereber Mosque Library",
        "city": "Timbuktu, Mali",
        "region": "AFRICA & MIDDLE EAST",
        "number": 67,
        "mystery": "Timbuktu — legendary city of gold and learning at the edge of the Sahara. The Djinguereber\nMosque, built in 1327, houses a library of priceless manuscripts. A preservationist's\ncatalog names these handwritten texts that reveal Africa's forgotten intellectual history.",
        "stages": [{
            "desc": "The mosque library is cool despite the desert heat. Manuscripts fill every shelf — astronomy,\nmathematics, medicine. A catalog entry names what these ancient texts are collectively called.",
            "triggers": ["examine library", "read catalog entry", "search mosque shelves", "check ancient texts", "look at preservation catalog", "examine manuscripts", "inspect catalog"],
            "success": "The catalog entry reads: 'We are the _____ of Timbuktu — 700,000 handwritten texts on\nastronomy, law, medicine, and philosophy. They prove Africa's written intellectual\ntradition stretches back a millennium.'",
            "hint": "The Djinguereber Mosque library. The catalog entry names these ancient texts."
        }],
        "final_answer": "MANUSCRIPT",
        "answer_hint": "The handwritten texts of Timbuktu — ancient _____ repositories (10 letters).",
        "points": 5,
        "lore": "Timbuktu was a major center of Islamic learning by the 15th century. Over 700,000 manuscripts survive in private and public collections, covering astronomy, medicine, law, and philosophy."
    },
    {
        "id": "lalibela",
        "name": "Lalibela Rock-Hewn Churches",
        "city": "Lalibela, Ethiopia",
        "region": "AFRICA & MIDDLE EAST",
        "number": 68,
        "mystery": "Eleven monolithic churches — carved downward into solid volcanic rock in the 12th century\n— form the 'New Jerusalem' of Ethiopia. The most famous, a cross-shaped church standing\nin a deep pit, hides a golden cross naming this sacred structure.",
        "stages": [{
            "desc": "Descending into the rock-hewn pit, you stand before the most famous of Lalibela's churches\n— carved in the shape of a Greek cross. A golden processional cross names this holy site.",
            "triggers": ["descend into pit", "examine rock church", "look at golden cross", "search carved church", "check cross-shaped church", "examine golden cross name", "inspect rock carving"],
            "success": "The golden cross reads: 'I am _____ _____ — the House of Saint George. Carved from a single\nblock of volcanic rock, I am the most famous of Lalibela's eleven churches.'",
            "hint": "Descend into the pit. A golden cross names this rock-hewn wonder."
        }],
        "final_answer": "BETGIYORGIS",
        "answer_hint": "Ethiopia's most famous rock-hewn church — _____ _____ (11 letters, no space).",
        "points": 5,
        "lore": "Lalibela's 11 rock-hewn churches were built in the late 12th-early 13th century under King Lalibela. Bete Giyorgis (House of St. George) is carved 40 feet into the volcanic tuff."
    },
    {
        "id": "serengeti",
        "name": "Serengeti Ngorongoro Crater Outpost",
        "city": "Serengeti, Tanzania",
        "region": "AFRICA & MIDDLE EAST",
        "number": 69,
        "mystery": "The Serengeti hosts the largest land migration on Earth — 1.5 million wildebeest moving\nin a 500-mile cycle. A ranger's logbook at the Ngorongoro Crater outpost describes this\nannual event in a single word — the great _____ of the herds.",
        "stages": [{
            "desc": "The ranger outpost overlooks the vast Serengeti plains. A logbook open on the desk describes\nthe annual movement of millions of animals across these grasslands.",
            "triggers": ["examine ranger logbook", "read migration description", "search outpost", "check desk logbook", "look at herd record", "examine annual event entry", "inspect ranger notes"],
            "success": "The logbook reads: 'Every year, 1.5 million wildebeest and 200,000 zebras follow the rains\nin a 500-mile circuit. It is the greatest wildlife _____ on Earth.'",
            "hint": "The ranger outpost. The logbook describes the great annual event."
        }],
        "final_answer": "MIGRATION",
        "answer_hint": "The great annual movement of Serengeti herds — the Great _____ (9 letters).",
        "points": 5,
        "lore": "The Serengeti ecosystem hosts the largest terrestrial mammal migration on Earth. Over 1.5 million wildebeest and hundreds of thousands of zebras and gazelles follow seasonal rains."
    },
    {
        "id": "table_mountain",
        "name": "Table Mountain Cable Station",
        "city": "Cape Town, South Africa",
        "region": "AFRICA & MIDDLE EAST",
        "number": 70,
        "mystery": "Table Mountain's flat top — a 1,000-meter-high mesa — dominates the Cape Town skyline.\nA cable car operator's maintenance log describes a hidden panel at the summit naming\nthe geographic feature this mountain overlooks: the meeting point of two oceans.",
        "stages": [{
            "desc": "The cable station at the summit is windswept. A maintenance log describes a bronze compass\nrose embedded in the rock at the highest point, naming the nearby geographic landmark.",
            "triggers": ["examine cable station", "read maintenance log", "search summit", "check bronze compass", "look at geographic marker", "examine compass rose", "inspect rock marker"],
            "success": "The compass rose reads: 'From this summit, you can see the _____ of Good Hope — the\nlegendary headland where the Atlantic meets the Indian Ocean.'",
            "hint": "The summit cable station. A bronze compass rose names the nearby landmark."
        }],
        "final_answer": "CAPE",
        "answer_hint": "The geographic landmark Table Mountain overlooks — the _____ of Good Hope (4 letters).",
        "points": 5,
        "lore": "Table Mountain is estimated to be 260 million years old. The Cape of Good Hope was first rounded by Bartolomeu Dias in 1488, opening the sea route to Asia."
    },
    {
        "id": "robben_island",
        "name": "Robben Island Cell Block",
        "city": "Cape Town, South Africa",
        "region": "AFRICA & MIDDLE EAST",
        "number": 71,
        "mystery": "Robben Island's maximum-security prison held political prisoners for over 400 years. Cell\n46664 housed the world's most famous political prisoner for 18 years. His name is scratched\ninto the wall beside his bunk.",
        "stages": [{
            "desc": "The cell is tiny — barely 6 feet by 8 feet. A thin mat serves as a bed. On the wall beside\nit, a name is scratched into the paint by a man who would become a global icon.",
            "triggers": ["examine cell 46664", "read scratched name", "search prison block", "check tiny cell", "look at bunk wall", "examine prisoner carving", "inspect paint scratches"],
            "success": "The scratched name reads: 'I spent 18 years in this cell. I emerged to lead my nation out\nof apartheid and became its first Black president. Who am I?'",
            "hint": "Cell 46664. A scratched name on the wall identifies the famous prisoner."
        }],
        "final_answer": "MANDELA",
        "answer_hint": "The anti-apartheid leader imprisoned on Robben Island (7 letters).",
        "points": 5,
        "lore": "Nelson Mandela spent 18 of his 27 years of imprisonment on Robben Island. He was released in 1990 and became South Africa's first democratically elected president in 1994."
    },
    {
        "id": "great_zimbabwe",
        "name": "Great Zimbabwe Medieval Ruins",
        "city": "Masvingo, Zimbabwe",
        "region": "AFRICA & MIDDLE EAST",
        "number": 72,
        "mystery": "Great Zimbabwe — the largest stone ruins in sub-Saharan Africa — was the capital of a\nmedieval kingdom that traded gold with China and Persia. The Conical Tower in the Hill\nComplex holds a stone tablet naming the civilization that built this city.",
        "stages": [{
            "desc": "The Hill Complex overlooks the Great Enclosure. The Conical Tower — a mysterious dry-stone\nstructure — holds a stone tablet at its center. The tablet names the builders.",
            "triggers": ["examine conical tower", "read stone tablet", "search hill complex", "check tower center", "look at builder tablet", "examine dry stone", "inspect medieval ruins"],
            "success": "The tablet reads: 'This city — called _____ — is the largest pre-colonial stone structure\nsouth of the Sahara. Our kingdom traded gold with the Swahili coast for five centuries.'",
            "hint": "The Hill Complex. A stone tablet inside the Conical Tower names the civilization."
        }],
        "final_answer": "ZIMBABWE",
        "answer_hint": "The medieval kingdom whose stone capital gave this country its name (8 letters).",
        "points": 5,
        "lore": "Great Zimbabwe was built between the 11th-15th centuries and housed up to 18,000 people. The name 'Zimbabwe' comes from the Shona phrase 'dzimba dzemabwe' (houses of stone)."
    },
    {
        "id": "tsingy",
        "name": "Tsingy de Bemaraha Stone Forest",
        "city": "Madagascar",
        "region": "AFRICA & MIDDLE EAST",
        "number": 73,
        "mystery": "The Tsingy — a 'stone forest' of razor-sharp limestone pinnacles — stretches across western\nMadagascar. In a narrow canyon between the stone blades, a wildlife researcher's field\ncamera captured Madagascar's most famous animal, unique to this island.",
        "stages": [{
            "desc": "The limestone pinnacles tower overhead. A field camera strapped to a rock records the\nisland's unique wildlife. The most recent image is of Madagascar's iconic creature.",
            "triggers": ["examine field camera", "look at wildlife image", "check camera trap", "search stone canyon", "examine animal photo", "inspect field equipment", "study camera data"],
            "success": "The camera shows: 'I live only on Madagascar — nowhere else on Earth. My long ringed tail\nand bright eyes have made me the symbol of this island's unique biodiversity.'",
            "hint": "The stone forest canyon. Check the field camera for Madagascar's most iconic animal."
        }],
        "final_answer": "LEMUR",
        "answer_hint": "Madagascar's iconic primate — found nowhere else on Earth (5 letters).",
        "points": 5,
        "lore": "Madagascar split from Africa 165 million years ago, creating unique biodiversity. Lemurs are found nowhere else — over 100 species evolved in isolation on the island."
    },
    {
        "id": "petra",
        "name": "Petra Treasury Secret Floor",
        "city": "Petra, Jordan",
        "region": "AFRICA & MIDDLE EAST",
        "number": 74,
        "mystery": "The Treasury — carved from a rose-red cliff face 2,000 years ago by the Nabataeans — is\nPetra's most famous monument. A hidden floor panel in the Treasury chamber is marked with\nthe name of the civilization that built this city along the frankincense trade route.",
        "stages": [{
            "desc": "The Treasury's interior chamber is cool and carved from living rock. A floor panel near\nthe back wall is marked with Nabataean script — the name of the people who built Petra.",
            "triggers": ["examine treasury interior", "look at floor panel", "read nabataean script", "search hidden chamber", "check floor marking", "examine carved script", "inspect rose-red rock"],
            "success": "The floor panel reads: 'We are the _____ — masters of desert water engineering. We built\nthis city as our capital along the frankincense and myrrh trade routes.'",
            "hint": "The Treasury interior. A floor panel bears the script of Petra's builders."
        }],
        "final_answer": "NABATAEAN",
        "answer_hint": "The ancient civilization that built Petra (9 letters).",
        "points": 5,
        "lore": "Petra was built by the Nabataeans around 300 BCE as their capital. Their sophisticated water management system supported 30,000 people in the desert via dams, cisterns, and aqueducts."
    },
    {
        "id": "western_wall",
        "name": "Western Wall Tunnels",
        "city": "Jerusalem",
        "region": "AFRICA & MIDDLE EAST",
        "number": 75,
        "mystery": "The Western Wall — the last remnant of the Second Temple — is Judaism's holiest site. In\nthe tunnels beneath, a sealed chamber contains a stone from the Temple's foundation naming\nthe king who built the First Temple on this very mount 3,000 years ago.",
        "stages": [{
            "desc": "The tunnels run deep along the buried courses of the wall. A sealed chamber holds a massive\nfoundation stone with ancient Hebrew script naming the builder of the First Temple.",
            "triggers": ["examine sealed chamber", "read ancient hebrew", "search western wall tunnels", "check foundation stone", "look at temple builder name", "examine hebrew script", "inspect massive stone"],
            "success": "The foundation stone reads: 'I built the First Temple on Mount Moriah — a house for the\nArk of the Covenant. My wisdom was legendary across the ancient world.'",
            "hint": "The Western Wall tunnels. A foundation stone names the builder of the First Temple."
        }],
        "final_answer": "SOLOMON",
        "answer_hint": "The king who built the First Temple in Jerusalem (7 letters).",
        "points": 5,
        "lore": "The Western Wall is the only remaining part of the Second Temple complex, built by Herod. King Solomon's First Temple stood on this site from c. 960-586 BCE until destroyed by the Babylonians."
    },
    {
        "id": "burj_khalifa",
        "name": "Burj Khalifa Maintenance Level 163",
        "city": "Dubai, UAE",
        "region": "AFRICA & MIDDLE EAST",
        "number": 76,
        "mystery": "The Burj Khalifa pierces the sky at 2,717 feet — the tallest structure ever built. On\nmaintenance level 163, accessible only to engineers, a plaque describes how at this\nheight, you can see the curvature of the Earth — and names what surrounds the tower above.",
        "stages": [{
            "desc": "The maintenance level's air is thin and cold. A plaque on the wall describes the sensation\nof being this high: 'Where the tower ends and the _____ begins.'",
            "triggers": ["examine maintenance plaque", "read height description", "search level 163", "check plaque", "look at curvature description", "examine sky reference", "inspect engineering plaque"],
            "success": "The plaque reads: 'At 2,717 feet, the Burj Khalifa reaches into the upper _____ — where\nthe air thins and the Earth curves visibly beneath you.'",
            "hint": "Maintenance level 163. The plaque describes what surrounds the tower at this height."
        }],
        "final_answer": "ATMOSPHERE",
        "answer_hint": "The layer of gases surrounding Earth — what the Burj Khalifa reaches into (10 letters).",
        "points": 5,
        "lore": "The Burj Khalifa (2010) stands 2,717 feet (828 m) with 163 floors. It holds records for tallest building, highest occupied floor, and highest outdoor observation deck."
    },
    {
        "id": "cappadocia",
        "name": "Cappadocia Underground City",
        "city": "Cappadocia, Turkey",
        "region": "AFRICA & MIDDLE EAST",
        "number": 77,
        "mystery": "Cappadocia's soft volcanic rock hides 36 underground cities — some descending 8 levels\nand housing 20,000 people. A sealed room in the deepest level of the largest city bears\na Hittite-era inscription naming this particular subterranean settlement.",
        "stages": [{
            "desc": "You descend through narrow tunnels into the deepest level. A sealed chamber, untouched for\nmillennia, has a wall inscription in Hittite characters naming this underground city.",
            "triggers": ["examine sealed room", "read hittite inscription", "search deepest level", "check underground city", "look at wall text", "examine ancient name", "inspect hittite script"],
            "success": "The inscription reads: 'I am _____ — the largest underground city in Cappadocia. For\nthousands of years, my tunnels sheltered Hittites, early Christians, and Byzantines alike.'",
            "hint": "The deepest level of Cappadocia's largest underground city. A Hittite inscription names it."
        }],
        "final_answer": "KAYMAKLI",
        "answer_hint": "The largest underground city in Cappadocia (8 letters).",
        "points": 5,
        "lore": "Cappadocia's underground cities were carved from soft volcanic tuff. Kaymakli extends 8 levels deep with stables, churches, kitchens, and ventilation shafts — housing up to 3,500 people."
    },
    {
        "id": "hagia_sophia",
        "name": "Hagia Sophia Upper Gallery",
        "city": "Istanbul, Turkey",
        "region": "AFRICA & MIDDLE EAST",
        "number": 78,
        "mystery": "Hagia Sophia — Church, Mosque, Museum, Mosque again — has witnessed 1,500 years of\nhistory. In the upper gallery, a Viking mercenary scratched runes into the marble\nparapet. Below the runes, a mosaic names the Byzantine Emperor who built this wonder.",
        "stages": [{
            "desc": "The upper gallery overlooks the vast dome. Graffiti from a thousand years of visitors\ncovers the marble. A 9th-century mosaic in the south gallery names the great Emperor.",
            "triggers": ["examine upper gallery", "look at south gallery mosaic", "read emperor mosaic", "search gallery", "check viking runes", "examine byzantine mosaic", "inspect marble graffiti"],
            "success": "The mosaic reads: 'I ordered the construction of this greatest church in Christendom,\ncompleted in 537 AD. 'Solomon, I have outdone you,' I declared.'",
            "hint": "The upper gallery south side. A Byzantine mosaic names Hagia Sophia's builder."
        }],
        "final_answer": "JUSTINIAN",
        "answer_hint": "The Byzantine Emperor who built Hagia Sophia (9 letters).",
        "points": 5,
        "lore": "Hagia Sophia was built 532-537 AD under Emperor Justinian I. For nearly 1,000 years it was the largest cathedral in the world. Its dome spans 102 feet and rises 182 feet high."
    },
    {
        "id": "taj_mahal",
        "name": "Taj Mahal Crypt",
        "city": "Agra, India",
        "region": "ASIA",
        "number": 79,
        "mystery": "The Taj Mahal — an ivory-white marble mausoleum built for love. In the crypt beneath the\ncentral dome, the cenotaph of the woman whose death inspired this wonder bears her name.\nWho was the beloved empress of Shah Jahan?",
        "stages": [{
            "desc": "The crypt is cool and quiet. The marble cenotaph is inlaid with semi-precious stones —\nlapis lazuli, turquoise, carnelian. An inscription in Persian names the woman entombed here.",
            "triggers": ["examine crypt", "read cenotaph inscription", "look at marble inlay", "search below dome", "check empress name", "examine persian text", "inspect cenotaph"],
            "success": "The inscription reads: 'I was the wife of Shah Jahan — the _____ Mahal, the Chosen One\nof the Palace. In my memory, he built the most beautiful tomb ever conceived.'",
            "hint": "The crypt beneath the central dome. The cenotaph bears the empress's name."
        }],
        "final_answer": "MUMTAZ",
        "answer_hint": "The beloved empress buried in the Taj Mahal — _____ Mahal (6 letters).",
        "points": 5,
        "lore": "The Taj Mahal was built 1632-1653 by Emperor Shah Jahan for his wife Mumtaz Mahal, who died in childbirth. It took 20,000 artisans and 1,000 elephants to construct."
    },
    {
        "id": "varanasi",
        "name": "Varanasi Ganges River Steppes",
        "city": "Varanasi, India",
        "region": "ASIA",
        "number": 80,
        "mystery": "Varanasi — the oldest continuously inhabited city on Earth — stretches along the western\nbank of India's most sacred river. At dawn, priests perform the ancient fire ritual on the\nstone steppes. A submerged shrine in the river names this holy waterway.",
        "stages": [{
            "desc": "The river steppes descend into the sacred waters. A submerged stone shrine near the\nDashashwamedh Ghat bears a Sanskrit inscription naming the holiest river in Hinduism.",
            "triggers": ["examine submerged shrine", "read sanskrit inscription", "search river steppes", "wade into river", "check stone ghat", "look at river shrine", "inspect sanskrit text"],
            "success": "The inscription reads: 'I am the _____ — the holiest river of India. From the Himalayas\nto the Bay of Bengal, I carry the hopes and ashes of a billion souls.'",
            "hint": "The river steppes at dawn. A submerged shrine bears the name of the sacred river."
        }],
        "final_answer": "GANGES",
        "answer_hint": "India's most sacred river — the holy _____ (6 letters).",
        "points": 5,
        "lore": "Varanasi has been continuously inhabited for 3,000+ years. The Ganges is considered the most sacred river in Hinduism, with its waters believed to purify the soul."
    },
    {
        "id": "sigiriya",
        "name": "Sigiriya Rock Fortress Lion Paw",
        "city": "Sigiriya, Sri Lanka",
        "region": "ASIA",
        "number": 81,
        "mystery": "Sigiriya — the 'Lion Rock' — rises 660 feet above the Sri Lankan jungle. A 5th-century\nfortress-palace crowns its summit. Between the giant lion paws at the entrance, a stone\ntablet names the king who built this sky citadel.",
        "stages": [{
            "desc": "Between the colossal lion paws — the remains of a giant brick lion that once guarded the\nentrance — a stone tablet records the name of the king who made Sigiriya his capital.",
            "triggers": ["examine lion paws", "read stone tablet", "search between paws", "check giant paws", "look at king inscription", "examine fortress entrance", "inspect royal tablet"],
            "success": "The tablet reads: 'I am King _____ — I built this sky fortress after seizing the throne\nfrom my father. My reign lasted 18 years until my brother's army came.'",
            "hint": "Between the giant lion paws at the entrance. A stone tablet names the builder king."
        }],
        "final_answer": "KASSAPA",
        "answer_hint": "The 5th-century Sri Lankan king who built Sigiriya (7 letters).",
        "points": 5,
        "lore": "Sigiriya was built by King Kassapa I (477-495 AD). The fortress-palace on top of the rock includes gardens, pools, and the famous frescoes of the 'Sigiriya Maidens.'"
    },
    {
        "id": "bagan",
        "name": "Bagan Ancient Pagodas",
        "city": "Bagan, Myanmar",
        "region": "ASIA",
        "number": 82,
        "mystery": "Over 2,200 temples and pagodas dot the Bagan plain — the remnants of a Buddhist empire that\nflourished from the 9th to 13th centuries. The Ananda Temple, the finest of them all, holds\na stone inscription naming these iconic Buddhist monuments.",
        "stages": [{
            "desc": "The Ananda Temple's golden spire gleams against the sky. A stone inscription at its base\nnames the architectural form these sacred structures take — a tiered tower common across Asia.",
            "triggers": ["examine ananda temple", "read stone inscription", "search temple base", "check golden spire", "look at architectural name", "examine pagoda form", "inspect buddhist tower"],
            "success": "The inscription reads: 'These sacred Buddhist monuments are called _____s — multi-tiered\ntowers that house relics of the Buddha. Over 2,200 of them stand across the Bagan plain.'",
            "hint": "The Ananda Temple. A stone inscription names these Buddhist monuments."
        }],
        "final_answer": "PAGODA",
        "answer_hint": "The multi-tiered Buddhist tower found across Bagan (6 letters).",
        "points": 5,
        "lore": "The Bagan Archaeological Zone contains over 2,200 temples and pagodas built between the 9th-13th centuries. The Ananda Temple (1105 AD) is considered the finest surviving example."
    },
    {
        "id": "angkor_wat",
        "name": "Angkor Wat Central Sanctuary",
        "city": "Siem Reap, Cambodia",
        "region": "ASIA",
        "number": 83,
        "mystery": "Angkor Wat — the largest religious monument on Earth — spans 400 acres of moats, galleries,\nand towers. In the central sanctuary, a stone stele names the Khmer king who built this\nHindu-Buddhist masterpiece in the 12th century.",
        "stages": [{
            "desc": "The central sanctuary rises on a tiered pyramid. A stone stele at its base, carved in\nSanskrit and Khmer, records the name of the god-king who commissioned this temple-city.",
            "triggers": ["examine central sanctuary", "read stone stele", "search sanctuary base", "check khmer carving", "look at king inscription", "examine sanskrit text", "inspect royal stele"],
            "success": "The stele reads: 'I am King _____ II — the builder of Angkor Wat. My empire stretched from\nVietnam to Malaysia. This temple is my cosmic mountain on Earth.'",
            "hint": "The central sanctuary. A stone stele names the Khmer king who built Angkor Wat."
        }],
        "final_answer": "SURYAVARMAN",
        "answer_hint": "The Khmer king who built Angkor Wat — '_____ II' (11 letters).",
        "points": 5,
        "lore": "Angkor Wat was built 1113-1150 AD by King Suryavarman II as a Hindu temple to Vishnu. It later became Buddhist. It's the largest religious structure in the world at 400 acres."
    },
    {
        "id": "ha_long_bay",
        "name": "Ha Long Bay Hidden Grotto",
        "city": "Quang Ninh, Vietnam",
        "region": "ASIA",
        "number": 84,
        "mystery": "Ha Long Bay — 'Bay of the Descending Dragon' — features 1,600 limestone karst islands\nrising from emerald water. In a hidden grotto inside one island, a local legend carved\ninto the wall names the mythical creature that created this landscape.",
        "stages": [{
            "desc": "Inside a hidden grotto, stalactites drip into crystal pools. A Vietnamese folk carving on\nthe wall depicts a sinuous creature whose thrashing tail carved the bay's islands.",
            "triggers": ["enter hidden grotto", "examine folk carving", "read wall legend", "search limestone cave", "check carved creature", "look at dragon legend", "inspect vietnamese art"],
            "success": "The carving reads: 'I am the _____ — the descending creature whose name this bay bears.\nWhen I dove from the sky, my tail carved these 1,600 islands into the sea.'",
            "hint": "The hidden grotto. A folk carving depicts the mythical creature of legend."
        }],
        "final_answer": "DRAGON",
        "answer_hint": "The mythical creature that gave Ha Long Bay its name — 'Descending _____' (6 letters).",
        "points": 5,
        "lore": "Ha Long Bay means 'Bay of the Descending Dragon.' Legend says a dragon family was sent by the gods to protect Vietnam from invaders, and their tails carved the 1,600 karst islands."
    },
    {
        "id": "grand_palace",
        "name": "Grand Palace Emerald Buddha Chamber",
        "city": "Bangkok, Thailand",
        "region": "ASIA",
        "number": 85,
        "mystery": "The Grand Palace gleams with gold leaf and mirrored tiles. In the Temple of the Emerald\nBuddha, a sacred statue carved from a single block of jade sits on a golden throne. The\nstatue's name describes its most striking feature — the precious green stone it's made from.",
        "stages": [{
            "desc": "The Temple of the Emerald Buddha (Wat Phra Kaew) shimmers. The sacred statue — only 26 inches\ntall — sits atop an 11-meter golden pedestal. A label names the material of the Buddha itself.",
            "triggers": ["examine emerald buddha", "read statue label", "search temple chamber", "check golden pedestal", "look at sacred material", "examine jade statue", "inspect buddha description"],
            "success": "The label reads: 'I am the _____ Buddha — carved not from emerald but from a single block\nof jade. I am the most sacred Buddhist artifact in all of Thailand.'",
            "hint": "The Temple of the Emerald Buddha. The label names the stone of the sacred statue."
        }],
        "final_answer": "EMERALD",
        "answer_hint": "The precious green stone the sacred Buddha is named after (7 letters).",
        "points": 5,
        "lore": "The Grand Palace was built in 1782. The Emerald Buddha, despite its name, is carved from jade or jasper. It's the palladium of Thai Buddhism and is ritually re-robed by the King himself."
    },
    {
        "id": "petronas",
        "name": "Petronas Twin Bridges Machine Room",
        "city": "Kuala Lumpur, Malaysia",
        "region": "ASIA",
        "number": 86,
        "mystery": "The Petronas Twin Towers — the world's tallest twin skyscrapers — are connected by a\ndouble-decker bridge spanning the 41st and 42nd floors. In the bridge's machine room,\na plaque describes what this mid-air connector lets you walk across.",
        "stages": [{
            "desc": "The Skybridge machine room hums with the motors that stabilize the bridge. A plaque on the\nwall describes this feat of engineering and what the bridge spans between the two towers.",
            "triggers": ["examine machine room", "read bridge plaque", "search skybridge level", "check engineering plaque", "look at bridge description", "examine mid-air connector", "inspect twin towers"],
            "success": "The plaque reads: 'This _____ Bridge connects the twin towers 558 feet above the street.\nIt is not attached at both ends — it slides in and out to prevent breaking during high winds.'",
            "hint": "The Skybridge machine room, level 41. A plaque names this mid-air connector."
        }],
        "final_answer": "SKYBRIDGE",
        "answer_hint": "The double-decker connector between the Petronas Towers (9 letters, no space).",
        "points": 5,
        "lore": "The Petronas Twin Towers (1998) stand 1,483 feet each. The Skybridge on levels 41-42 is 192 feet long and not rigidly attached — it floats to allow movement during wind and seismic events."
    },
    {
        "id": "marina_bay",
        "name": "Marina Bay Sands Skypark Drainage System",
        "city": "Singapore",
        "region": "ASIA",
        "number": 87,
        "mystery": "Marina Bay Sands' Skypark — a 1,115-foot-long infinity pool resting atop three 55-story\nhotel towers. In the pool's drainage and filtration room, a maintenance access panel is\nlabeled with the shape that resembles this building's unique silhouette.",
        "stages": [{
            "desc": "The filtration room beneath the infinity pool hums with pumps. An access panel on the main\npump is stamped with an icon representing the building's most distinctive feature.",
            "triggers": ["examine filtration room", "read access panel", "search pump room", "check stamped icon", "look at building shape", "examine skypark symbol", "inspect pump label"],
            "success": "The panel reads: 'The Skypark resembles a floating _____ resting atop three towers — the\nmost iconic silhouette in Singapore's skyline. This shape defines the entire structure.'",
            "hint": "The Skypark filtration room. An access panel describes the building's shape."
        }],
        "final_answer": "SHIP",
        "answer_hint": "The Skypark resembles a floating _____ atop three towers (4 letters).",
        "points": 5,
        "lore": "Marina Bay Sands (2010) cost $5.5 billion. The Skypark is 1,115 feet long — longer than the Eiffel Tower laid down — and the infinity pool holds 376,500 gallons of water."
    },
    {
        "id": "borobudur",
        "name": "Borobudur Stupa Labyrinth",
        "city": "Java, Indonesia",
        "region": "ASIA",
        "number": 88,
        "mystery": "Borobudur — the world's largest Buddhist temple — is a 9th-century stepped pyramid built\nfrom 2 million stone blocks. Its 2,672 relief panels and 504 Buddha statues line a\npilgrimage path. At the summit, a sealed stupa names the enlightened being this temple honors.",
        "stages": [{
            "desc": "The summit of Borobudur is crowned with perforated stupas, each containing a statue. The\nlargest central stupa is sealed. A stone tablet names the one this temple is dedicated to.",
            "triggers": ["examine central stupa", "read stone tablet", "search summit", "check sealed stupa", "look at temple dedication", "examine buddhist monument", "inspect summit tablet"],
            "success": "The tablet reads: 'I am the _____ — the Awakened One. This temple is a three-dimensional\nmandala representing the path to enlightenment. Follow the galleries upward.'",
            "hint": "The summit stupa. A stone tablet names the enlightened being this temple honors."
        }],
        "final_answer": "BUDDHA",
        "answer_hint": "The Awakened One — the enlightened being Borobudur is dedicated to (6 letters).",
        "points": 5,
        "lore": "Borobudur was built c. 800 AD. It's a three-dimensional mandala — pilgrims walk through 10 levels of galleries covering 3 miles, following the path from desire to enlightenment."
    },
    {
        "id": "chocolate_hills",
        "name": "Chocolate Hills Observation Deck",
        "city": "Bohol, Philippines",
        "region": "ASIA",
        "number": 89,
        "mystery": "The Chocolate Hills — 1,268 near-identical conical mounds stretching to the horizon — turn\nbrown in the dry season, giving them their name. A geological survey marker at the\nobservation deck describes the type of landform these hills represent.",
        "stages": [{
            "desc": "The observation deck offers a 360-degree view of 1,268 symmetrical mounds. A geological\nsurvey marker describes what type of terrain these are — a term for weathered limestone formations.",
            "triggers": ["examine observation deck", "read geological marker", "search deck", "check survey plaque", "look at landform type", "examine limestone hills", "inspect geological description"],
            "success": "The marker reads: 'The Chocolate Hills are a _____ landscape — ancient coral limestone\nweathered by millennia of rainfall into these symmetrical conical mounds.'",
            "hint": "The observation deck. A geological survey marker describes the landform type."
        }],
        "final_answer": "KARST",
        "answer_hint": "The geological term for the weathered limestone landscape of the Chocolate Hills (5 letters).",
        "points": 5,
        "lore": "The Chocolate Hills comprise 1,268 conical limestone hills spread over 20 square miles. They are a protected National Geological Monument of the Philippines."
    },
    {
        "id": "great_wall",
        "name": "Great Wall of China Badaling Watchtower",
        "city": "Beijing, China",
        "region": "ASIA",
        "number": 90,
        "mystery": "The Great Wall snakes across 13,000 miles of mountains — the longest structure ever built.\nAt the Badaling watchtower, a garrison commander's logbook names the collective _____ of\nChinese rulers who built, rebuilt, and extended these fortifications over 2,000 years.",
        "stages": [{
            "desc": "Inside the Ming-era watchtower at Badaling, a garrison commander's logbook lies on a stone\ndesk. It names the collective succession of ruling families who built the Wall.",
            "triggers": ["examine watchtower", "read commander logbook", "search garrison post", "check stone desk", "look at ruling families", "examine wall builder records", "inspect logbook"],
            "success": "The logbook reads: 'Not one emperor, not one _____ — but many over 2,000 years built this\nWall. The Ming alone added 5,500 miles. We built to defend against the northern nomads.'",
            "hint": "The Badaling watchtower. The garrison logbook names the collective ruling families."
        }],
        "final_answer": "DYNASTY",
        "answer_hint": "The succession of ruling families who built the Great Wall (7 letters).",
        "points": 5,
        "lore": "The Great Wall was built over 2,000+ years by multiple dynasties. The Ming Dynasty (1368-1644) built the most famous sections, extending the Wall to over 5,500 miles."
    },
    {
        "id": "forbidden_city",
        "name": "Forbidden City Imperial Library",
        "city": "Beijing, China",
        "region": "ASIA",
        "number": 91,
        "mystery": "The Forbidden City — 980 buildings, 8,886 rooms — was home to 24 emperors. The Imperial\nLibrary housed the Emperor's most precious scrolls. A catalog entry names the dynasty\nthat built this palace complex in the early 15th century.",
        "stages": [{
            "desc": "The Imperial Library is hushed. Rows of ancient scrolls and silk-bound books fill the\nshelves. A lacquered catalog box holds a scroll naming the dynasty that raised these walls.",
            "triggers": ["examine imperial library", "read catalog scroll", "search library shelves", "check lacquered box", "look at dynasty scroll", "examine forbidden city builders", "inspect catalog"],
            "success": "The catalog scroll reads: 'I am the _____ Dynasty — the last Han Chinese imperial house. I\nbuilt the Forbidden City from 1406-1420. My treasure fleets sailed to Africa.'",
            "hint": "The Imperial Library. A lacquered catalog box holds the name of the builders."
        }],
        "final_answer": "MING",
        "answer_hint": "The dynasty that built the Forbidden City (4 letters).",
        "points": 5,
        "lore": "The Forbidden City was built 1406-1420 under the Ming Dynasty's Yongle Emperor. Commoners were forbidden on pain of death — hence 'Forbidden City.' It's the world's largest palace complex."
    },
    {
        "id": "terracotta_army",
        "name": "Terracotta Army Pit 1 Trenches",
        "city": "Xi'an, China",
        "region": "ASIA",
        "number": 92,
        "mystery": "Pit 1 contains over 6,000 life-sized terracotta soldiers — each with unique facial features\n— buried to guard China's first emperor in the afterlife. A bronze tablet at the excavation\nedge names the _____ who unified China and ordered this immortal army.",
        "stages": [{
            "desc": "The trench reveals row upon row of terracotta warriors, horses, and chariots. A bronze\ntablet at the excavation edge names the emperor who commanded this army for eternity.",
            "triggers": ["examine pit trenches", "read bronze tablet", "search excavation edge", "check terracotta army", "look at emperor name", "examine first emperor tablet", "inspect clay soldiers"],
            "success": "The tablet reads: 'I am _____ Shi Huang — the First Emperor of a unified China. I\nstandardized writing, currency, and measures. My mausoleum took 700,000 workers 38 years.'",
            "hint": "Pit 1 excavation edge. A bronze tablet names the First Emperor."
        }],
        "final_answer": "QIN",
        "answer_hint": "The dynasty of China's First Emperor — '_____ Shi Huang' (3 letters).",
        "points": 5,
        "lore": "The Terracotta Army was buried c. 210 BCE with Qin Shi Huang, the First Emperor of China. It was discovered in 1974 by local farmers drilling a well. No two faces are alike."
    },
    {
        "id": "potala",
        "name": "Potala Palace Secret Shrine",
        "city": "Lhasa, Tibet",
        "region": "ASIA",
        "number": 93,
        "mystery": "The Potala Palace — 13 stories, 1,000 rooms, perched on Red Mountain at 12,100 feet — was\nthe winter residence of Tibetan Buddhism's spiritual leaders. A secret shrine hidden behind\na prayer wheel names the highest spiritual authority of Tibetan Buddhism.",
        "stages": [{
            "desc": "Behind a massive prayer wheel in a hidden chapel, a secret shrine glows with yak-butter\nlamps. The shrine honors the spiritual leader whose title has been held by 14 incarnations.",
            "triggers": ["examine secret shrine", "read shrine dedication", "spin prayer wheel", "search hidden chapel", "check yak-butter lamps", "look at spiritual leader", "inspect tibetan shrine"],
            "success": "The shrine reads: 'I am the _____ Lama — the Ocean of Wisdom. For over 600 years, each\nincarnation has guided the spiritual path of the Tibetan people.'",
            "hint": "Behind the prayer wheel. The secret shrine names the spiritual leader of Tibet."
        }],
        "final_answer": "DALAI",
        "answer_hint": "The spiritual leader of Tibetan Buddhism — the _____ Lama (5 letters).",
        "points": 5,
        "lore": "The Potala Palace was built 1645-1694 by the 5th Dalai Lama. It rises 13 stories, contains 1,000 rooms, and stands at 12,100 feet above sea level — making it the highest palace on Earth."
    },
    {
        "id": "nijo_castle",
        "name": "Nijo Castle Nightingale Floor",
        "city": "Kyoto, Japan",
        "region": "ASIA",
        "number": 94,
        "mystery": "Nijo Castle's 'nightingale floors' were designed to chirp like birds when walked upon — a\nsecurity system against assassins. A samurai's scroll hidden in the floorboards names the\nmilitary ruler who commissioned this castle to display his power over the Emperor.",
        "stages": [{
            "desc": "The nightingale floor sings beneath your feet. A loose board in the main corridor reveals\na hidden scroll — a samurai's message naming the warlord who unified Japan.",
            "triggers": ["examine nightingale floor", "look under loose board", "read samurai scroll", "search corridor floor", "check chirping boards", "examine hidden scroll", "inspect warlord name"],
            "success": "The scroll reads: 'I am _____ — the supreme military ruler of Japan. I built this castle\nin 1603 to show the Emperor that a new era had begun. The age of the samurai.'",
            "hint": "The nightingale floor corridor. A hidden scroll names Japan's unifying warlord."
        }],
        "final_answer": "SHOGUN",
        "answer_hint": "The military ruler of feudal Japan — the supreme warlord (6 letters).",
        "points": 5,
        "lore": "Nijo Castle was built 1603 by Tokugawa Ieyasu, the first Tokugawa Shogun. The 'nightingale floors' squeak intentionally — the nails rub against clamps in the floorboards, creating a bird-like chirping."
    },
    {
        "id": "mt_fuji",
        "name": "Mt. Fuji Fifth Station Shrine",
        "city": "Shizuoka, Japan",
        "region": "ASIA",
        "number": 95,
        "mystery": "Mount Fuji — Japan's sacred 12,388-foot volcano — has inspired pilgrims and artists for\ncenturies. The Fifth Station, at 7,500 feet, marks the boundary between the secular world\nand the sacred mountain. A Shinto shrine here bears the mountain's sacred name.",
        "stages": [{
            "desc": "The Fifth Station shrine is simple and weathered. A wooden dedication plaque, renewed each\nyear, bears the kanji for the sacred peak itself — the name of Japan's most iconic symbol.",
            "triggers": ["examine fifth station shrine", "read dedication plaque", "look at japanese kanji", "search shrine", "check wooden plaque", "examine sacred mountain name", "inspect shinto marker"],
            "success": "The plaque reads: 'I am _____ -san — the sacred fire mountain. For a thousand years, the\nJapanese have climbed my slopes as an act of worship. Hokusai painted me 36 times over.'",
            "hint": "The Fifth Station Shinto shrine. A dedication plaque bears the mountain's sacred name."
        }],
        "final_answer": "FUJI",
        "answer_hint": "Japan's sacred volcanic mountain — Mount _____ (4 letters).",
        "points": 5,
        "lore": "Mount Fuji (12,388 ft) is an active stratovolcano, last erupting in 1707. It has been a sacred site for over 1,000 years. The Fifth Station marks the traditional start of the climbing route."
    },
    {
        "id": "akihabara",
        "name": "Akihabara Underground Cyber Lab",
        "city": "Tokyo, Japan",
        "region": "ASIA",
        "number": 96,
        "mystery": "Beneath Akihabara's neon-lit electronics district, a secret underground cyber lab runs\non servers cooled by liquid nitrogen. A terminal screen displays a single Japanese word\nthat describes the obsessed fans of anime, manga, and video games who rule this district.",
        "stages": [{
            "desc": "The underground lab glows with LED strips and server racks. A terminal screen displays a\nJapanese cultural term that has become a global phenomenon — the identity of Akihabara's tribe.",
            "triggers": ["examine underground lab", "read terminal screen", "search cyber lab", "check server room", "look at japanese term", "examine akihabara culture", "inspect terminal display"],
            "success": "The terminal reads: 'We are the _____ — the passionate, obsessed fans of anime, manga,\nand video games. Akihabara is our spiritual home. Our culture now spans the globe.'",
            "hint": "The underground cyber lab. A terminal screen displays the culture of Akihabara."
        }],
        "final_answer": "OTAKU",
        "answer_hint": "The Japanese term for obsessed anime/manga/gaming fans (5 letters).",
        "points": 5,
        "lore": "Akihabara is Tokyo's Electric Town — the global center of otaku culture. Originally known for post-WWII radio parts shops, it evolved into the world's mecca for electronics, anime, and gaming."
    },
    {
        "id": "gyeongbokgung",
        "name": "Gyeongbokgung Palace Pavilion",
        "city": "Seoul, South Korea",
        "region": "ASIA",
        "number": 97,
        "mystery": "Gyeongbokgung — the 'Palace of Shining Happiness' — was the main royal palace of Korea's\nlongest-ruling dynasty. In the Hyangwonjeong Pavilion, a royal edict stored in a lacquer\nbox names the _____ that ruled Korea for over 500 years.",
        "stages": [{
            "desc": "The Hyangwonjeong Pavilion floats on a lotus pond. A lacquer box on a reading desk holds\na royal edict naming the dynasty that made this palace their seat of power.",
            "triggers": ["examine pavilion", "read royal edict", "search lacquer box", "cross lotus pond", "check reading desk", "look at dynasty edict", "inspect korean palace"],
            "success": "The edict reads: 'I am the _____ Dynasty — the last and longest royal house of Korea.\nWe ruled from 1392 to 1910, and Gyeongbokgung was the crown of our kingdom.'",
            "hint": "The Hyangwonjeong Pavilion. A royal edict names Korea's longest-ruling dynasty."
        }],
        "final_answer": "JOSEON",
        "answer_hint": "The Korean dynasty that ruled for 500+ years — the _____ Dynasty (6 letters).",
        "points": 5,
        "lore": "Gyeongbokgung was built in 1395 as the main palace of the Joseon Dynasty. The dynasty lasted 518 years (1392-1910), making it one of the longest-ruling royal houses in world history."
    },
    {
        "id": "dmz",
        "name": "DMZ Subterranean Infiltration Tunnel",
        "city": "DMZ, Korea",
        "region": "ASIA",
        "number": 98,
        "mystery": "The Korean DMZ — the most heavily fortified border on Earth — hides four infiltration\ntunnels dug by North Korea beneath the 38th parallel. In Tunnel 3, a painted sign on the\nrock wall names the '_____ village' where armistice negotiations have been held since 1953.",
        "stages": [{
            "desc": "Tunnel 3 burrows through granite 240 feet beneath the DMZ. Near the sealed northern end, a\npainted sign on the rock wall marks the location of the famous border village.",
            "triggers": ["examine tunnel 3", "read painted sign", "search infiltration tunnel", "check rock wall sign", "look at truce village", "examine dmz tunnel", "inspect border marker"],
            "success": "The sign reads: 'I am _____ — the Truce Village where North and South Korea sit face\nto face across the Military Demarcation Line. Since 1953, we have talked without peace.'",
            "hint": "Tunnel 3 beneath the DMZ. A sign names the truce village on the border."
        }],
        "final_answer": "PANMUNJOM",
        "answer_hint": "The 'truce village' where Korean armistice talks are held (9 letters).",
        "points": 5,
        "lore": "The DMZ is 155 miles long and 2.5 miles wide. Panmunjom is where the 1953 Korean Armistice Agreement was signed. North Korean infiltration tunnels were discovered in 1974, 1975, 1978, and 1990."
    },
    {
        "id": "sydney_opera",
        "name": "Sydney Opera House Sub-basement",
        "city": "Sydney, Australia",
        "region": "OCEANIA & ANTARCTICA",
        "number": 99,
        "mystery": "The Sydney Opera House — its white sails billowing over Sydney Harbour — is a UNESCO\nWorld Heritage masterpiece. In the sub-basement, the original 1957 competition-winning\nsketch is framed. The architect's signature names the Danish visionary who designed it.",
        "stages": [{
            "desc": "The sub-basement holds the Opera House archives. A framed sketch — the winning 1957\ncompetition entry — hangs on the wall. The architect's bold signature spans the corner.",
            "triggers": ["examine sub-basement", "look at framed sketch", "read architect signature", "search archives", "check competition sketch", "examine winning design", "inspect signature"],
            "success": "The sketch bears the signature: 'I won an international competition to design this Opera\nHouse. My vision — white sails on the harbor — became Australia's greatest icon.'",
            "hint": "The sub-basement archives. The architect's signature is on the 1957 sketch."
        }],
        "final_answer": "UTZON",
        "answer_hint": "The Danish architect who designed the Sydney Opera House (5 letters).",
        "points": 5,
        "lore": "The Sydney Opera House was designed by Jorn Utzon and opened in 1973. Its iconic shell roof uses 1,056,000 white ceramic tiles. Utzon never saw the completed building in person."
    },
    {
        "id": "mcmurdo",
        "name": "McMurdo Research Station Sub-Ice Vault",
        "city": "Antarctica",
        "region": "OCEANIA & ANTARCTICA",
        "number": 100,
        "mystery": "\n  \033[1;33m~ GRAND FINALE: Clue 100 — McMurdo Station, Antarctica ~\033[0m\n\nAntarctica — the frozen continent at the bottom of the world. Beneath the McMurdo Research\nStation, a sub-ice vault carved 50 feet into the Ross Ice Shelf holds the final clue.\nHere, the race for the Master Family Serum reaches its end. A frozen holographic terminal\n— left by the original family patriarchs — asks one final question: the name of the\nlegendary explorer who first reached the South Pole, whose spirit of discovery unites all\nfour houses.",
        "stages": [{
            "desc": "The sub-ice vault is a cathedral of blue ice. The holographic terminal flickers — a message\nfrom the patriarchs. It asks: 'Who was the first to stand at the South Pole, the explorer\nwhose courage embodies the spirit of all four families?'",
            "triggers": ["examine holographic terminal", "read final question", "search ice vault", "approach frozen terminal", "look at explorer question", "examine patriarch message", "inspect blue ice vault"],
            "success": "The final message reads: 'On December 14, 1911, a Norwegian explorer reached the southernmost\npoint of Earth. His achievement united the world in wonder. His name is the final key.'",
            "hint": "The sub-ice vault. The holographic terminal asks the final question of the race."
        }],
        "final_answer": "AMUNDSEN",
        "answer_hint": "The Norwegian explorer who first reached the South Pole in 1911 (8 letters).",
        "points": 5,
        "lore": "The McMurdo Research Station is the largest Antarctic research base. Ernest Shackleton led the 1914-1917 Endurance expedition — one of history's greatest survival stories. The South Pole was first reached by Roald Amundsen in 1911; Shackleton's leadership under impossible odds became legendary."
    },
]

# ── Shop Items ───────────────────────────────────────────────────────

SHOP_ITEMS = {
    # Tools
    "flashlight": {
        "name": "Flashlight",
        "type": "tool",
        "price": 25,
        "description": "Reveals hidden text in dark locations. One-time use per dark area.",
        "effect": "Illuminates dark areas, revealing clues that would otherwise be missed.",
    },
    "notepad": {
        "name": "Pen & Notepad",
        "type": "tool",
        "price": 15,
        "description": "Auto-records all clues you discover for later review.",
        "effect": "Passively records solved clues. Use 'notes' to review everything you've found.",
    },
    "magnifier": {
        "name": "Magnifying Glass",
        "type": "tool",
        "price": 40,
        "description": "Reveals subtle details in location descriptions. One-time use.",
        "effect": "When used at a location, reveals an extra hint for the current puzzle stage.",
    },
    "compass": {
        "name": "Compass",
        "type": "tool",
        "price": 30,
        "description": "Points toward your next unsolved location's general direction.",
        "effect": "Reveals which unsolved location will yield the most points.",
    },
    "lockpick": {
        "name": "Lockpick Set",
        "type": "tool",
        "price": 50,
        "description": "Skip one puzzle stage entirely. Single use.",
        "effect": "Automatically advances you past the current puzzle stage.",
    },
    "granite": {
        "name": "Granite Chunk",
        "type": "tool",
        "price": 20,
        "description": "A throwable stone. Can be used as a distraction or to break fragile barriers.",
        "effect": "Distraction tool — when stuck, may reveal an alternative approach.",
    },
    # ── Weapons (tiered by cost/damage) ──────────────────────────
    # Melee weapons are reusable. Ranged/explosive are single-use.
    "butter_knife": {
        "name": "Butter Knife",
        "type": "weapon",
        "tier": 1,
        "price": 10,
        "damage": 0.5,
        "description": "Barely a weapon. Still sharp enough to annoy. Reusable.",
        "reusable": True,
    },
    "brass_knuckles": {
        "name": "Brass Knuckles",
        "type": "weapon",
        "tier": 2,
        "price": 15,
        "damage": 1,
        "description": "Solid brass punch enhancer. Reusable.",
        "reusable": True,
    },
    "fencing_foil": {
        "name": "Fencing Foil",
        "type": "weapon",
        "tier": 3,
        "price": 20,
        "damage": 1.5,
        "description": "A light, flexible blade. Quick but shallow. Reusable.",
        "reusable": True,
    },
    "iron_crowbar": {
        "name": "Iron Crowbar",
        "type": "weapon",
        "tier": 4,
        "price": 25,
        "damage": 2,
        "description": "Heavy iron. Doubles as a door opener. Reusable.",
        "reusable": True,
    },
    "hunting_knife": {
        "name": "Hunting Knife",
        "type": "weapon",
        "tier": 5,
        "price": 30,
        "damage": 2.5,
        "description": "Serrated edge, balanced grip. Reusable.",
        "reusable": True,
    },
    "steel_broadsword": {
        "name": "Steel Broadsword",
        "type": "weapon",
        "tier": 6,
        "price": 35,
        "damage": 3,
        "description": "A full-length battle blade. Reusable.",
        "reusable": True,
    },
    "blowdart_pipe": {
        "name": "Blowdart Pipe",
        "type": "weapon",
        "tier": 7,
        "price": 40,
        "damage": 3.5,
        "description": "Silent, poison-tipped dart. Single use.",
        "reusable": False,
    },
    "throwing_stars": {
        "name": "Throwing Stars",
        "type": "weapon",
        "tier": 8,
        "price": 45,
        "damage": 4,
        "description": "A set of 3 razor-sharp shuriken. Single use.",
        "reusable": False,
    },
    "crossbow": {
        "name": "Crossbow",
        "type": "weapon",
        "tier": 9,
        "price": 50,
        "damage": 4.5,
        "description": "Compact crossbow with a single bolt. Single use.",
        "reusable": False,
    },
    "stun_gun": {
        "name": "Stun Gun",
        "type": "weapon",
        "tier": 10,
        "price": 55,
        "damage": 5,
        "description": "High-voltage shock. Single use.",
        "reusable": False,
    },
    "katana": {
        "name": "Katana",
        "type": "weapon",
        "tier": 11,
        "price": 60,
        "damage": 5.5,
        "description": "A master-crafted Japanese blade. Whisper-silent cut. Reusable.",
        "reusable": True,
    },
    "spike_trap": {
        "name": "Spike Trap",
        "type": "weapon",
        "tier": 12,
        "price": 65,
        "damage": 6,
        "description": "A concealed floor trap. Deploy and wait. Single use.",
        "reusable": False,
    },
    "smoke_poison_gas": {
        "name": "Smoke Poison Gas",
        "type": "weapon",
        "tier": 13,
        "price": 70,
        "damage": 6.5,
        "description": "Toxic cloud that lingers. Also poisons the target. Single use.",
        "poisons": True,
        "reusable": False,
    },
    "acid_vial": {
        "name": "Acid Vial",
        "type": "weapon",
        "tier": 14,
        "price": 75,
        "damage": 7,
        "description": "Glass vial of corrosive acid. Horrific burns. Single use.",
        "reusable": False,
    },
    "grenade": {
        "name": "Grenade",
        "type": "weapon",
        "tier": 15,
        "price": 80,
        "damage": 7.5,
        "description": "Standard fragmentation grenade. Single use.",
        "reusable": False,
    },
    "landmine": {
        "name": "Landmine",
        "type": "weapon",
        "tier": 16,
        "price": 85,
        "damage": 8,
        "description": "Pressure-triggered explosive. Plant and retreat. Single use.",
        "reusable": False,
    },
    "dynamite_stick": {
        "name": "Dynamite Stick",
        "type": "weapon",
        "tier": 17,
        "price": 90,
        "damage": 8.5,
        "description": "Old-school high explosive with a short fuse. Single use.",
        "reusable": False,
    },
    "rocket_launcher": {
        "name": "Rocket Launcher",
        "type": "weapon",
        "tier": 18,
        "price": 95,
        "damage": 9,
        "description": "Shoulder-fired devastation. Single use.",
        "reusable": False,
    },
    "c4_explosive": {
        "name": "C4 Explosive",
        "type": "weapon",
        "tier": 19,
        "price": 100,
        "damage": 9.5,
        "description": "Military-grade plastic explosive. Remote detonation. Single use.",
        "reusable": False,
    },
    "mega_bomb": {
        "name": "Mega Bomb",
        "type": "weapon",
        "tier": 20,
        "price": 105,
        "damage": 10,
        "description": "The ultimate equalizer. 10 damage — INSTANT KILL. Single use.",
        "reusable": False,
    },
    # Defense
    "shield": {
        "name": "Shield",
        "type": "defense",
        "price": 60,
        "description": "Blocks 2 damage per use. Has 3 uses before breaking.",
        "block": 2,
        "uses": 3,
    },
    "health_potion": {
        "name": "Health Potion",
        "type": "defense",
        "price": 50,
        "description": "Restores 3 HP. Cannot exceed maximum health of 10.",
        "heal": 3,
    },
    "antidote": {
        "name": "Antidote",
        "type": "defense",
        "price": 40,
        "description": "Cures poison status. Also restores 1 HP.",
        "cure_poison": True,
        "heal": 1,
    },
    "armor": {
        "name": "Armor Vest",
        "type": "defense",
        "price": 90,
        "description": "Reduces all incoming damage by 1. Permanent passive effect.",
        "damage_reduction": 1,
    },
}
