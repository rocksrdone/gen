import json
names=["María Marcelina Samarrón Pedregón","Jesús Estrada Domínguez","Cosme Samarrón","María Eulogia Pedregón de la Cruz","Jesús Estrada","María Eulogia Domínguez Villa","José Candelario de Jesús Estrada Domínguez","José Vicente Isac de Jesús Estrada Domínguez","José Miguel Antonio de Jesús Estrada Domínguez","Genoveva Estrada Samarrón","J. Asención Estrada Samarrón","Lauro Estrada Samarrón","Eduvigis Estrada Samarrón","Merced Estrada Samarrón","Pedro Estrada Samarrón","Miguel Estrada Samarrón","Concepción Estrada Samarrón","Jesús Estrada Samarrón","Rosario Estrada Samarrón","Salomé Zamarrón Pedregón","María Encarnación Samarrón de la Cruz","José Bernardo de Jesús Samarrón Pedregón","Primo García","Loreto Hernández Pérez","Juan García","Petra Tena","Feliciana Ruiz","Reyes Madrid","Lucinda Rascón","Cruz Uribe Chávez"]
n=len(names); ids=list(range(1,n+1))
sex=list("FMMFMFMMMF?MFFMM?MFMFMMMMFFMFF")
born=["1875 (bapt. 26 Apr) or 1873","about 1868–1876","","","","","19 Jan 1869","26 May 1859","bapt. 16 Jul 1850","about 1890","bapt. 1 Jan 1896","about 1899–1900","about 1903–1904","about 1904","bapt. 16 Jun 1905","bapt. 3 Dec 1909","12 Sep 1914","about 1916–1919","about 1911–1917","about 1868","bapt. 27 Mar 1877","bapt. 10 Jul 1882","about 1882","","","","about 1915","","about 1916","about 1888–1898"]
died=["after Jan 1945, before 1980","after Jan 1945, before 1980","before Oct 1914","before Oct 1914","after Oct 1914","before Oct 1914","","","","registered 2 Feb 1940","","7 Jan 1945","Aug 1980","","","","","","","26 Jan 1953","","about 1950"]+[""]*8
status=["Proven"]*6+["Hypothesis","Hypothesis","Proven","Proven","Probable"]+["Proven"]*10+["Probable"]+["Proven"]*7+["Not this family"]
bc=[""]*n; bc[0]="CONFLICT: ages imply 1881 – 1886"; bc[11]="OK: born May 1899 – Jan 1900 (2 ages agree)"
People=dict(id=ids,Name=names,Sex=sex,Born=born,Died=died,Status=status,Line=["Samarrón"]*n,FS_ID=["9X9N-8HK"]+[""]*(n-1),Birth_Place=[1]+[0]*(n-1),Death_Place=[0]*11+[5]+[0]*(n-12),Notes=["Also recorded as Zamarrón, Pedregón, Figueroa."]+[""]*(n-1),Birth_Check=bc,Dead_Ends=[19,19]+[0]*(n-2),Ancestry_Review=[""]*n)
P=[2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,3,4,3,3,4,4,3,4,5,6,5,5,5,6,6,6,2,23,24,25,15,16,28,18,2]
Rr=[10,11,12,13,14,15,16,17,18,19,10,11,12,13,14,15,16,17,18,19,1,1,20,21,20,21,22,22,2,2,7,8,9,7,8,9,1,10,13,14,26,27,19,29,7]
rel=["Parent of"]*36+["Spouse of"]*8+["Sibling of"]
conf=["Proven"]*26+["Probable","Probable"]+["Proven"]*16+["Possible"]
Relationships=dict(id=list(range(1,46)),Person=P,Related=Rr,Relation=rel,Confidence=conf,Notes=[""]*45)
ev_p=[2,2,2,1,1,1,1,10,12,12,12,12,12,16,16,16,13,13,13,14,19,19,17,17,18,18,20,20]
ev_s=[1,4,10,1,1,4,10,5,4,10,10,10,10,4,40,10,7,8,57,9,4,11,4,1,4,41,38,38]
fact=["Age","Age","Alive on date","Age","Parents","Age","Alive on date","Age","Age","Age","Death","Marital status","Occupation","Age","Age","Age","Age","Age","Age","Age","Age","Age","Age","Birth","Age","Age","Age","Parents"]
aw=["originario de Guerrero, 38 años, agricultor","Jesús Estrada, 62","Sobreviven al finado: sus Padres","originaria de este lugar, 28 años","los finados Cosme Samarrón y Eulogia Pedegón","Marselina Samarrón, 48","Sobreviven al finado: sus Padres","célibe, edad dieciocho años","Lauro, 30","45 años","Barrio Allende","soltero","agricultor","Miguel, 22","26","informante, hermano, 35","17","35","76","19","Rosario, 19","26","Concepción, 16","nació el 12 de septiembre","Jesús, 14","25","85","Cosme Zamarrón y Eulogia Pedregón"]
rd=[-1743033600,-1250726400,-788313600,-1743033600,-1743033600,-1250726400,-788313600,-1924473600,-1250726400,-788400000,-788400000,-788400000,-788400000,-1250726400,-955843200,-788313600,-1519948800,-968457600,335577600,-1471910400,-1250726400,-843696000,-1250726400,-1743033600,-1250726400,-804038400,-534297600,-534297600]
age=[38,62,None,28,None,48,None,18,30,45,None,None,None,22,26,35,17,35,76,19,19,26,16,None,14,25,85,None]
bf=[-2973628800,-3238704000,None,-2658009600,None,-2796854400,None,-2523916800,-2228860800,-2239920000,None,None,None,-1976486400,-1807747200,-1924300800,-2087942400,-2104444800,-2094336000,-2102976000,-1881792000,-1695600000,-1787097600,None,-1724025600,-1624492800,-3248121600,None]
bt=[-2942092800,-3207168000,None,-2626560000,None,-2765404800,None,-2492467200,-2197411200,-2208470400,None,None,None,-1944950400,-1776297600,-1892851200,-2056406400,-2072908800,-2062800000,-2071440000,-1850342400,-1664150400,-1755648000,None,-1692489600,-1593043200,-3216672000,None]
Evidence=dict(id=list(range(1,29)),Person=ev_p,Source=ev_s,Fact=fact,As_Written=aw,Record_Date=rd,Age=age,Info_Type=["Secondary"]*28,Place=[5]*28,Notes=[""]*28,Born_From=bf,Born_To=bt)
codes=[f"S{i}" for i in range(1,62) if i!=39]
Sources=dict(id=list(range(1,61)),Code=codes,Label=[c+" – Record title" for c in codes],Record_URL=["https://example.org/"+c for c in codes],Image_URL=[""]*60)
fx=dict(People=People,Relationships=Relationships,Evidence=Evidence,Sources=Sources,
 Names=dict(id=[1,2,3],Person=[1,1,1],Name_As_Written=["Marcelina Zamarrón","Marcelina Figueroa","Lenora M Figueroa"],Source=[10,17,35],Notes=["","","Ancestry tree name; wrong (D2)"]),
 Places=dict(id=[1,2,3,5],Name=["Yepómera","Temósachi","San Buenaventura","Ignacio Zaragoza"]),
 Searches=dict(id=[1,2,3],People=[["L",2,1],["L",12],["L",12]],Looking_For=["Jesús Estrada × Marcelina","Lauro Estrada grave / headstone photo","Lauro Estrada grave / headstone photo"],Register=["Temósachi civil marriages","Find a Grave","BillionGraves"],Site=["FamilySearch","Find a Grave","BillionGraves"],Result=["Not found","No results online","No results online"],Next_Try=["","Needs in-person / paid access","Needs in-person / paid access"],Years=["1888–1890","1945–1945","1945–1945"],Dead_End=[True,True,True],Date_Searched=[1791504000,1791590400,1791590400]),
 Ancestry_Sync=dict(id=[1,2],Person=[1,12],Ancestry_Title=["Name","Name"],Ancestry_Says=["Lenora M Figueroa","Loreto Estrada"],Status=["Conflict – review","Fully extracted"],Checklist=["0/5","5/5"],Open_Fix=[True,False],Item_Type=["Profile name","Profile name"]),
 Conclusions=dict(id=[1,2,10],Code=["D1","D2","D10"],Title=["Cruz Uribe is not Marcelina's mother.","Her name is Marcelina, not \"Lenora.\"","The 1873 vs 1875 baptism."],Strength=["Proven","Proven","Unresolved"],People=[["L",1,30],["L",1],["L",1]]),
 ToDo=dict(id=[1],Question=["1873 or 1875 baptism: which is Marcelina?"],Priority=["Medium"],Status=["Open"],Next_Step=["Look for a burial of the 1873 child."],People=[["L",1]]),
 Stories=dict(id=[1],Story=["Family remembers her name as Genoveva."],Told_By=["Family"],Verified=["Contradicted"],Notes=[""],People=[["L",1,10]]),
 DNA_Clusters=dict(id=[1,2,3],Name=["Estrada × Samarrón","Samarrón × Pedregón","Estrada × Domínguez"],Color=["Blue","Green","Orange"]),
 DNA_Kits=dict(id=[1],Tester=["My kit"]),
 DNA_Matches=dict(id=[1,2,3],Match_Name=["Ana R.","Luis E.","M. Torres"],Shared_cM=[212.0,88.5,41.0],Segments=[9,5,3],Longest_cM=[48.0,30.1,19.0],Side=["Paternal","Paternal","Unknown"],Cluster=[1,1,0],Status=["Reviewing","New","New"],Common_Ancestor=[2,0,0],Ancestry_Predicted=["2nd–3rd cousin","","" ],Tree=["Public linked","",""],Tree_Size=[120,None,None],Match_URL=["","",""]),
 DNA_Shared=dict(id=[1],Match_A=[1],Match_B=[2],Shared_cM=[35.0]))
json.dump(fx,open('/home/claude/genealogy-widgets/test/fixture.json','w'),ensure_ascii=False)
print("ok")
