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

// --- Datos reales: promedio anual del Régimen Definitivo (PIB_RegDef_TC) ---
const chartDataRegimen = [
  { year: 1994, growth: 4.88 },
  { year: 1995, growth: 3.17 },
  { year: 1996, growth: 1.6 },
  { year: 1997, growth: 5.08 },
  { year: 1998, growth: 6.26 },
  { year: 1999, growth: 4.18 },
  { year: 2000, growth: 3.32 },
  { year: 2001, growth: 3.35 },
  { year: 2002, growth: 3.18 },
  { year: 2003, growth: 4.27 },
  { year: 2004, growth: 4.0 },
  { year: 2005, growth: 4.24 },
  { year: 2006, growth: 7.19 },
  { year: 2007, growth: 8.56 },
  { year: 2008, growth: 4.98 },
  { year: 2009, growth: -0.36 },
  { year: 2010, growth: 4.94 },
  { year: 2011, growth: 4.62 },
  { year: 2012, growth: 4.91 },
  { year: 2013, growth: 2.8 },
  { year: 2014, growth: 3.34 },
  { year: 2015, growth: 3.67 },
  { year: 2016, growth: 2.94 },
  { year: 2017, growth: 2.4 },
  { year: 2018, growth: 2.05 },
  { year: 2019, growth: 1.59 },
  { year: 2020, growth: -6.09 },
  { year: 2021, growth: 6.94 },
  { year: 2022, growth: 4.28 },
  { year: 2023, growth: 3.89 },
  { year: 2024, growth: 3.79 },
  { year: 2025, growth: 3.07 },
]

// --- Colores por administración (mismos del gráfico Plotly) ---
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

// --- Determinar administración por año ---
function getAdminByYear(year: number): string {
  if (year >= 1994 && year < 1998) return "Olsen"
  if (year >= 1998 && year < 2002) return "Rodríguez"
  if (year >= 2002 && year < 2006) return "Pacheco"
  if (year >= 2006 && year < 2010) return "Arias"
  if (year >= 2010 && year < 2014) return "Chinchilla"
  if (year >= 2014 && year < 2018) return "Solís"
  if (year >= 2018 && year < 2022) return "Alvarado"
  if (year >= 2022 && year <= 2026) return "Chaves"
  return "N/A"
}

const chartConfig = {
  growth: {
    label: "Crecimiento promedio anual del Régimen Definitivo (%)",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

export function ChartCrecimientoRegimenDefinitivo() {
  const data = chartDataRegimen

  return (
    <Card className="py-0">
      <CardHeader className="border-b px-6 py-4">
        <CardTitle className="text-base sm:text-lg">
          Costa Rica: Crecimiento interanual promedio del Régimen Definitivo por año
        </CardTitle>
        <CardDescription>
          Promedio anual del crecimiento del PIB en régimen definitivo, coloreado
          según la administración presidencial.
        </CardDescription>
      </CardHeader>

      <CardContent className="px-2 sm:p-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[300px] w-full"
        >
          <BarChart
            data={data}
            margin={{
              left: 12,
              right: 12,
              bottom: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="year"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={16}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              domain={[-8, 10]}
              tickFormatter={(value) => `${value.toFixed(1)}%`}
            />

            <ChartTooltip
              content={
                <ChartTooltipContent
                  nameKey="growth"
                  labelFormatter={(_, payload) => {
                    const year = payload?.[0]?.payload?.year
                    const admin = getAdminByYear(Number(year))
                    return `Administración ${admin} – ${year}`
                  }}
                  valueFormatter={(v) =>
                    `${Number(v).toFixed(2).replace(".", ",")} %`
                  }
                />
              }
            />

            <Bar dataKey="growth">
              {data.map((item) => {
                const admin = getAdminByYear(item.year)
                return (
                  <Cell
                    key={item.year}
                    fill={adminColors[admin] ?? "#8884d8"}
                  />
                )
              })}
            </Bar>
          </BarChart>
        </ChartContainer>

        {/* Leyenda de administraciones */}
        <div className="mt-6 flex flex-wrap items-center justify-center gap-4 text-xs">
          {Object.entries(adminColors).map(([name, color]) => (
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
          Gráfico 2. Crecimiento interanual promedio del Régimen Definitivo por año,
          coloreado según administración. Fuente: elaboración propia con datos del BCCR.
        </p>
      </CardContent>
    </Card>
  )
}
