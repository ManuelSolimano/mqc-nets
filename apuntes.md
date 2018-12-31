
# Apuntes

## Lecturas
1. [Padovani et al. (2017) Active galactic nuclei: What's in a name?](http://adsabs.harvard.edu/abs/arXiv:1707.07134)
2. [Hickox and Alexander (2018) Obscured active galactic nueclei (review) ](https://ui.adsabs.harvard.edu/#abs/arXiv:1806.04680)
3. [Yeche et al. (2010) Artificial neural networks for quasar selection and photometric redshift determination](http://adsabs.harvard.edu/abs/2010A%26A...523A..14Y)
4. [Pasquet-Itam and Pasquet (2018) Deep learning approach for classifying, detecting and predicting photometric redshifts of quasars in the Sloan Digital Sky Survey stripe 82](http://adsabs.harvard.edu/abs/2017arXiv171202777P)
5. [Busca and Balland (2018) QuasarNET: Human-level spectral classification and redshifting with Deep Neural Networks](https://arxiv.org/abs/1808.09955)
6. [Domingos, P (2012) A few useful things to know about machine learning ](https://dl.acm.org/citation.cfm?id=234775)
7. [Nielsen M. (2015) Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com)

## Glosario

* __AGN__: Núcleo galáctico activo. Región central de una galaxia que emite grandes cantidades de radiación producto de la acreción de materia hacia un agujero negro supermasivo.
* __Cuásar__: Originalmente "fuentes de radio casi-estelares" son AGN muy brillantes que se observan como fuentes puntuales en el cielo. Pueden observarse en redshifts muy altos (hasta la fecha $z \sim 7.1$). Ya no se requiere detección en radio para clasificarlos como cuásares.
* __SED__: energía versus frecuencia o longitud de onda.
* __QLF__: Función de luminosidad de cuásares. Distribución de densidad de cuásares por volumen co-móvil en el universo como función de su luminosidad intrínseca y su redshift.
* __PSD__: densidad de poder espectral, definida como la amplitud al cuadrado del flujo, es una medida del la variabilidad de una fuente.
* __PLO__: Point-like objects. Pueden ser estrellas o cuásares distantes.
* __IGM__: Medio intergaláctico.
* __BAO__: Oscilaciones acústicas bariónicas. Son fluctuaciones en la densidad de materia bariónica visible en el universo causadas por ondas acústicas en el plasma primordial del universo temprano (antes de la época de recombinación).
* __ Neurona sigmoidal__: Función que recibe N variables continuas $x_j$ y retorna el valor dado por $\sigma{\sum{j}^N{w_j x_j} + b}$, donde los $w_j$ son los pesos, $b$ es el "bias" de la neurona y $\sigma$ es la función sigmoidal.
* __MLP__: Multilayer Perceptron. Es una red de neuronas sigmoidales dispuestas en capas. Los valores de salida de las neuronas de una capa sirven de entrada para las neuronas de la capa siguiente. 

### Active Galactic Nuclei: what's in a name?
Este artículo presenta una revisión del estado del arte (hasta el 2017) del entendimiento de los AGN desde el punto de vista observacional en todas las frecuencias del espectro electromagnético.

Los AGN emiten más radiación que los núcleos de galaxias normales. Este componente extra no está relacionado con la fusión nuclear de las estrellas, sino a la presencia de un agujero negro supermasivo ($\geq 10^6 M_\odot$) que "acreta" el gas circundante.

Se mencionan las principales propiedades observables de los AGN:
1. Luminosidades muy altas, pueden ser detectados hasta redshift muy altos.
2. Las regiones emisoras son pequeñas en la mayoría de las bandas (del orden de miliparsecs), como se infiere de su rápida variabilidad.
3. Fuerte evolución de su función de luminosidad.
4. Emisión detectable en todo el EM.

Existen una gran variedad de clasificaciones fenomenológicas de AGN. En el artículo se listan casi 50 tipos distintos de objetos. Sin embargo, se espera que las diferencias entre estas clasificaciones responda a cambios en un número pequeño de parámetros, como la orientación, la tasa de acreción, la presencia de jets y posiblemente el ambiente de la galaxia huésped. Por eso un modelo unificado sería útil para entender la física de los AGN y el rol que juegan en la evolución de galaxias.

En seguida se explora el cuadro observacional que presentan los AGN seleccionados en cada una de las zonas del espectro: radio, infrarrojo, óptico/UV, rayos X y rayos gamma. Además, se consideran los AGN seleccionados por su variabilidad. Para efectos de este trabajo nos interesa principalmente la banda óptica.

#### AGN seleccionados en el óptico/ultravioleta
Los sondeos ópticos son capaces de identificar  cuantitativamente más AGNs que en otras longitudes de onda, pero usualmente están sesgados hacia fuentes brillantes  y no oscurecidas (cuásares). A pesar de ese sesgo, el contenido de información en las fuentes ópticas que sí son identificadas es muy alto.

La fotometría de banda ancha es sensible a la presencia de lineas de emisión anchas en varios filtros como función del redshift ya que alteran los colores típicos de un AGN y los separan del locus estelar (en diagramas color-color). La fotometría de banda angosta por otro lado, permite usar características espectrales no solo para identificar AGN sino también para estimar su redshift. Pero la espectroscopía óptica es la que tiene la última palabra tanto para confirmar que se trate de un AGN como para determinar su redshift.

Un problema de la banda óptica comparada com los rayos X duros es que las fuentes ópticas brillantes no son necesariamente AGN. Hay mucha contaminación estelar. Es más, ya que los cuasáres luminosos son fuentes puntuales pero están superados en núpero por las estrellas de nuestra galaxia es muy difícil crear una muestra  completa de cuásares a ciertos redshit. Es decir, existen "agujeros" en rangos de redshift que están muy contaminados por las estrellas.

En cuanto a los AGN  de baja luminosidad, son un desafío para los sondeos fotométricos ópticos (como DES o LSST) ya que sin espectroscopía es muy difícil distingir una galaxia normal de una activa. Además estudiar la variabilidad puede no ser de mucha ayuda para tales fuentes considerando que, mientras la amplitud de la variabilidad aumenta a menores luminosida de, la emisión óptica del motor central disminuye.

Como se menciona más arriba, el contenido de información en el continuo óptico, las lineas de emisión y las líneas de absorción es muy alto. Por ejemplo, el estudio de AGNs con líneas anchas de absorción ha evidenciado la presencia de vientos de material con velocidades de decenas de kilómetros por segundo. Además, la espectroscopía óptica provee información adicional para estimar las masas de los agujeros negros que dan poder a los cuásares.

Por último las observaciones en el óptico permiten estimar la QLF (función de luminosidad de cuásares). La mejor estimación que existe actualmente proviene de los datos del SDSS, que sabemos está sesgada hacia el lado luminoso de la distribución de AGNs. Conocer la QLF tiene importancia en cosmología ya que daría información sobre la reionización del universo temprano.

#### AGN seleccionados por variabilidad
La variabilidad de la radiación en todas las frecuencias ha sido reconocida como una de las características principales de los AGN. Por lo tanto sirve como herramienta diagnóstica.

La variabilidad del flujo es errática, aperiódica y se extiende en un rango extenso de escalas temporales (de minutos a años).
La densidad de poder espectral (PSD) depende fuertemente de la banda de frecuencias.Por ejemplo, en rayos X la variabilidad observada es mucho más rápida que en el óptico. La escala de tiempos mínima medida en una banda dada provee una  estimación de l tamaño del componente de la fuente que está emitiendo en esa banda. Por eso se deduce que la emisión en rayos X proviene de la zona interior del disco de acreción mientras que la emisión en el óptico proviene de zonas más externas. 

El estudio de la variabilidad en el óptico/UV es difícil debido a que el muestreo de las observaciones terrestres es escaso e irregular. Sin embargo, el uso de datos de observatorios espaciales (como Kepler y Swift) ha permitido estudios más detallados. Uno de los descubrimientos más importantes en el entendimiento de la variabilidad óptica fue la detección de desfases entre longitudes de onda más largas respecto a las más cortas en escalas de tiempo de días o menores. La explicación actual considera un reprocesamiento de los rayos X en el disco.

A pesar de que los rayos X sean los más adecuados para identificar AGN de acuerdo a su variabilidad, algunos sondeos ópticos como el ZTF o el LSST sondearán las fuentes variables en áreas mucho mayores que las que actualmente los observatorios de rayos X pueden observar.

### Artificial neural networks for quasar selection and redshift determination

La motivación de este paper se encuentra en el hecho de que la selección de cuasáres en altos redshift no solo es útil para estudiar esa población de AGNs, sino también para estudiar los absorbedores en el medio intergaláctico. En particuar se ha encontrado que los efectos de las oscilaciones acústicas barónicas (BAO) se pueden detectar en el "bosque Lyman-$\alpha$". Por eso, el objetivo de este trabajo es clasificar cuásares y PLOs en una muestra del SDSS-DR7, además de estimar sus redshift. Para ello utilizan redes neuronales artificiales usando una arquitectura de Multilayer Perceptron.

Para entrenar la primera red, se seleccionaron 30000 PLOs, es decir, objetos puntuales que se sabe que no son cuásares. La mitad de esa muestra se usó como set de entrenamiento y la otra mitad como set de testeo. Además, se usó una lista de 122818 cuásares confirmados por espectroscopía obtenidos los catálogos 2QZ, SDSS-2dF LRG, 2SLAQ y SDSS-DR7. Estos cuásares tienen redshifts en el rango $0.05 \leq z \leq 5.0$ y magnitudes $g$ in el rango $18 \leq g \leq 22$. No obstante, se realizó un corte en el redshift y se incluyeron solamente aquellos cuásares con $z > 2.2$. Luego la muestra de cuásares confirmados posee 33918 elementos, la mitad de ellos fueron usados para el entrenamiento y la otra mitad para el testeo.

Tras un análisis preliminar se determinó que las carácteristicas que se usarían para alimentar la red son los cuatro colores usuales (u-g, g-r, r-i, i-z) además de la magnitud  $g$  y los errores para las cinco bandas. Es decir, el vector de características tiene 10 dimensiones.

La arquitectura propuesta consta de cuatro capas de neuronas sigmoidales. La capa de entrada, la capa de salida y dos capas ocultas.  La capa de entrada tiene 10 neuronas mientras que la capa de salida tiene solo una neurona, cuyo output sería 0 para si el objeto no es un cuásar o 1 si el objeto sí es un cuásar. La función objetivo es la función de coste cuadrático y el algoritmo de optimización es el descenso estocástico del gradiente. Además, para reducir el "overfitting" se implementó una detención temprana de acuerdo a la función objetivo evaluada en el set de testeo. Es decir, el set de testeo fue utilizado también como set de validación.

Tras realizar una serie de pruebas para encontrar los hiper-parámetros adecuados, así como el número óptimo de neuronas ocultas, los autores entrenan la red y grafican los resultados en un histograma. En el gráfico se muestra una clara separación de poblaciones. Para separar las poblaciones se define un umbral $y_{NN}^{min}$ entre 0 y 1. También se define la "eficiencia" como la razón del número de objetos con un valor de salida de la rad mayor al umbral respecto al número total de objetos en la muestra. Entonces, con distintos valores de $y_{NN}^{min}$ se obtienen distintos valores para la eficiencia de clasificación de cuásares.Se obtuvo una eficiencia de PLOs de 99.6%, 99.2% y 98.5% para eficiencias de cuásares de 50%, 70% y 85%.

El segundo modelo, usado para la estimación de redshift fotométrico, es solo una ligera variación de la red anterior. La única diferencia está en que la neurona de salida ya no es sigmoidal sino lineal, para poder abarcar valores mayores a 1.0. Además en la muestra de entrenamiento se incluyeron más cuásares confirmados, formando un total de 95266 objetos con $z \geq 1$.

Los resultados se evaluaron estudiando los residuos $z_{NN} - z_{spec}$. A dicha curva se ajustaron tres gausianas y se encontró que la fracción de "outliers" es de solo 0.2%Además el RMS de los residuos es del orden de 0.15, lo cual indica que el método resultó bastante exitoso al menos para el rango de redshift relevante para los estudios de BAO.
 
### A few useful things to know about machine learning

Este artículo analiza algunos aspectos del machine learning que son usualmente omitidos por los libros de texto, pero que suelen ser vistos como las "artes oscuras" que se requieren para realizar una aplicación exitosa del machine learning. El autor se centra en el problema de clasificación, a pesar de que existan otros problemas que pueden ser tratados con estas técnicas.

Un clasificcador es es un sistema que recibe un vector de carácteristicas y entrega un valor discreto o clase. Mientras que un aprendiz recibe un set de entrenamiento de ejemplos  $(\mathbf{x_i}, y_i)$ donde $\mathbf{x_i}$ es el vector de características y $y_i$ es su clase correspondiente. Un aprendiz retorna un clasificador.

Todo algoritmo de aprendizaje de máquinas tiene tres componentes:
1. Representación: Es la estructura formal del clasificador diseñada de una manera que sea entendible por un computador. Un ejemplo de representación es una red neuronal.
2. Evaluación: Corresponde a la función que cuantifica la bondad del clasificador, es decir, permite discernir entre un buen y un mal clasificador. También se le llama función objetivo o de costo. 
3. Optimización: Por último, es necesario buscar entre todos los algoritmos posibles para la representación dada aquel que tenga mejor puntuación. Esto significa normalmente optimizar la función objetivo. En el contexto de redes neuronales el algoritmo de optimización usual es el descenso estocástico de gradiente.

Muchos libros están organizados respecto a las representaciones, lo que hace pensar que las otras componentes no son igualmente importantes.

#### La generalización es lo que vale
El objetivo fundamental del aprendizaje de máquinas es generalizar más allá del set de entrenamiento. Es decir, inducir información general a partir de ejemplos particulares.Por eso, es una buena práctica separar los datos disponibles en un set  de entrenamiento y uno de testeo, de manera  de poder evaluar qué tan bien opera el clasificador en datos que no ha visto antes.
Esto implica que muchas veces no es necesario encontrar el óptimo absoluto de la función objetivo, basta con óptimos locales siempre que el resultado generalice.

#### Los datos por sí solos no son suficientes
Además de los datos, en general es necesario asumir ciertas cosas o tener algún conocimiento previo sobre los datos. De acuerdo a los teoremas de "no free lunch" no hay manera de que un aprendiz se superior al azar en todas las posibles funciones a ser aprendidas. No obstante, hipótesis generales como suavidad de la función, dependencias limitadas o complejidad limitada suelen ser suficientes para que los algoritmos de aprendizaje automático funcionen bien. Este tipo de conocimiento entrega una heurística para elegir la representación adecuada, que será la que exprese dichos conocimientos con mayor naturalidad.

 
