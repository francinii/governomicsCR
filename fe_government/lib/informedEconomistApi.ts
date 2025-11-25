export const apiBase = process.env.NEXT_PUBLIC_BE_URL ?? "http://localhost:8000"

export const REPORT_ENDPOINT = "/api/v1/pib-chat/report"

export type BackendResult =
  | { ok: true; data: string }
  | { ok: false; error: string }

export async function sendQuestion(question: string): Promise<BackendResult> {

  console.log(process.env);

  try {
    const res = await fetch(`${apiBase}${REPORT_ENDPOINT}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    
      body: JSON.stringify({ question }),
    })

    // Error HTTP
    if (!res.ok) {
      let message = `HTTP ${res.status}`

      try {
        const errJson = await res.json().catch(() => null)
        if (errJson?.detail) message = errJson.detail
        else {
          const text = await res.text()
          if (text) message = text
        }
      } catch {}

      return { ok: false, error: message }
    }

    const data = await res.json()
    const text =
      typeof data?.response === "string"
        ? data.response
        : JSON.stringify(data)

    return { ok: true, data: text }
  } catch {
    return {
      ok: false,
      error:
        "No fue posible contactar el backend.",
    }
  }
}
