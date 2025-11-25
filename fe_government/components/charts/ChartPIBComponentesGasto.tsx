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
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

import { pibComponentesGastoDataset } from "@/app/data/pibComponentesGastoDataset"

// Colores por administración
const adminColors: Record<string, string> = {
  Olsen: "#f97316",
  Rodríguez: "#fed7aa",
  Pacheco: "#a855f7",
  Arias: "#22c55e",
  Chinchilla: "#fb923c",
  Solís: "#9ca3af",
  Alvarado: "#ec4899",
  Chaves: "#38bdf8",
}

// Componentes del gasto
const components = [
  { key: "consumoHogares", label: "Consumo Hogares" },
  { key: "consumoGobierno", label: "Consumo Gobierno" },
  { key: "inversion", label: "Inversión" },
  { key: "exportaciones", label: "Exportaciones" },
  { key: "importaciones", label: "Importaciones" },
]

const chartConfig = {
  value: {
    label: "Crecimiento interanual (%)",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

export function ChartPIBComponentesGasto() {
  return (
    <Card>
      <CardHeader className="border-b px-6 py-4">
        <CardTitle className="text-base sm:text-lg">
          PIB: Crecimiento por Administración y Componentes del Gasto
        </CardTitle>
        <CardDescription>
          Promedio interanual por administración y tipo de componente.
        </CardDescription>
      </CardHeader>

      <CardContent className="px-2 sm:p-6">
        {/* 2 gráficos por fila */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {components.map((comp) => {
            // ⬇️ ordenar Y de mayor a menor para este componente
            const sortedData = [...pibComponentesGastoDataset].sort(
              (a, b) => b[comp.key] - a[comp.key]
            )

            return (
              <div key={comp.key} className="w-full">
                {/* Título por gráfico */}
                <h3 className="text-center text-sm font-semibold mb-3 text-blue-600">
                  {comp.label}
                </h3>

                <ChartContainer
                  config={chartConfig}
                  className="aspect-auto h-[320px] w-full"
                >
                  <BarChart
                    data={sortedData}
                    layout="vertical"
                    margin={{ left: 30, right: 12, bottom: 12 }}
                  >
                    <CartesianGrid horizontal={false} />

                    {/* ✔️ Mostrar todos los nombres y legibles */}
                    <YAxis
                      type="category"
                      dataKey="label"
                      width={80}
                      tickLine={false}
                      axisLine={false}
                      tick={{ fontSize: 11 }}
                    />

                    <XAxis
                      type="number"
                      tickLine={false}
                      axisLine={false}
                      tickMargin={8}
                      domain={[-15, 25]}
                      tickFormatter={(v) => `${v.toFixed(1)}%`}
                    />

                    <ChartTooltip
                      content={
                        <ChartTooltipContent
                          nameKey={comp.key}
                          labelFormatter={(admin) => `Administración: ${admin}`}
                          valueFormatter={(v) =>
                            `${Number(v).toFixed(2).replace(".", ",")} %`
                          }
                        />
                      }
                    />

                    <Bar dataKey={comp.key}>
                      {sortedData.map((row) => (
                        <Cell
                          key={row.label}
                          fill={adminColors[row.label] ?? "#8884d8"}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ChartContainer>
              </div>
            )
          })}
        </div>

        <p className="mt-4 text-xs text-muted-foreground text-center">
          Gráfico 7. Crecimiento promedio del PIB por componentes del gasto y por
          administración. Fuente: elaboración propia con datos del BCCR.
        </p>
      </CardContent>
    </Card>
  )
}
