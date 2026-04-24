"use client";

import { useEffect, useMemo, useState } from "react";

export interface InvestmentInput {
  nome: string;
  tipo: string;
  quantidade: string;
  valor_aplicado: string;
  valor_atual_estimado: string;
  data_compra: string;
  tipo_operacao: string;
  corretora: string;
}

interface InvestmentFormProps {
  initialData?: Partial<InvestmentInput> | null;
  onSubmit: (values: InvestmentInput) => Promise<void>;
}

const emptyForm: InvestmentInput = {
  nome: "",
  tipo: "",
  quantidade: "",
  valor_aplicado: "",
  valor_atual_estimado: "",
  data_compra: "",
  tipo_operacao: "compra",
  corretora: "",
};

export default function InvestmentForm({ initialData, onSubmit }: InvestmentFormProps) {
  const [values, setValues] = useState<InvestmentInput>({
    ...emptyForm,
    ...(initialData || {}),
  });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (initialData) {
      setValues((current) => ({ ...current, ...initialData }));
    }
  }, [initialData]);

  const isValid = useMemo(() => {
    return (
      values.nome.trim().length > 0 &&
      values.tipo.trim().length > 0 &&
      values.quantidade.trim().length > 0 &&
      values.valor_aplicado.trim().length > 0 &&
      values.valor_atual_estimado.trim().length > 0 &&
      values.data_compra.trim().length > 0
    );
  }, [values]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    if (!isValid) {
      setError("Preencha todos os campos obrigatórios.");
      return;
    }
    setSaving(true);
    try {
      await onSubmit(values);
      setValues({ ...emptyForm });
    } catch (exception) {
      setError("Falha ao enviar o investimento.");
    } finally {
      setSaving(false);
    }
  }

  function updateField(field: string, value: string) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  return (
    <form onSubmit={handleSubmit} className="stack">
      <label>
        Nome
        <input
          value={values.nome}
          onChange={(event) => updateField("nome", event.target.value)}
          required
        />
      </label>
      <label>
        Tipo
        <input
          value={values.tipo}
          onChange={(event) => updateField("tipo", event.target.value)}
          required
        />
      </label>
      <label>
        Quantidade
        <input
          type="number"
          step="any"
          value={values.quantidade}
          onChange={(event) => updateField("quantidade", event.target.value)}
          required
        />
      </label>
      <label>
        Valor aplicado
        <input
          type="number"
          step="0.01"
          value={values.valor_aplicado}
          onChange={(event) => updateField("valor_aplicado", event.target.value)}
          required
        />
      </label>
      <label>
        Valor atual estimado
        <input
          type="number"
          step="0.01"
          value={values.valor_atual_estimado}
          onChange={(event) => updateField("valor_atual_estimado", event.target.value)}
          required
        />
      </label>
      <label>
        Data de compra
        <input
          type="date"
          value={values.data_compra}
          onChange={(event) => updateField("data_compra", event.target.value)}
          required
        />
      </label>
      <label>
        Tipo de operação
        <select
          value={values.tipo_operacao}
          onChange={(event) => updateField("tipo_operacao", event.target.value)}
        >
          <option value="compra">Compra</option>
          <option value="venda">Venda</option>
        </select>
      </label>
      <label>
        Corretora
        <input
          value={values.corretora}
          onChange={(event) => updateField("corretora", event.target.value)}
        />
      </label>
      {error ? <p className="error">{error}</p> : null}
      <button type="submit" className="button" disabled={saving}>
        {saving ? "Salvando..." : "Salvar investimento"}
      </button>
    </form>
  );
}
