import gmpy2 as gp 
from Crypto.Util.number import long_to_bytes
p=112983326124950989398452664020884343990593972121437521229983671256995718590173945373937152908726620186104272774050862217468375577689828068882572993388413759480203155777950051623133715095643241300457798189355964216397132132093938036862971963625738151613795858960872772697053409205870049664199243000980470815199

q=112983326124950989398468156396587292169653144740214998405502361004995318114570205727008960607043425438431014707888005510563170761169996289583551179190998821781303805366461968502933889330413468413219232917467268301027986018185379141738602424878358547239596339308379613327614666751368936584486052702226593960411
n = 12765231982257032754070342601068819788671760506321816381988340379929052646067454855779362773785313297204165444163623633335057895252608396010414744222572161530653104640020689896882490979790275711854268113058363186249545193245142912930804650114934761299016468156185416083682476142929968501395899099376750415294540156026131156551291971922076435528869024742993840057342092865203064721826362149723366381892539617642364692012936270150691803063945919154346756726869466855557344213050973081755499746750276623648407677639812809665472258655462846021403503851719008687214848550916999977775070011121527941755954255781343103086789
e = 459650454686946706615371845737527916539205656667844780634386049268800615782964920944229084502752167395446158290854047696006034750210758341744841762479191173017773034647739346927390580848998121830029134542880713409306092967282675122699586503684943407535067216738556403169403622104762516293879994387324370835718056251706150557820106296417750402984941838652433642298378976899556042987560946508887315484380807248331504458640857234708123277403252632993828101306072382329879857946191508782246793011691530554606521701055094223574951862129713872918021549814674387049788995785872980320871421550616327471735316980754238323013
c = 10992248752412909788626396175372747713079469256270100576886987393986576680666320383209810005318254336440105142571546847427454822405793626080251363454531982746373841267986148332456716023293306870382809568309620264499225135226626560298741596462262513921032733814032790312163314776421380481083058518893602887082464123177575742160690315666730642727773288362853901330620841098230284739614618790097180848133698381487679399364400048499041582830157094876815030301231505774900176910650887780842536610942820066913075027528705150102760422836458745949063992228680293226303245265232017738712226154128654682937687199768621565945171

d = gp.invert(e,(p-1)*(q-1))
print(long_to_bytes(gp.powmod(c,d,n)))