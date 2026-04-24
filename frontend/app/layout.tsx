import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Dash Investimentos",
  description: "Dashboard de investimentos com login e CRUD para investidores.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
