// Dataset procesado desde pib_sectores.txt  :contentReference[oaicite:0]{index=0}

// Orden canónico
export const canonicalOrder = [
  "Olsen",
  "Rodríguez",
  "Pacheco",
  "Arias",
  "Chinchilla",
  "Solís",
  "Alvarado",
  "Chaves",
];

// Colores oficiales por administración
export const presidentialColors: Record<string, string> = {
  Olsen: "#f97316",
  Rodríguez: "#fed7aa",
  Pacheco: "#a855f7",
  Arias: "#22c55e",
  Chinchilla: "#fb923c",
  Solís: "#9ca3af",
  Alvarado: "#ec4899",
  Chaves: "#38bdf8",
};

// === Dataset final para FE ===
// Contiene los sectores Agro, Servicios e Industria

export const pibSectoresDataset = [
  // --- Agro ---
  { sector: "Agro", admin: "Olsen", growth: 5.9, rank: 1 },
  { sector: "Agro", admin: "Pacheco", growth: 3.2, rank: 2 },
  { sector: "Agro", admin: "Chinchilla", growth: 2.7, rank: 3 },
  { sector: "Agro", admin: "Solís", growth: 2.2, rank: 4 },
  { sector: "Agro", admin: "Rodríguez", growth: 1.9, rank: 5 },
  { sector: "Agro", admin: "Arias", growth: 1.8, rank: 6 },
  { sector: "Agro", admin: "Chaves", growth: 0.7, rank: 7 },
  { sector: "Agro", admin: "Alvarado", growth: 0.2, rank: 8 },

  // --- Servicios ---
  { sector: "Servicios", admin: "Arias", growth: 6.0, rank: 1 },
  { sector: "Servicios", admin: "Pacheco", growth: 5.2, rank: 2 },
  { sector: "Servicios", admin: "Solís", growth: 4.6, rank: 3 },
  { sector: "Servicios", admin: "Chinchilla", growth: 4.6, rank: 4 },
  { sector: "Servicios", admin: "Olsen", growth: 4.4, rank: 5 },
  { sector: "Servicios", admin: "Rodríguez", growth: 4.3, rank: 6 },
  { sector: "Servicios", admin: "Alvarado", growth: 3.0, rank: 7 },
  { sector: "Servicios", admin: "Chaves", growth: 1.9, rank: 8 },

  // --- Industria ---
  { sector: "Industria", admin: "Chinchilla", growth: 5.5, rank: 1 },
  { sector: "Industria", admin: "Rodríguez", growth: 4.0, rank: 2 },
  { sector: "Industria", admin: "Pacheco", growth: 3.9, rank: 3 },
  { sector: "Industria", admin: "Solís", growth: 3.5, rank: 4 },
  { sector: "Industria", admin: "Arias", growth: 3.5, rank: 5 },
  { sector: "Industria", admin: "Chaves", growth: 2.4, rank: 6 },
  { sector: "Industria", admin: "Olsen", growth: 2.1, rank: 7 },
  { sector: "Industria", admin: "Alvarado", growth: 1.2, rank: 8 },
];
