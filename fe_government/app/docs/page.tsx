import { SidebarInset } from "@/components/ui/sidebar"
import { SiteHeader } from "@/components/site-header"
import { Separator } from "@/components/ui/separator"
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@/components/ui/tabs"
import Link from "next/link"

export default function DocsPage() {
  return (
    <SidebarInset>
      <SiteHeader title="Documentación - GovernomicsCR" />
      <div className="flex flex-1 flex-col">
        <div className="@container/main flex flex-1 flex-col gap-2">
          <div className="mx-auto flex max-w-3xl flex-col gap-4 py-4 md:gap-6 md:py-6">
            {/* Header */}
            <div className="space-y-3 text-center">
              <div className="flex justify-center gap-2">
                <Badge variant="secondary">v0.1</Badge>
                <Badge>Beta</Badge>
                <Badge variant="outline">Público</Badge>
              </div>
              <h1 className="text-3xl font-bold tracking-tight">
                GovernomicsCR: IA para análisis comparativo del crecimiento
                económico por administración en Costa Rica
              </h1>
              <p className="text-muted-foreground">
                GovernomicsCR es un sistema analítico impulsado por modelos de
                lenguaje que transforma datos oficiales del Banco Central de
                Costa Rica en reportes comparativos entre administraciones
                presidenciales. El sistema integra un pipeline multiagente
                orquestado con LangGraph, un backend en FastAPI y un frontend
                en React con shadcn ui.
              </p>
            </div>

            <Separator />

            {/* Resumen (Abstract) */}
            <section id="resumen" className="space-y-4">
              <h2 className="text-xl font-semibold">Resumen del sistema</h2>
              <Card>
                <CardHeader>
                  <CardTitle>GovernomicsCR</CardTitle>
                  <CardDescription>
                    Sistema analítico basado en LLMs y datos oficiales del BCCR
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2 text-sm text-muted-foreground">
                  <p>
                    GovernomicsCR es un sistema de análisis económico diseñado
                    para examinar y comparar el crecimiento de la economía
                    costarricense a través de distintas administraciones
                    presidenciales. El sistema integra datasets estructurados,
                    un pipeline multiagente construido con LangGraph y un
                    backend en FastAPI que automatiza la generación de reportes
                    técnicos.
                  </p>
                  <p>
                    El frontend, desarrollado en React con la librería de
                    componentes shadcn ui, ofrece una interfaz tipo chat que
                    permite formular consultas en lenguaje natural, seleccionar
                    preguntas predefinidas y recibir salidas analíticas
                    estructuradas. GovernomicsCR procesa datos históricos de
                    PIB y sintetiza indicadores por oferta, demanda, régimen,
                    industrias y PIB agregado.
                  </p>
                  <p>
                    Los resultados demuestran la viabilidad de utilizar modelos
                    de lenguaje de gran escala para apoyar la monitorización
                    económica y el análisis de políticas públicas, manteniendo
                    la trazabilidad frente al baseline oficial del Banco
                    Central de Costa Rica.
                  </p>
                </CardContent>
              </Card>
            </section>

            <Separator />

            {/* Introducción */}
            <section id="introduccion" className="space-y-4">
              <h2 className="text-xl font-semibold">Introducción</h2>
              <p>
                En sectores intensivos en datos, como la banca y los seguros,
                gran parte del ciclo de información —acceso a datos
                estructurados, estandarización, preprocesamiento y
                visualización mediante dashboards— se encuentra altamente
                automatizado. Sin embargo, la interpretación técnica de esos
                datos, la redacción de informes narrativos y la respuesta a
                consultas analíticas complejas continúan siendo tareas
                predominantemente manuales.
              </p>
              <p>
                Cada vez que se actualizan las series macroeconómicas, los
                analistas deben volver a revisar gráficos, contrastar períodos,
                buscar explicaciones y redactar hallazgos. Este trabajo es
                intensivo en tiempo y depende fuertemente del criterio
                especializado de economistas, estadísticos y profesionales
                afines.
              </p>
              <p>
                GovernomicsCR se inserta precisamente en este punto del flujo:
                busca automatizar la capa analítica y narrativa, es decir, la
                parte del proceso que todavía recae casi por completo en el
                conocimiento experto humano.
              </p>
              <p>
                De cara a las elecciones presidenciales de febrero de 2026, la
                ciudadanía costarricense necesita información clara, verificable
                y objetiva sobre el desempeño económico de las últimas
                administraciones. Aunque el Banco Central de Costa Rica (BCCR)
                publica datos oficiales completos y confiables, su neutralidad
                institucional le impide ofrecer comparaciones directas entre
                gobiernos, y no existe una herramienta que automatice la
                interpretación de esa información.
              </p>
              <p>
                GovernomicsCR propone una solución que combina datos oficiales
                del BCCR con modelos de lenguaje de gran escala (LLMs) para
                generar reportes automatizados, responder preguntas económicas
                en lenguaje natural y facilitar comparaciones inter
                administrativas de forma transparente, reproducible y basada en
                evidencia.
              </p>
            </section>

            {/* Problemática */}
            <section id="problematica" className="space-y-4">
              <h2 className="text-xl font-semibold">Problemática</h2>
              <p>
                A pesar del alto grado de automatización en el manejo técnico de
                datos, persisten tres desafíos estructurales que motivan la
                creación de GovernomicsCR:
              </p>
              <ul className="list-disc space-y-2 pl-6 text-sm text-muted-foreground">
                <li>
                  <span className="font-semibold">
                    La interpretación no está automatizada.
                  </span>{" "}
                  Cada actualización de datos requiere que un analista revise
                  series, valide comportamientos, interprete causas y redacte
                  hallazgos.
                </li>
                <li>
                  <span className="font-semibold">
                    La elaboración de informes sigue siendo manual.
                  </span>{" "}
                  Los dashboards facilitan la exploración visual, pero no
                  generan automáticamente narrativas, comparaciones ni
                  explicaciones contextualizadas.
                </li>
                <li>
                  <span className="font-semibold">
                    No existe integración entre datos oficiales y chatbots
                    especializados.
                  </span>{" "}
                  Las instituciones disponen de la información, pero carecen de
                  herramientas capaces de producir respuestas precisas y
                  contextualizadas directamente desde datos estructurados.
                </li>
              </ul>
              <Alert>
                <AlertTitle>Vacío en períodos electorales</AlertTitle>
                <AlertDescription>
                  En contextos electorales, la ausencia de herramientas de
                  interpretación automatizada se traduce en debates apoyados en
                  percepciones o análisis ad hoc. GovernomicsCR busca reducir
                  esta brecha proporcionando análisis objetivos basados en la
                  data del BCCR.
                </AlertDescription>
              </Alert>
            </section>

            <Separator />

            {/* PIB y desagregaciones */}
            <section id="pib-desagregaciones" className="space-y-4">
              <h2 className="text-xl font-semibold">
                El PIB y sus desagregaciones
              </h2>
              <p className="text-sm text-muted-foreground">
                El Producto Interno Bruto (PIB) es la medida estándar de la
                producción agregada de un país y se define como el valor
                monetario de los bienes y servicios finales producidos en una
                economía durante un período determinado. En Costa Rica, el BCCR
                publica estimaciones trimestrales del PIB junto con diversas
                desagregaciones que permiten analizar la economía desde tres
                enfoques principales: oferta, demanda y régimen.
              </p>

              <h3 className="font-medium text-sm">
                Oferta: actividades económicas
              </h3>
              <p className="text-sm text-muted-foreground">
                Desde la perspectiva de la oferta, el PIB se desagrega en
                actividades económicas como Agricultura, Manufactura,
                Construcción, Comercio, Transporte, Información y
                Comunicaciones, Finanzas y Seguros, Actividades Profesionales,
                Administración Pública, Enseñanza y Salud, entre otras. A un
                nivel más agregado, estas actividades pueden agruparse en:
              </p>
              <ul className="list-disc space-y-1 pl-6 text-sm text-muted-foreground">
                <li>Sector primario: agricultura, silvicultura y pesca.</li>
                <li>
                  Sector secundario: manufactura, minas y canteras,
                  electricidad y construcción.
                </li>
                <li>Sector terciario: todas las actividades de servicios.</li>
              </ul>

              <h3 className="font-medium text-sm">
                Demanda: componentes del gasto
              </h3>
              <p className="text-sm text-muted-foreground">
                Desde la perspectiva de la demanda, la producción total Y se
                descompone en consumo de hogares, consumo del gobierno,
                inversión, exportaciones e importaciones, dando lugar a la
                identidad macroeconómica fundamental: Y = C + G + I + X − M.
                Esto permite analizar el peso de la demanda interna (C + G + I)
                y de la demanda externa (X − M) en el crecimiento.
              </p>

              <h3 className="font-medium text-sm">Régimen de comercio</h3>
              <p className="text-sm text-muted-foreground">
                Finalmente, la contabilidad nacional costarricense permite
                separar la producción en Régimen Definitivo (empresas que
                producen para el mercado local o exportan sin incentivos) y
                Régimen Especial (Zonas Francas). Dado el peso creciente del
                Régimen Especial, esta desagregación es clave para entender las
                diferencias estructurales en productividad y articulación
                internacional.
              </p>
            </section>

            <Separator />

            {/* Objetivos */}
            <section id="objetivos" className="space-y-4">
              <h2 className="text-xl font-semibold">Objetivos</h2>

              <h3 className="font-medium">Objetivo general</h3>
              <p className="text-sm text-muted-foreground">
                Desarrollar un sistema de análisis económico basado en modelos
                de lenguaje de gran escala capaz de procesar, interpretar y
                comparar el crecimiento económico costarricense entre
                administraciones gubernamentales a partir de datos oficiales del
                BCCR.
              </p>

              <h3 className="font-medium">Objetivos específicos</h3>
              <ul className="list-disc space-y-2 pl-6 text-sm text-muted-foreground">
                <li>
                  Preprocesar datos históricos oficiales del Banco Central de
                  Costa Rica en un entorno analítico que sirva como contexto
                  para los agentes del sistema.
                </li>
                <li>
                  Implementar un backend inteligente que combine modelos de
                  lenguaje con LangChain y LangGraph, permitiendo la interacción
                  conversacional con los datos y consultas analíticas
                  avanzadas.
                </li>
                <li>
                  Diseñar una interfaz gráfica que facilite la interacción con
                  el agente analítico y simplifique el acceso a la información
                  económica.
                </li>
              </ul>
            </section>

            <Separator />

            {/* Trabajo relacionado */}
            <section id="trabajo-relacionado" className="space-y-4">
              <h2 className="text-xl font-semibold">Trabajo relacionado</h2>
              <p className="text-sm text-muted-foreground">
                El principal referente institucional para datos económicos en
                Costa Rica es el Banco Central de Costa Rica, que publica
                indicadores oficiales sobre producción, inflación, demanda y
                otros agregados macroeconómicos. No obstante, estas
                publicaciones se presentan en formatos estáticos y sin
                herramientas de interpretación automatizada.
              </p>
              <p className="text-sm text-muted-foreground">
                A nivel internacional, diversos trabajos han demostrado la
                utilidad de los modelos de lenguaje grande (LLMs) para el
                análisis financiero y la síntesis de información económica.{" "}
                <span className="italic">FinBERT</span> adapta BERT a textos
                financieros para tareas como clasificación de sentimientos e
                identificación de temas ESG, mientras que{" "}
                <span className="italic">BloombergGPT</span> entrena un modelo
                de 50 mil millones de parámetros sobre un gran corpus de datos
                financieros, logrando métricas superiores en tareas de dominio
                sin sacrificar desempeño generalista.
              </p>
              <p className="text-sm text-muted-foreground">
                En ciencia política, se han explorado LLMs para codificación de
                texto, predicción electoral y análisis de opinión, pero también
                se ha señalado el riesgo de sesgos ideológicos y falta de
                contextualización histórica. Herramientas como{" "}
                <span className="italic">Political-LLM</span> incorporan
                mecanismos específicos para análisis de políticas públicas y
                mitigación de sesgos.
              </p>
              <p className="text-sm text-muted-foreground">
                GovernomicsCR busca posicionarse como una herramienta que
                minimice la parcialidad y genere informes exclusivamente
                basados en datos económicos oficiales, evitando incorporar
                juicios políticos externos al baseline del BCCR.
              </p>
            </section>

            <Separator />

            {/* Metodología */}
            <section id="metodologia" className="space-y-4">
              <h2 className="text-xl font-semibold">Metodología</h2>
              <p className="text-sm text-muted-foreground">
                El diseño metodológico se compone de tres módulos principales:
                preprocesamiento de datos, integración con LLMs mediante
                pipelines multiagente e interfaz de usuario.
              </p>

              <Tabs defaultValue="preproceso">
                <TabsList className="flex flex-wrap">
                  <TabsTrigger value="preproceso">
                    Preprocesamiento
                  </TabsTrigger>
                  <TabsTrigger value="llm">Integración con LLMs</TabsTrigger>
                  <TabsTrigger value="multiagente">
                    Pipelines multiagente
                  </TabsTrigger>
                  <TabsTrigger value="ui">Interfaz de usuario</TabsTrigger>
                  <TabsTrigger value="flujo">Flujo de integración</TabsTrigger>
                  
                </TabsList>

                <TabsContent
                  value="preproceso"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <p>
                    El preprocesamiento inicia con la recopilación de la serie
                    histórica del PIB por oferta, demanda y régimen publicada
                    por el BCCR. Se homogenizan etiquetas de administraciones,
                    se limpian las estructuras temporales y se generan los
                    dataframes base.
                  </p>
                  <p>
                    A partir de estos datos se construyen cinco subdatasets:
                    componente de gasto, sectorial, régimen, industrias y PIB
                    general, cada uno asociado a agentes especializados dentro
                    del sistema.
                  </p>
                </TabsContent>

                <TabsContent
                  value="llm"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <p>
                    La integración con modelos de lenguaje se realiza
                    conectando los dataframes con el modelo{" "}
                    <code>gpt-4.1-mini</code> (y variantes compatibles) usando
                    LangChain y LangGraph. Los prompts se diseñan para forzar
                    al modelo a ejecutar cálculos deterministas sobre los
                    dataframes, en lugar de razonar desde memoria difusa.
                  </p>
                  <p>
                    De esta forma, cada cifra reportada por el sistema debe
                    provenir directamente de los datos del BCCR cargados en
                    contexto.
                  </p>
                </TabsContent>

                <TabsContent
                  value="multiagente"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <p>
                    Los agentes se organizan en módulos especializados
                    (gasto, sectores, régimen, industrias y PIB general)
                    ubicados en el backend. Cada agente recibe un subconjunto de
                    datos, un prompt especializado y devuelve un análisis
                    parcial que luego es integrado.
                  </p>
                  <p>
                    Para preguntas generales se utiliza un pipeline lineal con
                    un solo agente. Para la generación de informes se emplea un
                    pipeline multiagente paralelo: cinco agentes trabajan en
                    simultáneo y un agente integrador sintetiza los resultados
                    en un informe único.
                  </p>
                </TabsContent>

                <TabsContent
                  value="ui"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <p>
                    La interfaz de usuario se implementa como un chat en React y
                    shadcn ui. El usuario selecciona el modo (preguntas
                    generales o generación de informe), escribe su consulta y
                    recibe respuestas en lenguaje natural acompañadas de
                    reportes estructurados.
                  </p>
                  <p>
                    La UI incluye preguntas predefinidas, indicadores de carga,
                    manejo de errores y un bloque informativo que muestra el
                    endpoint y modo de operación (demo o API).
                  </p>
                </TabsContent>

                <TabsContent
                  value="flujo"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <ol className="list-decimal space-y-1 pl-6">
                    <li>
                      El usuario elige un modo (pregunta general o informe) y
                      envía una consulta desde el frontend.
                    </li>
                    <li>
                      El backend recibe la solicitud y selecciona el pipeline
                      adecuado.
                    </li>
                    <li>
                      El pipeline carga los datos relevantes desde los
                      dataframes.
                    </li>
                    <li>
                      Se construye el prompt correspondiente y se envía al
                      agente especializado.
                    </li>
                    <li>
                      El agente consulta el LLM, procesa la respuesta y la
                      estructura.
                    </li>
                    <li>
                      El resultado es devuelto al frontend y presentado al
                      usuario.
                    </li>
                  </ol>
                </TabsContent>

                <TabsContent
                  value="metricas"
                  className="space-y-2 text-sm text-muted-foreground"
                >
                  <p>
                    Para evaluar el sistema se definieron métricas de coherencia
                    analítica (alineación con los datasets del BCCR),
                    estabilidad del pipeline (variación entre ejecuciones
                    repetidas), tiempo de respuesta y calidad percibida de los
                    informes.
                  </p>
                  <p>
                    La coherencia se midió comparando respuestas de los agentes
                    con valores de referencia en archivos como{" "}
                    <code>pib_yoy.txt</code>,{" "}
                    <code>pib_yoy_sectores.txt</code> y{" "}
                    <code>pib_yoy_componentes_gasto.txt</code>. La estabilidad
                    se evaluó repitiendo consultas estándar (Q1–Q5) y
                    analizando la consistencia numérica y narrativa.
                  </p>
                </TabsContent>
              </Tabs>
            </section>

            <Separator />

            {/* Resultados */}
            <section id="resultados" className="space-y-4">
              <h2 className="text-xl font-semibold">Resultados</h2>

              <h3 className="font-medium">
                Coherencia analítica y validación frente al baseline
              </h3>
              <p className="text-sm text-muted-foreground">
                El sistema fue evaluado en dos niveles: (1) coherencia del
                pipeline de preguntas generales y (2) coherencia del pipeline de
                generación de informes. En el primer caso se utilizaron cinco
                preguntas estandarizadas (Q1–Q5) que cubren PIB general, gasto,
                industria, régimen y sectores. En todos los casos, las cifras
                reportadas por los agentes coincidieron con los valores
                presentes en los dataframes del BCCR, confirmando que el LLM
                opera como un intérprete de datos y no como un generador
                especulativo.
              </p>
              <p className="text-sm text-muted-foreground">
                En el segundo nivel se revisó el informe completo sobre el
                gobierno más reciente. Se comprobó que los valores citados para
                consumo de hogares, consumo de gobierno, inversión, sectores,
                régimen especial y PIB general se corresponden con los extremos
                y promedios de las series históricas, sin distorsiones ni
                alucinaciones numéricas.
              </p>

              <h3 className="font-medium">Estabilidad del pipeline</h3>
              <p className="text-sm text-muted-foreground">
                La estabilidad se evaluó repitiendo la consulta comparativa
                entre las administraciones de Carlos Alvarado y Rodrigo Chaves
                en cinco ejecuciones consecutivas (P1–P5). Las respuestas
                conservaron los mismos valores críticos —por ejemplo, la
                contracción máxima de −6.96 en 2020 y el pico de crecimiento de
                11.08–11.09 en 2021 para Alvarado, y el máximo de 5.19 para
                Chaves en 2023— variando únicamente en estilo y nivel de
                detalle. Esto sugiere un comportamiento altamente replicable.
              </p>

              <h3 className="font-medium">Tiempo de respuesta</h3>
              <p className="text-sm text-muted-foreground">
                Las consultas generales (Q1–Q5) presentan tiempos de ejecución
                entre aproximadamente 4.5 y 7.8 segundos, con un promedio en
                torno a 6.4 segundos. Estas latencias son consistentes con un
                pipeline lineal que carga dataframes y realiza razonamiento
                numérico sobre ellos.
              </p>
              <p className="text-sm text-muted-foreground">
                El informe comparativo completo requiere alrededor de 24.3
                segundos. Aunque significativamente mayor, este tiempo se
                explica por la combinación de ejecución paralela de cinco
                agentes temáticos y una fase secuencial de integración donde el
                agente final sintetiza los resultados en un documento extenso.
                Es un trade-off consciente entre profundidad analítica y
                latencia.
              </p>
            </section>

            <Separator />

            {/* Discusión */}
            <section id="discusion" className="space-y-4">
              <h2 className="text-xl font-semibold">Discusión</h2>
              <p className="text-sm text-muted-foreground">
                El principal hallazgo es que un LLM, correctamente
                parametrizado, puede transformarse de un generador de texto
                generalista en un intérprete de resultados económicos. El uso
                de LangChain y LangGraph obliga al modelo a ejecutar cálculos
                deterministas sobre dataframes del BCCR, reduciendo
                significativamente el riesgo de alucinaciones.
              </p>
              <p className="text-sm text-muted-foreground">
                El diseño modular de GovernomicsCR, basado en pipelines
                multiagente, ofrece un buen equilibrio entre completitud y
                escalabilidad, aunque introduce diferencias esperables en el
                tiempo de respuesta entre consultas simples y generación de
                informes complejos. Este trade-off es aceptable en un contexto
                de análisis económico donde la prioridad es la calidad del
                diagnóstico más que la respuesta en tiempo real.
              </p>
            </section>

            <Separator />

            {/* Conclusiones */}
            <section id="conclusiones" className="space-y-4">
              <h2 className="text-xl font-semibold">
                Conclusiones y trabajo futuro
              </h2>
              <p className="text-sm text-muted-foreground">
                GovernomicsCR se establece como una prueba de concepto
                robusta para la aplicación de IA en el análisis económico
                público costarricense. El sistema demuestra que es posible
                comparar objetivamente el desempeño de distintas
                administraciones utilizando LLMs anclados a datos oficiales.
              </p>
              <p className="text-sm text-muted-foreground">
                Como trabajo futuro se plantea incorporar modelos predictivos
                para simular escenarios de política, ampliar la base de
                indicadores (empleo, inflación, balanza de pagos), incluir más
                visualizaciones interactivas y explorar mecanismos adicionales
                para auditar el razonamiento numérico del modelo.
              </p>
            </section>

            <Separator />

            {/* Referencias (resumen) */}
            <section id="referencias" className="space-y-3">
              <h2 className="text-xl font-semibold">Referencias</h2>
              <ul className="space-y-1 list-disc pl-6 text-sm text-muted-foreground">
                <li>
                  Banco Central de Costa Rica. Cuentas Nacionales Trimestrales,
                  varias ediciones.
                </li>
                <li>Blanchard, O. Macroeconomics. Pearson, 2011.</li>
                <li>Huang et al. FinBERT: A Pretrained Language Model for Financial Communications.</li>
                <li>Wu et al. BloombergGPT: A Large Language Model for Finance.</li>
                <li>
                  Linegar et al. Large Language Models in Political Science:
                  Opportunities and Risks.
                </li>
                <li>Rotaru et al. Elections, LLMs and Bias in News Ranking.</li>
                <li>Li et al. Political-LLM: LLMs for Public Policy Analysis.</li>
              </ul>
            </section>

            <Separator />

            {/* Pie */}
            <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
              <Link href="/chatbot" className="underline underline-offset-4">
                ← Volver al chatbot económico
              </Link>
              <span className="text-muted-foreground">
                Última actualización: {new Date().toLocaleDateString("es-CR")}
              </span>
            </div>
          </div>
        </div>
      </div>
    </SidebarInset>
  )
}
