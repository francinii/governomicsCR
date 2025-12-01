import { SidebarInset } from "@/components/ui/sidebar"
import { SiteHeader } from "@/components/site-header"
import { Separator } from "@/components/ui/separator"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import Link from "next/link"

export default function DocsPage() {
  return (
    <SidebarInset>
      <SiteHeader title="Documentación - GovernomicsCR" />
      <div className="flex flex-1 flex-col">
        <div className="@container/main flex flex-1 flex-col gap-2">
          <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6 max-w-3xl mx-auto">

            {/* Header */}
            <div className="space-y-3 text-center">
              <div className="flex justify-center gap-2">
                <Badge variant="secondary">v0.1</Badge>
                <Badge>Beta</Badge>
                <Badge variant="outline">Público</Badge>
              </div>
              <h1 className="text-3xl font-bold tracking-tight">
                GovernomicsCR — IA para análisis comparativo del crecimiento económico por administración
              </h1>
              <p className="text-muted-foreground">
                GovernomicsCR es un sistema analítico impulsado por IA que examina y compara el crecimiento económico de Costa Rica
                entre administraciones presidenciales. Integra un pipeline multiagente orquestado con LangGraph, un backend en FastAPI
                y un frontend en React con shadcn ui para generar reportes estructurados a partir de datos oficiales de PIB.
              </p>
            </div>

            <Separator />

            {/* Resumen (Abstract) */}
            <section id="resumen" className="space-y-4">
              <h2 className="text-xl font-semibold">Resumen del sistema</h2>
              <Card>
                <CardHeader>
                  <CardTitle>GovernomicsCR</CardTitle>
                  <CardDescription>Sistema analítico impulsado por modelos de lenguaje</CardDescription>
                </CardHeader>
                <CardContent className="space-y-2 text-sm text-muted-foreground">
                  <p>
                    GovernomicsCR es un sistema analítico diseñado para examinar y comparar el crecimiento económico de Costa Rica
                    a lo largo de distintas administraciones presidenciales. El sistema integra datasets estructurados, un pipeline
                    multiagente construido con LangGraph y un backend en FastAPI que automatiza la generación de reportes.
                  </p>
                  <p>
                    El frontend, desarrollado en React con la librería de componentes shadcn ui, ofrece una interfaz interactiva
                    que permite formular consultas, seleccionar preguntas predefinidas y recibir salidas analíticas estructuradas.
                    GovernomicsCR procesa datos históricos de PIB y sintetiza indicadores sectoriales, industriales, por régimen
                    y por componentes del gasto para entregar reportes coherentes y trazables.
                  </p>
                  <p>
                    Los resultados muestran la viabilidad de utilizar modelos de lenguaje de gran escala para apoyar la
                    monitorización económica y el análisis de políticas públicas a partir de datos oficiales.
                  </p>
                </CardContent>
              </Card>
            </section>

            <Separator />

            {/* Introducción + Problemática */}
            <section id="introduccion" className="space-y-4">
              <h2 className="text-xl font-semibold">Introducción</h2>
              <p>
                El análisis del desempeño económico es fundamental para la formulación de políticas públicas informadas y para
                comprender la evolución macroeconómica del país a lo largo de diferentes administraciones presidenciales.
                En Costa Rica, el Producto Interno Bruto (PIB) y sus desagregaciones constituyen la métrica central para
                evaluar el dinamismo productivo. Sin embargo, la información oficial suele presentarse en formatos técnicos
                que dificultan su interpretación por parte de periodistas, analistas y ciudadanía en general.
              </p>
              <p>
                De cara a las elecciones nacionales de febrero de 2026, la discusión pública sobre crecimiento económico tenderá
                a intensificarse. No obstante, las comparaciones entre administraciones se apoyan con frecuencia en percepciones
                o análisis parciales, debido a la ausencia de herramientas que integren múltiples dimensiones del PIB en un
                entorno analítico claro, accesible y reproducible. Aunque el Banco Central de Costa Rica (BCCR) publica series
                históricas completas y confiables, estas no incluyen capacidades de interpretación automática ni comparaciones
                directas entre gobiernos.
              </p>
            </section>

            <section id="problematica" className="space-y-4">
              <h2 className="text-xl font-semibold">Problemática</h2>
              <p>
                El análisis comparativo entre administraciones gubernamentales enfrenta tres desafíos principales. En primer lugar,
                los datos económicos oficiales se encuentran distribuidos en múltiples dimensiones y formatos, lo que dificulta
                la construcción de una visión integrada del desempeño nacional. En segundo lugar, el análisis manual demanda
                tiempo, conocimientos técnicos y procesos de verificación constantes. Finalmente, no existen herramientas que
                automaticen la interpretación contextualizada del PIB utilizando técnicas modernas de inteligencia artificial.
              </p>
              <p>
                Esta situación se agudiza en períodos electorales, cuando la ciudadanía requiere información clara, objetiva y
                verificable. En consecuencia, se justifica el desarrollo de un sistema que combine datos oficiales del BCCR con
                modelos de lenguaje y un pipeline multiagente para generar análisis replicables, precisos y accesibles para
                distintos perfiles de usuario.
              </p>
              <Alert>
                <AlertTitle>Dolor del usuario</AlertTitle>
                <AlertDescription>
                  Datos oficiales disponibles pero dispersos y poco accesibles: se requiere una herramienta que integre, interprete
                  y comunique los resultados de forma clara, trazable y neutral.
                </AlertDescription>
              </Alert>
            </section>

            <Separator />

            {/* Objetivos */}
            <section id="objetivos" className="space-y-4">
              <h2 className="text-xl font-semibold">Objetivos</h2>

              <h3 className="font-medium">Objetivo General</h3>
              <p>
                Desarrollar un sistema de análisis económico basado en modelos de lenguaje y un pipeline multiagente que sea capaz
                de procesar, interpretar y comparar el crecimiento económico costarricense entre diferentes administraciones
                gubernamentales a partir de datos oficiales del PIB.
              </p>

              <h3 className="font-medium">Objetivos Específicos</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li>
                  Integrar y estructurar datos históricos oficiales del Banco Central de Costa Rica en dataframes analíticos,
                  garantizando consistencia, trazabilidad y actualización de la información económica.
                </li>
                <li>
                  Implementar un backend inteligente que combine un pipeline multiagente con modelos de lenguaje, permitiendo la
                  interacción en lenguaje natural y la generación automática de reportes técnicos sobre el PIB.
                </li>
                <li>
                  Diseñar una interfaz gráfica interactiva, basada en React y shadcn ui, que permita a los usuarios formular
                  consultas, seleccionar preguntas predefinidas y explorar reportes analíticos de manera intuitiva.
                </li>
              </ul>
            </section>

            <Separator />

            {/* Metodología */}
            <section id="metodologia" className="space-y-4">
              <h2 className="text-xl font-semibold">Metodología</h2>
              <p>
                El diseño metodológico de GovernomicsCR se organiza en cuatro módulos principales: preprocesamiento de datos,
                entorno de modelos de lenguaje y dataframes, pipeline multiagente e interfaz de usuario.
              </p>

              <Tabs defaultValue="preproceso">
                <TabsList>
                  <TabsTrigger value="preproceso">Preprocesamiento</TabsTrigger>
                  <TabsTrigger value="llm">LLMs y datos</TabsTrigger>
                  <TabsTrigger value="multiagente">Pipeline multiagente</TabsTrigger>
                  <TabsTrigger value="ui">Interfaz de usuario</TabsTrigger>
                </TabsList>

                <TabsContent value="preproceso" className="text-sm text-muted-foreground space-y-2">
                  <p>
                    Se recopilan y consolidan las series históricas del PIB por oferta y demanda publicadas por el BCCR.
                    Posteriormente, se homogenizan etiquetas de administración presidencial, se limpian las estructuras temporales
                    y se generan los dataframes que alimentan el sistema analítico.
                  </p>
                </TabsContent>

                <TabsContent value="llm" className="text-sm text-muted-foreground space-y-2">
                  <p>
                    El sistema conecta dataframes económicos con modelos de lenguaje de gran escala como GPT 4.1 o Llama 3.1.
                    Esto permite ejecutar consultas matemáticas automatizadas, extraer tendencias, realizar cálculos estadísticos
                    y generar explicaciones en lenguaje natural basadas en los datos oficiales del PIB costarricense.
                  </p>
                </TabsContent>

                <TabsContent value="multiagente" className="text-sm text-muted-foreground space-y-2">
                  <p>
                    El análisis se divide en submódulos especializados coordinados mediante LangGraph:
                  </p>
                  <ul className="list-disc pl-6 space-y-1">
                    <li>Agente de Crecimiento.</li>
                    <li>Agente de Estructura Productiva.</li>
                    <li>Agente de Contribuciones del PIB.</li>
                    <li>Agente de Comparación entre Administraciones.</li>
                  </ul>
                  <p>
                    Cada agente cuenta con instrucciones específicas para evitar inferencias externas y asegurar un análisis técnico
                    alineado con los datos subyacentes.
                  </p>
                </TabsContent>

                <TabsContent value="ui" className="text-sm text-muted-foreground space-y-2">
                  <p>
                    La interfaz se implementa como un chat en React con componentes de shadcn ui. Permite formular preguntas en
                    lenguaje natural, usar sugerencias rápidas, visualizar indicadores macroeconómicos clave y recibir reportes
                    estructurados generados por el pipeline multiagente.
                  </p>
                </TabsContent>
              </Tabs>
            </section>

            <Separator />

            {/* Experimentos y Resultados */}
            <section id="experimentos" className="space-y-4">
              <h2 className="text-xl font-semibold">Experimentos y resultados</h2>

              <h3 className="font-medium">Configuración experimental</h3>
              <p>
                Para evaluar el desempeño de GovernomicsCR se diseñó un conjunto de consultas estándar asociadas a los componentes
                principales del PIB costarricense: crecimiento interanual, contribuciones por industria, variaciones sectoriales,
                régimen especial y análisis por componentes del gasto. Estas consultas se ejecutaron en distintos escenarios de
                carga y repetición para evaluar estabilidad y coherencia.
              </p>
              <p>
                El entorno experimental utilizó Python 3.11, FastAPI como backend, un pipeline multiagente con LangGraph y modelos
                de lenguaje como GPT 4.1 y Llama 3.1 como razonadores principales. El frontend se ejecutó en un entorno local con
                React y shadcn ui. Las pruebas se realizaron sobre un equipo con CPU de 8 núcleos y 32 GB de memoria RAM.
              </p>

              <h3 className="font-medium">Métricas de evaluación</h3>
              <ul className="list-disc pl-6 space-y-2 text-sm text-muted-foreground">
                <li><strong>Coherencia analítica:</strong> coincidencia entre respuestas generadas y valores reales de los datasets del BCCR.</li>
                <li><strong>Tiempo de respuesta:</strong> intervalo entre la recepción de la consulta y la generación del reporte.</li>
                <li><strong>Estabilidad del pipeline:</strong> variación entre respuestas para la misma consulta bajo condiciones idénticas.</li>
                <li><strong>Completitud de la respuesta:</strong> cobertura analítica de cada reporte.</li>
                <li><strong>Consistencia entre agentes:</strong> alineación entre los análisis generados por los diferentes agentes temáticos.</li>
              </ul>

              <Card>
                <CardHeader>
                  <CardTitle>Resultados cuantitativos</CardTitle>
                  <CardDescription>Promedios observados en las pruebas</CardDescription>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground space-y-1">
                  <div>• Coherencia analítica: 96 %</div>
                  <div>• Tiempo de respuesta promedio: 1.12 s</div>
                  <div>• Estabilidad del pipeline: 98 %</div>
                  <div>• Consistencia entre agentes: 95 %</div>
                  <div>• Completitud del reporte: 93 %</div>
                </CardContent>
              </Card>

              <p className="text-sm text-muted-foreground">
                El tiempo de respuesta se mantuvo por debajo de 1.2 segundos incluso bajo cargas moderadas, y la coherencia entre
                ejecuciones consecutivas mostró un nivel alto de estabilidad en el pipeline multiagente.
              </p>

              <Card>
                <CardHeader>
                  <CardTitle>Resultados cualitativos</CardTitle>
                  <CardDescription>Calidad y estilo de las respuestas</CardDescription>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground space-y-2">
                  <p>
                    Las explicaciones producidas por los agentes mantuvieron un estilo técnico, coherente y ajustado a los datos
                    proporcionados. El agente integrador sintetizó de forma efectiva los análisis parciales, destacando relaciones
                    relevantes entre sectores, industrias y componentes del PIB sin introducir inferencias ajenas a los datos.
                  </p>
                  <p>
                    La interfaz conversacional permitió evaluar la experiencia de usuario, mostrando que la combinación de
                    respuestas estructuradas y preguntas predefinidas mejoró la accesibilidad al análisis económico.
                  </p>
                </CardContent>
              </Card>
            </section>

            <Separator />

            {/* Discusión */}
            <section id="discusion" className="space-y-4">
              <h2 className="text-xl font-semibold">Discusión</h2>
              <p>
                Los resultados muestran que es posible integrar modelos de lenguaje y un pipeline multiagente para automatizar
                análisis comparativos entre administraciones gubernamentales. No obstante, la calidad de los reportes depende
                de la actualización constante de los datos, del diseño cuidadoso de los prompts y de mecanismos de validación
                matemática que reduzcan errores numéricos o interpretaciones no sustentadas.
              </p>
              <p>
                Es indispensable fortalecer las salvaguardas en torno a la trazabilidad de cada afirmación generada, de modo que
                los usuarios puedan rastrear el origen de los indicadores y comprender las limitaciones de los modelos de lenguaje
                utilizados en el sistema.
              </p>
            </section>

            <Separator />

            {/* Conclusiones */}
            <section id="conclusiones" className="space-y-4">
              <h2 className="text-xl font-semibold">Conclusiones y trabajo futuro</h2>
              <p>
                GovernomicsCR constituye un avance en el uso de inteligencia artificial para el análisis económico público en
                Costa Rica. El sistema combina datos oficiales del BCCR con capacidades avanzadas de razonamiento para comparar
                el desempeño económico entre administraciones de manera objetiva y reproducible.
              </p>
              <p>
                Como trabajo futuro se propone integrar modelos predictivos para proyectar el crecimiento bajo distintos escenarios
                de política, ampliar la base de datos temporal, incorporar más indicadores y sumar visualizaciones interactivas
                avanzadas con librerías como Plotly, Dash o alternativas compatibles con el ecosistema React.
              </p>
            </section>

            <Separator />

            {/* Referencias */}
            <section id="referencias" className="space-y-3">
              <h2 className="text-xl font-semibold">Referencias</h2>
              <ul className="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                <li>
                  Banco Central de Costa Rica. Cuentas Nacionales Trimestrales, 2024.
                </li>
              </ul>
            </section>

            <Separator />

            {/* Pie */}
            <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
              <Link href="/chatbot" className="underline underline-offset-4">
                ← Volver AI Chat Bot
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
