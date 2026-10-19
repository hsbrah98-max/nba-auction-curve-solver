"""GBA 2026-27 board v2: news-based. Base order Rotoworld 9-cat top 200, moved by
Oct 2026 injury/role news (ESPN + RotoWire injury pages, ESPN/RotoWire sleepers & busts).
Prices: 15-man rosters, $300, 9 or 10 teams."""
import json, math, pathlib, importlib.util
spec = importlib.util.spec_from_file_location("v1", pathlib.Path(__file__).with_name("build_sheet.py"))
src = pathlib.Path(__file__).with_name("build_sheet.py").read_text()
RANKS = src.split('RANKS = """')[1].split('"""')[0].split("|")
base = {s.rsplit(" ",1)[0]:(i+1, s.rsplit(" ",1)[1]) for i,s in enumerate(RANKS)}

# name: (new rank, tag, note). T=underpriced, buy to max. V=fair price only. A=avoid/let go. O=out, don't draft.
N = {
 "Tyrese Haliburton":(7,"T","Says he's 100% with no restrictions; Pacers optimistic for opening night. LeagueWinner lists him as undervalued."),
 "Jayson Tatum":(9,"V","Came back in March from the Achilles. Only resting in preseason. Top option with Brown gone, but not a top-5 price."),
 "Austin Reaves":(16,"T","LeBron gone, career-high usage expected (RotoWire). LeagueWinner says he goes too late."),
 "Derrick White":(20,"T","Brown gone, likely No. 2 scorer; PG misses games. Sleeper on RotoWire and Athlon."),
 "Anthony Davis":(32,"V","Missed 14+ games in 10 of 14 seasons, never played for WAS. ESPN bust."),
 "Walker Kessler":(30,"T","Primary big next to Luka. 14.4/10.8/1.8 blk on 70% in 5 games before shoulder surgery. Minor finger issue now."),
 "Donovan Clingan":(36,"T","77 games last year, 11.6 reb, 1.7 blk in 27 min. Uncontested starter, 30+ min possible."),
 "Brandon Miller":(38,"T","Usage rising with LaMelo gone; breakout pick (ESPN). Leg issue held him out Saturday, check it."),
 "Bam Adebayo":(55,"V","Giannis overlaps his role. RotoWire fade."),
 "LeBron James":(52,"A","Projects as 4th-5th option on PHI, plus rest days (ESPN bust)."),
 "Joel Embiid":(68,"A","57 of 164 games over two seasons; usage drops with Brown and LeBron. RotoWire fade."),
 "Julius Randle":(42,"T","Thin Nets roster; ESPN projects about 24/10/5."),
 "Ausar Thompson":(46,"T","LeagueWinner: drafted a round too late."),
 "Naz Reid":(50,"T","Likely starter in CHA, boards + 3s (ESPN sleeper)."),
 "Kel'el Ware":(51,"T","MIL youth movement favors him over Turner. Blocks, 3s, FT up to 74%."),
 "Matas Buzelis":(60,"V","Rolled his right ankle Friday and didn't return. Check before bidding."),
 "Kon Knueppel":(88,"V","Hamstring; GM unsure he's ready for the opener."),
 "Tyler Herro":(80,"V","RotoWire fade; shares the ball with Jaquez in MIL."),
 "De'Aaron Fox":(96,"A","Squeezed by Harper and Castle (RotoWire bust). Sore in preseason."),
 "VJ Edgecombe":(98,"A","LeBron and Brown take his touches (RotoWire bust)."),
 "Neemias Queta":(125,"A","Timeshare with Mitchell Robinson (RotoWire fade)."),
 "Zion Williamson":(108,"A","No 3s, 5.7 reb last year; ESPN doubts 50 games."),
 "Jakob Poeltl":(128,"A","ESPN bust; Murray-Boyles eats minutes."),
 "Ja Morant":(150,"A","79 games in 3 years, crowded backcourt (ESPN and RotoWire bust)."),
 "Kristaps Porzingis":(170,"O","Out indefinitely, missed camp."),
 "Nic Claxton":(130,"V","Hamstring, re-evaluated in 2 weeks. Bulls bigs all hurt."),
 "Cameron Boozer":(74,"T","Top rookie, starting as MEM's best player. 18/7/4 in Summer League."),
 "Caleb Wilson":(84,"T","No. 4 pick, starting PF. 23.5/7.3 in Summer League (ESPN sleeper)."),
 "Collin Murray-Boyles":(82,"T","Bigger role expected (RotoWire breakout)."),
 "Day'Ron Sharpe":(81,"T","Starter after the Claxton trade, double-double upside. Shoulder soreness, check it."),
 "Ajay Mitchell":(90,"T","Wiggins, Joe and Dort gone. RotoWire sleeper."),
 "Cedric Coward":(92,"T","Starting guard; 13.6 ppg in 25.8 min as a rookie (ESPN breakout)."),
 "Ace Bailey":(100,"T","18.5 ppg as a rookie; Utah's focal point (ESPN breakout)."),
 "Coby White":(104,"T","LaMelo gone, $74M deal (RotoWire sleeper). Calf strain, out for preseason."),
 "Anthony Black":(106,"T","Healthy, finished 70% at the rim (ESPN and Athlon). Full practice Friday."),
 "Scotty Pippen Jr.":(110,"T","May start at PG; assists and steals (ESPN breakout)."),
 "Jaime Jaquez Jr.":(112,"T","Could start in MIL after the Giannis trade (ESPN sleeper)."),
 "Daniel Gafford":(118,"T","Lively out indefinitely with a foot injury. Gafford starts."),
 "Dylan Harper":(86,"T","RotoWire guard breakout."),
 "Sam Merrill":(150,"V",""),
 "Brandon Ingram":(300,"O","Partially torn Achilles. Out past Nov 1."),
 "Jimmy Butler":(300,"O","Knee. Out until about January."),
 "Mark Williams":(300,"O","Torn labrum, surgery. Out until February."),
 "Jusuf Nurkic":(300,"O","Toe. Out 4+ weeks."),
 "Dereck Lively II":(300,"O","Foot. Out indefinitely."),
 "Isaiah Stewart":(300,"O","Ankle. Out at least 2 weeks."),
 "Nikola Vucevic":(185,"A","RotoWire fade."),
 "Tobias Harris":(160,"V","Calf; Spurs won't rush him."),
}
EXTRA = {"Darius Acuff Jr.":("SAC",122,"T","Rookie, expected to play 30+ minutes right away (RotoWire sleeper).")}

# Default tags for top names with no news move
DEF = {r: "T" if r<=4 else "" for r in range(1,201)}
rows=[]
for name,(r,team) in base.items():
    nr,tag,note = N.get(name,(r,"",""))
    rows.append(dict(n=name,t=team,b=r,k=nr+0.01*r/200,g=tag or ("T" if r<=3 else ""),x=note))
for name,(team,nr,tag,note) in EXTRA.items():
    rows.append(dict(n=name,t=team,b="-",k=nr,g=tag,x=note))
rows.sort(key=lambda d:d["k"])

def curve(teams):
    n=teams*15; budget=teams*300; top=88 if teams==9 else 86
    lo,hi=5,80
    for _ in range(60):
        k=(lo+hi)/2
        s=sum(1+(top-1)*math.exp(-(i)/k) for i in range(n))
        lo,hi=(k,hi) if s<budget else (lo,k)
    return [round(1+(top-1)*math.exp(-i/k)) for i in range(n)]
c9,c10=curve(9),curve(10)
i=0
for d in rows:
    if d["g"]=="O": d["p9"]=d["p10"]=0; d["r"]="OUT"; continue
    i+=1; d["r"]=i
    d["p9"]=c9[i-1] if i<=len(c9) else 0
    d["p10"]=c10[i-1] if i<=len(c10) else 0

# 10th-category nudges in dollars (DD = double-doubles, TP = 3P%)
DD={"Nikola Jokic":4,"Domantas Sabonis":5,"Josh Giddey":4,"Jalen Johnson":3,"Jalen Duren":4,"Walker Kessler":3,"Donovan Clingan":4,"Zach Edey":3,"Karl-Anthony Towns":3,"Alperen Sengun":3,"Victor Wembanyama":2,"Rudy Gobert":3,"Evan Mobley":2,"Julius Randle":3,"Day'Ron Sharpe":2,"Jarrett Allen":2,"Onyeka Okongwu":2,"Amen Thompson":2,"Giannis Antetokounmpo":3,"Luka Doncic":2,"Scottie Barnes":2,"Ivica Zubac":2,"Bam Adebayo":2,"Trae Young":2,"James Harden":2,"Cade Cunningham":2,
    "Stephen Curry":-2,"Kon Knueppel":-1,"Derrick White":-1,"Tyrese Maxey":-1}
TP={"Stephen Curry":4,"Kon Knueppel":2,"Trey Murphy III":2,"Nickeil Alexander-Walker":2,"Derrick White":2,"Desmond Bane":2,"Lauri Markkanen":2,"Karl-Anthony Towns":2,"Tyrese Haliburton":2,"Shai Gilgeous-Alexander":1,"Sam Hauser":2,"Sam Merrill":1,"Duncan Robinson":1,"Grayson Allen":1,"Michael Porter Jr.":2,"Naz Reid":1,"Norman Powell":2,
    "Josh Giddey":-2,"LaMelo Ball":-2,"Trae Young":-2,"Anthony Edwards":-1,"Ja Morant":-2,"Jalen Green":-2,"Cooper Flagg":-1,"Giannis Antetokounmpo":-1,"Amen Thompson":-1,"Scottie Barnes":-1}
for d in rows: d["dd"]=DD.get(d["n"],0); d["tp"]=TP.get(d["n"],0)
pathlib.Path(__file__).with_name("players_v2.json").write_text(json.dumps(rows))
print("sum9",sum(c9),"sum10",sum(c10),"top",c9[:5],"n",len(rows))
for d in rows[:40]: print(d["r"],d["n"],d["p9"],d["g"])
