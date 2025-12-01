"use client"

import * as React from "react"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, Cell } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

import {
  pibSectoresDataset,
  presidentialColors,
  canonicalOrder,
} from "@/app/data/pibSectoresDataset"

export function ChartCrecimientoSectores() {
  const sectores = ["Agro", "Servicios", "Industria"]

  return (
    <Card className="py-0">
      <CardHeader className="border-b px-6 py-4">
        <CardTitle className="text-base sm:text-lg">
          Costa Rica: Crecimiento Promedio del PIB por Administración y Sector
        </CardTitle>
        <CardDescription>
          Comparación del desempeño sectorial por administración presidencial.
        </CardDescription>
      </CardHeader>

      <CardContent className="px-4 sm:px-6">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {sectores.map((sector) => {
            const dataSector = pibSectoresDataset
              .filter((d) => d.sector === sector)
              .sort((a, b) => a.rank - b.rank)

            return (
              <div key={sector} className="flex flex-col">
                <h3 className="text-center font-semibold text-sky-600 mb-2">
                  {sector}
                </h3>

                <ChartContainer
                  className="aspect-auto h-[300px] w-full"
                  config={{
                    growth: { label: "Crecimiento (%)", color: "var(--chart-1)" },
                  }}
                >
                  <BarChart data={dataSector}>
                    <CartesianGrid vertical={false} />

                    <XAxis
                      dataKey="rank"
                      tickLine={false}
                      axisLine={false}
                      tickMargin={6}
                      label={{
                        value: "Posiciones",
                        position: "insideBottom",
                        offset: -2,
                        dy: 12,
                      }}
                    />

                    <YAxis
                      tickLine={false}
                      axisLine={false}
                      tickMargin={6}
                      tickFormatter={(value) => `${value.toFixed(1)}%`}
                      label={{
                        value: "Crecimiento Interanual (%)",
                        angle: -90,
                        position: "insideLeft",
                        style: { textAnchor: "middle" },
                      }}
                    />

                    <ChartTooltip
                      content={
                        <ChartTooltipContent
                          labelFormatter={(_, payload) => {
                            const row = payload?.[0]?.payload
                            return `${row.admin} – ${sector}`
                          }}
                          valueFormatter={(v) =>
                            `${Number(v).toFixed(2).replace(".", ",")} %`
                          }
                        />
                      }
                    />

                    <Bar dataKey="growth">
                      {dataSector.map((row, idx) => (
                        <Cell
                          key={idx}
                          fill={presidentialColors[row.admin]}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ChartContainer>
              </div>
            )
          })}
        </div>

        {/* Leyenda general */}
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3 text-xs">
          {Object.entries(presidentialColors).map(([name, color]) => (
            <div key={name} className="flex items-center gap-2">
              <span
                className="h-3 w-3 rounded-sm"
                style={{ backgroundColor: color }}
              />
              <span>{name}</span>
            </div>
          ))}
        </div>

        <p className="mt-4 text-xs text-muted-foreground text-center">
          Gráfico 6. Crecimiento promedio del PIB por administración y sector.
          Fuente: elaboración propia con datos del BCCR.
        </p>
      </CardContent>
    </Card>
  )
}
