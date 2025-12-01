"use client"

import * as React from "react"
import {
  Area,
  AreaChart,
  CartesianGrid,
  XAxis,
  YAxis,
  type TooltipProps,
} from "recharts"

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
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
} from "@/components/ui/chart"
import { economicActivityDataset } from "@/app/data/economicActivityDataset"

// Convertimos el dataset a formato para el AreaChart
const chartData = economicActivityDataset.map((row) => ({
  actividad: row.actividad,
  mayor: row.tasa_mayor,
  menor: row.tasa_menor,
  adminMayor: row.admin_mayor,
  adminMenor: row.admin_menor,
}))

// Colores INVERTIDOS (mayor usa chart-2, menor usa chart-1)
const chartConfig = {
  mayor: {
    label: "Administración con mayor crecimiento",
    color: "var(--chart-2)",
  },
  menor: {
    label: "Administración con menor crecimiento",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

// Tooltip custom usando directamente los payload de Recharts
function CustomTooltip(
  props: TooltipProps<number, string>
) {
  const { active, payload } = props

  if (!active || !payload || payload.length === 0) return null

  const row = payload[0].payload as (typeof chartData)[number]

  // Buscamos las entradas de mayor y menor por nombre (label de la serie)
  const mayorEntry = payload.find(
    (p) => p.name === chartConfig.mayor.label
  )
  const menorEntry = payload.find(
    (p) => p.name === chartConfig.menor.label
  )

  return (
    <div className="rounded-md border bg-background px-3 py-2 text-xs shadow-sm">
      <div className="mb-1 font-medium">
        Actividad: {row.actividad}
      </div>

      {mayorEntry && (
        <div className="flex items-center gap-2">
          <span
            className="h-2 w-2 rounded-full"
            style={{ backgroundColor: mayorEntry.color ?? chartConfig.mayor.color }}
          />
          <span>
            {row.adminMayor}:{" "}
            {Number(mayorEntry.value ?? 0).toFixed(2)} %
          </span>
        </div>
      )}

      {menorEntry && (
        <div className="mt-1 flex items-center gap-2">
          <span
            className="h-2 w-2 rounded-full"
            style={{ backgroundColor: menorEntry.color ?? chartConfig.menor.color }}
          />
          <span>
            {row.adminMenor}:{" "}
            {Number(menorEntry.value ?? 0).toFixed(2)} %
          </span>
        </div>
      )}
    </div>
  )
}

export function ChartAreaCrecimientoActividades() {
  return (
    <Card className="pt-0">
      <CardHeader className="flex flex-col items-start gap-2 space-y-0 border-b py-5 sm:flex-row sm:items-center">
        <div className="grid flex-1 gap-1">
          <CardTitle>Crecimiento promedio por actividad económica</CardTitle>
          <CardDescription>
            Áreas que muestran el crecimiento promedio mínimo y máximo por
            actividad económica según la administración.
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[280px] w-full"
        >
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="fillMayor" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-mayor)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-mayor)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillMenor" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-menor)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-menor)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>

            <CartesianGrid vertical={false} />
            
            <XAxis
              dataKey="actividad"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              interval={0} 
              angle={-35}
              textAnchor="end"
              tick={{ fontSize: 10 }}
            />

            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              domain={[-8, 24]}
              tickFormatter={(v) => `${v.toFixed(1)}%`}
            />

            {/* Tooltip usando el componente custom */}
            <ChartTooltip cursor={false} content={<CustomTooltip />} />

            {/* Serie: menor crecimiento */}
            <Area
              dataKey="menor"
              type="natural"
              name={chartConfig.menor.label}
              fill="url(#fillMenor)"
              stroke="var(--color-menor)"
            />
            {/* Serie: mayor crecimiento */}
            <Area
              dataKey="mayor"
              type="natural"
              name={chartConfig.mayor.label}
              fill="url(#fillMayor)"
              stroke="var(--color-mayor)"
            />

            <ChartLegend content={<ChartLegendContent />} />
          </AreaChart>
        </ChartContainer>

        <p className="mt-3 text-xs text-muted-foreground text-center">
          Gráfico 4. Crecimiento promedio mínimo y máximo por actividad económica
          según administración. Fuente: elaboración propia con datos del BCCR.
        </p>
      </CardContent>
    </Card>
  )
}
