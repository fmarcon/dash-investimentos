"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import InvestmentForm from "../../components/InvestmentForm";
import { clearToken, getToken } from "../../lib/auth";
import { createInvestment, deleteInvestment, getInvestments, updateInvestment } from "../../lib/api";

interface Investment {
  id: number;
  nome: string;
  tipo: string;
  quantidade: string;
  valor_aplicado: string;
  valor_atual_estimado: string;
  data_compra: string;
  tipo_operacao: string;
  corretora: string;
  lucro_prejuizo: string;
}

export default function InvestmentsPage() {
  const router = useRouter();
  const [investments, setInvestments] = useState<Investment[]>([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState("");
  const [selected, setSelected] = useState<Investment | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    fetchInvestments();
  }, [router]);

  const totals = useMemo(() => {
    const invested = investments.reduce((sum, item) => sum + Number(item.valor_aplicado), 0);
    const current = investments.reduce((sum, item) => sum + Number(item.valor_atual_estimado), 0);
    const profit = investments.reduce((sum, item) => sum + Number(item.lucro_prejuizo), 0);
    return { invested, current, profit };
  }, [investments]);

  async function fetchInvestments() {
    setLoading(true);
    try {
      const data = await getInvestments();
      setInvestments(data);
    } catch (error) {
      setFeedback("Erro ao carregar investimentos.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSave(values: Partial<Investment>) {
    try {
      if (selected) {
        await updateInvestment(selected.id, values);
        setFeedback("Investimento atualizado com sucesso.");
      } else {
        await createInvestment(values);
        setFeedback("Investimento criado com sucesso.");
      }
      setSelected(null);
      await fetchInvestments();
    } catch (error) {
      setFeedback("Erro ao salvar investimento.");
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteInvestment(id);
      setFeedback("Investimento excluído com sucesso.");
      await fetchInvestments();
    } catch (error) {
      setFeedback("Erro ao excluir investimento.");
    }
  }

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  return (
    <main className="page-container">
      <div className="page-header">
        <div>
          <h1>Investimentos</h1>
          <p>Gestão de carteira e métricas de lucro/prejuízo.</p>
        </div>
        <button className="button secondary" onClick={handleLogout}>
          Sair
        </button>
      </div>

      <section className="metrics-grid">
        <div className="metric-card">
          <span>Total investido</span>
          <strong>R$ {totals.invested.toFixed(2)}</strong>
        </div>
        <div className="metric-card">
          <span>Valor atual</span>
          <strong>R$ {totals.current.toFixed(2)}</strong>
        </div>
        <div className="metric-card">
          <span>Resultado</span>
          <strong className={totals.profit >= 0 ? "positive" : "negative"}>
            R$ {totals.profit.toFixed(2)}
          </strong>
        </div>
      </section>

      <section className="card stack">
        <div className="section-header">
          <h2>{selected ? "Editar investimento" : "Novo investimento"}</h2>
          {selected ? (
            <button className="button secondary" onClick={() => setSelected(null)}>
              Cancelar edição
            </button>
          ) : null}
        </div>
        <InvestmentForm initialData={selected} onSubmit={handleSave} />
      </section>

      {feedback ? <p className="feedback">{feedback}</p> : null}

      <section className="card">
        <h2>Lista de investimentos</h2>
        {loading ? (
          <p>Carregando...</p>
        ) : investments.length === 0 ? (
          <p>Nenhum investimento cadastrado ainda.</p>
        ) : (
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Tipo</th>
                  <th>Quantidade</th>
                  <th>Aplicado</th>
                  <th>Atual</th>
                  <th>Lucro</th>
                  <th>Corretora</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {investments.map((investment) => (
                  <tr key={investment.id}>
                    <td>{investment.nome}</td>
                    <td>{investment.tipo}</td>
                    <td>{investment.quantidade}</td>
                    <td>R$ {Number(investment.valor_aplicado).toFixed(2)}</td>
                    <td>R$ {Number(investment.valor_atual_estimado).toFixed(2)}</td>
                    <td className={Number(investment.lucro_prejuizo) >= 0 ? "positive" : "negative"}>
                      R$ {Number(investment.lucro_prejuizo).toFixed(2)}
                    </td>
                    <td>{investment.corretora}</td>
                    <td className="actions-cell">
                      <button className="button secondary" onClick={() => setSelected(investment)}>
                        Editar
                      </button>
                      <button className="button danger" onClick={() => handleDelete(investment.id)}>
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}
