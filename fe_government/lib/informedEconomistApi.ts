export const apiBase = process.env.NEXT_PUBLIC_BE_URL ?? "http://localhost:8000"

export const REPORT_ENDPOINT = "/api/v1/pib-chat/report"
export const GENERAL_INFO_ENDPOINT = "/api/v1/pib-chat/general_information"

export type BackendResult =
  | { ok: true; data: string }
  | { ok: false; error: string }

export async function sendQuestion(question: string, endpoint: string = REPORT_ENDPOINT): Promise<BackendResult> {

  try {
    const res = await fetch(`${apiBase}${endpoint}`, {
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
      } catch { }

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
      error: "No fue posible contactar el backend.",
    }
  }
}
