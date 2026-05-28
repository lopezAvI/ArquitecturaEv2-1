import streamlit as st
import sqlite3
import pandas as pd
import logging
import unicodedata
import difflib
#Para ejecutar localmente: streamlit run App.py en terminal
# 1. Configuración Profesional del Log
logging.basicConfig(
    filename='log_cambios_etl.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class MotorETL:
    """Clase encargada de manejar la Extracción, Transformación y Carga."""
    
    def __init__(self, db_nombre='comunas_evaluacion.db'):
        self.db_nombre = db_nombre
        
        # DICCIONARIO MAESTRO (Master Data) - Lista Oficial de Comunas
        self.comunas_oficiales = [
            "ALGARROBO", "ALHUE", "ALTO BIOBIO", "ALTO DEL CARMEN", "ALTO HOSPICIO", "ANCUD", "ANDACOLLO", "ANGOL", "ANTOFAGASTA", "ANTARTICA", "ANTUCO", "ARAUCO", "ARICA", "AYSEN",
            "BUIN", "BULNES", "CABILDO", "CABO DE HORNOS", "CABRERO", "CALAMA", "CALBUCO", "CALDERA", "CALERA", "CALERA DE TANGO", "CALLE LARGA", "CAMARONES", "CAMINA", "CANELA", "CARAHUE", "CARTAGENA", "CASABLANCA", "CASTRO", "CATEMU", "CAUQUENES", "CERRILLOS", "CERRO NAVIA", "CHAITEN", "CHANARAL", "CHANCO", "CHEPICA", "CHIGUAYANTE", "CHILE CHICO", "CHILLAN", "CHILLAN VIEJO", "CHIMBARONGO", "CHOLCHOL", "CHONCHI", "CISNES", "COBQUECURA", "COCHAMO", "COCHRANE", "CODEGUA", "COELEMU", "COIHUECO", "COINCO", "COLBUN", "COLCHANE", "COLINA", "COLLIPULLI", "COLTAUCO", "COMBARBALA", "CONCEPCION", "CONCHALI", "CONCON", "CONSTITUCION", "CONTULMO", "COPIAPO", "COQUIMBO", "CORONEL", "CORRAL", "COYHAIQUE", "CUNCO", "CURACAUTIN", "CURACAVI", "CURACO DE VELEZ", "CURANILAHUE", "CURARREHUE", "CUREPTO", "CURICO", 
            "DALCAHUE", "DIEGO DE ALMAGRO", "DONIHUE", "EL BOSQUE", "EL CARMEN", "EL MONTE", "EL QUISCO", "EL TABO", "EMPEDRADO", "ERCILLA", "ESTACION CENTRAL", "FLORIDA", "FREIRE", "FREIRINA", "FRESIA", "FRUTILLAR", "FUTALEUFU", "FUTRONO", 
            "GALVARINO", "GENERAL LAGOS", "GORBEA", "GRANEROS", "GUAITECAS", "HIJUELAS", "HUALAIHUE", "HUALANE", "HUALPEN", "HUALQUI", "HUARA", "HUASCO", "HUECHURABA", "ILLAPEL", "INDEPENDENCIA", "IQUIQUE", "ISLA DE MAIPO", "ISLA DE PASCUA", 
            "JUAN FERNANDEZ", "LA CALERA", "LA CISTERNA", "LA CRUZ", "LA ESTRELLA", "LA FLORIDA", "LA GRANJA", "LA HIGUERA", "LA LIGUA", "LA PINTANA", "LA REINA", "LA SERENA", "LA UNION", "LAGO RANCO", "LAGO VERDE", "LAGUNA BLANCA", "LAJA", "LAMPA", "LANCO", "LAS CABRAS", "LAS CONDES", "LAUTARO", "LEBU", "LICANTEN", "LIMACHE", "LINARES", "LITUECHE", "LLANQUIHUE", "LLAY LLAY", "LO BARNECHEA", "LO ESPEJO", "LO PRADO", "LOLOL", "LONCOCHE", "LONGAVI", "LONQUIMAY", "LOS ALAMOS", "LOS ANDES", "LOS ANGELES", "LOS LAGOS", "LOS MUERMOS", "LOS SAUCES", "LOS VILOS", "LOTA", "LUMACO", 
            "MACHALI", "MACUL", "MAFIL", "MAIPU", "MALLOA", "MARCHIHUE", "MARIA ELENA", "MARIA PINTO", "MARIQUINA", "MAULLIN", "MEJILLONES", "MELIPEUCO", "MELIPILLA", "MOLINA", "MONTE PATRIA", "MOSTAZAL", "MULCHEN", "NACIMIENTO", "NANCAGUA", "NATALES", "NAVIDAD", "NEGRETE", "NINHUE", "NIQUEN", "NOGALES", "NUEVA IMPERIAL", "NUNOA", "O'HIGGINS", "OLIVAR", "OLLAGUE", "OLMUE", "OSORNO", "OVALLE", 
            "PADRE HURTADO", "PADRE LAS CASAS", "PAIHUANO", "PAILLACO", "PAINE", "PALENA", "PALMILLA", "PANGUIPULLI", "PANQUEHUE", "PAPUDO", "PAREDONES", "PARRAL", "PEDRO AGUIRRE CERDA", "PELARCO", "PELLUHUE", "PEMUCO", "PENCAHUE", "PENCO", "PENALOLEN", "PERALILLO", "PERQUENCO", "PETORCA", "PEUMO", "PICA", "PICHIDEGUA", "PICHILEMU", "PINTO", "PIRQUE", "PITRUFQUEN", "PLACILLA", "PORTEZUELO", "PORVENIR", "POZO ALMONTE", "PRIMAVERA", "PROVIDENCIA", "PUCHUNCAVI", "PUCON", "PUDAHUEL", "PUENTE ALTO", "PUERTO MONTT", "PUERTO OCTAY", "PUERTO VARAS", "PUMANQUE", "PUNITAQUI", "PUNTA ARENAS", "PUQUELDON", "PUREN", "PURRANQUE", "PUTAENDO", "PUTRE", "PUYEHUE", 
            "QUEILEN", "QUELLON", "QUEMCHI", "QUILACO", "QUILICURA", "QUILLECO", "QUILLON", "QUILLOTA", "QUILPUE", "QUINCHAO", "QUINTA DE TILCOCO", "QUINTA NORMAL", "QUINTERO", "QUIRIHUE", "RANCAGUA", "RANQUIL", "RAUCO", "RECOLETA", "RENAICO", "RENCA", "RENGO", "REQUINOA", "RETIRO", "RINCONADA", "RIO BUENO", "RIO CLARO", "RIO HURTADO", "RIO IBANEZ", "RIO NEGRO", "RIO VERDE", "ROMERAL", 
            "SAAVEDRA", "SAGRADA FAMILIA", "SALAMANCA", "SAN ANTONIO", "SAN BERNARDO", "SAN CARLOS", "SAN CLEMENTE", "SAN ESTEBAN", "SAN FABIAN", "SAN FELIPE", "SAN FERNANDO", "SAN GREGORIO", "SAN IGNACIO", "SAN JAVIER", "SAN JOAQUIN", "SAN JOSE DE MAIPO", "SAN JUAN DE LA COSTA", "SAN MIGUEL", "SAN NICOLAS", "SAN PABLO", "SAN PEDRO", "SAN PEDRO DE ATACAMA", "SAN PEDRO DE LA PAZ", "SAN RAFAEL", "SAN RAMON", "SAN ROSENDO", "SAN VICENTE", "SANTA BARBARA", "SANTA CRUZ", "SANTA JUANA", "SANTA MARIA", "SANTIAGO", "SANTO DOMINGO", "SIERRA GORDA", 
            "TALAGANTE", "TALCA", "TALCAHUANO", "TALTAL", "TEMUCO", "TENO", "TEODORO SCHMIDT", "TIERRA AMARILLA", "TILTIL", "TIMAUKEL", "TIRUA", "TOCOPILLA", "TOLTEN", "TOME", "TORRES DEL PAINE", "TORTEL", "TRAIGUEN", "TREGUACO", "TUCAPEL", "VALDIVIA", "VALLENAR", "VALPARAISO", "VICHUQUEN", "VICTORIA", "VICUNA", "VILCUN", "VILLA ALEGRE", "VILLA ALEMANA", "VILLARRICA", "VINA DEL MAR", "VITACURA", "YUMBEL", "YUNGAY", "ZAPALLAR"
        ]

    def limpiar_texto(self, texto):
        if pd.isna(texto): 
            return ""
        texto = str(texto).strip().upper()
        texto_limpio = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        return texto_limpio

    def ejecutar_etl(self, archivo_subido):
        try:
            logging.info("--- INICIO DE PROCESO ETL ---")
            
            # EXTRACCIÓN (Lee directamente el archivo subido en la web)
            df = pd.read_csv(archivo_subido, header=None, names=['nombre_comuna'])
            total_leidos = len(df)
            
            # TRANSFORMACIÓN 1: Limpieza básica
            df['nombre_comuna'] = df['nombre_comuna'].apply(self.limpiar_texto)
            df = df[df['nombre_comuna'] != ""]
            
            # TRANSFORMACIÓN 2: Master Data Management
            comunas_validadas = []
            for comuna in df['nombre_comuna']:
                if comuna in self.comunas_oficiales:
                    comunas_validadas.append(comuna)
                else:
                    similares = difflib.get_close_matches(comuna, self.comunas_oficiales, n=1, cutoff=0.80)
                    if similares:
                        comunas_validadas.append(similares[0])
            
            df = pd.DataFrame(comunas_validadas, columns=['nombre_comuna'])
            
            # TRANSFORMACIÓN 3: Eliminar duplicados
            df = df.drop_duplicates(subset=['nombre_comuna'])
            df = df.sort_values(by='nombre_comuna').reset_index(drop=True)
            
            total_unicos = len(df)
            datos_descartados = total_leidos - total_unicos
            
            # CARGA (LOAD)
            conexion = sqlite3.connect(self.db_nombre)
            df.to_sql('COMUNAS_NORM', conexion, if_exists='replace', index=True, index_label='id')
            conexion.close()

            logging.info(f"Carga exitosa: {total_unicos} registros guardados.")
            logging.info("--- FIN DE PROCESO ETL ---\n")
            
            lista_limpia = df['nombre_comuna'].tolist()
            return total_leidos, total_unicos, datos_descartados, lista_limpia

        except Exception as e:
            logging.error(f"Fallo crítico en ETL: {str(e)}")
            raise e

# --- INTERFAZ WEB CON STREAMLIT ---
st.set_page_config(page_title="Panel ETL - Arquitectura", layout="wide")

st.title("Panel de Control ETL")
st.markdown("Carga el archivo `.txt` para normalizar los datos de comunas e integrarlos a la base de datos oficial.")

archivo_subido = st.file_uploader("Seleccionar Dataset (.txt)", type=["txt"])

if archivo_subido is not None:
    if st.button("Procesar Datos", type="primary"):
        with st.spinner("Ejecutando proceso ETL..."):
            try:
                etl = MotorETL()
                total_leidos, total_unicos, descartados, lista_limpia = etl.ejecutar_etl(archivo_subido)
                
                st.success("¡PROCESO COMPLETADO CON ÉXITO!")
                
                # Mostrar resumen
                col1, col2, col3 = st.columns(3)
                col1.metric("Líneas leídas", total_leidos)
                col2.metric("Datos descartados/corregidos", descartados)
                col3.metric("Comunas únicas guardadas", total_unicos)
                
                # Mostrar lista resultante
                st.subheader("DATOS LIMPIOS (COMUNAS_NORM)")
                df_mostrar = pd.DataFrame(lista_limpia, columns=["Comuna Normalizada"])
                df_mostrar.index += 1
                st.dataframe(df_mostrar, use_container_width=True)
                
                # Botón para descargar el LOG
                try:
                    with open("log_cambios_etl.txt", "rb") as log_file:
                        st.download_button(
                            label="Descargar archivo Log",
                            data=log_file,
                            file_name="log_cambios_etl.txt",
                            mime="text/plain"
                        )
                except FileNotFoundError:
                    st.warning("El archivo log aún no se ha generado correctamente.")
                    
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
