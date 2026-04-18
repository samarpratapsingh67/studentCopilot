import { useMemo, useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Predict from './pages/Predict';

const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');

  const activePage = useMemo(() => {
    if (currentPage === 'predict') {
      return <Predict />;
    }

    return <Dashboard onGoPredict={() => setCurrentPage('predict')} />;
  }, [currentPage]);

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute -top-28 right-0 h-64 w-64 rounded-full bg-orange-500/20 blur-3xl" />
      <div className="pointer-events-none absolute bottom-0 left-0 h-64 w-64 rounded-full bg-emerald-500/20 blur-3xl" />

      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />

      <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{activePage}</main>
    </div>
  );
};

export default App;
