"""Build the initial discovery queue once; preserve IDs on subsequent imports."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DISCOVERY = ROOT / "research" / "discovery"
DATE = "2026-10-16"

# Pre-freeze editorial cleanup. These are discarded leads, not researched decisions.
DROP_WORKS = set("""
Against a Dark Background
The End of Eternity
The World Set Free
The Island of Doctor Moreau
The Earth War
The Unpleasant Profession of Jonathan Hoag
The Light of Other Days
Memoirs Found in a Bathtub
Fiasco
Hogan's Endgame Enigma
Robot Uprisings
The Forever Free
The Truth of Fact, the Truth of Feeling
Exhalation
The Heart Goes Last
The Handmaid's Tale
Utopia
News from Nowhere
Us
The Scarlet Plague
The Iron Heel
The War with the Newts
War with the Robots
Time Is the Simplest Thing
The Big Front Yard
Utopia 14
Cat's Cradle
The Big Time
The Happiness Machine
The Nine Billion Names of God
The Machine That Won the War
Evidence
The Tercentenary Incident
The Fun They Had
The Dead Past
The Last Answer
The Winnowing
Who Goes There?
The Waveries
The Mute Inglorious Tam
The Cosmic Rape
To Marry Medusa
More Than Human
The Dreaming Jewels
Always Coming Home
The Ones Who Walk Away from Omelas
The Word for World Is Forest
The Lathe of Heaven
The Left Hand of Darkness
The Birthday of the World
The Wanderground
The Kin of Ata Are Waiting for You
Ecotopia
The Fifth Head of Cerberus
Halting State
Rule 34
Quarantine
Zendegi
The Clockwork Rocket
Terminal World
Great North Road
Misspent Youth
The Evolutionary Void
Radicalized
The Lost Cause
Nexus
Life 2.0
The Difference Engine
The Demolished Man
The Stars My Destination
The Squares of the City
The Hierarchies
The Factory
Gathering Blue
The City of Ember
The Hunger Games
Version Control
Never Let Me Go
Gattaca
In Time
High-Rise
Robot & Frank
Tau
Archive
Ron’s Gone Wrong
Lightyear
Strange World
Aniara
Time Masters
The Man Who Fell to Earth
Solaris (1972)
Love and Monsters
Finch
The Last Mimzy
Almost Human
The Expanse
Foundation
Electric Dreams: The Commuter
Philip K. Dick's Electric Dreams: Real Life
Black Mirror: Nosedive
Black Mirror: Be Right Back
Black Mirror: Rachel, Jack and Ashley Too
Black Mirror: Joan Is Awful
Love, Death & Robots: Ice
Love, Death & Robots: Suits
Love, Death & Robots: Mason's Rats
The Twilight Zone: The Obsolete Man
The Twilight Zone: The Lonely
The Twilight Zone (1985): The Mind of Simon Foster
The Outer Limits: The Sixth Finger
The Outer Limits: The Refuge
The Outer Limits: Valerie 23
Rick and Morty: Analyze Piss
Solar Opposites
Scavengers Reign
Final Space
Transformers: Rescue Bots
Serial Experiments Lain
Dennou Boukenki Webdiver
Den-noh Coil
Eden of the East
Patema Inverted
RahXephon
Macross Plus
Macross Frontier
Macross Delta
Mobile Suit Gundam
Mobile Suit Gundam: The Witch from Mercury
Robot Carnival: Starlight Angel
Robot Carnival: Cloud
Memories: Magnetic Rose
Memories: Cannon Fodder
The Animatrix: Matriculated
Somali and the Forest Spirit
Angel's Egg
Key the Metal Idol
Eureka Seven
Eureka Seven AO
Gurren Lagann
Neon Genesis Evangelion
The End of Evangelion
Genocidal Organ
Doraemon: Nobita's Secret Gadget Museum
Chojin Locke
Crusher Joe
Outlaw Star
Cowboy Bebop
Planetes
Orb: On the Movements of the Earth
Fallout 4
Cyberpunk 2077: Phantom Liberty
Deus Ex: Human Revolution
Deus Ex: Mankind Divided
Citizen Sleeper 2: Starward Vector
Observation
The Moment of Silence
Mirror's Edge Catalyst
RUINER
Dex
Republique
The Outer Worlds: Peril on Gorgon
The Outer Worlds: Murder on Eridanos
Surviving the Aftermath
Anno 2205
Distant Worlds
Master of Orion
Galactic Civilizations
AI War 2
SteamWorld Build
SteamWorld Heist
The Fall Part 2: Unbound
Roboquest
The Metropolitan Man
20020
Superman: Birthright
Superman: Peace on Earth
Superman: House of Brainiac
Superman: Lost
Kingdom Come
The Invisibles
East of West
Ascender
The Flintstones (2016)
Upgrade Soul
2000 AD: The V.C.s
The Airtight Garage
Wake
Orbital
Universal War One
Universal War Two
Aquablue
""".strip().splitlines())

# Fallout 4's Institute and Graygarden are retained explicitly below.
KEEP_EXCEPTIONS = {
    ("Fallout 4", "The Institute"),
    ("Fallout 4", "Graygarden"),
    ("The Expanse", "Earth under Basic Assistance"),
}

DROP_SOCIETIES = set("""
Culture Interesting Times Gang
Fastolfe's proposed robot-supported expansion
The Building's bureaucratic society
King Krool's automated kingdom
A-Io on Urras
Aka before the Corporation
Gogol labor economy
Amalgam's immortal society
Chiku's machine-assisted interstellar civilization
Querencia within the Void
Cloud polity after the conflict
Commercial digient development economy
Post-crisis QualityLand
Pralor robotic civilization in Prototype
Mintakan society as boundary case
Mokra-controlled Alsaurian society
Malon waste economy
Mirror Universe Terran slave economy
Soliton wave and automated Texas-class program
Regor 2's astrological welfare state
Krill civilization
Lysella's encounter with replicator society
Futurekind-era human refuge and Malcassairo
Jagrafess-directed media state
Land of Fiction's Master Brain
Gallifrey under the Matrix
Serrakin-Hebridans' corporate society
Satellite-mediated human societies
Destiny's automated human life-support society
Terminus Foundation
Captive digital crew society
MASS-assisted segregated society
Neo-Victorian phyle
West Block's excluded residents
Robotania's independent robot state
Posthuman robotic and biological successors
Teresa's advanced Terezart civilization
Mu's shipboard society
Ataraxia's computer-governed human society
Durandal's proposed Destiny Plan society
Frontier Setter's autonomous interstellar project
Android Resistance civilization
Post-APE human civilization
Robot-production consumer society
Antarctic outpost as comparison case
Queen Millennia
Vault 81
Songbird and autonomous Blackwall systems
Templar anti-augmentation society
SHODAN's projected transformed reality
Surface humanity before the comet impact
New Jerusalem after the megastructure decision
Machine kingdom of the Forest
Machine amusement park
Quen civilization
Nemesis's posthuman collective
Andromeda Initiative settlements
Cephalon Suda's knowledge collective
Entrati's Necraloid-supported enclave
Aperture under Wheatley
Combine's wider synthetic civilization
Commercial virtual-world society
AVR-dominated human civilization
Gorgon's automated pharmaceutical economy
Rizzo's parasite-managed colony
Academic Privilege automated technocracy
Shared Burdens mechanized commonwealth
Self-Aware Colony society
Sophons
The Vodyani's Ark society
Morrigi automated civilization
Seraphim civilization
Lunar Corporation's Matriarch society
Capital City post-scarcity colony configuration
Mechanically augmented segregated society
Caleb's autonomous robot civilization
""".strip().splitlines())

CORRECTIONS = {
    ("The State of the Art", "Culture Zetetic Elench"): ("Excession", "Zetetic Elench"),
    ("Child of Time", "The Firstborn's managed civilizations"): ("Time Odyssey", "The Firstborn's managed civilizations"),
    ("Child of Time", "Miran civilization"): ("The Time Odyssey", "Mir's administered Earth"),
    ("Galactic North", "Inhibitor and Greenfly-dominated galaxy"): ("Galactic North", "Greenfly-dominated galaxy"),
    ("The Invincible", "Machine ecosystem on Regis III"): ("The Invincible", "Regis III machine ecology"),
    ("Bicentennial Man", "Robot-served human consumer society"): ("The Bicentennial Man", "Robot-supported human society"),
    ("The Surrogates", "Surrogate-dependent human society"): ("Surrogates", "Human society using robotic surrogates"),
    ("Terra e...", "Ataraxia's computer-governed human society"): ("Toward the Terra", "Superior Dominance's human order"),
    ("Star Trek: Voyager", "Automated Pralix settlement in Critical Care"): ("Star Trek: Voyager", "Dinaali medical allocation system in Critical Care"),
    ("Ixion", "Remus's Romulus population"): ("IXION", "Remus Society's Remus colony"),
    ("The Accidental Time Machine", "Matt's computer-governed future"): ("The Accidental Time Machine", "La's computer-governed future"),
    ("The Uploaded", "Living poor and uploaded ancestors"): ("The Uploaded", "Living poor and uploaded ancestors"),
}

# Article anchors and accessible full texts establish the first research batches.
PRIORITY = [
    ("The Culture", "Culture civilian habitats and ships"),
    ("The Machine Stops", "Humanity under the Machine before collapse"),
    ("Manna", "United States automated welfare compounds"),
    ("Manna", "Australia Project"),
    ("WALL-E", "Axiom passengers under Buy n Large and AUTO"),
    ("Star Trek", "United Federation of Planets core worlds"),
    ("The Evitable Conflict", "Earth under the Machines"),
    ("Noon Universe", "Earth of the Noon Universe"),
    ("Brave New World", "World State"),
    ("Nineteen Eighty-Four", "Oceania"),
    ("The Midas Plague", "Compulsory-consumption society"),
    ("The Time Machine", "Eloi and Morlock social order"),
    ("The Futurological Congress", "Chemically managed future Earth"),
    ("Psycho-Pass", "Japan under the Sibyl System"),
    ("Detroit: Become Human", "United States before the android revolution"),
    ("Detroit: Become Human", "Android autonomy after peaceful liberation"),
    ("Fallout", "Prewar United States automation economy"),
    ("Fallout 4", "The Institute"),
    ("Cyberpunk 2077", "Night City's corporate automation economy"),
    ("Her", "Human service economy before the AIs depart"),
]

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    rows, discarded, by_key = [], [], {}
    for path in sorted(DISCOVERY.glob("*.tsv")):
        with path.open(encoding="utf-8") as fh:
            for line, row in enumerate(csv.DictReader(fh, delimiter="\t"), 2):
                original = (row["work"], row["society"])
                reason = None
                if original[0] in DROP_WORKS and original not in KEEP_EXCEPTIONS:
                    reason = "Weak, redundant, or incorrectly recalled discovery lead; not admitted to frozen queue."
                if original[1] in DROP_SOCIETIES or "as comparison case" in original[1] or "as exclusion control" in original[1]:
                    reason = "Insufficiently distinct or relevant discovery lead; not admitted to frozen queue."
                if reason:
                    discarded.append({"work": original[0], "society": original[1], "reason": reason})
                    continue
                work, society = CORRECTIONS.get(original, original)
                media = sorted(set("tv" if m == "v" else m for m in row["media"].split(",")))
                key = (work.casefold(), society.casefold())
                if key in by_key:
                    by_key[key]["media"] = sorted(set(by_key[key]["media"]) | set(media))
                    by_key[key]["discovery_locations"].append(f"{path.name}:{line}")
                    continue
                item = {"work": work, "society": society, "media": media,
                        "discovery_locations": [f"{path.name}:{line}"]}
                by_key[key] = item
                rows.append(item)

    # Add a core boundary case explicitly requested in the supplied article.
    rows.append({"work": "Dune", "society": "Imperium after the Butlerian Jihad",
                 "media": ["book", "movie", "tv"], "discovery_locations": ["статья.txt"]})
    priority_index = {p: i for i, p in enumerate(PRIORITY)}
    rows.sort(key=lambda r: priority_index.get((r["work"], r["society"]), len(PRIORITY)))

    manifest_path = DATA / "candidates.json"
    existing = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"candidates": []}
    old = {(r["work"], r["society"]): r for r in existing["candidates"]}
    if old:
        # A frozen queue can only be appended; never silently reorder or renumber it.
        missing = set(old) - {(r["work"], r["society"]) for r in rows}
        if missing:
            raise ValueError(f"Frozen candidates removed from inputs: {missing}")
        final = list(existing["candidates"])
        for r in rows:
            if (r["work"], r["society"]) not in old:
                final.append({"id": f"c{len(final)+1:04d}", "order": len(final)+1,
                              **r, "discovery_status": "pending", "metadata_verified": False})
    else:
        final = [{"id": f"c{i:04d}", "order": i, **r, "discovery_status": "pending",
                  "metadata_verified": False} for i, r in enumerate(rows, 1)]
    payload = {"schema_version": "1.0", "frozen_on": DATE,
               "scope": "Unverified research candidates, not confirmed post-work societies",
               "candidate_count": len(final), "candidates": final}
    dump(manifest_path, payload)
    dump(ROOT / "research" / "discovery" / "discarded-leads.json", discarded)
    md = ["# Frozen discovery queue", "", "These are unverified candidates. Media and scope are provisional until individual research.", ""]
    md += [f"{r['order']}. **{r['id']}** — {r['work']} ({r['society']}) — {', '.join(r['media'])}" for r in final]
    (ROOT / "research" / "candidate-list.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    print(json.dumps({"candidates": len(final), "discarded_leads": len(discarded), "sha256": digest}))

if __name__ == "__main__":
    main()
