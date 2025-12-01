"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"

import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Plus, Check } from "lucide-react"

import { sendQuestion, apiBase, REPORT_ENDPOINT } from "@/lib/informedEconomistApi"
import { quickPrompts } from "@/demo/prompts"
import { demoAnswer } from "@/demo/qa"

type Msg = { role: "user" | "assistant"; content: string }
type Mode = "demo" | "api"

const macroKpis = {
  gdpYoY: "+3.2%",
  inflationYoY: "4.6%",
  unemployment: "8.5%",
  fiscalBalance: "-4.2% del PIB",
}

export default function InformedEconomistChat() {
  const [mode, setMode] = React.useState<Mode>("api")
  const [messages, setMessages] = React.useState<Msg[]>([
    {
      role: "assistant",
      content:
        "Hola 👋 Soy tu analista macro. Pregúntame sobre PIB, oferta/demanda, contribuciones, términos políticos y validaciones.",
    },
  ])

  const [input, setInput] = React.useState("")
  const [busy, setBusy] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const [quickOpen, setQuickOpen] = React.useState<string>("") // quick-prompts

  const listRef = React.useRef<HTMLDivElement | null>(null)

  React.useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight
    }
  }, [messages.length])

  const send = async (text?: string) => {
    const content = (text ?? input).trim()
    if (!content || busy) return

    setMessages(prev => [...prev, { role: "user", content }])
    setInput("")
    setBusy(true)
    setError(null)

    // MODO DEMO: no llama al backend
    if (mode === "demo") {
      const demo = demoAnswer(content)
      setMessages(prev => [...prev, { role: "assistant", content: demo }])
      setBusy(false)
      return
    }

    // MODO API: llama a FastAPI
    const result = await sendQuestion(content)

    if (result.ok) {
      setMessages(prev => [...prev, { role: "assistant", content: result.data }])
      setBusy(false)
      return
    }

    setError(result.error)
    setMessages(prev => [
      ...prev,
      {
        role: "assistant",
        content: `⚠️ Error al consultar el backend:\n\n${result.error}`,
      },
    ])
    setBusy(false)
  }

  return (
    <div className="mx-auto w-full max-w-4xl h-[80vh] rounded-xl border bg-card shadow-sm overflow-hidden flex flex-col">
      {/* Header KPIs */}
      <div className="flex flex-wrap items-center gap-2 border-b px-4 py-3">
        <Badge variant="secondary">PIB YoY: {macroKpis.gdpYoY}</Badge>
        <Badge variant="secondary">Inflación: {macroKpis.inflationYoY}</Badge>
        <Badge variant="secondary">Desempleo: {macroKpis.unemployment}</Badge>
        <Badge variant="secondary">Balance fiscal: {macroKpis.fiscalBalance}</Badge>
        {mode === "demo" && <Badge variant="destructive">Demo</Badge>}
      </div>

      {/* Controles */}
      <div className="flex flex-col gap-3 px-4 py-3 border-b">
        <div className="flex flex-wrap items-center gap-3">
          <Accordion
            type="single"
            collapsible
            className="w-full"
            value={quickOpen}
            onValueChange={setQuickOpen}
          >
            <AccordionItem value="quick-prompts">
              <AccordionTrigger className="text-sm">
                Sugerencias rápidas
              </AccordionTrigger>
              <AccordionContent>
                <div className="flex flex-wrap gap-2 pt-2">
                  {quickPrompts.map((q) => (
                    <Button
                      key={q}
                      variant="outline"
                      size="sm"
                      disabled={busy}
                      onClick={() => {
                        // 1) enviar prompt
                        send(q)
                        // 2) cerrar el accordion
                        setQuickOpen("")
                      }}
                    >
                      {q}
                    </Button>
                  ))}
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>

      <Separator />

      {/* CHAT: ocupa el espacio disponible dentro del card; scroll solo aquí si hace falta */}
      <div
        ref={listRef}
        className="flex flex-col gap-3 overflow-y-auto px-4 py-4 flex-1"
      >
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`whitespace-pre-wrap rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-foreground"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {busy && (
          <div className="flex justify-start">
            <div className="rounded-2xl bg-muted px-3 py-2 text-sm italic opacity-80">
              pensando…
            </div>
          </div>
        )}

        {error && (
          <div className="rounded-md border border-destructive/50 bg-destructive/10 px-3 py-2 text-sm text-destructive">
            {error}
          </div>
        )}
      </div>

      {/* INPUT */}
      <div className="border-t p-3">
        <div className="flex items-end gap-2">
          {/* Botón + con menú de opciones */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                type="button"
                variant="outline"
                size="icon"
                className="shrink-0"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              <DropdownMenuLabel>Opciones de chat</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => setMode("api")}
                className="flex items-center justify-between gap-2"
              >
                <span>Usar API</span>
                {mode === "api" && <Check className="h-4 w-4" />}
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setMode("demo")}
                className="flex items-center justify-between gap-2"
              >
                <span>Modo demo (sin backend)</span>
                {mode === "demo" && <Check className="h-4 w-4" />}
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Textarea central */}
          <Textarea
            placeholder="Escribe tu consulta…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                send()
              }
            }}
            className="min-h-[44px] flex-1"
          />

          {/* Botón enviar */}
          <Button
            type="button"
            onClick={() => send()}
            disabled={busy || !input.trim()}
            className="shrink-0"
          >
            Enviar
          </Button>
        </div>

        <p className="mt-2 text-xs text-muted-foreground">
          {mode === "api" ? (
            <>
              API → <code>{REPORT_ENDPOINT}</code>{" "}
              {apiBase ? `(base: ${apiBase})` : ""}
            </>
          ) : (
            "Modo demo (sin backend)"
          )}
        </p>
      </div>

    </div>
  )
}
