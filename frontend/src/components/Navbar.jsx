const Navbar = ({ currentPage, onNavigate }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'predict', label: 'Predict Churn' },
  ];

  return (
    <header className="sticky top-0 z-30 border-b border-slate-800/70 bg-slate-950/65 backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-orange-300">Retention Lab</p>
          <h1 className="text-lg font-semibold text-white sm:text-xl">Netflix Churn Intelligence</h1>
        </div>
        <nav className="flex items-center gap-2 rounded-full border border-slate-700/70 bg-slate-900/60 p-1">
          {navItems.map((item) => {
            const active = currentPage === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onNavigate(item.id)}
                className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                  active
                    ? 'bg-orange-500 text-slate-950 shadow-lg shadow-orange-500/25'
                    : 'text-slate-300 hover:text-white'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
