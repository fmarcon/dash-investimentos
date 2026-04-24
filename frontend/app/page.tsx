import Link from "next/link";

export default function Home() {
  return (
    <main className="page-container">
      <div className="card">
        <h1>Dash Investimentos</h1>
        <p>Administre seus investimentos com login e gestão de carteira em uma SPA moderna.</p>
        <div className="actions">
          <Link href="/login" className="button">
            Entrar
          </Link>
          <Link href="/investments" className="button secondary">
            Ver investimentos
          </Link>
        </div>
      </div>
    </main>
  );
}
