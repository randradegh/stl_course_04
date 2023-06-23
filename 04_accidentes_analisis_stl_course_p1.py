##
# Análisis de accidentes de tránsito en la CDMX. Uso de streamlit, dataframes, pandas.
##
####
## Status: revisado
## Fecha revisión: 20220517
####

##
# Utilerías del proyecto
##
from utils import *


header("9 casos de negocio con Streamlit")
st.subheader("04. Análisis de Accidentes de Tránsito en la CDMX. Parte 1.")
st.subheader("Introducción")

st.markdown("""
    El objetivo de esta aplicación es realizar un análisis sobre los accidentes de tránsito
    en las diversas alcaldías de la Ciudad de México, México, **durante el año 2020**.

    Los dos *datasets* que usaremos en esta sesión fueron extraídos de una base datos en PostgreSQL
    que se alimentó, a su vez, con datos del INEGI.


    
    Se construirá una app interactiva que permita que el usuario seleccione los 
    datos que desea analizar.

    Se mostrarán gráficos que permitan sacar algunas conclusiones acerca de las 
    diferencias en el comportamiento en cada alcaldía, además de la relación con 
    las fechas y las horas en que suceden los accidentes,
""")
st.markdown("""
    
    ### Temas a analizar
    - ¿Qué variables tiene nuestro _dataset_?
    - ¿En qué alcaldias ocurrieron más accidentes?
    - ¿Qué grupos tipos de accidentes fueron los más frecuentes?
    - ¿Cómo se distribuyeron los accidentes por fechas?
    - Otras preguntas.

    Alguna de las preguntas se responderán para cada alcaldía de manera 
    interactiva.

    ### Carga de datos y contenido del _dataset_.
    
    Cargamos los datos usando el método read_csv() de Pandas.
    #### Carga de los datos
""")


with st.echo(code_location="above"):
    df_alc_fechas = pd.read_csv('cant_alcaldias_fecha_accidentes_2020_cdmx.csv', sep = '|')

st.markdown(f"""
    Contamos con las siguientes variables o _features_
    """)

st.write(df_alc_fechas.columns)

st.markdown(f"""
    Así, trabajaremos inicialmente con datos acerca de la cantidad de los accidentes ocurridos en cada alcaldía y para cada día específico.
    
    El _dataset_ contiene {df_alc_fechas.shape[1]} columnas y {df_alc_fechas.shape[0]} filas. (Los datos se obtuvieron usando el método _shape()_)

    Aquí los primeros 5 renglones:
""")

st.write(df_alc_fechas.tail(5))

st.markdown(f"""
    Como podemos observar hay un registro (renglón) para cada evento, por lo tanto 
    es necesario agrupar los datos para su análisis y visualización.

    Para empezar, vamos a agrupar los datos por la suma de los accidentes para 
    cada alcaldía, sin importar la fecha. 
    Así, pasamos de {df_alc_fechas.shape[0]} filas a una para cada alcadía.
""")

with st.echo(code_location="above"):
    df_alc = df_alc_fechas.groupby(['alcaldia']).sum().reset_index('alcaldia').sort_values(by=['alcaldia'])
    st.write(df_alc[['alcaldia','cantidad']])

"""
Este *dataframe* lo usaremos un poco más adelante para un objeto (*widget*) de Streamlit 
que nos permitirá seleccionar una alcaldía.
"""

##
# Bar plot
##

st.write("___")

st.markdown("""
    ### Visualización de los datos

    Vamos a iniciar con un gráfico de barras para visualizar la cantidad de accidentes 
    que se tienen registrados para cada alcaldía para todo el rango de fechas del 
    _dataset_ correspondiente.
""")
with st.echo(code_location="above"):
    st.write("""
        ---
        #### Gráfico de Barras (_bar_)
    """)
    #color = 'red'
    color = '#A2D9CE'
    
    fig1 = px.bar(df_alc, x='alcaldia', y='cantidad', color = 'cantidad',
        color_continuous_scale='darkmint',
        template='gridon', 
        title="Total de Accidentes por Alcaldía"
        )
    
    fig1.update_layout(width=900,height=500)
    fig1.update_xaxes(title_text='Alcaldía')
    fig1.update_yaxes(title_text='Cantidad Total de Accidentes')
    
    fig1.update_layout({
            'font_color' : '#2C3E50',
            'plot_bgcolor': color,
            'paper_bgcolor': color,
    })
    
    # Mostramos el gráfico
    fig1

st.write("""
    Observamos que en la alcaldía **Cuauhtémoc** se dan la mayor cantidad de accidentes y en **Milpa Alta** la menor.

    Sería interesante hacer el análisis considerando la densidad de población o los translados para cada alcaldía.

    ## Análisis temporal
    Ahora analizaremos el comportamiento de los accidentes a través del tiempo.
    
    Haremos una gráfica tipo serie de tiempo de los accidentes por fecha de ocurrencia.

    Necesitamos contruir un _dataframe_ que solamente contenga la cantidad de accidentes 
    de toda la ciudad para cada fecha, así que agruparemos nuestros datos por fecha.
    
    Mostramos los 10 primeros registros de todos los accidente con la fecha del suceso.
    """)

"""
    Este *dataset* lo usaremos más adelante para visualizar todos los accidentes de la CDMX a 
    lo largo del año 2020.
"""

##
# Serie de tiempo para todas las alcaldías
##
with st.echo(code_location='above'):
    df2 = df_alc_fechas.groupby('fecha').sum().reset_index('fecha')
    st.write(df2[['fecha','cantidad']].head(10))

##
# Explicar a los alumnos la razón del reset_index
##

# Seleccionamos la alcaldía a analizar

# Lista de alcaldías

"""
#### Selección de la alcaldía a visualizar
"""
st.write("""
    Observe que al _selectbox()_  en la barra lateral le pasamos como parámetro solamente la lista de 
    las alcaldías: `df.alc.alcaldia`
""")

with st.echo(code_location='above'):

    option = st.sidebar.selectbox(
        'Seleccione la alcaldía a analizar', df_alc.alcaldia)
    
st.write("___")
color = 'black'
fig_all = px.line(df2, 
    x='fecha', 
    y="cantidad",
    #template='plotly_dark', 
    title="Total de Accidentes por Fecha, Todas las Alcaldías"
    )

fig_all.update_layout(width=900, height=500)
fig_all.update_xaxes(title_text='Fecha del Accidente')
fig_all.update_yaxes(title_text='Cantidad Total de Accidentes')
fig_all['data'][0]['line']['color']='#8E44AD'

fig_all.update_layout({
        #'color' : 'red',
        'font_color' : 'white',
        'plot_bgcolor': color,
        'paper_bgcolor': color,
})

#fig_all

##
# Gráfico de barras de accidentes por día y por alcaldía
##
##

##
# Serie de tiempo para alcaldía seleccionada
##


"""
Para la creación del gŕafico para una alcaldía específica usaremos el valor regresado por el _selectbox()_.
___
### Gráfico

Para visualizar el gráfico con los datos de la alcaldía seleccionada solamente 
    debemos pasar el valor de la opción elegida en dos líneas del código para tal efecto:

Para generar el _dataset_ adecuado:
    
`df_al_sel = df_alc_fechas[df_alc_fechas['alcaldia'] == option]`

y para generar el titulo correspondiente:

`title="Total de Accidentes por Fecha, Alcaldía " + option`
"""

color = 'black'
df_alc_sel = df_alc_fechas[df_alc_fechas['alcaldia'] == option]
df2 = df_alc_sel.groupby('fecha').sum().reset_index('fecha')
    
fig_selected = px.line(df2, 
    x='fecha', 
    y="cantidad",
    template='plotly_dark', 
    title="Total de Accidentes por Fecha, Alcaldía " + option
    )

fig_selected.update_layout(width=900, height=500)
fig_selected.update_xaxes(title_text='Fecha del Accidente')
fig_selected.update_yaxes(title_text='Cantidad Total de Accidentes')
fig_selected['data'][0]['line']['color']='#ff8f00'

fig_selected.update_layout({
        'font_color' : 'white',
        'plot_bgcolor': color,
        'paper_bgcolor': color,
})


st.write("""
    #### Series de tiempo de la CDMX y la alcaldía seleccionada
    Usamos dos columnas para colocar lado a lado la serie de tiempo correspondiente a la 
    CDMX y la de la alcaldía seleccionada, de tal manera que podamos compararlas.

    Observe que es posible generar cada una de los gráficos en un primer momento y 
    visualizarlas cuando sea necesario.

    En este caso los dos gráficos ya construídos son `fig_all` y `fig_selected`.

    *(Para este momento construir los gráficos debe ser algo rutinario)*
""")

with st.echo(code_location='above'):
    col01, col02 = st.columns(2)

    ancho = 600
    alto = 500
    with col01:
        fig_all.update_layout(width=ancho, height=alto)
        fig_all

    with col02:
            fig_selected.update_layout(width=ancho, height=alto)
            fig_selected

##
# Análisis de tipos de accidentes
##


# Análisis por tiempo
##

st.write("""
    ___
    
    #### Análisis de tipos de accidentes por mes y por alcaldía

    Los datos que se pueden obtener del INEGI son más extensos de lo que hemos visto. 

    Incluyen tambien la variable (_feature_) de tipo de accidentes, codificada por 
    un número entero, lo cual mostramos en el siguiente diccionario de Python y su 
    definición extraída de la documentación proporcionada por el INEGI:
    """)

with st.echo(code_location='above'):
    tipos_acc = {
    1: 'Colisión con vehículo automotor',
    2: 'Colisión con peatón (atropellamiento)',
    3: 'Colisión con animal',
    4: 'Colisión con objeto fijo',
    5: 'Volcadura',
    6: 'Caída de pasajero',
    7: 'Salida del camino',
    8: 'Incendio',
    9: 'Colisión con ferrocarril',
    10: 'Colisión con motocicleta',
    11: 'Colisión con ciclista',
    12: 'Otro'
    }

    st.write(tipos_acc)

st.write(
        """
        Usaremos el diccionario llamado `tipos_acc` más adelante.

        #### Descarga de los datos
        Descargamos los datos que han sido generados con PostgreSQL a partir de los 
        datos originales.
        """)

with st.echo(code_location='above'):

    
    df_tacc = pd.read_csv("mun_my_tipaccid.csv", sep='|')
    """
    #### Datos originales
    """
    st.write(df_tacc.head(5))
    st.write("""
        Usamos el método `map()` para convertir los códigos de los tipos de accidentes 
        en la descripción correspondiente.
    """)
    df_tacc = df_tacc.rename(columns={"mpio": "Alcaldía", "anio_mes": "Año Mes", "tipaccid": "Tipo de Accidente", "cantidad": "Cantidad"})
    df_tacc['Tipo de Accidente'] = df_tacc['Tipo de Accidente'].map(tipos_acc) 
    """
    #### Datos con nuevos nombres en columnas
    """
    st.write(df_tacc.head(5))


st.write("""
    Con los datos preparados ya estamos listos para avanzar en el análisis de los tipos de accidentes 
    por alcaldía.

    Plotly Express nos permite graficar varios gráficos de barras apiladas para comparar por alcaldía
    la frecuancia de los diveros tipos de accidentes, con pocas líneas de código.
""")

with st.echo(code_location='above'):
    fig = px.bar(df_tacc, x="Año Mes", y="Cantidad", 
             title = "Tipos de Accidentes por Alcaldía, 2020. Fuente: INEGI", 
             color="Tipo de Accidente", facet_col ="Alcaldía", facet_col_wrap= 4,
    width = 1200, height = 1000
)
    BGCOLOR = "#0B0B61"

    fig.update_layout({
        'plot_bgcolor': BGCOLOR,
        'paper_bgcolor': BGCOLOR,
        'font_family':"Cantarell",
        'font_size': 14,
        'font_color' :"white",
        'title_font_family':"Cantarell",
        'title_font_color':"#0174DF",
        'legend_title_font_color':"white"    
    })

    fig

"""
___
"""

#footer("Copyrigth © 2022, RAF")