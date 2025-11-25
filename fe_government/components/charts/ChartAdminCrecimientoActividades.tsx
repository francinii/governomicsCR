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

import { economicAdminDataset } from "@/app/data/economicAdminDataset"

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

// Preparamos datos para Recharts
const chartData = economicAdminDataset.map((row) => ({
  admin: row.admin,
  mayor: row.maxGrowth,
  menor: row.minGrowth,
  actividadMayor: row.maxActivity,
  actividadMenor: row.minActivity,
}))

// Config gráfico
const chartConfig = {
  mayor: {
    label: "Actividad con mayor crecimiento",
    color: "var(--chart-2)",
  },
  menor: {
    label: "Actividad con menor crecimiento",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

// Tooltip custom
function CustomTooltip(props: TooltipProps<number, string>) {
  const { active, payload } = props

  if (!active || !payload || payload.length === 0) return null

  const row = payload[0].payload as (typeof chartData)[number]

  const mayorEntry = payload.find((p) => p.name === chartConfig.mayor.label)
  const menorEntry = payload.find((p) => p.name === chartConfig.menor.label)

  return (
    <div className="rounded-md border bg-background px-3 py-2 text-xs shadow-sm">
      <div className="mb-1 font-medium">
        Administración: {row.admin}
      </div>

      {mayorEntry && (
        <div className="flex items-center gap-2">
          <span
            className="h-2 w-2 rounded-full"
            style={{
              backgroundColor:
                adminColors[row.admin] ??
                mayorEntry.color ??
                chartConfig.mayor.color,
            }}
          />
          <span>
            {row.actividadMayor}: {Number(mayorEntry.value).toFixed(2)} %
          </span>
        </div>
      )}

      {menorEntry && (
        <div className="mt-1 flex items-center gap-2">
          <span
            className="h-2 w-2 rounded-full"
            style={{
              backgroundColor:
                adminColors[row.admin] ??
                menorEntry.color ??
                chartConfig.menor.color,
            }}
          />
          <span>
            {row.actividadMenor}: {Number(menorEntry.value).toFixed(2)} %
          </span>
        </div>
      )}
    </div>
  )
}

// Componente principal
export function ChartAdminCrecimientoActividades() {
  return (
    <Card className="pt-0">
      <CardHeader className="flex flex-col items-start gap-2 border-b py-5">
        <div className="grid flex-1 gap-1">
          <CardTitle>Crecimiento por administración</CardTitle>
          <CardDescription>
            Actividades económicas con mayor y menor crecimiento por administración.
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-[300px] w-full">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="fillMayor" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-mayor)" stopOpacity={0.8} />
                <stop offset="95%" stopColor="var(--color-mayor)" stopOpacity={0.1} />
              </linearGradient>

              <linearGradient id="fillMenor" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-menor)" stopOpacity={0.8} />
                <stop offset="95%" stopColor="var(--color-menor)" stopOpacity={0.1} />
              </linearGradient>
            </defs>

            <CartesianGrid vertical={false} />

            <XAxis
              dataKey="admin"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
            />

            <YAxis
              tickLine={false}
              axisLine={false}
              domain={[-7, 22]}
              tickFormatter={(v) => `${v.toFixed(1)}%`}
            />

            <ChartTooltip cursor={false} content={<CustomTooltip />} />

            <Area
              dataKey="menor"
              type="natural"
              name={chartConfig.menor.label}
              fill="url(#fillMenor)"
              stroke="var(--color-menor)"
            />

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
          Gráfico 5. Actividades de mayor y menor crecimiento por administración.
          Fuente: elaboración propia con datos del BCCR.
        </p>
      </CardContent>
    </Card>
  )
}
