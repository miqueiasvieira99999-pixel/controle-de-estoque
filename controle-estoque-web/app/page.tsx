export default function Home() {
  return (
    <main className="min-h-screen bg-slate-100">

      <header className="bg-blue-700 text-white p-5 shadow">
        <h1 className="text-3xl font-bold">
          Controle de Estoque
        </h1>

        <p>
          Sistema WEB — Projeto COPEL
        </p>
      </header>

      <section className="p-6">

        <div className="grid grid-cols-4 gap-4">

          <div className="bg-white p-5 rounded shadow">
            <h2>Total Materiais</h2>
            <strong>369</strong>
          </div>

          <div className="bg-white p-5 rounded shadow">
            <h2>Entradas</h2>
            <strong>0</strong>
          </div>

          <div className="bg-white p-5 rounded shadow">
            <h2>Saídas</h2>
            <strong>0</strong>
          </div>

          <div className="bg-white p-5 rounded shadow">
            <h2>Saldo</h2>
            <strong>0</strong>
          </div>

        </div>

      </section>

    </main>
  )
}