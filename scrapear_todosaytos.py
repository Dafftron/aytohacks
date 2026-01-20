import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Lista de municipios de Toledo
municipios = [
    'ajofrin', 'alameda-de-la-sagra', 'albarreal-de-tajo', 'alcabon', 'alcanizo',
    'alcaudete-de-la-jara', 'alcolea-de-tajo', 'aldea-en-cabo', 'aldeanueva-de-barbarroya',
    'aldeanueva-de-san-bartolome', 'almendral-de-la-canada', 'almonacid-de-toledo',
    'almorox', 'anover-de-tajo', 'arcicollar', 'arges', 'azutan', 'barcience', 'bargas',
    'belvis-de-la-jara', 'borox', 'buenaventura', 'burguillos-de-toledo', 'burujon',
    'cabanas-de-la-sagra', 'cabanas-de-yepes', 'cabezamesada', 'calera-y-chozas',
    'caleruela', 'calzada-de-oropesa', 'camarena', 'camarenilla', 'campillo-de-la-jara',
    'camunas', 'cardiel-de-los-montes', 'carmena', 'carpio-de-tajo', 'carranque',
    'carriches', 'casar-de-escalona', 'casarrubios-del-monte', 'casasbuenas',
    'castillo-de-bayuela', 'cazalegas', 'cebolla', 'cedillo-del-condado', 'los-cerralbos',
    'cervera-de-los-montes', 'chozas-de-canales', 'chueca', 'ciruelos', 'cobeja',
    'cobisa', 'consuegra', 'corral-de-almaguer', 'cuerva', 'domingo-perez', 'dosbarrios',
    'erustes', 'escalona', 'escalonilla', 'espinoso-del-rey', 'esquivias', 'la-estrella',
    'fuensalida', 'galvez', 'garciotum', 'gerindote', 'guadamur', 'la-guardia',
    'las-herencias', 'herreruela-de-oropesa', 'hinojosa-de-san-vicente', 'hontanar',
    'hormigos', 'huecas', 'huerta-de-valdecarabanos', 'la-iglesuela', 'illescas',
    'lagartera', 'layos', 'lillo', 'lominchar', 'lucillos', 'madridejos', 'magan',
    'malpica-de-tajo', 'manzaneque', 'maqueda', 'marjaliza', 'marrupe', 'mascaraque',
    'la-mata', 'mazarambroz', 'mejorada', 'menasalbas', 'mentrida', 'mesegar-de-tajo',
    'miguel-esteban', 'mocejon', 'mohedas-de-la-jara', 'montearagon', 'montesclaros',
    'mora', 'nambroca', 'nava-de-ricomalillo', 'navahermosa', 'navalcan', 'navalmoralejo',
    'los-navalmorales', 'los-navalucillos', 'navamorcuende', 'noblejas', 'noez', 'nombela',
    'noves', 'numancia-de-la-sagra', 'nuno-gomez', 'ocana', 'olias-del-rey', 'ontigola',
    'orgaz', 'oropesa', 'otero', 'palomeque', 'pantoja', 'paredes-de-escalona',
    'parrillas', 'pelahustan', 'pepino', 'polan', 'portillo-de-toledo',
    'la-puebla-de-almoradiel', 'la-puebla-de-montalban', 'la-pueblanueva',
    'el-puente-del-arzobispo', 'puerto-de-san-vicente', 'pulgar', 'quero',
    'quintanar-de-la-orden', 'quismondo', 'el-real-de-san-vicente', 'recas',
    'retamoso-de-la-jara', 'rielves', 'robledo-del-mazo', 'el-romeral',
    'san-bartolome-de-las-abiertas', 'san-martin-de-montalban', 'san-martin-de-pusa',
    'san-pablo-de-los-montes', 'san-roman-de-los-montes', 'santa-ana-de-pusa',
    'santa-cruz-de-la-zarza', 'santa-cruz-del-retamar', 'santa-olalla',
    'santo-domingo-caudilla', 'sartajada', 'segurilla', 'sesena', 'sevilleja-de-la-jara',
    'sonseca', 'sotillo-de-las-palomas', 'talavera-de-la-reina', 'tembleque', 'el-toboso',
    'toledo', 'torralba-de-oropesa', 'la-torre-de-esteban-hambran', 'torrecilla-de-la-jara',
    'el-torrico', 'torrijos', 'totanes', 'turleque', 'ugena', 'urda', 'valdeverdeja',
    'valmojado', 'velada', 'las-ventas-con-pena-aguilera', 'las-ventas-de-retamosa',
    'las-ventas-de-san-julian', 'la-villa-de-don-fadrique', 'villacanas',
    'villafranca-de-los-caballeros', 'villaluenga-de-la-sagra', 'villamiel-de-toledo',
    'villaminaya', 'villamuelas', 'villanueva-de-alcardete', 'villanueva-de-bogas',
    'villarejo-de-montalban', 'villarrubia-de-santiago', 'villaseca-de-la-sagra',
    'villasequilla', 'villatobas', 'el-viso-de-san-juan', 'los-yebenes', 'yeles',
    'yepes', 'yuncler', 'yunclillos', 'yuncos'
]

base_url = 'https://www.todoslosayuntamientos.es/castilla-la-mancha/toledo/'
resultados = []

print(f'Scrapeando {len(municipios)} municipios de todoslosayuntamientos.es...')

for i, muni in enumerate(municipios):
    try:
        url = base_url + muni + '/'
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar emails en la página
            texto = soup.get_text()
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
            emails = list(set([e.lower() for e in emails if 'todoslosayuntamientos' not in e and 'info@' not in e[:5]]))

            # Buscar nombre oficial
            nombre = muni.replace('-', ' ').title()
            h1 = soup.find('h1')
            if h1:
                nombre = h1.get_text().strip()
                nombre = re.sub(r'^Ayuntamiento de ', '', nombre, flags=re.IGNORECASE)

            resultados.append({
                'NOMBRE_URL': muni,
                'NOMBRE': nombre,
                'Email_TodosAyto': emails[0] if emails else '',
                'Email_TodosAyto_2': emails[1] if len(emails) > 1 else ''
            })

            print(f'[{i+1}/{len(municipios)}] {nombre}: {emails}')
        else:
            print(f'[{i+1}/{len(municipios)}] {muni}: Error {response.status_code}')
            resultados.append({'NOMBRE_URL': muni, 'NOMBRE': muni, 'Email_TodosAyto': '', 'Email_TodosAyto_2': ''})

        time.sleep(0.5)  # Pausa para no saturar

    except Exception as e:
        print(f'[{i+1}/{len(municipios)}] {muni}: Error - {str(e)}')
        resultados.append({'NOMBRE_URL': muni, 'NOMBRE': muni, 'Email_TodosAyto': '', 'Email_TodosAyto_2': ''})

# Guardar resultados
df = pd.DataFrame(resultados)
df.to_excel('C:/aytohacks/Toledo_TodosAytos.xlsx', index=False)
print(f'\nCompletado: {len(df)} municipios guardados en Toledo_TodosAytos.xlsx')
print(f'Con email: {len(df[df["Email_TodosAyto"] != ""])}')
