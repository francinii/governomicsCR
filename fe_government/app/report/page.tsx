import { SidebarInset } from "@/components/ui/sidebar"
import { SiteHeader } from "@/components/site-header"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import Link from "next/link"
import { ChartCrecimientoPIBAdministracion } from "@/components/charts/ChartCrecimientoPIBAdministracion"
import { ChartCrecimientoRegimenDefinitivo } from "@/components/charts/ChartCrecimientoRegimenDefinitivo"
import { ChartCrecimientoRegimenEspecial } from "@/components/charts/ChartCrecimientoRegimenEspecial"
import { ChartAreaCrecimientoActividades } from "@/components/charts/ChartCrecimientoActividades"
import { ChartAdminCrecimientoActividades } from "@/components/charts/ChartAdminCrecimientoActividades"
import { ChartCrecimientoSectores } from "@/components/charts/ChartCrecimientoSectores"
import { ChartPIBComponentesGasto } from "@/components/charts/ChartPIBComponentesGasto"

export default function DocsPage() {
  return (
    <SidebarInset>
      <SiteHeader title="Documentación - Análisis de Crecimiento Económico" />
      <div className="flex flex-1 flex-col">
        <div className="@container/main flex flex-1 flex-col gap-2">
          <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6 max-w-3xl mx-auto">

            {/* Header */}
            <div className="space-y-3 text-center">
              <div className="flex justify-center gap-2">
                <Badge variant="secondary">Informe</Badge>
                <Badge>Notebook-based</Badge>
                <Badge variant="outline">Costa Rica</Badge>
              </div>
              <h1 className="text-3xl font-bold tracking-tight">
                Análisis del Ritmo de Crecimiento Económico Costarricense por Administración
              </h1>
              <p className="text-muted-foreground">
                Informe generado a partir de un notebook de Python que analiza el crecimiento del PIB
                costarricense por administración, régimen de comercio, actividades económicas, sectores productivos
                y componentes de la demanda, utilizando series oficiales del Banco Central de Costa Rica (BCCR).
              </p>
            </div>

            <Alert>
              <AlertTitle>Origen del informe</AlertTitle>
              <AlertDescription>
                Este documento se generó a partir de un notebook (Jupyter) que procesa datos del BCCR, calcula
                tasas de crecimiento interanual y produce las figuras incluidas en esta página.
              </AlertDescription>
            </Alert>

            <Separator />

            {/* Introducción */}
            <section id="introduccion" className="space-y-4">
              <h2 className="text-xl font-semibold">Introducción</h2>
              <p>
                El informe presenta una lectura integral del crecimiento reciente de la economía costarricense,
                comparando el ritmo de expansión entre administraciones presidenciales desde Figueres Olsen
                (1994–1998) hasta Rodrigo Chaves (2022–presente). El análisis se organiza en distintos niveles
                de desagregación: PIB total, régimen de comercio (definitivo y zonas francas), actividades
                económicas, sectores productivos (primario, secundario y terciario) y componentes del gasto
                desde la óptica de la demanda.
              </p>
              <p>
                Para comparar el desempeño entre gobiernos, se promedian las tasas de variación interanual
                del PIB tendencia–ciclo en el período efectivo de cada administración. De esta manera, no
                solo se cuantifica el ritmo de crecimiento, sino que también se identifica su composición
                y los motores sectoriales que lo explican.
              </p>
            </section>

            <Separator />

            {/* Metodología y datos */}
            <section id="metodologia" className="space-y-4">
              <h2 className="text-xl font-semibold">Metodología y datos</h2>
              <p>
                La metodología se basa en el cálculo de tasas de variación interanual del PIB tendencia–ciclo
                y su promedio dentro del intervalo de cada administración. Los datos provienen de las Cuentas
                Nacionales Trimestrales del Banco Central de Costa Rica, que se organizan en distintos
                dataframes para facilitar el análisis por régimen, actividad, sector productivo y componente
                de la demanda.
              </p>
              <Tabs defaultValue="vista-general">
                <TabsList>
                  <TabsTrigger value="vista-general">Vista general</TabsTrigger>
                  <TabsTrigger value="admins">Administraciones</TabsTrigger>
                  <TabsTrigger value="dimensiones">Dimensiones analizadas</TabsTrigger>
                </TabsList>
                <TabsContent value="vista-general" className="text-sm text-muted-foreground space-y-1">
                  <p>
                    • Cálculo de tasas interanuales del PIB tendencia–ciclo.
                  </p>
                  <p>
                    • Promedio por administración para obtener un indicador sintético de dinamismo.
                  </p>
                  <p>
                    • Uso de notebooks para automatizar extracción, cálculos y generación de gráficos.
                  </p>
                </TabsContent>
                <TabsContent value="admins" className="text-sm text-muted-foreground space-y-1">
                  <p>
                    El período de análisis abarca las administraciones: Figueres Olsen, Miguel Ángel
                    Rodríguez, Abel Pacheco, Óscar Arias, Laura Chinchilla, Luis Guillermo Solís,
                    Carlos Alvarado y Rodrigo Chaves.
                  </p>
                </TabsContent>
                <TabsContent value="dimensiones" className="text-sm text-muted-foreground space-y-1">
                  <p>• PIB total.</p>
                  <p>• Régimen definitivo y zonas francas.</p>
                  <p>• Actividades económicas específicas.</p>
                  <p>• Sectores productivos primario, secundario y terciario.</p>
                  <p>• Componentes del gasto (consumo, inversión, exportaciones e importaciones).</p>
                </TabsContent>
              </Tabs>
            </section>

            <Separator />

            {/* PIB total por administración */}
            <section id="pib-total" className="space-y-4">
              <h2 className="text-xl font-semibold">Crecimiento de la economía en su conjunto</h2>
              <p>
                El gráfico siguiente muestra el ritmo de crecimiento promedio del PIB tendencia–ciclo por
                administración. Las administraciones con mayor dinamismo económico son las de Óscar Arias
                (4.80%), Rodrigo Chaves (4.51%) y Miguel Ángel Rodríguez (4.34%), seguidas por Abel Pacheco
                (4.25%), Laura Chinchilla (4.18%) y Figueres Olsen (4.12%). Con un crecimiento más moderado
                se ubica Luis Guillermo Solís (3.88%), mientras que el desempeño más bajo corresponde a
                Carlos Alvarado, con 2.35%.
              </p>
              <p>
                Aunque el impacto de la pandemia coincidió con la administración de Carlos Alvarado, la
                desaceleración no se explica únicamente por ese choque; los datos previos al COVID-19 ya
                mostraban un crecimiento promedio cercano al 2.24%, lo que indica un debilitamiento
                estructural anterior.
              </p>

              <ChartCrecimientoPIBAdministracion />
            </section>

            <Separator />

            {/* Régimen de comercio */}
            <section id="regimen-comercio" className="space-y-4">
              <h2 className="text-xl font-semibold">Desempeño por régimen de comercio</h2>
              <p>
                El análisis diferencia entre el régimen definitivo y las zonas francas. En el régimen
                definitivo, el mayor dinamismo se observa bajo la administración de Óscar Arias (4.86%),
                seguida por Laura Chinchilla (4.19%), Abel Pacheco (4.09%) y Miguel Ángel Rodríguez (4.00%).
                Rodrigo Chaves (3.60%) y Luis Guillermo Solís (3.06%) muestran un crecimiento moderado, mientras
                que Carlos Alvarado presenta el crecimiento más bajo (1.38%).
              </p>

              <ChartCrecimientoRegimenDefinitivo />

              <p>
                En contraste, las zonas francas muestran un patrón distinto: las administraciones de
                Luis Guillermo Solís (15.78%), Figueres Olsen (15.67%) y Miguel Ángel Rodríguez (12.46%)
                lideran en dinamismo, seguidas por Rodrigo Chaves (10.77%) y Carlos Alvarado (10.76%).
                Pacheco (7.38%), Óscar Arias (4.20%) y Laura Chinchilla (3.98%) registran crecimientos
                relativamente menores en este régimen.
              </p>

              <ChartCrecimientoRegimenEspecial />
            </section>

            <Separator />

            {/* Actividades económicas */}
            <section id="actividades" className="space-y-4">
              <h2 className="text-xl font-semibold">Desempeño por actividades económicas</h2>
              <p>
                El informe examina, actividad por actividad, cuáles administraciones lideraron y cuáles
                quedaron rezagadas. La administración de Miguel Ángel Rodríguez destaca por registrar el
                mayor número de actividades con el crecimiento promedio más alto, en sectores como
                Información y Comunicaciones (19.04%), Actividades Profesionales (13.14%), Electricidad,
                Agua y Saneamiento (6.92%) y Minas y Canteras (4.49%).
              </p>
              <p>
                En contraste, la administración de Carlos Alvarado aparece de forma recurrente como la de
                menor crecimiento en varios sectores, incluyendo Construcción (–2.47%), Minas y Canteras
                (–1.11%), Agricultura (0.22%), Inmobiliario (1.30%), Enseñanza, Salud y Asistencia Social
                (2.14%), Información y Comunicaciones (3.43%) y Actividades Profesionales (4.30%).
              </p>

              <ChartAreaCrecimientoActividades />

              <p className="text-sm text-muted-foreground">
                El informe también identifica, para cada administración, la actividad con mayor y menor dinamismo,
                mostrando patrones como: servicios financieros liderando bajo Arias, actividades profesionales bajo
                Chaves, y manufactura como actividad de mejor desempeño en la administración de Alvarado, pero con
                resultados negativos en construcción.
              </p>

              <ChartAdminCrecimientoActividades />
            </section>

            <Separator />

            {/* Sectores productivos */}
            <section id="sectores" className="space-y-4">
              <h2 className="text-xl font-semibold">Crecimiento por sectores productivos</h2>
              <p>
                Al agrupar las actividades en sectores primario, secundario e industrial, se observa que
                en el sector agropecuario la administración de Figueres Olsen lidera con un 5.85%, mientras
                que Carlos Alvarado registra el menor crecimiento (0.22%). En servicios, la administración
                de Óscar Arias alcanza 6.04%, seguida de Chinchilla, Solís y Rodríguez, con Alvarado nuevamente
                en la última posición (1.90%).
              </p>
              <p>
                En el sector industrial, el mayor crecimiento promedio corresponde a Rodrigo Chaves (5.52%),
                seguido de Carlos Alvarado (4.00%) y Miguel Ángel Rodríguez (3.89%). Las administraciones de
                Chinchilla y Solís exhiben una expansión industrial más moderada.
              </p>

              <ChartCrecimientoSectores />
            </section>

            <Separator />

            {/* Demanda: componentes del gasto */}
            <section id="demanda" className="space-y-4">
              <h2 className="text-xl font-semibold">Demanda: crecimiento por componentes del gasto</h2>
              <p>
                Desde la perspectiva de la demanda, el análisis distingue entre consumo de hogares, consumo
                del gobierno, inversión, exportaciones e importaciones. En consumo privado, el mayor dinamismo
                se observa durante la administración de Laura Chinchilla (5.56%), seguida por Óscar Arias y
                Luis Guillermo Solís, mientras que Carlos Alvarado presenta el crecimiento más bajo (1.33%).
              </p>
              <p>
                En inversión, Figueres Olsen lidera con un 8.25%, seguido por Arias (5.83%) y Chinchilla (5.71%),
                mientras que Carlos Alvarado y, en menor medida, Solís y Chaves muestran tasas de expansión más
                moderadas. En exportaciones, el mayor dinamismo corresponde a Rodrigo Chaves (10.08%), seguido
                por Figueres Olsen y Pacheco; en importaciones, destaca Laura Chinchilla con 8.94%.
              </p>

              <ChartPIBComponentesGasto />
            </section>

            <Separator />

            {/* Conclusiones */}
            <section id="conclusiones" className="space-y-4">
              <h2 className="text-xl font-semibold">Conclusiones</h2>
              <p>
                En términos agregados, el informe concluye que Figueres Olsen lidera el crecimiento en el
                sector agropecuario, Óscar Arias lidera en servicios y Rodrigo Chaves lidera en industria.
                Por otra parte, los menores crecimientos sectoriales se asocian principalmente a la administración
                de Carlos Alvarado en agro y servicios, y a la administración de Laura Chinchilla en industria.
              </p>
              <p>
                La combinación de análisis por administración, régimen, actividad, sector y demanda permite
                construir una visión matizada del desempeño económico reciente de Costa Rica. El uso de notebooks
                para automatizar cálculos y gráficos garantiza reproducibilidad y facilita la actualización del
                informe conforme se incorporan nuevos datos.
              </p>
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
