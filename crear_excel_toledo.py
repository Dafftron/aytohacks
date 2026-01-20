import pandas as pd

# Datos de la Diputación de Toledo
datos_raw = """AJOFRÍN,925390002,administrativo@ajofrin.es,www.ajofrin.es
ALAMEDA DE LA SAGRA,925500181,alcaldia@alamedadelasagra.es,www.aytoalamedasagra.com
ALBARREAL DE TAJO,925749641,ayuntamiento@albarrealdetajo.es,albarrealdetajo.es
ALCABÓN,925779480,ayto.alcabon@gmail.com,alcabon.es
ALCAÑIZO,925431026,alcanizo@munitoledo.es,alcanizo.org
ALCAUDETE DE LA JARA,925853003,ayuntamiento@alcaudetedelajara.es,alcaudetedelajara.es
ALCOLEA DE TAJO,925436325,ayuntamiento@alcoleadetajo.es,alcoleadetajo.com
ALDEA EN CABO,925781001,pirocas@terra.es,
ALDEANUEVA DE BARBARROYA,925706074,info@aldeanuevadebarbarroya.org,aldeanuevadebarbarroya.org
ALDEANUEVA DE SAN BARTOLOMÉ,925441001,ayto.aldeanuevasanbartolome@gmail.com,aldeanovita.es
ALMENDRAL DE LA CAÑADA,925879601,info@almendraldelacanada.es,http://www.almendraldelacanada.es
ALMONACID DE TOLEDO,925314001,ayuntamiento@almonaciddetoledo.es,almonaciddetoledo.es
ALMOROX,918623002,chus@almorox.es,almorox.es
AÑOVER DE TAJO,925506003,alcaldia@anoverdetajo.es,anoverdetajo.es
ARCICÓLLAR,925350598,ayuntamiento@arcicollar.com,aytoarcicollar.es
ARGÉS,925376281,adminarges@telefonica.net,arges.es
AZUTÁN,925436434,ayuntaazutan@yahoo.es,
BARCIENCE,925760718,ayuntamiento@barcience.com,barcience.com
BARGAS,925493242,info@bargas.es,bargas.es
BELVÍS DE LA JARA,925858001,belvis-jara@local.jccm.es,belvisdelajara.org
BOROX,925528900,general@ayuntamientodeborox.com,ayuntamientodeborox.com
BUENAVENTURA,925875001,aytobuenaventura@gmail.com,aytobuenaventura.es
BURGUILLOS DE TOLEDO,925393055,ayuntamiento@burguillosdetoledo.org,burguillosdetoledo.org
BURUJÓN,925756081,burujon@burujon.es,burujon.es
CABAÑAS DE LA SAGRA,925355014,cabanas-sagra@local.jccm.es,cabanasdelasagra.com
CABAÑAS DE YEPES,925137181,cabanasyepes@gmail.com,
CABEZAMESADA,925209211,aytocabezamesada@telefonica.net,
CALERA Y CHOZAS,925846004,calera-y-chozas@local.jccm.es,caleraychozas.com
CALERUELA,925435081,caleruela@local.jccm.es,caleruela.org
CALZADA DE OROPESA LA,925435132,aytolacalzada@gmail.com,lacalzadadeoropesa.es
CAMARENA,918174019,ayto-camarena@ayto-camarena.com,ayto-camarena.com
CAMARENILLA,925359026,ayuntamiento@aytocamarenilla.org,aytocamarenilla.org
CAMPILLO DE LA JARA EL,925455501,administracion@ayto-campillo.com,
CAMUÑAS,925470161,ayuntamiento@camunas.es,camunas.es
CARDIEL DE LOS MONTES,925862525,ayuntamiento-cardiel@hotmail.com,
CARMENA,925742151,aytocarmena@outlook.es,ayuntamientocarmena.com
CARPIO DE TAJO EL,925757171,ayuntamiento@elcarpiodetajo.es,elcarpiodetajo.es
CARRANQUE,925544065,administracioncultura@carranque.es,carranque.es
CARRICHES,925880333,carriches@diputoledo.es,
CASAR DE ESCALONA EL,925863004,casaconsistorialcasar@hotmail.com,casarescalona.es
CASARRUBIOS DEL MONTE,918172007,ayuntamiento@casarrubiosdelmonte.es,casarrubiosdelmonte.es
CASASBUENAS,925370281,ay.casasbuenas@telefonica.net,
CASTILLO DE BAYUELA,925862001,info@castillodebayuela.com,
CAZALEGAS,925869002,oficinageneral@cazalegas.es,cazalegas.es
CEBOLLA,925866002,info@ayuntamientodecebolla.com,ayuntamientodecebolla.com
CEDILLO DEL CONDADO,925508011,registro@cedillodelcondado.es,cedillodelcondado.es
CERRALBOS LOS,925872061,ayuntamientocerralbos@gmail.com,
CERVERA DE LOS MONTES,925875501,ayuntcervera@hotmail.com,
CHOZAS DE CANALES,918176186,ayuntamiento@aytochozasdecanales.es,aytochozasdecanales.es
CHUECA,925390181,chueca@local.jccm.es,
CIRUELOS,925154401,aytociruelos@ciruelos.es,ciruelos.es
COBEJA,925551940,cobejaayto@outlook.com,aytocobeja.es
COBISA,925376326,secretaria@cobisa.es,cobisa.es
CONSUEGRA,925480185,info@aytoconsuegra.es,consuegra.es
CORRAL DE ALMAGUER,925190325,ayuntamiento@corraldealmaguer.es,corraldealmaguer.es
CUERVA,925424983,oficinasmunicipales@cuerva.es,www.cuerva.es
DOMINGO PÉREZ,925880239,domingoperez@diputoledo.es,
DOSBARRIOS,925137111,alcalde@dosbarrios.com,dosbarrios.com
ERUSTES,925880032,ayto.erustes@gmail.com,
ESCALONA,925780012,ayuntamiento@escalona.es,escalona.es
ESCALONILLA,925758111,ayuntamiento@escalonilla.com,
ESPINOSO DEL REY,925703601,ayuntamientoespinoso@gmail.com,espinosodelrey.es
ESQUIVIAS,925520161,esquivias@diputoledo.es,esquivias.es
ESTRELLA LA,925458119,la-estrella@local.jccm.es,
FUENSALIDA,925776013,alcaldia@fuensalida.com,fuensalida.com
GÁLVEZ,925400150,ayuntamientodegalvez@ayto-galvez.es,ayto-galvez.es
GARCIOTUM,925862401,ayuntamiento@garciotum.com,www.garciotum.com
GERINDOTE,925760901,gerindote.ayto@gmail.com,
GUADAMUR,925291301,secretario@guadamur.es,guadamur.es
GUARDIA LA,925138006,turismo@laguardiatoledo.es,laguardiatoledo.es
HERENCIAS LAS,925816909,info@lasherencias.es,lasherencias.es
HERRERUELA DE OROPESA,925435036,info@herrerueladeoropesa.org,herrerueladeoropesa.org
HINOJOSA DE SAN VICENTE,925878032,hinojosa-san-vicente@local.jccm.es,hinojosadesanvicente.com
HONTANAR,925410200,ayuntamientohontanar@gmail.com,hontanar.es
HORMIGOS,925740076,hormigosayto@gmail.com,ayuntamientohormigos.es
HUECAS,925784781,ayuntamiento@huecas.es,huecas.es
HUERTA DE VALDECARÁBANOS,925129161,huerta-valdecarabanos@local.jccm.es,
IGLESUELA DEL TIÉTAR LA,925874701,info@laiglesuela.es,www.laiglesuela.es
ILLESCAS,925511051,alcaldia@illescas.es,illescas.es
LAGARTERA,925430831,ayuntamiento@lagartera.es,lagartera.es
LAYOS,925376450,layos@diputoledo.es,layos.org
LILLO,925562321,lillo@local.jccm.es,aytodelillo.es
LOMINCHAR,925558101,lominchar@diputoledo.es,ayuntamiento-de-lominchar.es
LUCILLOS,925865002,lucillos@hotmail.es,
MADRIDEJOS,925460016,puntoinformacion@madridejos.es,madridejos.es
MAGÁN,925360305,magan@diputoledo.es,magan.es
MALPICA DE TAJO,925877211,ayuntamiento@malpicadetajo.es,malpicadetajo.es
MANZANEQUE,925344720,aytomanzaneque@telefonica.net,
MAQUEDA,925790001,alcaldia@maqueda.es,maqueda.es
MARJALIZA,925320000,aytomarjaliza@yahoo.es,
MARRUPE,925879001,aytomarrupe@gmail.com,
MASCARAQUE,925316026,ayuntamiento@mascaraque.es,mascaraque.es
MATA LA,925747450,oficina@ayuntamientolamata.es,lamata.es
MAZARAMBROZ,925397502,aytomazarambroz@aytomazarambroz.com,aytomazarambroz.es
MEJORADA,925890001,mejorada@diputoledo.es,
MENASALBAS,925407006,aytomenasalbas@menasalbas.es,menasalbas.es
MÉNTRIDA,918177002,mentrida@mentrida.es,www.mentrida.es
MESEGAR DE TAJO,925880559,ayto.mesegar@gmail.com,
MIGUEL ESTEBAN,925172361,ayuntamiento@aytomiguelesteban.es,miguelesteban.es
MOCEJÓN,925360008,secretaria@mocejon.es,mocejon.es
MOHEDAS DE LA JARA,925441801,ayuntamientomohedas@hotmail.com,
MONTEARAGÓN,925865032,montearagon@munitoledo.es,ayuntamiento-de-montearagon.es
MONTESCLAROS,925868401,montesclaros@local.jccm.es,ayuntamientodemontesclaros.com
MORA,925300025,ayto@mora.es,mora.es
NAMBROCA,925366001,ayuntamiento@nambroca.com,nambroca.com
NAVA DE RICOMALILLO LA,925444001,ayto_nava@hotmail.com,
NAVAHERMOSA,925410111,navahermosa@local.jccm.es,navahermosa.es
NAVALCÁN,925844011,ayuntamiento@navalcan.com,navalcan.com
NAVALMORALEJO,925436317,ayuntanavalmoralejo@yahoo.es,
NAVALMORALES LOS,925404181,ayuntamiento@losnavalmorales.es,www.losnavalmorales.es
NAVALUCILLOS LOS,925426381,ayuntamiento@losnavalucillos.es,losnavalucillos.es
NAVAMORCUENDE,925868001,navamorcuende@local.jccm.es,
NOBLEJAS,925140281,gestion@noblejas.es,noblejas.es
NOEZ,925374062,aytonoezics@gmail.com,
NOMBELA,925792001,nombela@local.jccm.es,nombela.es
NOVÉS,925778101,ayuntamiento@noves.es,noves.es
NUMANCIA DE LA SAGRA,925537433,registro@ayunt-numancia.es,ayuntamientonumanciadelasagra.com
NUÑO GÓMEZ,925878501,ayto.nunogomez@gmail.com,
OCAÑA,925120968,turismo@ocana.es,ocana.es
OLÍAS DEL REY,925491005,registro@aytoolias.es,oliasdelrey.es
ONTÍGOLA,925142041,alcaldia@ontigola.es,ontigola.es
ORGAZ,925317365,alcaldia@ayto-orgaz.es,ayto-orgaz.es
OROPESA,925430002,oropesa@munitoledo.es,oropesadetoledo.org
OTERO,925861632,ayuntamientootero@gmail.com,
PALOMEQUE,925508172,info@ayuntamientodepalomeque.es,www.ayuntamientopalomeque.es
PANTOJA,925554681,concejalia@ayuntamientopantoja.es,
PAREDES DE ESCALONA,925780951,aytoparedesdeescalona@yahoo.es,www.paredesdeescalona.es
PARRILLAS,925844177,ayuntamiento@parrillas.es,ayuntamientoparrillas.es
PELAHUSTÁN,925740701,pelahustan@local.jccm.es,
PEPINO,925709411,soledad@ayto-pepino.com,ayto-pepino.com
POLÁN,925370001,ayuntamiento@aytopolan.com,aytopolan.es
PORTILLO DE TOLEDO,925785121,alcaldia@portillodetoledo.es,portillodetoledo.es
PUEBLA DE ALMORADIEL LA,925178001,puebla@lapuebladealmoradiel.es,lapuebladealmoradiel.es
PUEBLA DE MONTALBÁN LA,925745858,ayuntamiento@pueblademontalban.com,pueblademontalban.com
PUEBLANUEVA LA,925860002,info@lapueblanueva.com,www.aytopueblanueva.com
PUENTE DEL ARZOBISPO EL,925436162,info@puentedelarzobispo.com,
PUERTO DE SAN VICENTE,925441740,ayuntamientopuertodesanvicente@gmail.com,
PULGAR,925292291,pulgar@local.jccm.es,www.ayuntamientopulgar.es
QUERO,926577004,ayuntamiento@quero.es,www.quero.es
QUINTANAR DE LA ORDEN,925180750,ayuntamiento@aytoquintanar.org,quintanardelaorden.es
QUISMONDO,925790203,atencionciudadano@gmail.com,
REAL DE SAN VICENTE EL,925879201,elrealdesanvicente@munitoledo.es,
RECAS,925522181,ayto@recas.es,recas.es
RETAMOSO DE LA JARA,925703168,ayto_retamoso19@hotmail.com,
RIELVES,925743471,aytorielves@yahoo.es,aytorielves.es
ROBLEDO DEL MAZO,925456701,ayuntamientorobledo@hotmail.es,http://valledelgevalo.es/
ROMERAL EL,925126000,elromeral@telefonica.net,elromeral.es
SAN BARTOLOMÉ DE LAS ABIERTAS,925704001,juanmanuel@ayun-sanbartolomedelasabiertas.es,ayun-sanbartolomedelasabiertas.com
SAN MARTÍN DE MONTALBÁN,925417003,ayuntamiento@sanmartindemontalban.com,sanmartindemontalban.com
SAN MARTÍN DE PUSA,925420153,ayuntamiento@sanmartindepusa.es,sanmartindepusa.com
SAN PABLO DE LOS MONTES,925415181,info@aytosanpablodelosmontes.es,aytosanpablodelosmontes.es
SAN ROMÁN DE LOS MONTES,925887002,info@sanromandelosmontes.com,sanromandelosmontes.org
SANTA ANA DE PUSA,925703001,aytosantaana@hotmail.com,ayuntamientosantaanadepusa.es
SANTA CRUZ DE LA ZARZA,925125181,alcaldia@santacruzdelazarza.es,santacruzdelazarza.es
SANTA CRUZ DEL RETAMAR,925794003,victor@santacruzdelretamar.es,santacruzdelretamar.es
SANTA OLALLA,925797008,ayuntamiento@santaolalla.es,santaolalla.es
SANTO DOMINGO CAUDILLA,925779005,ayuntamiento@santodomingo-caudilla.es,santodomingo-caudilla.es
SARTAJADA,925868388,ayuntamientodesartajada@hotmail.com,
SEGURILLA,925890061,ayuntamientosegurilla@hotmail.com,
SESEÑA,918957005,info@ayto-sesena.org,ayto-sesena.org
SEVILLEJA DE LA JARA,925455001,ayuntamientosevilleja@hotmail.es,
SONSECA,925380075,secretaria@sonseca.es,sonseca.es
SOTILLO DE LAS PALOMAS,925875801,aytosotillo@hotmail.com,
TALAVERA DE LA REINA,925720100,secretariaparticular@talavera.org,talavera.es
TEMBLEQUE,925145261,turismotembleque@hotmail.es,www.ayuntamientodetembleque.es
TOBOSO EL,925197077,secretaria@eltoboso.es,eltoboso.es
TOLEDO,925269700,alcaldia@toledo.es,toledo.es
TORRALBA DE OROPESA,925431001,alcaldia@torralbadeoropesa.org,torralbadeoropesa.org
TORRE DE ESTEBAN HAMBRÁN LA,925795101,oficinatorre@gmail.com,latorredestebanhambran.es
TORRECILLA DE LA JARA,925704701,aytotorrecilladelajara@hotmail.com,
TORRICO,925436351,torrico@diputoledo.es,eltorrico.com
TORRIJOS,925770801,sac@torrijos.es,torrijos.es
TOTANÉS,925400871,aytototanes@totanes.es,
TURLEQUE,925327081,info@ayuntamientoturleque.es,ayuntamiento.es/turleque
UGENA,925533063,atencionalciudadano@ugena.es,ugena.es
URDA,925472100,ayuntamiento@urda.es,urda.es
VALDEVERDEJA,925454511,ayuntamientovaldeverdeja@gmail.com,valdeverdeja.es
VALMOJADO,918170029,cultura@valmojado.com,valmojado.com
VELADA,925892031,alcaldia@ayuntamientovelada.es,
VENTAS CON PEÑA AGUILERA LAS,925418002,ventaspaguilera@gmail.com,
VENTAS DE RETAMOSA LAS,918173486,administracion@lasventasderetamosa.es,lasventasderetamosa.es
VENTAS DE SAN JULIÁN LAS,925431134,aytolasventas@gmail.com,
VILLA DE DON FADRIQUE LA,925195061,ayuntamiento@villadonfadrique.es,villadonfadrique.com
VILLACAÑAS,925560342,ayuntamiento@aytovillacanas.com,aytovillacanas.com
VILLAFRANCA DE LOS CABALLEROS,926558640,alcaldia@aytovillafranca.es,villafrancadeloscaballeros.es
VILLALUENGA DE LA SAGRA,925530007,ayuntamiento@villaluengadelasagra.es,villaluengadelasagra.es
VILLAMIEL DE TOLEDO,925793084,info@villamieldetoledo.com,villamieldetoledo.com
VILLAMINAYA,925345001,ayuntamiento@aytovillaminaya.es,villaminaya.es
VILLAMUELAS,925346501,villamuelas@diputoledo.es,www.villamuelas.es
VILLANUEVA DE ALCARDETE,925166525,info@villanuevadealcardete.es,villanuevadealcardete.es
VILLANUEVA DE BOGAS,925313041,ayto.vvabogas@gmail.com,
VILLAREJO DE MONTALBÁN,925420093,ayun.villarejodemon@gmail.com,
VILLARRUBIA DE SANTIAGO,925150281,secretaria@villarrubiadesantiago.es,www.villarrubiadesantiago.es
VILLASECA DE LA SAGRA,925278011,registro@villasecadelasagra.es,villasecadelasagra.es
VILLASEQUILLA,925310001,alcaldesa@aytovillasequilla.com,villasequilla.com
VILLATOBAS,925152181,apoyoalcaldia@villatobas.es,villatobas.es
VISO DE SAN JUAN EL,925559648,registro@elvisodesanjuan.es,elvisodesanjuan.es
YÉBENES LOS,925348537,turismo@losyebenes.es,www.turismo.losyebenes.es
YELES,925545002,administracion@yeles.es,www.yeles.es
YEPES,925154001,yepes@local.jccm.es,yepes.es
YUNCLER,925531001,aytoyuncler@gmail.com,aytoyuncler.com
YUNCLILLOS,925356081,yunclillos@diputoledo.es,
YUNCOS,925537990,info@yuncos.es,yuncos.es"""

# Procesar datos
filas = []
for linea in datos_raw.strip().split('\n'):
    partes = linea.split(',')
    if len(partes) >= 3:
        nombre = partes[0].strip()
        telefono = partes[1].strip()
        email = partes[2].strip()
        web = partes[3].strip() if len(partes) > 3 else ''
        if email and '@' in email:
            filas.append({
                'NOMBRE': nombre,
                'Telefono': telefono,
                'Email_1': email,
                'Web': web,
                'Provincia': 'Toledo',
                'Email_Enviado': ''
            })

df = pd.DataFrame(filas)
df.to_excel('C:/aytohacks/Toledo_Diputacion.xlsx', index=False)
print(f'Excel creado: {len(df)} ayuntamientos con email')
print(df.head(10))
