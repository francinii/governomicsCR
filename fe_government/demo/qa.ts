// /demo/qa.ts
// Respuestas DEMO basadas en gráficos exportados desde los notebooks.
// Coloca tus PNG en /public/demo/plots/ con los nombres usados abajo.

function mdImg(src: string, alt = "") {
  return `![${alt}](${src})`
}

export function demoAnswer(query: string): string {
  const q = query.toLowerCase()

  if (q.includes("resumen") && q.includes("demanda")) {
    return [
      "## Resumen PIB por demanda (CR 2021–2024)",
      mdImg("/demo/plots/pib_demanda_trimestral.png", "PIB por Demanda trimestral"),
      "- **Consumo privado**: normalización post-pandemia, tracción sostenida.",
      "- **Formación Bruta de Capital**: repunte 2022–2023; moderación 2024 por tasas.",
      "- **Exportaciones netas**: resilientes con volatilidad en manufactura avanzada.",
      "",
      "_Gráfico generado en `borrador_demanda.ipynb` (export PNG)._",
      "Fuentes: BCCR (series trimestrales, demanda).",
    ].join("\n")
  }

  if (q.includes("contribuciones") || q.includes("industria")) {
    return [
      "## Contribuciones al crecimiento 2023-T2 por industria",
      mdImg("/demo/plots/contribuciones_crecimiento_2023T2.png", "Contribuciones por industria"),
      "- **Manufactura**: +1.2 pp (impulso de dispositivos médicos).",
      "- **Servicios empresariales/TIC**: +0.7 pp.",
      "- **Construcción**: +0.3 pp (obras privadas).",
      "- **Agro**: −0.2 pp (choques climáticos).",
      "",
      "_Gráfico generado en `borrador_oferta.ipynb` / `pib/oferta.py` (export PNG)._",
      "Nota: cifras indicativas para demo.",
    ].join("\n")
  }

  if (q.includes("comparar") && (q.includes("oferta") || q.includes("demanda"))) {
    return [
      "## Comparación: PIB por oferta vs demanda (2024 anual)",
      mdImg("/demo/plots/pib_oferta_vs_demanda_2024.png", "Oferta vs Demanda 2024"),
      "- **Brecha estadística** acotada tras revisión.",
      "- **Oferta**: fortaleza en servicios y manufactura de alta tecnología.",
      "- **Demanda**: consumo privado robusto; inversión sensible a tasas.",
      "",
      "_Gráficos generados en `borrador_oferta.ipynb` y `borrador_demanda.ipynb`._",
    ].join("\n")
  }

  if (q.includes("términos políticos") || q.includes("terminos politicos")) {
    return [
      "## Términos políticos que afectan la actividad",
      mdImg("/demo/plots/political_terms_wordcloud.png", "Nube de términos políticos"),
      "1) Regla fiscal y balance estructural.",
      "2) Reforma tributaria y eficiencia recaudatoria.",
      "3) Política de competencia y atracción IED.",
      "",
      "_Visual derivada de `political_terms.py` / `plots.py`._",
    ].join("\n")
  }

  if (q.includes("validaciones") || q.includes("serie trimestral")) {
    return [
      "## Validaciones visuales de la serie trimestral del PIB",
      mdImg("/demo/plots/pib_checks_seasonality.png", "Estacionalidad"),
      mdImg("/demo/plots/pib_checks_outliers.png", "Outliers"),
      "- Chequeo de estacionalidad (picos por trimestre).",
      "- Consistencia **YoY** vs **QoQ**.",
      "- Detección de puntos de quiebre (cambios metodológicos).",
      "",
      "_Generado en `validaciones.ipynb` / `cuentas_nacionales/visual_checks.py`._",
    ].join("\n")
  }

  return [
    "## Modo demo",
    "Puedo ayudarte con demanda/oferta, contribuciones, comparaciones, términos políticos y validaciones de series.",
    "Usa las preguntas rápidas o pide un gráfico específico exportado desde los notebooks.",
  ].join("\n")
}
