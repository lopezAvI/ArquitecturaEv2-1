import streamlit as st
import sqlite3
import pandas as pd
import unicodedata
import difflib
from datetime import datetime
import re

# ==========================================
# MOTOR ETL (Clase Maestra)
# ==========================================
class MotorETL:
    @staticmethod
    def limpiar_texto(texto):
        if pd.isna(texto): return ""
        texto = str(texto).strip().upper()
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

    @staticmethod
    def procesar_comunas(archivo):
        # Lista completa de 346 comunas de Chile
        comunas_oficiales = [
            "ALGARROBO", "ALHUE", "ALTO BIOBIO", "ALTO DEL CARMEN", "ALTO HOSPICIO", "ANCUD", "ANDACOLLO", "ANGOL", "ANTOFAGASTA", "ANTUCO", "ARAUCO", "ARICA", "AYSEN", "BUIN", "CABILDO", "CABO DE HORNOS", "CABRERO", "CALAMA", "CALBUCO", "CALDERA", "CALERA DE TANGO", "CALLE LARGA", "CAMARONES", "CAMINA", "CANELA", "CANETE", "CARAHUE", "CARTAGENA", "CASABLANCA", "CASTRO", "CATEMU", "CAUQUENES", "CERRILLOS", "CERRO NAVIA", "CHAITEN", "CHANCO", "CHANARAL", "CHEPICA", "CHIGUAYANTE", "CHILE CHICO", "CHILLAN", "CHILLAN VIEJO", "CHIMBARONGO", "CHOLCHOL", "CHONCHI", "CISNES", "COBQUECURA", "COCHAMO", "COCHRANE", "CODEGUA", "COELEMU", "COIHUECO", "COINCO", "COLBUN", "COLCHANE", "COLINA", "COLLIPULLI", "COLTAUCO", "COMBARBALA", "CONCEPCION", "CONCHALI", "CONCON", "CONSTITUCION", "CONTULMO", "COPIAPO", "COQUIMBO", "CORONEL", "CORRAL", "COYHAIQUE", "CUNCO", "CURACAUTIN", "CURACAVI", "CURACO DE VELEZ", "CURANILAHUE", "CURARREHUE", "CUREPTO", "CURICO", "DALCAHUE", "DIEGO DE ALMAGRO", "DONIHUE", "EL BOSQUE", "EL CARMEN", "EL MONTE", "EL QUISCO", "EL TABO", "EMPEDRADO", "ERCILLA", "ESTACION CENTRAL", "FLORIDA", "FREIRE", "FREIRINA", "FRESIA", "FRUTILLAR", "FUTALEUFU", "FUTRONO", "GALVARINO", "GENERAL LAGOS", "GORBEA", "GRANEROS", "GUAITECAS", "HIJUELAS", "HUALAIHUE", "HUALANE", "HUALPEN", "HUALQUI", "HUARA", "HUASCO", "HUECHURABA", "ILLAPEL", "INDEPENDENCIA", "IQUIQUE", "ISLA DE MAIPO", "ISLA DE PASCUA", "JUAN FERNANDEZ", "LA CALERA", "LA CISTERNA", "LA CRUZ", "LA ESTRELLA", "LA FLORIDA", "LA GRANJA", "LA HIGUERA", "LA LIGUA", "LA PINTANA", "LA REINA", "LA SERENA", "LA UNION", "LAGO RANCO", "LAGO VERDE", "LAGUNA BLANCA", "LAJA", "LAMPA", "LANCO", "LAS CABRAS", "LAS CONDES", "LAUTARO", "LEBU", "LICANTEN", "LIMACHE", "LINARES", "LITUECHE", "LLANQUIHUE", "LLAY-LLAY", "LO BARNECHEA", "LO ESPEJO", "LO PRADO", "LOLOL", "LONCOCHE", "LONGAVI", "LONQUIMAY", "LOS ALAMOS", "LOS ANDES", "LOS ANGELES", "LOS LAGOS", "LOS MUERMOS", "LOS SAUCES", "LOS VILOS", "LOTA", "LUMACO", "MACHALI", "MACUL", "MAFIL", "MAIPU", "MALLOA", "MARCHIHUE", "MARIA ELENA", "MARIA PINTO", "MARIQUINA", "MAULE", "MAULLIN", "MEJILLONES", "MELIPEUCO", "MELIPILLA", "MOLINA", "MONTE PATRIA", "MOSTAZAL", "MULCHEN", "NACIMIENTO", "NANCAGUA", "NATALES", "NAVIDAD", "NEGRETE", "NINHUE", "NOGALES", "NUEVA IMPERIAL", "NUNOA", "O'HIGGINS", "OLIVAR", "OLLAGUE", "OLMUE", "OSORNO", "OVALLE", "PADRE HURTADO", "PADRE LAS CASAS", "PAIHUANO", "PAILLACO", "PAINE", "PALENA", "PALMILLA", "PANGUIPULLI", "PANQUEHUE", "PAPUDO", "PARRAL", "PEDRO AGUIRRE CERDA", "PELARCO", "PELLUHUE", "PEMUCO", "PENCAHUE", "PENCO", "PENAFLOR", "PENALOLEN", "PERALILLO", "PERQUENCO", "PETORCA", "PEUMO", "PICA", "PICHIDEGUA", "PICHILEMU", "PINTO", "PIRQUE", "PITRUFQUEN", "PLACILLA", "PORTEZUELO", "PORVENIR", "POZO ALMONTE", "PRIMAVERA", "PROVIDENCIA", "PUCHUNCAVI", "PUCON", "PUDAHUEL", "PUENTE ALTO", "PUERTO MONTT", "PUERTO OCTAY", "PUERTO VARAS", "PUMANQUE", "PUNITAQUI", "PUNTA ARENAS", "PUQUELDON", "PUREN", "PURRANQUE", "PUTAENDO", "PUTRE", "PUYEHUE", "QUEILEN", "QUELLON", "QUEMCHI", "QUILACO", "QUILICURA", "QUILLECO", "QUILLON", "QUILLOTA", "QUILPUE", "QUINCHAO", "QUINTA DE TILCOCO", "QUINTA NORMAL", "QUINTERO", "QUIRIHUE", "RANCAGUA", "RANQUIL", "RAUCO", "RECOLETA", "RENAICO", "RENCA", "RENGO", "REQUINOA", "RETIRO", "RINCONADA", "RIO BUENO", "RIO CLARO", "RIO HURTADO", "RIO IBANEZ", "RIO NEGRO", "RIO VERDE", "ROMERAL", "SAAVEDRA", "SAGRADA FAMILIA", "SALAMANCA", "SAN ANTONIO", "SAN BERNARDO", "SAN CARLOS", "SAN CLEMENTE", "SAN ESTEBAN", "SAN FABIAN", "SAN FELIPE", "SAN FERNANDO", "SAN GREGORIO", "SAN IGNACIO", "SAN JAVIER", "SAN JOAQUIN", "SAN JOSE DE MAIPO", "SAN JUAN DE LA COSTA", "SAN MIGUEL", "SAN NICOLAS", "SAN PABLO", "SAN PEDRO", "SAN PEDRO DE ATACAMA", "SAN PEDRO DE LA PAZ", "SAN RAFAEL", "SAN RAMON", "SAN ROSENDO", "SAN VICENTE", "SANTA BARBARA", "SANTA CRUZ", "SANTA JUANA", "SANTA MARIA", "SANTIAGO", "SANTO DOMINGO", "SIERRA GORDA", "TALAGANTE", "TALCA", "TALCAHUANO", "TALTAL", "TEMUCO", "TENO", "TEODORO SCHMIDT", "TIERRA AMARILLA", "TILTIL", "TIMAUKEL", "TIRUA", "TOCOPILLA", "TOLTEN", "TOME", "TORRES DEL PAINE", "TORTEL", "TRAIGUEN", "TREGUACO", "TUCAPEL", "VALDIVIA", "VALLENAR", "VALPARAISO", "VICHUQUEN", "VICTORIA", "VICUNA", "VILCUN", "VILLA ALEGRE", "VILLA ALEMANA", "VILLARRICA", "VINA DEL MAR", "VITACURA", "YERBAS BUENAS", "YUMBEL", "YUNGAY", "ZAPALLAR"
        ]
        # Leemos línea por línea para evitar errores de estructura
        lines = archivo.getvalue().decode('latin-1').splitlines()
        clean = [MotorETL.limpiar_texto(l) for l in lines if l.strip()]
        
        # Filtro difuso
        validas = []
        for c in clean:
            if c in comunas_oficiales: validas.append(c)
            else:
                sim = difflib.get_close_matches(c, comunas_oficiales, n=1, cutoff=0.8)
                if sim: validas.append(sim[0])
        return pd.DataFrame(validas, columns=['nombre_comuna']).drop_duplicates()

    @staticmethod
    def procesar_famosos(archivo):
        raw = archivo.getvalue().decode('latin-1')
        records = re.findall(r'\d+\.\s+(.*?)\s+-\s+(.*?)(?=\n\d+\.|\Z)', raw, re.DOTALL)
        data = []
        hoy = datetime.now()
        for name, date in records:
            clean_date = re.sub(r'[./_|\\]', '-', date.strip())
            dt = pd.to_datetime(clean_date, errors='coerce', dayfirst=True)
            edad, cumple = 0, 0
            if not pd.isna(dt):
                edad = hoy.year - dt.year - ((hoy.month, hoy.day) < (dt.month, dt.day))
                cumple = 1 if (hoy.month == dt.month and hoy.day == dt.day) else 0
                clean_date = dt.strftime('%d-%m-%Y')
            data.append([name.replace('\n', ' ').strip(), clean_date, edad, cumple])
        return pd.DataFrame(data, columns=['Nombre', 'Fecha_Nacimiento', 'Edad', 'Cumpleaños_Hoy'])

    @staticmethod
    def procesar_lugares(archivo):
        raw = archivo.getvalue().decode('latin-1')
        lines = [l for l in raw.splitlines() if ';' in l and 'Nombre' not in l]
        data = []
        for l in lines:
            parts = l.split(';')
            if len(parts) >= 3:
                lugar, addr, geo = parts[0], parts[1], parts[2]
                lat, lon = (geo.split(',') + ['0','0'])[:2]
                addr_parts = addr.split(',')
                pais = addr_parts[-1].strip() if len(addr_parts) > 0 else "N/A"
                ciudad = addr_parts[-2].strip() if len(addr_parts) > 1 else "N/A"
                calle = addr_parts[0].strip()
                data.append([lugar, calle, ciudad, pais, lat, lon])
        return pd.DataFrame(data, columns=['Lugar', 'Calle', 'Ciudad', 'Pais', 'Lat', 'Lon'])

# ==========================================
# INTERFAZ WEB
# ==========================================
st.set_page_config(page_title="Motor ETL", layout="wide")
st.title("Motor ETL Profesional (EVALUACIÓN 2)")

t1, t2, t3 = st.tabs(["Comunas", "Famosos", "Lugares"])

with t1:
    f1 = st.file_uploader("Sube datos2026.txt", key='u1')
    if f1 and st.button("Procesar Comunas"):
        st.dataframe(MotorETL.procesar_comunas(f1))

with t2:
    f2 = st.file_uploader("Sube DATOS2026-2.txt", key='u2')
    if f2 and st.button("Procesar Famosos"):
        st.dataframe(MotorETL.procesar_famosos(f2))

with t3:
    f3 = st.file_uploader("Sube DATOS3.TXT", key='u3')
    if f3 and st.button("Procesar Lugares"):
        res = MotorETL.procesar_lugares(f3)
        st.write("Lugares", res[['Lugar']])
        st.write("Georeferencias", res[['Lat', 'Lon']])
        st.write("Direcciones", res[['Calle', 'Ciudad', 'Pais']])